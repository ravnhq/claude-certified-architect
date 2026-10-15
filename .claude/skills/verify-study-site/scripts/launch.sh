#!/usr/bin/env bash
# Build the study site from a snapshot of the current working tree and serve it
# on a free port, the way the Pages workflow builds it (minus the guide PDFs).
#
# Usage: launch.sh
# Prints the run id on the last line of stdout. Everything else goes to stderr.
#
# Owns: $BASE/runs/<id>/ (snapshot, build, server log, run.env) and one
# `node scripts/serve-docs.mjs` process. Evidence goes to $BASE/evidence/<id>/.
set -euo pipefail

REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
BASE="${TMPDIR:-/tmp}"; BASE="${BASE%/}/verify-study-site"
mkdir -p "$BASE"
BASE=$(cd "$BASE" 2>/dev/null && pwd -P || echo "$BASE")
RUN_ID="$(date +%Y%m%d-%H%M%S)-$$"
RUN="$BASE/runs/$RUN_ID"
EVIDENCE="$BASE/evidence/$RUN_ID"
DEPS="$BASE/deps"
mkdir -p "$RUN/repo" "$EVIDENCE" "$DEPS"
log() { echo "[launch $RUN_ID] $*" >&2; }

# 1. Snapshot: tracked + untracked-not-ignored files as they are on disk, so
#    uncommitted edits are what gets built. The generators write into
#    <track>/dist, which is committed — building in the real tree would dirty it.
#    .corpus/ is skipped: only import_practice_bank.py reads it, and CI never runs that.
log "snapshotting working tree"
git -C "$REPO" ls-files -z --cached --others --exclude-standard \
  | REPO="$REPO" perl -0 -ne 'chomp; print "$_\0" if -e "$ENV{REPO}/$_" && !m{^\.corpus/}' \
  | rsync -a --from0 --files-from=- "$REPO/" "$RUN/repo/"
SOURCE_REV=$(git -C "$REPO" rev-parse --short HEAD)
DIRTY=$(git -C "$REPO" status --porcelain --untracked-files=normal -- . ':!.corpus' | wc -l | tr -d ' ')

# 2. Pinned build deps (same pins as .github/workflows/pages.yml), cached across runs.
if [ ! -d "$DEPS/node_modules/marked" ] || [ ! -d "$DEPS/node_modules/html-minifier-terser" ]; then
  log "installing pinned build deps into $DEPS"
  (cd "$DEPS" && npm install --no-save --no-audit --no-fund \
    marked@13.0.3 minisearch@7.2.0 pdfjs-dist@4.10.38 html-minifier-terser@7.2.0 >&2)
fi
ln -s "$DEPS/node_modules" "$RUN/repo/node_modules"

# 3. Build, in CI order. Minify stays last.
log "building"
(
  cd "$RUN/repo"
  python3 utils/build_exam_html.py
  python3 utils/build_professional_exam.py
  node scripts/build-pages.mjs
  node scripts/minify-docs.mjs
) > "$RUN/build.log" 2>&1 || { log "build failed — see $RUN/build.log"; tail -20 "$RUN/build.log" >&2; exit 1; }

# 4. Serve on a free port.
PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1])')
# Started from this shell, not a subshell, so $! is node itself and nothing
# keeps the caller's stdout pipe open.
cd "$RUN/repo"
nohup node scripts/serve-docs.mjs "$PORT" > "$RUN/server.log" 2>&1 < /dev/null &
PID=$!
echo "$PID" > "$RUN/server.pid"
URL="http://localhost:$PORT/claude-certified-architect/"

cat > "$RUN/run.env" <<EOF
RUN_ID=$RUN_ID
RUN_DIR=$RUN
SITE=$RUN/repo/docs
EVIDENCE=$EVIDENCE
PORT=$PORT
PID=$PID
URL=$URL
SESSION=verify-study-site-$RUN_ID
SOURCE_REPO=$REPO
SOURCE_REV=$SOURCE_REV
SOURCE_DIRTY_FILES=$DIRTY
EOF
cp "$RUN/run.env" "$EVIDENCE/run.env"
cp "$RUN/build.log" "$EVIDENCE/build.log"

# 5. Readiness: the server's own banner, then a 200 on the home page.
for _ in $(seq 1 50); do
  grep -q 'Serving docs' "$RUN/server.log" 2>/dev/null \
    && curl -fsS -o /dev/null "${URL}index.html" && { log "ready at $URL (pid $PID)"; echo "$RUN_ID"; exit 0; }
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.2
done
log "server did not become ready — see $RUN/server.log"; cat "$RUN/server.log" >&2
exit 1
