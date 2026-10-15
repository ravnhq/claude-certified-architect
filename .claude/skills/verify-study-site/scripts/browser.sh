#!/usr/bin/env bash
# Run agent-browser against <run-id>'s server in that run's own Chrome session.
#
# Usage:
#   browser.sh <run-id> open <page>              # page is relative to the site root, e.g. practical/en.html
#   browser.sh <run-id> proof <feature> <name>   # snapshot + screenshot + URL into the evidence dir
#   browser.sh <run-id> <any agent-browser command and args>
#
# Chrome, not the default Lightpanda engine: the recipes need screenshots and
# localStorage that survives a reload.
set -euo pipefail

BASE="${TMPDIR:-/tmp}"; BASE="${BASE%/}/verify-study-site"
BASE=$(cd "$BASE" 2>/dev/null && pwd -P || echo "$BASE")
RUN_ID="${1:?usage: browser.sh <run-id> <command> [args]}"; shift
# shellcheck disable=SC1090
. "$BASE/runs/$RUN_ID/run.env"
command -v agent-browser > /dev/null || { echo "agent-browser is not on PATH; doctor.sh <run-id> checks it" >&2; exit 127; }
ab() { agent-browser --session "$SESSION" --engine chrome "$@"; }

case "${1:-}" in
  open)
    page="${2:?usage: browser.sh <run-id> open <page>}"
    ab open "${URL}${page#/}"
    ;;
  proof)
    feature="${2:?feature}"; name="${3:?name}"
    dir="$EVIDENCE/$feature"; mkdir -p "$dir"
    ab get url > "$dir/$name.url.txt"
    ab snapshot > "$dir/$name.aria.txt"
    ab screenshot "$dir/$name.png" > /dev/null
    echo "$dir/$name.{url.txt,aria.txt,png}"
    ;;
  *)
    ab "$@"
    ;;
esac
