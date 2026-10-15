# Practice exam

The practice exam draws a fresh attempt from a track's bank, lets the candidate answer in study mode (rationale shown per answer) or exam mode (revealed at the end), keeps progress across reloads, and scores the attempt on the 1,000 scale with a 720 cut and a per-domain breakdown.

## Sub-features

- `exam-draw` builds an attempt: Foundations 60 (12 per domain), Professional 63, Developer 53; `QUICK · 20` draws a short attempt.
- `exam-answer` records a choice; study mode reveals the correct option and every option's rationale.
- `exam-persist` restores the attempt, answers, and position after a reload.
- `exam-finish` warns about unanswered items, then shows the summary: verdict, scaled score, correct and incorrect counts, per-domain table, review of misses.
- `exam-restart` draws a new set from `⟳NEW SET` or the summary's `NEW ATTEMPT — NEW RANDOM DRAW`.
- `exam-drill` drills one domain's whole bank (`Drill one domain`) or past misses (`Drill my misses`), scored raw with no pass/fail.

## How to get to it (user POV)

- Home page track card → `Practice exam EN` (Professional, Developer) or the Foundations `EN` / `ES` / `PT` practice links.
- Direct pages: `practical/en.html`, `practical/es.html`, `practical/pt.html`, `practical/professional-en.html`, `practical/developer-en.html`.
- The question bank's `PRACTICE EXAM` link, and the preflight checklist's `Ravn practice exam` link.
- From the score report, `Start practice exam` opens `practical/en.html?targeted=1` (see [score-report.md](./score-report.md)).

## Driving it with agent-browser

Preconditions:

- Baseline from the index; no `ccaf-exam-en` key in `localStorage` (fresh session).

- **Open.** `b open practical/en.html`, then `b wait 1500` for the bank fetch. `b get text '#qCounter'` reads `1 / 60`; `b get text '#totalCount'` reads `60`; the `Questions` navigation lists buttons `1`–`60`.
- **Study mode.** `b find role button click --name "STUDY"`. `b get text '#modeHint'` reads `Answers reveal as you go`.
- **Answer.** `b click '#qCard button:nth-of-type(1)'`. `#answeredCount` reads `1` and `b get text '#qCard'` now carries the rationale under each option. `b proof practice-exam answered`.
- **Persistence.** `b reload`, `b wait 1500`. `#answeredCount` still reads `1` and `#qCard` shows the same stem. `b eval 'Object.keys(localStorage)'` lists `ccaf-exam-en`. `b proof practice-exam reloaded`.
- **Finish.** `b find role button click --name "FINISH & REVIEW"`. A confirm reads `59 question(s) are still unanswered…`; `b dialog accept`. `b get text '#summaryContent'` shows `Exam Complete`, `You answered 1 of 60 questions.`, a `PASS`/`FAIL` verdict, `<n>/1000`, and `Score by domain` with five rows of `x/12`. `b proof practice-exam summary`.
- **Back to answers.** `b find role button click --name "← Back to my answers"` returns to the question screen with the attempt intact.
- **New draw.** `b find role button click --name "⟳NEW SET"` (accept the discard confirm if one appears). `#answeredCount` returns to `0` and the first stem changes.
- **Domain drill.** `b select '#focusSelect' 'Domain 2 · Tool Design and MCP Integration'`, accepting any discard confirm. `#totalCount` becomes that domain's bank size and the length toggle is disabled.
- **Other tracks.** Repeat Open on `practical/professional-en.html` (expect `63`) and `practical/developer-en.html` (expect `53`).

## Gotchas

- The question text arrives with a bank fetch after load. Reading `#qCard` before `b wait` finishes shows an empty card.
- Every attempt is a random draw. Assert counts, ids, and structure, not a particular stem or correct letter, across runs.
- Finishing with unanswered items, starting a new set, switching length, or switching focus over a started attempt each raise a native confirm. Commands fail until it is answered.
- Switching to study mode over an exam-mode attempt with answers also asks to confirm.
- `ES` and `PT` draw only from the 136 hand-authored items; English draws from 607. Bank sizes differ by language.
- `?targeted=1` uses its own key (`ccaf-exam-en:targeted`), so a targeted attempt and a normal one do not overwrite each other.
