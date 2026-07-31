## 2026-07-13 — Added Professional certification guidance
- Did: added an English CCAR-P study guide from the official July 2026 blueprint.
- Did: separated Foundations and Professional paths in README and Pages navigation.
- Did: indexed the Professional guide in the existing full-text search.
- Verified: Pages build, syntax checks, Python compile checks, search resolution, and route HTTP 200s passed.
- Verified: official resource links returned HTTP 200; desktop landing and guide renders were inspected.
- Learned: local npm's shared cache has root-owned files; use a clean `/tmp` cache for temporary deps.
- Left: changes uncommitted for user review; production Pages deployment not run.

## 2026-07-13 — Closed the HTML, CSS, and JavaScript review
- Did: made guide slugs collision-safe and search self-hosted, labeled, stateful, and failure-aware.
- Did: made all practice answers native buttons and added landmarks, pressed state, focus styling, and mobile layouts.
- Did: raised subtle-text contrast and regenerated all three practice exams.
- Verified: build, syntax, Python compile, diff check, duplicate-ID, and search-anchor checks passed.
- Verified: keyboard answer and 390px runtime checks passed; search emitted no console errors.
- Verified: mobile Lighthouse scored accessibility 100 and best practices 100 on all representative pages.
- Left: full change set is uncommitted; production Pages deployment remains unverified.

## 2026-07-13 — Published Professional guidance and UI fixes
- Did: committed the complete Professional-track, accessibility, responsive, and search change set to `main`.
- Verified: staged scope excluded generated caches and retained all previously validated source and exam output.
- Left: production Pages workflow and published routes require post-push verification.

## 2026-07-17 — Green correct-answer feedback in practice exams
- Did: added `--good` green vars to the exam CSS template (`utils/build_exam_html.py`), switched all correct-answer states (option card, letter, explanation, sidebar dot, score card, review tag) from gold to green; regenerated exam_{en,es,pt}.html; ignored `__pycache__/`.
- Verified: rebuild PASS (136 questions × 3 langs); Chrome study-mode check shows correct option green, wrong selection red; diff limited to the 8 intended selectors per file.
- Left: production Pages verification for `main` still pending from 2026-07-13; distrust nothing new — exam files remain generated, edit the template only.

## 2026-07-30 — Added the CCAR-P Professional practice exam and expanded the guide
- Did: read the official Professional Exam Guide (v1.0, effective July 2026) and checked its seven-domain, 38-objective blueprint into `data/professional_objectives.json`.
- Did: expanded `professional_en.md` with all 38 objectives, criterion-referenced scoring, the full policy set, the official five-course prep path, and an analysis of the three official sample questions.
- Did: authored a 126-item practice bank mapped to the official objectives, 26 of them multiple-response, drawing 63 items per attempt at the blueprint weights.
- Did: split `build()` into a parameterized `render_page()` and added multiple-response and weighted-draw support to the shared engine; Foundations output stays byte-stable apart from the engine script.
- Did: added `utils/validate_professional_bank.py` and `utils/test_exam_engine.mjs` and wired both into CI ahead of the site build, so a failure cannot deploy the placeholder page.
- Verified: bank validation PASS (126 items; per domain 22/16/24/20/18/18/8; 38 of 38 objectives covered; multiple-response share 20.6%); Professional build PASS (63 drawn across 7 domains).
- Verified: engine check PASS — the Foundations flat 12-per-domain 60-item draw is unchanged, the Professional weighted draw matched the blueprint across 50 consecutive draws, and all-or-nothing scoring, option toggle, overflow cap, and the study-mode lock all pass.
- Verified: Foundations rebuild PASS (136 questions × 3 langs, unchanged) and site build PASS with the real Professional exam published and `docs/practical/en.html` untouched; a fresh-context verifier re-ran the checks and confirmed every published number against the official guide PDF.
- Learned: rebalancing option letters after authoring silently broke explanation cross-references in two items; the validator now rejects letter references in explanations.
- Learned: an adversarial read of all 126 items found two whose keyed answer beat a distractor on a technicality, absurd distractors in all five select-THREE items, three objective mis-filings, and several duplicate clusters — all fixed before commit.
- Left: production Pages verification still pending from 2026-07-13; the doc-drift assertion for the README and guide numbers and the keyed-option length skew are deferred follow-ups.
