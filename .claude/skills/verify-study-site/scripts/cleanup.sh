#!/usr/bin/env bash
# Stop what <run-id> owns and delete its scratch state. Evidence is kept.
#
# Usage: cleanup.sh <run-id>
# Safe to re-run, and safe on a run whose launch failed halfway.
set -uo pipefail

BASE="${TMPDIR:-/tmp}"; BASE="${BASE%/}/verify-study-site"
BASE=$(cd "$BASE" 2>/dev/null && pwd -P || echo "$BASE")
RUN_ID="${1:?usage: cleanup.sh <run-id>}"
RUN="$BASE/runs/$RUN_ID"
case "$RUN_ID" in */*|.*|'') echo "refusing odd run id '$RUN_ID'"; exit 1;; esac

for s in "verify-study-site-$RUN_ID" "verify-study-site-$RUN_ID-fixture"; do
  agent-browser session list 2>/dev/null | awk "{print \$1}" | grep -qx "$s" \
    && agent-browser --session "$s" close >/dev/null 2>&1 && echo "closed browser session $s"
done

if [ -f "$RUN/server.pid" ]; then
  PID=$(cat "$RUN/server.pid")
  # Only kill the pid if it is still this run's server; pids get reused.
  if kill -0 "$PID" 2>/dev/null && ps -o command= -p "$PID" | grep -q 'scripts/serve-docs.mjs' \
     && [ "$(lsof -a -p "$PID" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')" = "$RUN/repo" ]; then
    kill "$PID" && echo "stopped server pid $PID"
  fi
fi

[ -d "$RUN" ] && rm -rf "$RUN" && echo "removed $RUN"
[ -d "$BASE/evidence/$RUN_ID" ] && echo "evidence kept at $BASE/evidence/$RUN_ID"
exit 0
