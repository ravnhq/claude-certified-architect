# Practice exam

The practice exam draws a fresh attempt from a track's bank, lets the candidate answer in study mode (rationale shown per answer) or exam mode (revealed at the end), keeps progress across reloads, and scores the attempt on the 1,000 scale with a 720 cut and a per-domain breakdown.

## Sub-features

- `exam-draw` builds an attempt: Foundations 60 (12 per domain), Professional 63, Developer 53. `QUICK` draws about a third: 20, 21 and 19.
- `exam-answer` records a choice; study mode locks the item and shows the rationale for the chosen option and the correct one.
- `exam-timer` counts up `Time m:ss / 120:00` in exam mode on a full-length draw only.
- `exam-persist` restores the attempt, answers, position, mode, length and drill after a reload.
- `exam-finish` warns about unanswered items, then shows the summary: verdict, scaled score, correct and incorrect counts, per-domain table, review of misses.
- `exam-restart` draws a new set from `⟳NEW SET` or the summary's `NEW ATTEMPT — NEW RANDOM DRAW`.
- `exam-drill` drills one domain's whole bank from the domain select, or past wrong answers from the misses button (`My misses · N`), scored raw with no pass/fail.

## How to get to it (user POV)

- Home page track card → `Practice exam EN` (Professional, Developer) or the Foundations `EN` / `ES` / `PT` practice links.
- Direct pages: `practical/en.html`, `practical/es.html`, `practical/pt.html`, `practical/professional-en.html`, `practical/developer-en.html`.
- The question bank's `PRACTICE EXAM` link, and the preflight checklist's `Ravn practice exam` link.
- From the score report, `Start practice exam` opens the track's page with `?targeted=1` (see [score-report.md](./score-report.md)).

## Driving it with agent-browser

Preconditions:

- Baseline from the index; no `ccaf-exam-en` key in `localStorage` (fresh session).

- **Open.** `b open practical/en.html`, then `b wait 1500` for the bank fetch. `b get text '#qCounter'` reads `1 / 60`; `b get text '#totalCount'` reads `60`; the `Questions` navigation lists buttons `1`–`60`.
- **Study mode.** `b find role button click --name "STUDY"`. `b get text '#modeHint'` reads `Answers reveal as you go`.
- **Answer.** `b find nth 0 '#qCard .option-head' click` (option A; `nth 1` is B). `#answeredCount` reads `1` and `b get text '#qCard'` shows the rationale under the chosen and the correct option. `b proof practice-exam answered`.
- **Persistence.** `b reload`, `b wait 1500`. `#answeredCount` still reads `1` and `#qCard` shows the same stem. `b eval 'Object.keys(localStorage)'` lists `ccaf-exam-en`. `b proof practice-exam reloaded`.
- **Finish.** `b find role button click --name "FINISH & REVIEW"`. A confirm reads `59 question(s) are still unanswered…`; `b dialog accept`. `b get text '#summaryContent'` shows `Exam Complete`, `You answered 1 of 60 questions.`, a `PASS`/`FAIL` verdict, `<n>/1000`, and `Score by domain` with five rows of `x/12 · NN%`. `b proof practice-exam summary`.
- **Back to answers.** `b find role button click --name "← Back to my answers"` returns to the question screen with the attempt intact.
- **New draw.** `b find role button click --name "⟳NEW SET"`, then `b dialog accept` on `Start a new attempt with a fresh random draw?…`. `#answeredCount` returns to `0` and the first stem changes.
- **Domain drill.** `b select '#focusSelect' 'Domain 2 · Tool Design and MCP Integration'`, accepting any discard confirm. `#totalCount` becomes that domain's bank size (`97` when this map was written), `#drawNote` starts `⟳Domain 2 drill`, and `FULL · 60` and `QUICK · 20` are disabled. Select `All domains` to return.
- **Misses drill.** After a finished attempt with a wrong answer, `b find role button click --name "Drill my misses"`. `#totalCount` is the number of items answered wrong (unanswered ones do not count) and `#drawNote` starts `⟳Weak-spot drill`. The misses live in `ccaf-exam-en:misses`. Click the same button again to leave the drill.
- **Exam mode and timer.** On a full-length draw with no answers, `b find role button click --name "EXAM"`. `#modeHint` reads `Answers reveal at the end` and `b get text '#examTimer'` reads `Time 0:00 / 120:00`. Answer one item, then click `STUDY`: a confirm reads `Switching to Study reveals the correct answer for every question you have already answered. Continue?`.
- **Quick length.** `b find role button click --name "QUICK · 20"` (accept the confirm over a started attempt). `#totalCount` reads `20`.
- **Other tracks.** Repeat Open on `practical/professional-en.html` (expect `63`, quick `21`, seven domain rows `x/11 … x/4`) and `practical/developer-en.html` (expect `53`, quick `19`, eight domain rows).

## Gotchas

- The question text arrives with a bank fetch after load. Reading `#qCard` before `b wait` finishes shows a `Loading questions…` skeleton.
- Every attempt is a random draw. Assert counts, ids, and structure, not a particular stem or correct letter, across runs.
- Finishing with unanswered items, starting a new set, switching length, or switching focus over a started attempt each raise a native confirm. The click returns at once; every later command fails until `b dialog accept` or `b dialog dismiss` answers it. `b dialog status` shows whether one is open.
- Switching to study mode over an exam-mode attempt with answers also asks to confirm.
- Each option is one `.option` holding its own `.option-head` button, so `#qCard button:nth-of-type(n)` matches every option at once. Use `b find nth <i> '#qCard .option-head'`.
- The drill persists across reloads. During a misses drill the domain select is disabled and reads `All domains`; the misses button (`aria-pressed=true`) is the way out. Check `#drawNote` before assuming a fresh full draw.
- `Drill my misses` and `Drill one domain` are accessible names only. The buttons read `My misses · N` (or `No misses yet`, disabled) and the select reads `All domains`.
- The timer shows only on a full-length exam-mode draw; it is empty in study mode and on a quick draw.
- `ES` and `PT` draw only from the 136 hand-authored items; English draws from 607. Bank sizes differ by language.
- `?targeted=1` uses its own key (`ccaf-exam-en:targeted`), so a targeted attempt and a normal one do not overwrite each other.
