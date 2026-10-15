#!/usr/bin/env bash
# Read-only checks that <run-id> is the live instance this run built and owns.
#
# Usage: doctor.sh <run-id>
# Exits non-zero on the first failed check. Changes nothing.
set -uo pipefail

BASE="${TMPDIR:-/tmp}"; BASE="${BASE%/}/verify-study-site"
BASE=$(cd "$BASE" 2>/dev/null && pwd -P || echo "$BASE")
RUN_ID="${1:?usage: doctor.sh <run-id>}"
ENV_FILE="$BASE/runs/$RUN_ID/run.env"
[ -f "$ENV_FILE" ] || { echo "FAIL no run state at $ENV_FILE"; exit 1; }
# shellcheck disable=SC1090
. "$ENV_FILE"

fail() { echo "FAIL $*"; exit 1; }
ok() { echo "ok   $*"; }

# The recipes drive Chrome through agent-browser; a stale or dangling install fails every step.
AB_VERSION=$(agent-browser --version 2>/dev/null) || fail "agent-browser is not runnable from PATH ($(command -v agent-browser || echo 'not found'))"
ok "$AB_VERSION"

kill -0 "$PID" 2>/dev/null || fail "server pid $PID is not running"
CMD=$(ps -o command= -p "$PID")
case "$CMD" in *"scripts/serve-docs.mjs $PORT"*) ok "pid $PID is serve-docs on $PORT";; *) fail "pid $PID is not this run's server: $CMD";; esac
CWD=$(lsof -a -p "$PID" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
[ "$CWD" = "$RUN_DIR/repo" ] && ok "server cwd is the run snapshot" || fail "server cwd is $CWD, expected $RUN_DIR/repo"

OWNER=$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -1)
[ "$OWNER" = "$PID" ] && ok "port $PORT is owned by pid $PID" || fail "port $PORT is owned by '${OWNER:-nobody}', not $PID"

# The served bytes must be this run's build, not some other docs/ tree.
SERVED=$(curl -fsS "${URL}index.html" | shasum | cut -d' ' -f1) || fail "GET ${URL}index.html failed"
BUILT=$(shasum < "$SITE/index.html" | cut -d' ' -f1)
[ "$SERVED" = "$BUILT" ] && ok "served index.html matches $SITE/index.html" || fail "served index.html differs from this run's build"

grep -q 'docs/ built' "$RUN_DIR/build.log" || fail "build.log has no 'docs/ built' from build-pages.mjs"
# minify-docs.mjs runs last and rewrites docs/ in place; its line proves the build finished.
grep -q '^Minified ' "$RUN_DIR/build.log" && ok "build completed (source $SOURCE_REV, $SOURCE_DIRTY_FILES uncommitted files)" || fail "build.log has no 'Minified' line from minify-docs.mjs"
for page in practical/en.html guides/en.html preflight/en.html score-report.html practical/bank-en.html; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "${URL}$page")
  [ "$code" = 200 ] && ok "GET $page → 200" || fail "GET $page → $code"
done

echo "SITE=$SITE"
echo "URL=$URL"
echo "SESSION=$SESSION"
echo "EVIDENCE=$EVIDENCE"
