# Score report

The score report reader takes a candidate's score-report PDF, identifies the exam, matches each objective row to the blueprint, asks only for what it could not resolve, and builds a personalized study guide ordered by domain weight, with a practice exam weighted to weak objectives. The result is saved on the device; the PDF is not.

## Sub-features

- `report-upload` parses a PDF in the browser and identifies the exam from its `Exam code` line or exam name.
- `report-choose` asks for the exam when the report names none, an unknown one, or two that conflict.
- `report-review` opens `Report details` on its own only when a row is unmatched, has an invalid percentage, or repeats an objective.
- `report-plan` shows priority topics (below 80%) grouped by domain, heaviest domain first, with explanation, example, and guidance per topic.
- `report-practice` hands off to the track's targeted practice exam: `practical/en.html?targeted=1`, `professional-en.html?targeted=1` or `developer-en.html?targeted=1`.
- `report-persist` restores the plan on return; `Report details → Delete saved study data` removes it.
- `report-share` sits under `Share or export`: download the plan as `.md`, copy a `#r=` link that rebuilds the plan on another device, and copy, save or load a custom exam.

## How to get to it (user POV)

- Home page → `Upload a score report →`.
- Direct page: `score-report.html`.
- A share link: `score-report.html#r=<payload>`.

## Driving it with agent-browser

Preconditions:

- Baseline from the index; no `ccaf-score-report-target` key (fresh session).
- A fixture PDF: `PDF=$(.claude/skills/verify-study-site/scripts/make-score-report.sh "$RUN_ID" CCAR-F 8)`. Its eight rows score `35, 95, 50, 80, 65, 40, 90, 55` on objectives `A1`–`A8`.

- **Open.** `b open score-report.html`. The heading reads `Turn your score report into a study plan.` and the `Upload your report` region holds the `Upload score report` file button.
- **Upload.** `b upload '#report-file' "$PDF"`, then `b wait 2500`. `b get text main` reads `Your personalized study guide.`, starts `CCAR-F · CLAUDE CERTIFIED ARCHITECT FOUNDATIONS` and reads `5 priority topics · 3 other`. `b proof score-report plan`.
- **Stored result.** `b eval 'localStorage["ccaf-score-report-target"]'` holds `examIdentity.code` `CCAR-F` and all eight scores, `A1:35` through `A8:55`.
- **Persistence.** `b reload`, `b wait 1500`. The plan is back without a new upload and reads `Saved on this device`. `b proof score-report restored`.
- **Targeted practice.** `b find role link click --name "Start practice exam"`. The URL ends `practical/en.html?targeted=1`, `#totalCount` reads `60`, and `#drawNote` starts `⟳Targeted score-report drill`. `b proof score-report targeted-exam`.
- **Exam choice.** `PDF2=$(… make-score-report.sh "$RUN_ID" CCAR-F 8 --no-code)`; on the plan choose `Upload another report`, then `b upload '#report-file' "$PDF2"`. The page reports `Couldn’t identify the exam. Choose the exam shown on your report.` and an `EXAM` combobox. `b select 'select' 'Architect Foundations (CCAR-F)'`, then `b click '#confirm-exam'` (`Continue`). The plan appears with the same `5 priority topics · 3 other`. `b proof score-report exam-chosen`.
- **Delete.** `b click '#review-title'` to open `Report details`, then `b find role button click --name "Delete saved study data"`. No confirm appears. `ccaf-score-report-target` and `ccaf-exam-en:targeted` are gone and `ccaf-score-report-target:cleared` is set; a reload shows the upload screen. `b proof score-report deleted`.
- **Download.** With a plan showing, `b click '.report-share-summary'` opens `Share or export`. `b download '#download-guide' "$EVIDENCE/score-report/study-guide.md"` (`EVIDENCE` as doctor prints it) saves a file that starts `# Personalized study guide — CCAR-F · Claude Certified Architect Foundations`.
- **Share link.** Capture what the page copies, since Chrome denies `b clipboard read`: `b eval 'navigator.clipboard.writeText = t => { window.__copied = t; return Promise.resolve(); }'`, then `b find role button click --name "Copy link to study guide"`. `#share-status` reads `Study guide link copied…` and `b eval 'window.__copied'` returns `…/score-report.html#r=<payload>`. Delete the saved data as above, then `b open "score-report.html#r=<payload>"`: the same plan (`5 priority topics · 3 other`) returns and `ccaf-score-report-target` is stored again. `b proof score-report share-link-restored`.

## Gotchas

- The upload screen's heading stays in the DOM, hidden, after a plan is built, so `b get text h1` still reads `Turn your score report into a study plan.` Read the plan through `b get text main` or a snapshot.
- After the first upload the file input is behind `Upload another report`; choose it before uploading again.
- Fixture rows only match with ligatures off. A Chrome-printed "fi" becomes its own PDF text item ("Con fi gure"), and the row falls through to review. The helper disables ligatures; a hand-made fixture must too.
- A row matches by objective text, so fixtures must take their wording from the run's `score-report-data.json`. That is what the helper does.
- Each track hands off to its own page; a Foundations report always goes to the English exam, never `es.html` or `pt.html`.
- The `writeText` stub only records the copied text; the code under test still builds the link. Opening a `#r=` link overwrites the saved plan without a confirm.
- The custom-exam buttons (`Copy link to custom exam`, `Save custom exam (.json)`, `Load custom exam`) were not driven when this map was written.
