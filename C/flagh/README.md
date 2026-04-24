# flagh

Explain command-line flags instantly from your terminal.

`flagh` parses **man pages** (preferred) or **`--help`** output to extract and display documentation for specific flags — so you don't have to wade through an entire man page to understand what `-xvf` does.

## Usage

```
flagh <command> <flag> [<flag> ...]
```

## Examples

```bash
# Explain individual flags
flagh curl -s -o -L --max-time

# Combined short flags are auto-expanded
flagh tar -xzf
#  → expands to -x, -z, -f and explains each

# Works with long options too
flagh grep --color --include

# Mix and match
flagh ls -la --sort
```

## Sample output

```
curl flag explanation  (source: --help)
--------------------------------------------------

  -s
       -s, --silent      Silent mode

  -o
       -o, --output <file> Write to file instead of stdout

  -L
       -L, --location    Follow redirects

  --max-time
       -m, --max-time <fractional seconds> Maximum time allowed for transfer
```

## Build & install

```bash
# Build
make

# Install to /usr/local/bin (may need sudo)
sudo make install

# Or install to a custom location
make PREFIX=~/.local install
```

## How it works

1. Tries to fetch the **man page** for the command (most complete documentation).
2. Falls back to **`--help all`**, then **`--help`**, then **`-h`** output.
3. Parses the text to find each flag's definition line and its description block.
4. For combined short flags like `-la`, automatically expands and looks up each individual flag.
5. Colorized output when running in a terminal (auto-detected).

## Requirements

- A C compiler (gcc, clang, etc.)
- A Unix-like system (Linux, macOS, WSL)
- `man` and/or commands that support `--help`

## Uninstall

```bash
sudo make uninstall
```
