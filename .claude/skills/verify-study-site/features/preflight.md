# Preflight checklist

The preflight checklist gives each track ten readiness checks, the exam blueprint, and links to practice material. Ticks stay in the browser across visits and clear with one reset.

## Sub-features

- `preflight-tick` ticks or unticks a check by its label.
- `preflight-persist` restores ticks after a reload.
- `preflight-reset` clears every tick with `RESET CHECKLIST`.
- `preflight-tracks` switches between the Foundations, Professional, and Developer checklists.

## How to get to it (user POV)

- README and track pages link the Foundations checklist at `preflight/en.html`.
- From a checklist, the `Architect — Professional` and `Developer — Foundations` links.
- Direct pages: `preflight/en.html`, `preflight/architect-foundations.html`, `preflight/architect-professional.html`, `preflight/developer-foundations.html`.

## Driving it with agent-browser

Preconditions:

- Baseline from the index; no `ccaf-preflight:state` key.

- **Open.** `b open preflight/en.html`. The heading reads `Ten checks before you book the slot.`; the `Readiness checklist` region holds ten checkboxes, all `checked=false`.
- **Tick.** `b find role checkbox click --name "04 Can name and explain all 5 domains"`. That checkbox reports `checked=true`. `b proof preflight ticked`.
- **Persistence.** `b reload`. `b eval '[...document.querySelectorAll("input[type=checkbox]")].map(c=>c.checked?1:0).join("")'` reads `0001000000`, and `b eval 'localStorage["ccaf-preflight:state"]'` reads `{"checked":["04"]}`. `b proof preflight reloaded`.
- **Reset.** `b find role button click --name "RESET CHECKLIST"`. All ten read `0` and `ccaf-preflight:state` is gone. No confirm appears.
- **Other tracks.** `b find role link click --name "Architect — Professional"` opens `preflight/architect-professional.html` with its own ten checks.

## Gotchas

- A checkbox's accessible name is its whole label text, including the description and link text. Match on the leading number and title with a prefix, or use the checkbox index.
- Reset clears immediately, without a confirm; there is no undo.
- Each track keeps its own storage key. Read the key on the page you ticked.
