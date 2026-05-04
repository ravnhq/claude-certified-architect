# Claude Certified Architect — Foundations · Ravn Edition

Ravn-curated study materials for the **Claude Certified Architect — Foundations** certification, in the languages our team works in: **English**, **Spanish**, and **Portuguese**.

## Read online

The full guide and the practical exam are hosted on GitHub Pages:

**https://ravnhq.github.io/claude-certified-architect/**

The site has a language switcher (EN / ES / PT), full-text search, and a dark mode.

## Course access

- The certification is currently restricted to members of the Anthropic Partner Network and requires registration with a verified partner-company email — see [Claude Partner Network](https://claude.com/partners).
- Free for the first 5,000 partner-company employees; general availability priced at $99.
- To request access to the official course/exam portal: <https://anthropic.skilljar.com/claude-certified-architect-foundations-access-request>.

## Study guides

| Language | Markdown | PDF |
|---|---|---|
| English | [`guide_en.MD`](./guide_en.MD) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_en.pdf) |
| Spanish | [`guide_es.md`](./guide_es.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_es.pdf) |
| Portuguese | [`guide_pt.md`](./guide_pt.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_pt.pdf) |

PDFs are generated fresh on every deploy from the current markdown sources.

## Practical exam

Self-paced HTML quiz, runs entirely in your browser. Generated from each language's guide via:

```bash
python3 utils/build_practical_test_html.py        # all langs
python3 utils/build_practical_test_html.py en es  # specific langs
```

- English: [`practical_test_en.html`](./practical_test_en.html) — **76 questions** (5 scenarios).
- Spanish: [`practical_test_es.html`](./practical_test_es.html) — **76 questions** (5 scenarios).
- Portuguese: [`practical_test_pt.html`](./practical_test_pt.html) — **76 questions** (5 scenarios).

## How to use

1. Pick the guide that matches your preferred language.
2. Work through the scenarios and questions.
3. Use the **Practical Exercises** section to rehearse the key patterns: tool design, MCP integration, structured output, context management, and reliability.

## Repository layout

```
.
├── guide_{en,es,pt}.{md,MD}      # source-of-truth study guides
├── practical_test_*.html         # interactive quizzes built from the guides
├── extract_question.py           # parses guide_*.md → questions JSON
├── utils/build_practical_test_html.py  # questions JSON → practical_test_*.html
├── docs/                         # GitHub Pages site (static parts; CI generates the rest)
├── scripts/build-pages.mjs       # md → docs/ build (run by Pages workflow)
└── .github/workflows/
    └── pages.yml                 # generates PDFs and deploys docs/ to GitHub Pages
```

## Contributing

- Translation fixes and clarifications welcome via PR — please keep the heading structure aligned across `guide_en.MD`, `guide_es.md`, and `guide_pt.md` so question extraction stays consistent.
- PDFs regenerate automatically on merge to `main` as part of the Pages deploy.

## License

© Ravn. Originating study materials by Paul Larionov, used and adapted under the terms of the upstream license.
