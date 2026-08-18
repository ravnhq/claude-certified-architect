# Claude Certified Architect · Ravn Edition

Ravn-curated study materials for the Claude Certified Architect certifications, in English,
Spanish, and Portuguese.

**Read online: <https://ravnhq.github.io/claude-certified-architect/>**

The site has a language switcher (EN / ES / PT), full-text search, and a dark mode.

Before you book a Foundations slot, work through the
[preflight checklist](https://ravnhq.github.io/claude-certified-architect/preflight/en.html):
ten readiness checks, the exam blueprint, and a list of practice material. Your ticks stay in
the browser.

## Choose your track

| Track | Exam code | Best fit | What this repo gives you |
|---|---|---|---|
| **Architect – Foundations** | CCAR-F | Practitioners building with Claude Code, the Claude Agent SDK, the Claude API, and MCP | Study guide, practice exam, and cheatsheet in EN / ES / PT, plus the preflight checklist |
| **Architect – Professional** | CCAR-P | Architects responsible for production AI architecture, evaluation, governance, and lifecycle decisions | English study guide and a 126-question practice exam |
| **Developer – Foundations** | CCDV-F | Engineers building and shipping production applications, agents, and workflows on the Claude platform | English study guide |

The two exams use different blueprints. Foundations has five domains; Professional has seven.
Foundations material does not represent Professional coverage, and the reverse is equally true.

> **Professional material is English only.** Anthropic delivers the exam and its prep content in
> English and prohibits browser translation during proctored testing, so an ES/PT Professional
> track would train against wording the exam never uses. The Foundations material stays
> tri-language.

## Exam facts

Both figures below come from the official exam guides, which are the authoritative source and
which Anthropic marks subject to change.

| | Architect – Foundations | Architect – Professional | Developer – Foundations |
|---|---|---|---|
| Exam code | CCAR-F | CCAR-P | CCDV-F |
| Items | 60 | 63 | 53 |
| Time | 120 minutes | 120 minutes | 120 minutes |
| Passing score | 720 on a 100–1,000 scale | 720 on a 100–1,000 scale | 720 on a 100–1,000 scale |
| List fee | $125 USD | $175 USD | $125 USD |
| Validity | 12 months | 12 months | 12 months |
| Prerequisites | None | None | None |
| Delivery | Proctored by Pearson VUE, English only | Proctored by Pearson VUE, English only | Proctored by Pearson VUE, English only |

**No course is required to sit either exam.** The credential is awarded on exam performance alone.
Anthropic publishes free prep courses, and they help, but they are not a gate.

**On the fee.** $125 and $175 are the list prices in the exam guides. The amount at checkout
reflects any discount for your partner tier, so what you pay may be lower. Earlier promotional
pricing for the first wave of partner-company employees no longer describes the general case.

### Policies worth knowing before you register

- Up to **4 attempts** per exam in a rolling 12-month period. The fee applies to each attempt.
- Retake waits after a failure: **14 days**, then **30**, then **90**.
- Reschedule or cancel **more than 24 hours ahead**. Inside 24 hours, or a no-show, forfeits the fee.
- Bring a valid, unexpired **government photo ID** whose name matches your registration exactly.
- Renewal is **free and non-proctored** if you renew on time. Let the credential lapse and you
  retake the full exam at full fee.

## Official access

- Certification is restricted to members of the Anthropic Partner Network and requires
  registration with a verified partner-company email. See [Claude Partner Network](https://claude.com/partners).
- Register through the [Anthropic Partner Academy](https://anthropic-partners.skilljar.com/page/partner-certifications),
  then schedule with Pearson VUE using the credentials they email you.
- Official guides, both marked subject to change:
  [Foundations](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) ·
  [Professional](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf)
- See also the [certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications).

### Prep courses

Anthropic publishes **seven free prep courses** for Foundations and a **five-course path** for
Professional. None are required. Ranked by how much of the Foundations blueprint they actually
cover: **Claude Code in Action** (Domain 3, 20%), **Introduction to Model Context Protocol**
(Domain 2, 18%), and **Building with the Claude API** (Domains 2 and 4). Claude with Amazon
Bedrock and Claude on Google Cloud are long and only partly on-blueprint; Claude 101 and AI
Fluency are orientation rather than exam preparation.

- [Foundations prep courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
- [Professional prep path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional) — 5 courses, about 12 hours

## Foundations study guides

| Language | Markdown | PDF |
|---|---|---|
| English | [`guide_en.MD`](./guide_en.MD) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_en.pdf) |
| Spanish | [`guide_es.md`](./guide_es.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_es.pdf) |
| Portuguese | [`guide_pt.md`](./guide_pt.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_pt.pdf) |

PDFs are generated fresh on every deploy from the current markdown sources.

## Foundations practice exam

A self-paced HTML quiz that runs entirely in your browser. Each attempt draws **12 random
questions per domain — 60 in total** — from a pool of 136: the 76 scenario questions from the
guide plus 60 domain-style questions from the mock bank. The score is scaled to 1,000 with a
passing cut of **720**, mirroring the real scale.

Features: a fresh 60-question draw each attempt, questions randomized within each domain, a
**study** mode that reveals answers as you go with a rationale for every option, an **exam** mode
that reveals at the end, per-domain breakdown against the pass threshold, and progress saved in
`localStorage` so a refresh keeps your place. **Restart** draws a new set.

- [`exam_en.html`](./exam_en.html) · [`exam_es.html`](./exam_es.html) · [`exam_pt.html`](./exam_pt.html)

## Foundations cheatsheet

A one-page reference distilling the exam into **12 recurring principles** — each with the correct
approach and the trap to avoid — **5 questions to ask when two answers look equally good**, and a
breakdown of the 136-question, 5-domain pool with domain weights and answer-letter distribution.

- [`cheatsheet_en.html`](./cheatsheet_en.html) · [`cheatsheet_es.html`](./cheatsheet_es.html) · [`cheatsheet_pt.html`](./cheatsheet_pt.html)

## Developer study guide

[`developer_en.md`](./developer_en.md) · [read online](https://ravnhq.github.io/claude-certified-architect/guides/developer-en.html)

Covers the **eight-domain Developer – Foundations blueprint (CCDV-F)**: agents and workflows, applications and integration, Claude Code, eval and debugging, model selection and optimization, prompt and context engineering, security and safety, and tools and MCPs. It turns the official objectives into a practical preparation plan with the exam and policy details and the decision rules the blueprint rewards — without reproducing or predicting live exam content.

## Professional study guide

[`professional_en.md`](./professional_en.md) · [read online](https://ravnhq.github.io/claude-certified-architect/guides/professional-en.html)

Reproduces all **38 official objectives** across the seven domains, with the exam and policy
details, the official prep path, a breakdown of the three official sample questions, and the
official source list. Each domain section covers the decision rules and failure modes the
blueprint rewards, not just the objective titles.

## Professional practice exam

Draws **63 questions per attempt from a 126-question bank**, weighted to the official domain
percentages:

| Domain | Weight | Drawn | Bank |
|---|---:|---:|---:|
| 1. Solution Design & Architecture | 17% | 11 | 22 |
| 2. Claude Models, Prompting & Context Engineering | 13% | 8 | 16 |
| 3. Integration | 19% | 12 | 24 |
| 4. Evaluation, Testing & Optimization | 16% | 10 | 20 |
| 5. Governance, Safety & Risk Management | 14% | 9 | 18 |
| 6. Stakeholder Communication & Lifecycle Management | 14% | 9 | 18 |
| 7. Developer Productivity & Operational Enablement | 7% | 4 | 8 |
| **Total** | **100%** | **63** | **126** |

Every item is written against one of the 38 official objectives and records which one. About 21%
are **multiple-response** items, scored all-or-nothing and stating how many responses to select.
Scoring uses the real **720** cut with a per-domain breakdown.

- [`professional_exam_en.html`](./professional_exam_en.html)

> **These are Ravn-authored practice items, not real exam content.** They rehearse the reasoning
> the blueprint rewards; they do not predict or reproduce the live item bank.

## How to use

1. Choose your track.
2. **Foundations** — pick a language, work the scenarios, then alternate practice exam and
   cheatsheet. Run the preflight checklist before you book.
3. **Professional** — read the official guide first, map your experience against the 38
   objectives, build one end-to-end reference system, then rehearse trade-offs under time
   pressure. Use exam mode for the timed run and study mode to read the rationale on every miss.

## Build and test

```bash
npm install --no-save marked@13 minisearch@7   # build dependencies

python3 utils/build_exam_html.py               # → exam_{en,es,pt}.html
python3 utils/build_exam_html.py en es         # specific languages
python3 utils/build_professional_exam.py       # → professional_exam_en.html
python3 utils/build_cheatsheet.py              # → cheatsheet_{en,es,pt}.html
node scripts/build-pages.mjs                   # → docs/ site

python3 utils/validate_professional_bank.py    # bank vs. official blueprint
node utils/test_exam_engine.mjs                # engine checks, both tracks
node utils/test_exam_render.mjs                # render checks
```

The validator fails on a bad answer key, an objective absent from the official guide, an
uncovered objective, or a domain whose bank is smaller than its draw.

The Foundations exam and the site regenerate on every deploy. The cheatsheet is hand-authored,
so its committed HTML is what ships — re-run its generator only when editing the content, and
keep its stats in sync with `data/domains.json` and `utils/exam_data.py` (`DOMAIN_NAMES`).

## Repository layout

```
.
├── guide_{en,es,pt}.{md,MD}          # source-of-truth Foundations guides (76 scenarios)
├── professional_en.md                 # Professional guide (7-domain blueprint)
├── CCAF_Mock_Exam_*.txt              # source for the 60-question mock bank
├── reference/                        # official exam guide PDFs, version-pinned
├── exam_{en,es,pt}.html              # Foundations practice exam, 60 of 136 (built)
├── professional_exam_en.html         # Professional practice exam, 63 of 126 (built)
├── cheatsheet_{en,es,pt}.html        # 12-principle cheatsheet (static, hand-authored)
├── data/
│   ├── domains.json                  # question id → CCAF domain (1–5)
│   ├── duplicates.json               # mock ids dropped as dupes of guide questions
│   ├── mock_{en,es,pt}.json          # mock bank + ES/PT translations
│   ├── professional_objectives.json  # official CCAR-P blueprint: 7 domains, 38 objectives
│   └── professional_questions.json   # Ravn-authored CCAR-P bank (126 items)
├── utils/
│   ├── extract_question.py           # guide_*.md → scenario questions JSON
│   ├── parse_mock_exam.py            # mock .txt → mock questions JSON
│   ├── exam_data.py                  # merges guide + mock into the unified schema
│   ├── build_exam_html.py            # shared quiz engine + Foundations build
│   ├── build_professional_exam.py    # → professional_exam_en.html
│   ├── professional_blueprint.py     # shared CCAR-P domains + per-attempt draw
│   ├── validate_professional_bank.py # bank vs. official blueprint
│   ├── build_cheatsheet.py           # → cheatsheet_*.html
│   ├── test_exam_engine.mjs          # engine regression checks (both tracks)
│   └── test_exam_render.mjs          # render regression checks
├── docs/                             # GitHub Pages site (static parts; CI generates the rest)
├── scripts/build-pages.mjs           # md → docs/ build, incl. the preflight checklist
└── .github/workflows/pages.yml       # builds PDFs + exams, deploys docs/ to Pages
```

The preflight checklist has no markdown source. Its content lives in `scripts/build-pages.mjs`
as `PREFLIGHT_ITEMS`, `PREFLIGHT_FACTS`, `PREFLIGHT_DOMAINS`, and `PREFLIGHT_RESOURCES`. Edit it
there; `docs/preflight/` is a generated artifact and is overwritten on every build.

## Contributing

- Translation fixes and clarifications are welcome. Keep the heading structure aligned across
  `guide_en.MD`, `guide_es.md`, and `guide_pt.md` so question extraction stays consistent.
- Run the validator and both test scripts before opening a PR.
- **Do not commit material from the Partner Academy courses.** That content is partner-gated.
  Practice items and guide prose here are Ravn-authored; keep it that way.
- PDFs regenerate automatically on merge to `main` as part of the Pages deploy.

## License

© Ravn. Originating study materials by Paul Larionov, used and adapted under the terms of the
upstream license.
