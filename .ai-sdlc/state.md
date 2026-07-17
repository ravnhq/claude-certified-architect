# Project State
updated: 2026-07-17

## Goal
Publish Ravn-curated preparation materials for Claude Certified Architect tracks.
Keep the established multilingual Foundations materials working while adding accurate,
clearly sourced guidance for the Professional certification.

## Now
Professional-track guidance and all HTML/CSS/JS review fixes are implemented and
locally validated. Guide anchors are unique; search is self-hosted, resilient, and
accessible; practice exams are keyboard-operable, responsive, semantic, and AA-safe.
The complete change set is published on `main`; production Pages remains to be checked.
Practice-exam correct-answer feedback now uses a green accent (`--good: #6FA97C`)
instead of gold; gold still carries selection/emphasis, red still marks wrong/fail.
The exam CSS lives in `utils/build_exam_html.py` — edit there and regenerate, never
hand-edit `exam_<lang>.html`.

## Verification path
- `uv run python utils/build_exam_html.py` -- PASS 2026-07-17 (136 questions × 3 langs);
  Chrome study-mode check: correct option renders green, wrong stays red.
- `python3 -m py_compile extract_question.py parse_mock_exam.py utils/*.py` -- PASS 2026-07-13.
- `node --check scripts/build-pages.mjs` -- PASS 2026-07-13.
- `python3 utils/build_exam_html.py && node scripts/build-pages.mjs` -- PASS 2026-07-13.
- Static build audit: 11 pages, zero duplicate IDs, all sampled search anchors resolve.
- Chrome: keyboard answer PASS; 390px overflow PASS; search success/failure states PASS.
- Mobile Lighthouse: landing, Professional, and practice each score accessibility 100
  and best practices 100.

## Decisions
- Professional starts in English because the supplied authoritative guide is English-only.
- Keep Professional separate from Foundations exam/cheatsheet data; the blueprints differ.
- Cite and date official track facts because Anthropic marks the exam guide subject to change.
- Self-host the MiniSearch browser bundle generated from the pinned build dependency.
- Use native answer buttons and preserve the practice exam's existing single-choice behavior.

## Landmines
- No package manifest is committed; local Pages builds need the workflow's temporary npm deps.
- Foundations guide heading alignment feeds question extraction; do not change those sources here.

## Next
1. Verify the Pages workflow and published routes for the current `main` SHA.
2. Add translated Professional guides or a dedicated practice bank only as separate work.
