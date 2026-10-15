# Study guides and site chrome

The study guides render each track's markdown guide as a page with a contents rail and linkable headings. Every page shares the chrome: a search dialog over all guides with a language filter, a theme toggle that persists, and the home page's track chooser.

## Sub-features

- `guide-read` renders a guide with its `Contents` navigation and heading anchors.
- `guide-search` opens `Search the study guides`, searches all guides, filters by `ALL` / `EN` / `ES` / `PT`, and links each hit to its section.
- `site-theme` toggles dark and light and keeps the choice across pages and reloads.
- `site-home` offers three track cards with links to each track's guide, practice exam, question bank, and registration. Each card's `N MORE` disclosure holds the preflight checklist, and on Foundations the cheatsheets and guide PDFs.

## How to get to it (user POV)

- Home page (`index.html`) → a track card's `Study guide EN` link, or a Foundations `EN` / `ES` / `PT` guide link.
- Direct pages: `guides/en.html`, `guides/es.html`, `guides/pt.html`, `guides/professional-en.html`, `guides/developer-en.html`.
- `Search` and `Toggle theme` buttons in the `Page controls` navigation on every page that carries the site header. `Meta+k` or `Control+k` also opens search.

## Driving it with agent-browser

Preconditions:

- Baseline from the index; no `theme` key.

- **Home.** `b open index.html`. The heading reads `Claude Certified Architect — choose your track.` with headings `Architect — Foundations`, `Architect — Professional`, `Developer — Foundations`. `b proof study-guides home`.
- **Open a guide.** `b find role link click --name "Study guide EN"` opens `guides/professional-en.html` (the first of two such links), or `b open guides/en.html`. The `Contents` navigation lists chapter links such as `Chapter 1: Claude API — Fundamentals of Model Interaction`.
- **Contents jump.** `b find role link click --name "Chapter 2: Tools and tool_use"`. The URL gains `#chapter-2-tools-and-tool-use` and that heading is in view. `b proof study-guides contents-jump`.
- **Search.** `b find role button click --name "Search"`. A dialog headed `Search the study guides` opens with `Search terms`. `b fill '#search-input' 'stop_reason'`, `b wait 1200`. `b get text '#search-status'` reads `<n> results`, or `1 result` (20 when this map was written) and the hits link into guide sections (`guides/<page>.html#<slug>`). `b find role button click --name "EN"` limits hits to the English guides: `guides/en.html`, `guides/professional-en.html`, `guides/developer-en.html`. `b proof study-guides search`. `b press Escape` closes it.
- **More links.** On the home page, `b click 'details.chooser-more > summary'` opens the first card's `3 MORE`. `b find role link click --name "Preflight checklist"` opens `preflight/architect-foundations.html`. `b proof study-guides home-more`.
- **Theme.** `b eval 'document.documentElement.dataset.theme'` reads `dark`. `b find role button click --name "Toggle theme"` makes it `light` and `localStorage.theme` `light`. `b reload` keeps `light`. Toggle again to restore `dark`.

## Gotchas

- Search loads its index on first open; query only after the dialog shows `Search terms` and `b wait` has passed.
- Links inside a closed `N MORE` disclosure are hidden, so `snapshot -i` omits them and `find` cannot click them. Open the disclosure first.
- `Study guide EN` names both the Professional and the Developer card links; `find` takes the first. Use `b open` for a specific guide.
- Search spans every language by default, so the first hit may be Spanish or Portuguese. Use the language buttons before asserting an English hit.
- Heading ids are slugs of the heading text with a counter for repeats (`-2`, `-3`). Assert the slug the contents link carries, not one you derive.
- Pages carry `<base href="/claude-certified-architect/">`. A bare `#id` link would resolve to the home page; guide links are page-qualified for that reason.
- The PDF download links return 404 on a local run because PDFs are not built.
