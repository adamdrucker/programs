#!/usr/bin/env bash
# =============================================================================
# sacct_as_scontrol.sh
#
# Queries historical job data via sacct and formats the output to mimic
# the style of `scontrol show job <jobid>` for completed/failed/cancelled jobs.
#
# Usage:
#   ./sacct_as_scontrol.sh <jobid> [jobid2 ...]
#   ./sacct_as_scontrol.sh --user <username> [--starttime YYYY-MM-DD] [--endtime YYYY-MM-DD]
#   ./sacct_as_scontrol.sh --all --starttime YYYY-MM-DD --endtime YYYY-MM-DD
#
# Examples:
#   ./sacct_as_scontrol.sh 12345
#   ./sacct_as_scontrol.sh 12345 12346 12347
#   ./sacct_as_scontrol.sh --user jdoe --starttime 2024-01-01
#   ./sacct_as_scontrol.sh --all --starttime 2024-03-01 --endtime 2024-03-31
# =============================================================================

set -uo pipefail

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
JOBS=()
QUERY_USER=""
QUERY_ALL=false
START_TIME=""
END_TIME=""

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
usage() {
    sed -n '/^# Usage:/,/^# =/p' "$0" | grep '^#' | sed 's/^# \?//'
    exit 1
}

if [[ $# -eq 0 ]]; then
    usage
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --user)       QUERY_USER="$2"; shift 2 ;;
        --starttime)  START_TIME="$2"; shift 2 ;;
        --endtime)    END_TIME="$2";   shift 2 ;;
        --all)        QUERY_ALL=true;  shift   ;;
        --help|-h)    usage ;;
        [0-9]*)       JOBS+=("$1");    shift   ;;
        *)            echo "Unknown argument: $1"; usage ;;
    esac
done

# ---------------------------------------------------------------------------
# Build sacct command
# ---------------------------------------------------------------------------
# Fields pulled from sacct — add/remove as needed
SACCT_FORMAT="JobID,JobName,User,Account,Partition,QOS,\
Priority,NCPUS,NNodes,NTasks,CPUTime,CPUTimeRAW,Elapsed,ElapsedRaw,Timelimit,\
Submit,Eligible,Start,End,State,ExitCode,\
ReqMem,MaxRSS,MaxVMSize,\
NodeList,AllocTRES,ReqTRES,\
WorkDir,Comment,Cluster,\
DerivedExitCode,Reason,\
ReqCPUS,ReqNodes,\
StdOut,StdErr,StdIn,\
Constraints,Flags,Restarts,UID,GID,McsLabel"

SACCT_ARGS=(
    --parsable2          # use '|' delimiter, no trailing '|'
    --noheader
    --units=M            # memory in MB
    --format="$SACCT_FORMAT"
    --duplicates         # include all steps; we filter to batch/extern below
)

if [[ ${#JOBS[@]} -gt 0 ]]; then
    SACCT_ARGS+=(--jobs "$(IFS=,; echo "${JOBS[*]}")")
fi

if [[ -n "$QUERY_USER" ]]; then
    SACCT_ARGS+=(--user "$QUERY_USER")
fi

if [[ "$QUERY_ALL" == true ]]; then
    SACCT_ARGS+=(--allusers)
fi

if [[ -n "$START_TIME" ]]; then
    SACCT_ARGS+=(--starttime "$START_TIME")
fi

if [[ -n "$END_TIME" ]]; then
    SACCT_ARGS+=(--endtime "$END_TIME")
fi

# ---------------------------------------------------------------------------
# Helper: pad/truncate a value for display
# ---------------------------------------------------------------------------
fmt() {
    # fmt <value> [default_if_empty]
    local val="${1:-}"
    local default="${2:-(null)}"
    echo "${val:-$default}"
}

# ---------------------------------------------------------------------------
# Helper: convert sacct elapsed/timelimit (D-HH:MM:SS or HH:MM:SS) to seconds
# ---------------------------------------------------------------------------
to_seconds() {
    local t="${1:-0}"
    local days=0 h=0 m=0 s=0
    if [[ "$t" == *-* ]]; then
        days="${t%%-*}"
        t="${t#*-}"
    fi
    IFS=: read -r h m s <<< "$t"
    echo $(( days*86400 + 10#${h:-0}*3600 + 10#${m:-0}*60 + 10#${s:-0} ))
}

# ---------------------------------------------------------------------------
# Helper: map sacct State to scontrol-style JobState
# ---------------------------------------------------------------------------
map_state() {
    case "${1^^}" in
        COMPLETED)              echo "COMPLETED" ;;
        FAILED)                 echo "FAILED" ;;
        CANCELLED*)             echo "CANCELLED" ;;
        TIMEOUT)                echo "TIMEOUT" ;;
        NODE_FAIL)              echo "NODE_FAIL" ;;
        PREEMPTED)              echo "PREEMPTED" ;;
        OUT_OF_MEMORY)          echo "OUT_OF_MEMORY" ;;
        RUNNING)                echo "RUNNING" ;;
        PENDING)                echo "PENDING" ;;
        SUSPENDED)              echo "SUSPENDED" ;;
        *)                      echo "${1:-UNKNOWN}" ;;
    esac
}

# ---------------------------------------------------------------------------
# Run sacct and capture output
# ---------------------------------------------------------------------------
# Verify sacct is available
if ! command -v sacct &>/dev/null; then
    echo "ERROR: 'sacct' not found in PATH. Is Slurm installed and loaded?" >&2
    echo "       PATH=$PATH" >&2
    exit 1
fi

# Run sacct — capture stdout and stderr separately
SACCT_STDERR_FILE=$(mktemp)
RAW_OUTPUT=$(sacct "${SACCT_ARGS[@]}" 2>"$SACCT_STDERR_FILE")
SACCT_EXIT=$?

if [[ $SACCT_EXIT -ne 0 ]]; then
    echo "ERROR: sacct exited with status $SACCT_EXIT." >&2
    echo "       Command: sacct ${SACCT_ARGS[*]}" >&2
    echo "       sacct stderr output:" >&2
    sed 's/^/         /' "$SACCT_STDERR_FILE" >&2
    rm -f "$SACCT_STDERR_FILE"
    exit 1
fi

# Print any warnings sacct emitted even on success
if [[ -s "$SACCT_STDERR_FILE" ]]; then
    echo "WARNING: sacct produced stderr output:" >&2
    sed 's/^/         /' "$SACCT_STDERR_FILE" >&2
fi
rm -f "$SACCT_STDERR_FILE"

if [[ -z "$RAW_OUTPUT" ]]; then
    echo "No jobs found matching the given criteria."
    exit 0
fi

# ---------------------------------------------------------------------------
# Process each line — only top-level job entries (not .batch/.extern steps)
# ---------------------------------------------------------------------------
declare -A SEEN_JOBS

while IFS='|' read -r \
    JobID JobName User Account Partition QOS \
    Priority NCPUS NNodes NTasks CPUTime CPUTimeRAW Elapsed ElapsedRaw Timelimit \
    Submit Eligible Start End State ExitCode \
    ReqMem MaxRSS MaxVMSize \
    NodeList AllocTRES ReqTRES \
    WorkDir Comment Cluster \
    DerivedExitCode Reason \
    ReqCPUS ReqNodes \
    StdOut StdErr StdIn \
    Constraints Flags Restarts JobUID JobGID McsLabel
do
    # Skip sub-steps (*.batch, *.extern, *.0, etc.)
    [[ "$JobID" == *.* ]] && continue

    # Store all parent records — last one per JobID wins (handles requeue/preempt cycles)
    # Pack the full line into an associative array keyed by JobID
    SEEN_JOBS["$JobID"]="$JobID|$JobName|$User|$Account|$Partition|$QOS|$Priority|$NCPUS|$NNodes|$NTasks|$CPUTime|$CPUTimeRAW|$Elapsed|$ElapsedRaw|$Timelimit|$Submit|$Eligible|$Start|$End|$State|$ExitCode|$ReqMem|$MaxRSS|$MaxVMSize|$NodeList|$AllocTRES|$ReqTRES|$WorkDir|$Comment|$Cluster|$DerivedExitCode|$Reason|$ReqCPUS|$ReqNodes|$StdOut|$StdErr|$StdIn|$Constraints|$Flags|$Restarts|$JobUID|$JobGID|$McsLabel"

done <<< "$RAW_OUTPUT"

# Now emit one record per JobID using the last-seen (final) state
for JobID in "${!SEEN_JOBS[@]}"; do
    IFS='|' read -r \
        JobID JobName User Account Partition QOS Priority NCPUS NNodes NTasks \
        CPUTime CPUTimeRAW Elapsed ElapsedRaw Timelimit Submit Eligible Start End State ExitCode \
        ReqMem MaxRSS MaxVMSize NodeList AllocTRES ReqTRES WorkDir Comment Cluster \
        DerivedExitCode Reason ReqCPUS ReqNodes StdOut StdErr StdIn \
        Constraints Flags Restarts JobUID JobGID McsLabel \
        <<< "${SEEN_JOBS[$JobID]}"

    # -----------------------------------------------------------------------
    # Derive / clean up fields
    # -----------------------------------------------------------------------
    JobState=$(map_state "$State")
    ExitCodeNum="${ExitCode%%:*}"
    ExitCodeSig="${ExitCode##*:}"

    ElapsedSec=$(to_seconds "$Elapsed")
    TimelimitSec=$(to_seconds "$Timelimit")

    # Array job handling — in Slurm 25.05 array info is encoded in JobID as "base_taskid"
    if [[ "$JobID" == *_* ]]; then
        ArrayJobIdStr="${JobID%%_*}"
        ArrayTaskIdStr="${JobID##*_}"
    else
        ArrayJobIdStr="0"
        ArrayTaskIdStr="N/A"
    fi
    # JobIDRaw is no longer a separate field; use JobID
    JobIDRaw="$JobID"

    # Reason field (only meaningful for pending; use "None" for others)
    ReasonStr=$(fmt "$Reason" "None")

    # -----------------------------------------------------------------------
    # Print in scontrol show job style
    # -----------------------------------------------------------------------
    cat <<EOF
JobId=$(fmt "$JobIDRaw") JobName=$(fmt "$JobName")
   UserId=$(fmt "$User") GroupId=$(fmt "$Account") MCS_label=N/A
   Priority=$(fmt "$Priority" "N/A") Nice=0 Account=$(fmt "$Account") QOS=$(fmt "$QOS")
   JobState=$JobState Reason=$ReasonStr Dependency=(null)
   TimeLimit=$(fmt "$Timelimit" "UNLIMITED") SubmitTime=$(fmt "$Submit") EligibleTime=$(fmt "$Eligible")
   StartTime=$(fmt "$Start") EndTime=$(fmt "$End") Deadline=N/A
   SuspendTime=None SecsPreSuspend=0
   Partition=$(fmt "$Partition") AllocNode:Sid=N/A:0
   ReqNodeList=$(fmt "$ReqNodes" "(null)") ExcNodeList=(null)
   NodeList=$(fmt "$NodeList" "(null)")
   NumNodes=$(fmt "$NNodes" "0") NumCPUs=$(fmt "$NCPUS" "0") NumTasks=$(fmt "$NTasks" "0") TRES=$(fmt "$AllocTRES" "cpu=0,mem=0,node=0")
   ReqTRES=$(fmt "$ReqTRES" "cpu=1,mem=0N,node=1,billing=1")
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryNode=$(fmt "$ReqMem" "0") MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)
   Command=$(fmt "$JobName")
   WorkDir=$(fmt "$WorkDir" "(null)")
   StdErr=$(fmt "$StdErr" "(null)")
   StdIn=$(fmt "$StdIn" "/dev/null")
   StdOut=$(fmt "$StdOut" "(null)")
   Power=
   ArrayJobId=$(fmt "$ArrayJobIdStr") ArrayTaskId=$(fmt "$ArrayTaskIdStr")
   Constraints=$(fmt "$Constraints") Flags=$(fmt "$Flags") Restarts=$(fmt "$Restarts" "0")
   ExitCode=$ExitCode DerivedExitCode=$(fmt "$DerivedExitCode" "0:0")
   Comment=$(fmt "$Comment" "(null)")
   Cluster=$(fmt "$Cluster" "(null)")
   Duration=$Elapsed CPUTime=$(fmt "$CPUTime") TimeLimit=$(fmt "$Timelimit" "UNLIMITED") TimelimitSecs=${TimelimitSec}
   MaxRSS=$(fmt "$MaxRSS" "N/A") MaxVMSize=$(fmt "$MaxVMSize" "N/A")

EOF

done
