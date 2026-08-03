# Claude Certified Architect · Ravn Edition

Ravn-curated study materials for the **Foundations** and **Professional** Claude Certified Architect tracks.

## Read online

The full guide and the practical exam are hosted on GitHub Pages:

**https://ravnhq.github.io/claude-certified-architect/**

The site has a language switcher (EN / ES / PT), full-text search, and a dark mode.

Before you book a Foundations slot, work through the
[preflight checklist](https://ravnhq.github.io/claude-certified-architect/preflight/en.html):
ten readiness checks, the exam blueprint, and a list of practice material. Your ticks stay in
the browser.

## Choose your track

| Track | Best fit | Ravn guidance |
|---|---|---|
| **Foundations** | Practitioners building with Claude Code, the Claude Agent SDK, the Claude API, and MCP | Full guides in English, Spanish, and Portuguese; practice exam and cheatsheet |
| **Professional** | Mid- to senior-level architects and engineers responsible for production AI architecture, evaluation, governance, and lifecycle decisions | [English Professional study guide](./professional_en.md), based on the official July 2026 blueprint |

The Professional exam has a separate seven-domain blueprint. The Foundations practice exam and cheatsheet do not represent Professional exam coverage.

## Official access

### Foundations

- The certification is currently restricted to members of the Anthropic Partner Network and requires registration with a verified partner-company email — see [Claude Partner Network](https://claude.com/partners).
- Free for the first 5,000 partner-company employees; general availability priced at $99.
- To request access to the official course/exam portal: <https://anthropic.skilljar.com/claude-certified-architect-foundations-access-request>.

### Professional

- Exam code **CCAR-P**: 63 items, 120 minutes, scaled passing score of 720, and a $175 USD fee.
- Review the [official Professional Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf).
- Register through the [Anthropic Partner Academy Professional certification page](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification).

## Foundations study guides

| Language | Markdown | PDF |
|---|---|---|
| English | [`guide_en.MD`](./guide_en.MD) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_en.pdf) |
| Spanish | [`guide_es.md`](./guide_es.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_es.pdf) |
| Portuguese | [`guide_pt.md`](./guide_pt.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_pt.pdf) |

PDFs are generated fresh on every deploy from the current markdown sources.

## Professional study guide

| Language | Markdown | Read online |
|---|---|---|
| English | [`professional_en.md`](./professional_en.md) | [Open](https://ravnhq.github.io/claude-certified-architect/guides/professional-en.html) |

## Foundations practice exam

Self-paced HTML quiz, runs entirely in your browser. It works as a **question bank**: each
attempt draws **12 random questions per domain — 60 in total** — from a pool of 136 (the 76
scenario questions from the guide plus 60 domain-style questions from the mock bank), organized
by the five CCAF exam domains. The overall score is **scaled to 1000** with a passing cut of
**720**, mirroring the real exam's 100–1000 scale.

Features: a fresh 60-question draw each attempt, questions randomized **within each domain**, a
**study** mode (answers reveal as you go, with a rationale for every option) vs an **exam** mode
(answers reveal at the end), per-domain score breakdown with a pass threshold, and progress saved
in the browser (`localStorage`) so a refresh keeps your place and draw. **Restart** draws a new
set of 60.

Built from the guides + the mock bank via:

```bash
python3 utils/build_exam_html.py            # all langs → exam_{en,es,pt}.html
python3 utils/build_exam_html.py en es      # specific langs
```

- English: [`exam_en.html`](./exam_en.html)
- Spanish: [`exam_es.html`](./exam_es.html)
- Portuguese: [`exam_pt.html`](./exam_pt.html)

> The exam regenerates fresh on every deploy. Domain classification lives in
> [`data/domains.json`](./data/domains.json) (review notes in `data/domains_review.md`);
> the mock questions and their ES/PT translations live in `data/mock_{en,es,pt}.json`.

## Foundations cheatsheet

A one-page study reference that distills the exam into **12 recurring principles** (each with the
correct approach and the trap to avoid), **5 questions to ask when two answers look equally good**,
and a breakdown of the **136-question, 5-domain** exam (domain weights + answer-letter
distribution). Self-contained static pages in the same Ravn styling as the rest of the site.

- English: [`cheatsheet_en.html`](./cheatsheet_en.html)
- Spanish: [`cheatsheet_es.html`](./cheatsheet_es.html)
- Portuguese: [`cheatsheet_pt.html`](./cheatsheet_pt.html)

```bash
python3 utils/build_cheatsheet.py           # regenerate all langs → cheatsheet_{en,es,pt}.html
```

> Unlike the exam, the cheatsheet is hand-authored content, so the committed HTML is what
> deploys; re-run the generator only when editing the content. Keep its stats in sync with
> `data/domains.json` and `utils/exam_data.py` (`DOMAIN_NAMES`).

## How to use

1. Choose the certification track you plan to take.
2. For Foundations, pick a language, work through the scenarios, and use the practice exam and cheatsheet.
3. For Professional, map your experience against the seven weighted domains, build one end-to-end reference system, and rehearse architectural trade-offs under time pressure.

## Repository layout

```
.
├── guide_{en,es,pt}.{md,MD}      # source-of-truth study guides (76 scenario questions)
├── professional_en.md             # Professional-track guide (7-domain July 2026 blueprint)
├── CCAF_Mock_Exam_*.txt          # source for the 60-question mock bank
├── exam_{en,es,pt}.html          # the unified 136-question practice exam (built)
├── cheatsheet_{en,es,pt}.html    # 12-principle exam cheatsheet (static, hand-authored)
├── extract_question.py           # parses guide_*.md → scenario questions JSON
├── parse_mock_exam.py            # parses the mock .txt → mock questions JSON
├── data/
│   ├── domains.json              # question id → CCAF domain (1–5) — reviewable
│   ├── duplicates.json           # mock ids dropped as dupes of guide qs (empty)
│   └── mock_{en,es,pt}.json      # mock bank + ES/PT translations
├── utils/
│   ├── exam_data.py              # merges guide + mock into the unified schema
│   ├── build_exam_html.py        # unified schema → exam_*.html
│   └── build_cheatsheet.py       # → cheatsheet_*.html
├── docs/                         # GitHub Pages site (static parts; CI generates the rest)
├── scripts/build-pages.mjs       # md → docs/ build (run by Pages workflow)
└── .github/workflows/
    └── pages.yml                 # generates PDFs + exam HTML, deploys docs/ to Pages
```

## Contributing

- Translation fixes and clarifications welcome via PR — please keep the heading structure aligned across `guide_en.MD`, `guide_es.md`, and `guide_pt.md` so question extraction stays consistent.
- PDFs regenerate automatically on merge to `main` as part of the Pages deploy.

## License

© Ravn. Originating study materials by Paul Larionov, used and adapted under the terms of the upstream license.
