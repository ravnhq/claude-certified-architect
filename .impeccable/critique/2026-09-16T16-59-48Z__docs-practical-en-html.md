---
target: docs/practical/en.html
total_score: 20
max_score: 40
na_heuristics: 
p0_count: 1
p1_count: 5
target_identity: "file:/Users/pedro/Development/ravn/claude-certified-architect/docs/practical/en.html"
target_fingerprint: "sha256:2f1c415d7d7d9325b3645ad9cf01c599c704531f5f2cb8c89e3033ebed1d4279"
target_path: /Users/pedro/Development/ravn/claude-certified-architect/docs/practical/en.html
timestamp: 2026-09-16T16-59-48Z
slug: docs-practical-en-html
---
Method: dual-agent (A: design review, browser-driven · B: detector + static evidence)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | No timer, though the draw note promises "60 questions in 120 minutes"; zero live regions |
| 2 | Match System / Real World | 3 | Real domain weights and 720/1000 scale; misses labelled `F1-045`, never the blueprint task statement |
| 3 | User Control and Freedom | 2 | Study answers lock on first tap, no undo; summary's only labelled exit discards everything |
| 4 | Consistency and Standards | 2 | Discard guard on New set/length/domain but not on the Study↔Exam toggle that grades the attempt |
| 5 | Error Prevention | 1 | The most prominent button on every screen is irreversible and fires with 57 blanks, unguarded |
| 6 | Recognition Rather Than Recall | 3 | Labelled and grouped by domain with weights; the 60 navigator buttons carry no accessible state |
| 7 | Flexibility and Efficiency | 1 | Zero keydown handlers; 60 Tabs to the first answer; no flag-for-review |
| 8 | Aesthetic and Minimalist | 2 | 250px of chrome before Question 1 on a phone (30% of the viewport); 31,614px report |
| 9 | Error Recovery | 2 | Excellent per-item anatomy delivered as one 31,000px scroll under a single heading |
| 10 | Help and Documentation | 2 | Nothing says answers lock; no route from a weak domain to its guide |
| **Total** | | **20/40** | **Acceptable — bottom edge** |

## Design Specificity Verdict

**Partially specific: authored content in a generic shell.**

The content layer is unmistakably this product. The domain badge carries the blueprint weight
("Domain 1 · Agent Architecture and Orchestration — 27%"), the multi-select prompt reads "Select 2
responses" and at capacity "All 2 responses chosen. Deselect one to change your answer", the review
pane tags half-finished multis "(incomplete answer)", and the verdict uses the real 720/1000 cut with
an honest caveat. Somebody who sat this exam wrote it.

The interaction and visual layer could belong to any quiz engine built since 2015, and it diverges
from the project's own system:

- The page defines only `--r-sm: 4px` and `--r-md: 8px`. DESIGN.md's 18px card tier does not exist
  here; `.q-situation`, `.option`, `.score-card` and `.group-block` all measure 8px, so the
  three-tier shape language collapses to two.
- JetBrains Mono is embedded as a base64 `@font-face` at line 10 and used by **zero** elements on the
  exam screen (every computed `font-family` enumerated; result empty). The page pays the byte cost of
  the brand's second face and shows none of it. The bank id `F1-045` renders in Inter.
- Two off-palette hexes inline in `showSummary()`: `#e53e3e` (unanswered warning) sits ~10px above a
  verdict chip correctly using `--bad` `#C16B57`. Two different reds adjacent at the most emotionally
  loaded moment on the page.
- `.option-head:focus-visible` gets the branded gold ring. Prev, Next, Finish, both toggles and all 60
  navigator buttons fall through to Chrome's default `auto 1px rgb(0,95,204)`.

Brand is supposed to live in precise details on an Operate surface. Here the details are the weakest part.

### Deterministic scan

26 findings, exit 2, on the markup alone. The page is fully self-contained — inline `<style>`, its own
`:root`, no external stylesheet — so only this scope is evidence about it.

- **Confirmed:** 3 × `undersized-ui-text` (10.56px "Study"/"Exam"/"New set", only inside
  `@media (max-width: 420px)` — exactly the phone viewport); 3 × `design-system-color` (the inline
  Chakra-palette hexes above).
- **Detector caught what the review missed:** `.domain-label` and `.group-badge` both at 10px at
  *every* viewport, under the 11px floor the detector's own rule enforces but which it classified only
  as advisory; and `--fg-soft: #D4D4D4`, a `:root` token appearing nowhere in DESIGN.md.
- **False positives:** `overused-font` (Inter is the committed brand face); 2 of 3
  `design-system-radius` hits are `::-webkit-scrollbar-thumb` rules on 4px and 6px scrollbars, where
  half the track width is the only correct value.
- **Miscounted:** 16 × `design-system-font-size` is one finding, not sixteen. DESIGN.md publishes four
  sizes and sanctions more in prose without enumerating them, so the detector measures against a ramp
  the project never wrote down. Documentation gap, not drift.

**No visual overlay exists for this run.** Injection was not attempted: one browser session per
machine, and the design review held it for the full walkthrough.

## Overall Impression

The engine is better than its interface. Resume fidelity, multi-select handling and review anatomy are
the work of someone who understands the exam; the shell around them is default-quiz-app and, in two
places, actively hostile. The single biggest opportunity is the button hierarchy: the irreversible
action is the white primary on every screen and the action you take 59 times is a grey ghost beside it.

## What's Working

- **Resume fidelity.** Reload mid-attempt restored the same 60 ids in the same order, every answer,
  mode, length, focus and scroll position. That is the hardest promise in the phone-drill scene, met exactly.
- **Review anatomy.** Your letters and their text, the correct letters and their text, a separate
  "Why <letter>:" per letter, blanks read "Not answered", half-picked multis tagged "(incomplete answer)".
- **Multi-select at capacity** uses `aria-disabled` rather than `disabled`, so options stay tabbable,
  and `answer()` returns early instead of destroying keyboard focus.

## Priority Issues

**[P0] "Finish & Review" is the primary button everywhere and scores irreversibly, unguarded.**
White fill at 19.3:1, enabled from question 1 with zero answered, while "Next →" is a ghost at
`#A3A3A3`. On a phone it is the widest control (155px vs 84px), the only filled one, 31px tall,
bottom-right at thumb rest. Clicked at 3/60 it scored instantly: FAIL, 17/1000, 59 incorrect, 2
permanent misses written to storage. No confirm, and the way back is undiscoverable and 31,354px down.
*Fix:* make "Next →" the white primary and Finish a ghost; confirm naming the cost ("57 unanswered
will be scored as incorrect — finish anyway?"); add "← Back to my answers" as the first summary
control; hide Finish while the summary shows.

**[P1] The whole English bank ships inline: 1,556,137 bytes, 607 questions, 86.2% of the file.**
Every phone drill downloads 1.34 MB to answer 60 questions, on the scene PRODUCT.md names first-class.
*Fix:* split the bank to a fetched JSON payload, or ship per-domain shards the drill loads on demand.

**[P1] On phone, Next doesn't scroll to top.** Scrolled to 1,200, tapped Next, landed at 1,091 with
the "QUESTION 2" label and scenario 821px above the viewport; cards measure 1,062–1,524px. The
candidate reads option C of a question they never saw, then scrolls back a screen and a half, 59 times.
*Fix:* in `goto()`, after `renderQuestion()`, `scrollIntoView({block:'start'})` on mobile and
`content.scrollTop = 0` on desktop, honouring the existing reduced-motion query.

**[P1] Study mode grades on first tap with no undo, and the mode toggle is an unguarded grading switch.**
`setMode()` is the only state-changer without `confirmDiscard()`, which `newDraw()`, `setLength()` and
`setFocus()` all have. A mis-tap on a 337px option is a permanent wrong answer in the weak-spot record.
*Fix:* a deliberate "Check answer" step or a 5-second undo before `noteResult()` fires; route
`setMode()` through `confirmDiscard()` with copy naming the consequence.

**[P1] No timer, on a page that promises one.** The draw note reads "Full length mirrors the real exam
— 60 questions in 120 minutes"; there is no clock, verified statically and at runtime across arrival,
mid-attempt and summary. Pacing is what fails prepared candidates.
*Fix:* an elapsed/remaining clock in the topbar, Exam mode only, persisted beside the answers — or cut
"in 120 minutes" from the note.

**[P1] The score report is 31,614px with one heading and one action.** `.section-title` and
`.group-title` are `<div>`s, so the only heading is `h1 Exam Complete`; "New attempt" sits at y=31,214.
Unnavigable by screen reader, unreachable by thumb, and items are labelled `F1-045`, which maps to
nothing a candidate can study, while `task_id` maps to a chapter.
*Fix:* collapse items to one-line stems under real `<h2>`/`<h3>` per domain, show the task statement
id in the already-loaded mono, and move next steps to the top.

## Persona Red Flags

**Sam (keyboard / screen reader):** 70 tabbables with `sb-0`…`sb-59` sitting between the topbar and
`<main>` and no skip link — 60 Tabs to the first `.option-head`, every question. `#sb-1`'s accessible
name is literally "2", with no `aria-label` and no `aria-current`. Correct/incorrect state is
colour-only: `--good` `#6FA97C` against `--bad` `#C16B57` is **1.39:1**. Zero live regions, no headings
during the attempt, and the branded focus ring exists on one control type out of five.

**Casey (distracted mobile):** 250px of chrome before "QUESTION 1" — 30% of an 844px viewport. 72
targets under 44×44, including mode toggles at 23px, navigator buttons at 29px, and the entire sticky
Prev/Next/Finish bar at 31px with 8px gaps and 10.56px labels. "Answered: 3 / 60" sits at `order: 2`,
y=1,412 — below the question, so progress is invisible mid-drill.

**Dani (delivery lead, non-engineer):** lands on a cold open with no start screen and no framing,
already at Question 1 of 60 drawn, facing 8 header controls before the first question. Nothing states
that answers lock. The one thing that would help — a route from a weak domain to its guide chapter —
does not exist at either end of the attempt.

## Minor Observations

- The exam screen has no heading element at all; `.sidebar-header`, `.topbar-title` and
  `.section-title` are all `<div>`s.
- `prefers-reduced-motion` is fully honored here (7 transitions, 0 keyframes, all zeroed) — the
  site-wide concern from the earlier audit does not apply to this page.
- The page loads no `app.js`, so the site's search and theme toggle are inert chrome on this surface.
- Cognitive load fails 4 of 8 checks; the header cluster is 8 controls and the domain select is 6 options.
