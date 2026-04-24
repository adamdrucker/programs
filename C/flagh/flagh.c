/*
 * flagh — explain command-line flags from man pages (or --help).
 *
 * Usage:
 *   flagh <command> <flag> [<flag> ...]
 *
 * Examples:
 *   flagh nmap -sL -Pn --open
 *   flagh curl -s -o -L
 *   flagh ls -la
 *   flagh grep -rni --color
 *
 * Build:
 *   gcc -O2 -o flagh flagh.c
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdbool.h>

/* ── Limits ─────────────────────────────────────────────────────────────── */

#define MAX_FLAGS        64
#define MAX_FLAG_LEN     64
#define MAX_DOC_LEN      4096
#define MAX_PAGE_SIZE    (2 * 1024 * 1024)

/* ── Color helpers ──────────────────────────────────────────────────────── */

static int use_color = 0;

#define C_BOLD   "\033[1m"
#define C_DIM    "\033[2m"
#define C_CYAN   "\033[36m"
#define C_YELLOW "\033[33m"
#define C_GREEN  "\033[32m"
#define C_RED    "\033[31m"
#define C_RESET  "\033[0m"

#define COL(c) (use_color ? (c) : "")

/* ── Data structures ────────────────────────────────────────────────────── */

typedef struct {
    char flag[MAX_FLAG_LEN];
    char doc[MAX_DOC_LEN];
    int  found;
} FlagResult;

/* ── Run a command and capture stdout+stderr ────────────────────────────── */

static char *run_cmd(const char *argv[], size_t *out_len) {
    int pipefd[2];
    if (pipe(pipefd) < 0) return NULL;

    pid_t pid = fork();
    if (pid < 0) { close(pipefd[0]); close(pipefd[1]); return NULL; }

    if (pid == 0) {
        close(pipefd[0]);
        dup2(pipefd[1], STDOUT_FILENO);
        dup2(pipefd[1], STDERR_FILENO);
        close(pipefd[1]);
        setenv("MANWIDTH", "200", 1);
        setenv("COLUMNS", "200", 1);
        setenv("MAN_KEEP_FORMATTING", "0", 1);
        execvp(argv[0], (char *const *)argv);
        _exit(127);
    }

    close(pipefd[1]);

    size_t cap = 32768, len = 0;
    char *buf = malloc(cap);
    if (!buf) { close(pipefd[0]); return NULL; }

    ssize_t n;
    while ((n = read(pipefd[0], buf + len, cap - len - 1)) > 0) {
        len += (size_t)n;
        if (len + 1 >= cap) {
            cap *= 2;
            if (cap > MAX_PAGE_SIZE) break;
            char *nb = realloc(buf, cap);
            if (!nb) break;
            buf = nb;
        }
    }
    close(pipefd[0]);

    int status;
    waitpid(pid, &status, 0);

    buf[len] = '\0';
    if (out_len) *out_len = len;

    return buf;
}

/* ── Strip backspace-based formatting (man bold/underline) ──────────────── */

static char *strip_overstrikes(const char *src, size_t len) {
    char *out = malloc(len + 1);
    if (!out) return NULL;
    size_t j = 0;
    for (size_t i = 0; i < len; i++) {
        if (i + 1 < len && src[i + 1] == '\b') {
            i += 1;
            continue;
        }
        if (src[i] == '\b') {
            if (j > 0) j--;
            continue;
        }
        out[j++] = src[i];
    }
    out[j] = '\0';
    return out;
}

/* ── Get man page text ──────────────────────────────────────────────────── */

static char *get_man_text(const char *command) {
    const char *argv[] = {"man", command, NULL};
    size_t len = 0;
    char *raw = run_cmd(argv, &len);
    if (!raw || len < 100) { free(raw); return NULL; }

    /* reject non-manpage output */
    if (strstr(raw, "minimized") || strstr(raw, "No manual entry") ||
        strstr(raw, "No entry for") || strstr(raw, "unminimize")) {
        free(raw);
        return NULL;
    }

    /* a real man page should have standard section headings */
    if (!strstr(raw, "NAME") && !strstr(raw, "SYNOPSIS") &&
        !strstr(raw, "DESCRIPTION")) {
        free(raw);
        return NULL;
    }

    char *clean = strip_overstrikes(raw, len);
    free(raw);
    return clean;
}

/* ── Get --help text ────────────────────────────────────────────────────── */

static char *get_help_text(const char *command) {
    const char *try_flags[][3] = {
        {command, "--help", "all"},
        {command, "--help", NULL},
        {command, "-h",    NULL},
    };
    /* try --help all first (curl etc.), then --help, then -h */
    for (int t = 0; t < 3; t++) {
        size_t len = 0;
        char *txt = run_cmd(try_flags[t], &len);
        if (txt && len > 30) return txt;
        free(txt);
    }
    return NULL;
}

/* ── Trim trailing whitespace ───────────────────────────────────────────── */

static void trim_right(char *s) {
    size_t len = strlen(s);
    while (len > 0 && (s[len-1] == ' ' || s[len-1] == '\t' ||
                       s[len-1] == '\n' || s[len-1] == '\r'))
        s[--len] = '\0';
}

/* ── Check if a line looks like it starts a new flag definition ─────────── */

static int line_starts_flag(const char *line) {
    while (*line == ' ' || *line == '\t') line++;
    return (*line == '-');
}

/* ── Determine the indentation level of a line ──────────────────────────── */

static int indent_of(const char *line) {
    int n = 0;
    while (line[n] == ' ') n++;
    if (line[n] == '\t') return n + 8;
    return n;
}

/* ── Check if line is blank ─────────────────────────────────────────────── */

static int is_blank(const char *line) {
    while (*line) {
        if (*line != ' ' && *line != '\t' && *line != '\r' && *line != '\n')
            return 0;
        line++;
    }
    return 1;
}

/* ── Check flag boundary match ──────────────────────────────────────────── */

static int check_flag_boundary(const char *line, const char *hit,
                                const char *flag, size_t flen)
{
    char before = (hit == line) ? ' ' : *(hit - 1);
    char after  = *(hit + flen);

    int before_ok = (before == ' ' || before == ',' || before == '\t' ||
                     before == '[' || before == '|' || hit == line);

    int after_ok  = (after == '\0' || after == ' ' || after == ',' ||
                     after == '\t' || after == '=' || after == '[' ||
                     after == ']'  || after == '<' || after == '\n' ||
                     after == '\r');

    /* for single-char short flags like -s, reject if followed by alnum
       so that searching for -s doesn't match inside -sL */
    if (flen == 2 && flag[0] == '-' && flag[1] != '-') {
        if (after != '\0' && isalnum((unsigned char)after))
            after_ok = 0;
    }

    return before_ok && after_ok;
}

/* ── Check if the flag appears in the "option position" on a line ────────
 *
 * In both man pages and --help output, option definitions look like:
 *     -a, --all          description text
 *       -o FILE          description text
 *
 * The flag token appears early on the line (within ~40 columns after the
 * indent) and the line itself starts with a '-' after whitespace.
 * A line like "with -l, print the author" has -l far into a description
 * and the line's first non-space token is a word, not a dash.
 * ──────────────────────────────────────────────────────────────────────── */

static int flag_in_option_position(const char *line, const char *hit,
                                    const char *flag, size_t flen)
{
    (void)flag; (void)flen;

    /* the line must begin (after indent) with a '-' */
    const char *t = line;
    while (*t == ' ' || *t == '\t') t++;
    if (*t != '-') return 0;

    /*
     * The "option area" is the part of the line from the first dash up to
     * the start of the description text. In typical formats:
     *   "  -a, --all                  do not ignore..."
     *   "       -o <file>             write output to..."
     *
     * The option area ends where we see 2+ consecutive spaces (or tab)
     * followed by a non-dash, non-comma, non-space character — that's
     * the description column.
     *
     * We require the hit to fall within this option area.
     */
    const char *opt_start = t;  /* first dash */
    const char *opt_end = NULL;

    /* scan for the "gap" between options and description:
       look for at least 2 spaces followed by an alphanumeric char */
    for (const char *s = opt_start; *s && *s != '\n'; s++) {
        if (s[0] == ' ' && s[1] == ' ') {
            /* find the next non-space */
            const char *ns = s + 2;
            while (*ns == ' ') ns++;
            /* if what follows is not a dash or comma (not another flag token)
               and is alphanumeric, this is the description start */
            if (*ns && *ns != '-' && *ns != ',' && *ns != '\0' &&
                *ns != '\n' && isalpha((unsigned char)*ns)) {
                opt_end = s;
                break;
            }
        }
    }

    /* if no clear gap found, use the whole line as option area (unusual format) */
    if (!opt_end) opt_end = line + strlen(line);

    /* the hit must fall within [opt_start, opt_end) */
    return (hit >= opt_start && hit < opt_end);
}

/* ── Capture a flag description block starting at line pointer p ─────────
 *
 * Reads the matched line + indented continuation lines. Stops at:
 *   - next flag definition at same/lesser indent
 *   - section heading (zero indent)
 *   - double blank line
 * ──────────────────────────────────────────────────────────────────────── */

static size_t capture_block(const char *p, const char *eol, int match_indent,
                             char *doc, size_t doc_sz)
{
    size_t linelen = (size_t)(eol - p);
    size_t used = 0;

    if (linelen < doc_sz - 2) {
        memcpy(doc, p, linelen);
        doc[linelen] = '\n';
        used = linelen + 1;
    }

    const char *next = (*eol) ? eol + 1 : eol;
    int blank_count = 0;

    while (*next) {
        const char *neol = strchr(next, '\n');
        if (!neol) neol = next + strlen(next);
        size_t nlen = (size_t)(neol - next);

        char nline[2048];
        if (nlen >= sizeof(nline)) nlen = sizeof(nline) - 1;
        memcpy(nline, next, nlen);
        nline[nlen] = '\0';

        if (is_blank(nline)) {
            blank_count++;
            if (blank_count >= 2) break;
            if (used + 2 < doc_sz) { doc[used++] = '\n'; }
            next = (*neol) ? neol + 1 : neol;
            continue;
        }

        int ni = indent_of(nline);

        if (blank_count > 0 && ni <= match_indent && line_starts_flag(nline))
            break;
        blank_count = 0;

        /* check if the previous captured line ended with a comma — if so,
           this is a continuation (e.g. --color[=WHEN], / --colour[=WHEN]) */
        if (ni <= match_indent && line_starts_flag(nline)) {
            /* look back: did the last non-whitespace char we wrote end with ','? */
            size_t back = used;
            while (back > 0 && (doc[back-1] == '\n' || doc[back-1] == ' '))
                back--;
            if (back > 0 && doc[back-1] == ',') {
                /* comma continuation — keep going */
            } else {
                break;
            }
        }

        if (ni == 0 && !isspace((unsigned char)nline[0]) && nline[0] != '\0')
            break;

        if (ni < match_indent && ni > 0) break;

        /* a line at higher indent that starts a new flag definition
           (e.g. long-only options like --line-buffered in --help, or
           compact formats like curl --help all) should stop capture,
           unless the previous line ended with a comma (alias continuation) */
        if (ni > match_indent && line_starts_flag(nline)) {
            size_t back = used;
            while (back > 0 && (doc[back-1] == '\n' || doc[back-1] == ' '))
                back--;
            if (back > 0 && doc[back-1] == ',') {
                /* comma continuation — keep going */
            } else {
                break;
            }
        }

        if (used + nlen + 2 >= doc_sz) break;
        memcpy(doc + used, nline, nlen);
        used += nlen;
        doc[used++] = '\n';

        next = (*neol) ? neol + 1 : neol;
    }

    doc[used] = '\0';
    trim_right(doc);
    return used;
}

/* ── Search for a flag definition in text ───────────────────────────────
 *
 * Two-pass approach:
 *   Pass 1: look for the flag in "option position" (the line starts with
 *           a dash and the flag is near the left side). This is the real
 *           flag definition.
 *   Pass 2: if pass 1 fails, accept any line that has the flag with a
 *           valid boundary match (catches unusual formatting).
 * ──────────────────────────────────────────────────────────────────────── */

static int find_flag_in_text(const char *text, const char *flag,
                              char *doc, size_t doc_sz)
{
    if (!text || !flag || !doc) return 0;

    size_t flen = strlen(flag);

    for (int pass = 0; pass < 2; pass++) {
        doc[0] = '\0';
        const char *p = text;

        while (*p) {
            const char *eol = strchr(p, '\n');
            if (!eol) eol = p + strlen(p);
            size_t linelen = (size_t)(eol - p);

            char line[2048];
            if (linelen >= sizeof(line)) linelen = sizeof(line) - 1;
            memcpy(line, p, linelen);
            line[linelen] = '\0';

            /* look for flag on this line with boundary check */
            char *hit = strstr(line, flag);
            int matched = 0;
            while (hit) {
                if (check_flag_boundary(line, hit, flag, flen)) {
                    if (pass == 0) {
                        /* pass 1: must be in option position */
                        if (flag_in_option_position(line, hit, flag, flen)) {
                            matched = 1;
                            break;
                        }
                    } else {
                        /* pass 2: accept any boundary match on a flag-like line */
                        matched = 1;
                        break;
                    }
                }
                hit = strstr(hit + 1, flag);
            }

            if (!matched) {
                p = (*eol) ? eol + 1 : eol;
                continue;
            }

            int li = indent_of(line);

            /* skip section headings (zero-indent non-dash lines) */
            if (li == 0) {
                const char *trimmed = line;
                while (*trimmed == ' ' || *trimmed == '\t') trimmed++;
                if (*trimmed != '-') {
                    p = (*eol) ? eol + 1 : eol;
                    continue;
                }
            }

            size_t used = capture_block(p, eol, li, doc, doc_sz);

            if (used > flen + 2) return 1;

            doc[0] = '\0';
            p = (*eol) ? eol + 1 : eol;
        }
    }

    return 0;
}

/* ── Pretty-print a result ──────────────────────────────────────────────── */

static void print_result(const FlagResult *r) {
    if (r->found) {
        printf("\n  %s%s%s%s\n", COL(C_BOLD), COL(C_GREEN), r->flag, COL(C_RESET));
        const char *p = r->doc;
        while (*p) {
            const char *eol = strchr(p, '\n');
            if (!eol) eol = p + strlen(p);
            printf("      %.*s\n", (int)(eol - p), p);
            p = (*eol) ? eol + 1 : eol;
        }
    } else {
        printf("\n  %s%s%s%s\n", COL(C_BOLD), COL(C_RED), r->flag, COL(C_RESET));
        printf("      %sNo documentation found for this flag.%s\n",
               COL(C_DIM), COL(C_RESET));
    }
}

/* ── Print header ───────────────────────────────────────────────────────── */

static void print_header(const char *command, const char *source) {
    printf("\n%s%s%s flag explanation  %s(source: %s)%s\n",
           COL(C_BOLD), command, COL(C_RESET),
           COL(C_DIM), source, COL(C_RESET));
    printf("%s", COL(C_DIM));
    for (int i = 0; i < 50; i++) putchar('-');
    printf("%s\n", COL(C_RESET));
}

/* ── Main ───────────────────────────────────────────────────────────────── */

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr,
            "flagh — explain command-line flags\n\n"
            "Usage:\n"
            "  flagh <command> <flag> [<flag> ...]\n\n"
            "Examples:\n"
            "  flagh nmap -sL -Pn --open\n"
            "  flagh curl -s -o -L\n"
            "  flagh ls -la\n"
            "  flagh grep -rni --color\n"
        );
        return 1;
    }

    use_color = isatty(STDOUT_FILENO);

    const char *command = argv[1];

    /* collect raw flag arguments */
    char *raw_flags[MAX_FLAGS];
    int nraw = 0;

    for (int i = 2; i < argc && nraw < MAX_FLAGS; i++) {
        if (argv[i][0] != '-') continue;
        raw_flags[nraw++] = argv[i];
    }

    if (nraw == 0) {
        fprintf(stderr,
            "flagh: no flags provided. Pass at least one flag (e.g. -v, --help).\n");
        return 1;
    }

    /* fetch documentation — man page first, --help fallback */
    char *man_text  = get_man_text(command);
    char *help_text = NULL;

    if (!man_text) {
        help_text = get_help_text(command);
    }

    char *source_text = man_text ? man_text : help_text;
    const char *source_name = man_text ? "man page" : "--help";

    if (!source_text) {
        fprintf(stderr,
            "flagh: could not retrieve documentation for '%s'.\n"
            "       Tried: man %s, %s --help, %s -h\n",
            command, command, command, command);
        return 1;
    }

    print_header(command, source_name);

    /* process each flag */
    for (int i = 0; i < nraw; i++) {
        const char *flag = raw_flags[i];
        FlagResult res;
        strncpy(res.flag, flag, MAX_FLAG_LEN - 1);
        res.flag[MAX_FLAG_LEN - 1] = '\0';
        res.doc[0] = '\0';
        res.found = 0;

        /* 1) try the flag as-is */
        if (find_flag_in_text(source_text, flag, res.doc, MAX_DOC_LEN)) {
            res.found = 1;
            print_result(&res);
            continue;
        }

        /* 2) combined short flags like -la, -rni → expand to individual */
        if (flag[0] == '-' && flag[1] != '-' && strlen(flag) > 2) {
            printf("\n  %s%s%s%s  %s(expanding combined flags)%s\n",
                   COL(C_BOLD), COL(C_YELLOW), flag, COL(C_RESET),
                   COL(C_DIM), COL(C_RESET));

            for (size_t c = 1; flag[c]; c++) {
                char single[4] = {'-', flag[c], '\0'};
                FlagResult sub;
                strncpy(sub.flag, single, MAX_FLAG_LEN);
                sub.doc[0] = '\0';
                sub.found = 0;

                if (find_flag_in_text(source_text, single, sub.doc, MAX_DOC_LEN)) {
                    sub.found = 1;
                }

                /* fallback to --help if man was primary */
                if (!sub.found && man_text) {
                    if (!help_text) help_text = get_help_text(command);
                    if (help_text && find_flag_in_text(help_text, single,
                                                       sub.doc, MAX_DOC_LEN)) {
                        sub.found = 1;
                    }
                }

                print_result(&sub);
            }
            continue;
        }

        /* 3) fallback: try --help if man was primary source */
        if (man_text) {
            if (!help_text) help_text = get_help_text(command);
            if (help_text && find_flag_in_text(help_text, flag,
                                                res.doc, MAX_DOC_LEN)) {
                res.found = 1;
                print_result(&res);
                continue;
            }
        }

        print_result(&res);
    }

    printf("\n");

    free(man_text);
    free(help_text);
    return 0;
}
