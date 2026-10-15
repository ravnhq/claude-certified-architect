# Question bank

The question bank shows a track's whole item bank in one page, grouped by topic and objective, with a topic filter and a full-text search over stems, options, and explanations, and a live count of what matches.

## Sub-features

- `bank-browse` lists every item, grouped under topic headings and objective headings that carry their item counts.
- `bank-filter` narrows to one topic with `Filter by domain`.
- `bank-search` narrows by text; it combines with the topic filter.
- `bank-nav` jumps to a topic from the `Question bank` navigation.

## How to get to it (user POV)

- Home page track card → `Question bank EN`, or a Foundations `EN` / `ES` / `PT` bank link.
- The practice exam's `QUESTION BANK` link and the preflight checklist's `question bank` link.
- Direct pages: `practical/bank-en.html`, `bank-es.html`, `bank-pt.html`, `bank-professional-en.html`, `bank-developer-en.html`.

## Driving it with agent-browser

Preconditions:

- Baseline from the index.

- **Open.** `b open practical/bank-en.html`, `b wait 1500`. `b get text '#browseCount'` reads `607 of 607 questions`; headings include `AGENTIC LOOPS & ORCHESTRATION` and objective headings such as `1.1 Design and implement agentic loops…`. `b proof question-bank all`.
- **Search.** `b fill 'input[type=search]' 'PreToolUse'`, `b wait 500`. `#browseCount` drops below 607 (`28 of 607` when this map was written).
- **Filter.** `b select 'select' 'Hooks'`. `#browseCount` drops again (`15 of 607` with the search above). `b proof question-bank hooks-pretooluse`.
- **Empty state.** `b fill 'input[type=search]' 'stop_reason'` with `Hooks` still selected. `#browseCount` reads `0 of 607 questions` and the page shows `No question matches this filter.`
- **Clear.** `b fill 'input[type=search]' ''` and `b select 'select' 'All topics'`. `#browseCount` returns to `607 of 607 questions`.

## Gotchas

- The bank arrives with a fetch after load; read counts after `b wait`.
- The exact counts move whenever the bank is re-imported. Assert direction and the empty state, and quote counts as observed.
- The search box and the topic filter combine. Clear both before asserting a total.
- The topic labels on the English Foundations bank (`Hooks`, `MCP`, …) are groupings, not the five exam domains the practice exam uses.
