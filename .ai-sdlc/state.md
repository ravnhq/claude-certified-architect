# Project State
updated: 2026-07-30

## Goal
Publish Ravn-curated preparation materials for Claude Certified Architect tracks.
Keep the established multilingual Foundations materials working while adding accurate,
clearly sourced guidance for the Professional certification.

## Now
The Professional (CCAR-P) practice exam is delivered. `professional_en.md` carries all
38 official blueprint objectives, the scoring and policy detail, the official prep-course
path, and an official-only resource list. The 126-item bank in
`data/professional_questions.json` draws 63 items per attempt.
The quiz engine in `utils/build_exam_html.py` is shared: `build()` was split into a
parameterized `render_page()`, so Foundations and Professional run one engine. The engine
now scores multiple-response items all-or-nothing, and the per-domain draw accepts either
a scalar (Foundations: flat 12) or a map (Professional: weighted 11/8/12/10/9/9/4 = 63).
Foundations behavior is unchanged.
Earlier work still holds: guide anchors are unique; search is self-hosted, resilient, and
accessible; practice exams are keyboard-operable, responsive, semantic, and AA-safe.
Correct-answer feedback uses a green accent (`--good: #6FA97C`); gold carries
selection/emphasis, red marks wrong/fail.
The exam CSS and JS live in the Python template `utils/build_exam_html.py` — edit there
and regenerate. Never hand-edit the generated `exam_<lang>.html` or
`professional_exam_en.html`.
This change set sits on `feature/ccarp-professional-study-materials`; production Pages
remains to be checked.

## Verification path
- `python3 utils/validate_professional_bank.py` -- PASS 2026-07-30 (126 items; per domain
  22/16/24/20/18/18/8; all 38 official objectives covered; multiple-response share 20.6%).
- `python3 utils/build_professional_exam.py` -- PASS 2026-07-30 (126-item bank, 63 drawn
  across 7 domains).
- `node utils/test_exam_engine.mjs` -- PASS 2026-07-30: the Foundations flat 12-per-domain
  60-item draw is unchanged; the Professional weighted draw matched the blueprint across
  50 consecutive draws; multiple-response all-or-nothing scoring, option toggle, overflow
  cap, and the study-mode lock all pass.
- `python3 utils/build_exam_html.py` -- PASS 2026-07-30 (136 questions × 3 langs, unchanged).
- `node scripts/build-pages.mjs` -- PASS 2026-07-30: `docs/practical/professional-en.html`
  holds the real exam, and the Professional copier did not overwrite
  `docs/practical/en.html`.
- Regenerating both exams on the unmodified tree produced a zero diff before any engine
  change, so the post-change delta comes from the engine edit alone.
- A fresh-context verifier re-ran the checks above and confirmed every published number
  against the official exam guide PDF.
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
- All Professional material stays English-only. The official certification FAQ states that
  the exam and its prep content are English-only, and it prohibits browser translation
  during proctored testing, so a translated Professional guide would train the reader
  against wording the exam never uses. Foundations stays tri-language.
- Keep Professional separate from Foundations exam/cheatsheet *data*; the blueprints differ.
  The rendering engine is deliberately shared, the question banks are not.
- Practice items are Ravn-authored and are labeled as not real exam content. Write them
  against the official objectives; never copy from any published bank.
- `data/professional_objectives.json` is the checked-in official blueprint and the
  validation source of truth for the bank.
- Explanations must not reference another option by letter. Letters are reassigned when the
  bank is rebalanced; this had already broken two items silently, so the validator now
  rejects letter references.
- Name no third-party study resource in the guide. Several of them publish a
  five-domain/60-item blueprint, which is the Foundations shape, so the section was dropped
  instead of linked.
- Cite and date official track facts because Anthropic marks the exam guide subject to change.
- Self-host the MiniSearch browser bundle generated from the pinned build dependency.
- Use native answer buttons for every answer option. An item is single-response or
  multiple-response scored all-or-nothing; Foundations items stay single-response.

## Landmines
- No package manifest is committed; local Pages builds need the workflow's temporary npm deps.
- Foundations guide heading alignment feeds question extraction; do not change those sources here.

## Next
1. Verify the Pages workflow and published routes for the current SHA.
2. Add a doc-drift assertion so the draw and bank numbers in the README and guide prose
   cannot diverge silently from the code that owns them.
3. Revisit the roughly sixteen items whose keyed option is noticeably longer than its
   distractors.
4. Add translated Professional guides only if Anthropic ships a non-English exam.
