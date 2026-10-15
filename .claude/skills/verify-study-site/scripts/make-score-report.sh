#!/usr/bin/env bash
# Print a synthetic score-report PDF for the score-report upload recipes.
# The repo has no real report (they are personal), so this lays out what the
# reader parses: an "Exam code" line, the exam name, and one row per objective
# with its text on the left and an "NN%" score in a right-hand column.
# Objective text comes from this run's built score-report-data.json.
# Ligatures are off: Chrome prints "fi" as its own text item, which splits
# "Configure" into "Con fi gure" and the row no longer matches its objective.
#
# Usage: make-score-report.sh <run-id> [exam-code] [rows] [--no-code]
#   exam-code  CCAR-F (default), CCAR-P or CCDV-F
#   rows       objectives to include (default 8); scores cycle 35..95%
#   --no-code  omit the code and exam name, to drive the "choose the exam" path
# Prints the PDF path. Fixtures live in the evidence dir so the input survives cleanup.
set -euo pipefail

BASE="${TMPDIR:-/tmp}"; BASE="${BASE%/}/verify-study-site"
BASE=$(cd "$BASE" 2>/dev/null && pwd -P || echo "$BASE")
RUN_ID="${1:?usage: make-score-report.sh <run-id> [exam-code] [rows] [--no-code]}"
CODE="${2:-CCAR-F}"; ROWS="${3:-8}"; NOCODE="${4:-}"
# shellcheck disable=SC1090
. "$BASE/runs/$RUN_ID/run.env"

out="$EVIDENCE/fixtures"; mkdir -p "$out"
stem="score-report-$CODE-$ROWS${NOCODE:+-nocode}"
python3 - "$SITE/score-report-data.json" "$CODE" "$ROWS" "$NOCODE" > "$out/$stem.html" <<'EOF'
import html, json, sys
data, code, rows, nocode = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
exam = json.load(open(data))["exams"][code]
scores = [35, 95, 50, 80, 65, 40, 90, 55, 70, 45]
items = list(exam["objectives"].items())[:rows]
head = "" if nocode else f"<p>Exam code: {code}</p><h1>{html.escape(exam['name'])}</h1>"
body = "".join(
    f'<div class="row"><div class="obj">{html.escape(text)}</div><div class="pct">{scores[i % len(scores)]}%</div></div>'
    for i, (_, text) in enumerate(items))
print(f"""<!doctype html><meta charset="utf-8"><title>Score report fixture</title>
<style>body{{font:12px Helvetica,Arial,sans-serif;margin:40px;font-variant-ligatures:none}}
.row{{display:flex;justify-content:space-between;align-items:center;margin:0 0 26px}}
.obj{{width:70%}}.pct{{width:60px;text-align:right}}</style>
<p>Synthetic score report for verification. Not a real result.</p>{head}{body}""")
EOF

fx="$SESSION-fixture"
agent-browser --session "$fx" --engine chrome open "file://$out/$stem.html" > /dev/null
agent-browser --session "$fx" --engine chrome pdf "$out/$stem.pdf" > /dev/null
agent-browser --session "$fx" close > /dev/null 2>&1 || true
echo "$out/$stem.pdf"
