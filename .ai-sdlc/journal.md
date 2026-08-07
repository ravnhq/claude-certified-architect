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

## 2026-08-03 — Repaired ten code-review findings in the exam engine and its gates
- Did: gave `render_page()` explicit `pass_score` and `pass_pct` parameters. The Professional page now reads `_exam.pass_score` from its own blueprint instead of the Foundations constant, so the two cut scores can no longer move together by accident. Both are 720 today, so all four pages rebuilt byte-identical, which isolated this refactor from every later change.
- Did: made the review pane show every item that did not score. `showSummary()` returned before recording a half-picked multiple-response answer, so about 13 items per attempt were scored incorrect and then hidden, with no rationale. Grading now lives in a pure `classify()` and `tallyAttempt()` above the harness boundary.
- Did: split the review pane's merged rationale into one "Why <letter>:" block per correct letter, and labeled blank rows "Not answered" and half-picked rows "incomplete answer" instead of printing an empty dash.
- Did: escaped both innerHTML and the inline script payload. `md()` now escapes `&`, `<`, `>` before it applies markdown, `esc()` covers the domain and scenario names that bypass `md()`, and the JSON payloads escape `<` and U+2028/U+2029, so no item text can close the script block or inject markup.
- Did: kept at-capacity options in the tab order with `aria-disabled` instead of `disabled`, added a visible hint that names the deselect step, and made `answer()` return early on a no-op click so the repaint cannot discard keyboard focus. Revealed options keep real `disabled`; that state is terminal.
- Did: versioned the saved attempt and checked its per-domain mix, not only its total, so a blueprint revision that keeps 63 items cannot leave a returning candidate on the old weighting. A payload written before versioning existed is kept if it is otherwise valid, so upgrading the engine does not throw away an attempt a candidate has in progress.
- Did: taught the bank validator to compare the count the stem states with the count the item is keyed to, reading the number that follows each "select" rather than the whole stem, because one stem says "these two needs" as prose. Single-response stems are checked too.
- Did: made the explanation cross-reference guard catch a sentence-initial "Option D" by matching the keyword in both cases while keeping the letter uppercase. Whole-pattern `re.IGNORECASE` would have flagged the ordinary phrase "see a cost spike".
- Did: replaced the per-domain `round()` in `check_draw` with largest-remainder apportionment, which totals the exam size by construction, so a future weight revision cannot leave the gate rejecting every possible draw. Added a weights-total-100 assertion.
- Did: switched the harness to `fileURLToPath`, so a repo path containing a space no longer resolves to `%20` and fails with ENOENT.
- Did: added `utils/test_exam_render.mjs` and wired it into CI. It runs the whole engine against a stub DOM and reads the HTML back, covering the summary and question screens that the logic harness cannot reach.
- Verified: bank validation PASS (126 items, 38 of 38 objectives, 20.6% multiple-response); both builds PASS; engine harness PASS at 90 checks; render harness PASS at 28 checks; site build PASS.
- Verified: each new gate was proved against an injected defect, not only against the clean tree. A three-key item under a "(Select TWO.)" stem fails with the new stem message and not the pre-existing one; "Option D fails because" fails while "see a cost spike" passes; apportionment still totals 63 for weight sets whose naive `round()` gives 61 or 65; the render harness fails 6 of 10 checks against the pre-fix page.
- Verified: the harness runs clean from a directory whose name contains a space.
- Learned: a gate that only ever runs against a passing tree proves nothing. Three of these findings were latent holes in checks that had always reported green.
- Learned: the review pane defect survived because the harness cut its input at the sidebar boundary, so the whole render path was unexercised. The new render harness closes that gap.
- Left: the change set is uncommitted. Production Pages verification is still pending from 2026-07-13, and the doc-drift assertion and the keyed-option length skew remain deferred.
