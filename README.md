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
| **Architect – Professional** | CCAR-P | Architects responsible for production AI architecture, evaluation, governance, and lifecycle decisions | English study guide and a 63-question practice exam |
| **Developer – Foundations** | CCDV-F | Engineers building and shipping production applications, agents, and workflows on the Claude platform | English study guide and a 53-question practice exam |

The three exams use different blueprints. Foundations has five domains, Developer eight,
Professional seven. Foundations material does not represent Professional coverage, and the
reverse is equally true; the same holds between every pair of tracks.

> **Professional and Developer material is English only.** Anthropic delivers those exams and
> their prep content in English and prohibits browser translation during proctored testing, so
> ES/PT tracks would train against wording the exams never use. The Foundations material stays
> tri-language.

## Exam facts

Exam-structure figures below come from the official exam guides, which are the authoritative
source and which Anthropic marks subject to change. Delivery and language rules (Pearson VUE,
English only) come from the official [certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications),
not the guides.

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

**No course is required to sit any of the exams.** The credential is awarded on exam performance
alone. Anthropic publishes free prep courses, and they help, but they are not a gate.

**On the fee.** $125 and $175 are the list prices in the exam guides. The amount at checkout
reflects any discount for your partner tier, so what you pay may be lower — per the FAQ,
Registered-tier partners pay full price, Select/Preferred/Global Premier partners get 50% off,
and through August 31, 2026 Global Premier partners pay nothing. Foundations cost $99 until the
price rose to $125 on June 30, 2026; registrations before that date paid the lower price.

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
- The FAQ also lists a fourth certification, **Claude Certified Associate – Foundations** ($99).
  This repo does not cover it; it does not count toward Partner Network eligibility.
- Register through the [Anthropic Partner Academy](https://anthropic-partners.skilljar.com/page/partner-certifications),
  then schedule with Pearson VUE using the credentials they email you.
- Official guides, all marked subject to change:
  [Foundations](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) ·
  [Professional](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf) ·
  [Developer](https://anthropic-partners.skilljar.com/claude-certified-developer-foundations-certification)
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
| English | [`ccaf/guide_en.md`](./ccaf/guide_en.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_en.pdf) |
| Spanish | [`ccaf/guide_es.md`](./ccaf/guide_es.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_es.pdf) |
| Portuguese | [`ccaf/guide_pt.md`](./ccaf/guide_pt.md) | [Download](https://ravnhq.github.io/claude-certified-architect/pdf/guide_pt.pdf) |

PDFs are generated fresh on every deploy from the current markdown sources.

## Foundations practice exam

A self-paced HTML quiz that runs entirely in your browser. Each attempt draws **12 random
questions per domain — 60 in total**. The English bank holds 607 items: the 76 scenario
questions from the guide, 60 domain-style questions from the mock bank, and 471 imported
practice items tagged to the official task statements. Spanish and Portuguese draw from the
136 hand-authored items. The score is scaled to 1,000 with a passing cut of **720**, mirroring
the real scale.

Features: a fresh 60-question draw each attempt, questions randomized within each domain, a
**study** mode that reveals answers as you go with a rationale for every option, an **exam** mode
that reveals at the end, per-domain breakdown against the pass threshold, and progress saved in
`localStorage` so a refresh keeps your place. **Restart** draws a new set. A domain selector
drills a single domain's whole bank instead, scored raw with no pass/fail verdict.

- [`ccaf/dist/exam_en.html`](./ccaf/dist/exam_en.html) · [`ccaf/dist/exam_es.html`](./ccaf/dist/exam_es.html) · [`ccaf/dist/exam_pt.html`](./ccaf/dist/exam_pt.html)

## Foundations cheatsheet

A one-page reference distilling the exam into **12 recurring principles** — each with the correct
approach and the trap to avoid — **5 questions to ask when two answers look equally good**, and a
breakdown of the 136 hand-authored questions by domain, with weights and answer-letter distribution.

- [`ccaf/dist/cheatsheet_en.html`](./ccaf/dist/cheatsheet_en.html) · [`ccaf/dist/cheatsheet_es.html`](./ccaf/dist/cheatsheet_es.html) · [`ccaf/dist/cheatsheet_pt.html`](./ccaf/dist/cheatsheet_pt.html)

## Developer study guide

[`ccdf/guide_en.md`](./ccdf/guide_en.md) · [read online](https://ravnhq.github.io/claude-certified-architect/guides/developer-en.html)

Covers the **eight-domain Developer – Foundations blueprint (CCDV-F)**: agents and workflows, applications and integration, Claude Code, eval and debugging, model selection and optimization, prompt and context engineering, security and safety, and tools and MCPs. It turns the official objectives into a practical preparation plan with the exam and policy details and the decision rules the blueprint rewards — without reproducing or predicting live exam content.

## Developer practice exam

Draws **53 questions per attempt**, weighted to the official domain percentages:

| Domain | Weight | Drawn |
|---|---:|---:|
| 1. Agents and Workflows | 14.7% | 8 |
| 2. Applications and Integration | 33.1% | 17 |
| 3. Claude Code | 3.1% | 2 |
| 4. Eval, Testing, and Debugging | 2.6% | 1 |
| 5. Model Selection and Optimization | 16.8% | 9 |
| 6. Prompt and Context Engineering | 11.0% | 6 |
| 7. Security and Safety | 8.1% | 4 |
| 8. Tools and MCPs | 10.6% | 6 |
| **Total** | **100%** | **53** |

The bank behind that draw is several times the size of one
attempt, so repeat attempts overlap little. Every item is tagged to one of the 25 official
objectives and records which one. About 20% are **multiple-response** items, scored
all-or-nothing and stating how many responses to select. Scoring uses the real **720** cut with
a per-domain breakdown, on the same engine as the other two tracks. A domain selector drills a
single domain's whole bank instead, scored raw with no pass/fail verdict.

- [`ccdf/dist/exam_en.html`](./ccdf/dist/exam_en.html)

> **Not real exam content.** These items rehearse the reasoning the blueprint rewards; they do
> not predict or reproduce the live item bank.

## Professional study guide

[`ccap/guide_en.md`](./ccap/guide_en.md) · [read online](https://ravnhq.github.io/claude-certified-architect/guides/professional-en.html)

Reproduces all **38 official objectives** across the seven domains, with the exam and policy
details, the official prep path, a breakdown of the three official sample questions, and the
official source list. Each domain section covers the decision rules and failure modes the
blueprint rewards, not just the objective titles.

## Professional practice exam

Draws **63 questions per attempt**, weighted to the official domain percentages:

| Domain | Weight | Drawn |
|---|---:|---:|
| 1. Solution Design & Architecture | 17% | 11 |
| 2. Claude Models, Prompting & Context Engineering | 13% | 8 |
| 3. Integration | 19% | 12 |
| 4. Evaluation, Testing & Optimization | 16% | 10 |
| 5. Governance, Safety & Risk Management | 14% | 9 |
| 6. Stakeholder Communication & Lifecycle Management | 14% | 9 |
| 7. Developer Productivity & Operational Enablement | 7% | 4 |
| **Total** | **100%** | **63** |

The bank behind that draw is several times the size of one
attempt, so repeat attempts overlap little. Every item is tagged to one of the 38 official
objectives and records which one. About a quarter are **multiple-response** items, scored
all-or-nothing and stating how many responses to select. Scoring uses the real **720** cut with
a per-domain breakdown. A domain selector drills a single domain's whole bank instead, scored
raw with no pass/fail verdict.

- [`ccap/dist/exam_en.html`](./ccap/dist/exam_en.html)

> **Not real exam content.** These items rehearse the reasoning the blueprint rewards; they do
> not predict or reproduce the live item bank.

## How to use

1. Choose your track.
2. **Foundations** — pick a language, work the scenarios, then alternate practice exam and
   cheatsheet. Run the preflight checklist before you book.
3. **Developer** — read the guide, map your experience against the 25 objectives, then drill the
   practice exam. The domain weighting is deliberately uneven (Applications and Integration is a
   third of the exam), so check the per-domain breakdown before booking.
4. **Professional** — read the official guide first, map your experience against the 38
   objectives, build one end-to-end reference system, then rehearse trade-offs under time
   pressure. Use exam mode for the timed run and study mode to read the rationale on every miss.

### Review a score report

Upload a score-report PDF to get a personalized study guide and practice exam automatically.
The report stays on your device. If the exam cannot be identified, choose it; if any scores
need correction, the page asks only for those corrections. Report details remain available
below the guide. Each topic card expands into an objective-specific explanation, example,
and practical guidance. Personalization currently supports Architect Foundations (CCAR-F).

Objective scores and personalized exam progress are saved in this browser on this device,
so the guide and attempt can be resumed after closing the tab. The PDF and candidate details
are not saved. Use **Report details → Delete saved study data** to clear the personalized
guide and attempt. Clearing browser data also removes them; they do not sync across devices.

The practice exam draws from the existing bank, favors weaker topics, and retains coverage
across all five domains. Results show practice accuracy and explanations, not an official
score prediction.

## Design

[DESIGN.md](./DESIGN.md) documents the current Ravn identity, extracted with Firecrawl
and checked against the live site. Shared embedded fonts live in `docs/assets/fonts.css`;
edit generator styles and regenerate every exam, bank, and cheatsheet after design changes.

## Build and test

```bash
npm install --no-save marked@13.0.3 minisearch@7.2.0 pdfjs-dist@4.10.38 md-to-pdf   # pinned build dependencies

python3 utils/build_exam_html.py               # → ccaf/dist/exam_{en,es,pt}.html
python3 utils/build_exam_html.py en es         # specific languages
python3 utils/import_certsafari.py             # corpus + tags → ccap,ccdf data/questions.json
python3 utils/build_professional_exam.py       # → ccap/dist/exam_en.html
python3 utils/build_developer_exam.py          # → ccdf/dist/exam_en.html
python3 utils/build_cheatsheet.py              # → ccaf/dist/cheatsheet_{en,es,pt}.html
node scripts/build-pages.mjs                   # → docs/ site

python3 utils/validate_professional_bank.py    # CCAR-P bank vs. official blueprint
python3 utils/validate_developer_bank.py       # CCDV-F bank vs. official blueprint
node utils/test_exam_engine.mjs                # engine checks (Foundations + Professional pages)
node utils/test_exam_render.mjs                # render checks
```

Each validator fails on a bad answer key, an objective absent from the official guide, a stem
that states a different number of answers than its key, or a domain whose bank is smaller than
its draw. An objective no item covers is reported as a warning, since the CCAR-P and CCDV-F
banks are imported rather than commissioned.

The Foundations and Professional exams and the site regenerate on every deploy. The Developer
exam and the cheatsheet ship their committed HTML — re-run their generators only when editing
their content, and keep the cheatsheet stats in sync with `ccaf/data/domains.json` and
`utils/exam_data.py` (`DOMAIN_NAMES`).

## Repository layout

Each exam owns a top-level directory with the same internal shape:

| | CCAF (CCAR-F) | CCAP (CCAR-P) | CCDF (CCDV-F) |
|---|---|---|---|
| Study guide | `ccaf/guide_{en,es,pt}.md` | `ccap/guide_en.md` | `ccdf/guide_en.md` |
| Question data | `ccaf/data/` | `ccap/data/` | `ccdf/data/` |
| Source material | `ccaf/sources/` | `.corpus/certsafari/` | `ccdf/sources/`, `.corpus/certsafari/` |
| Exercises | `ccaf/exercises/` | — | — |
| Generated HTML | `ccaf/dist/` | `ccap/dist/` | `ccdf/dist/` |

`data/` holds the question banks and blueprint transcriptions; `sources/` holds third-party
inputs like the official exam-guide PDFs; `dist/` holds generated exam and cheatsheet HTML —
edit sources, not `dist/`. Shared tooling stays in `utils/` (importer, builders, validators,
engine tests) and `scripts/` (site build and the CertSafari collector).

The Foundations bank in `ccaf/data/questions.json` is Ravn-authored and edited by hand. The
CCAR-P and CCDV-F banks are not: `ccap/data/questions.json` and `ccdf/data/questions.json` are
generated by `utils/import_certsafari.py` from the CertSafari corpus under `.corpus/certsafari/`,
so an edit made directly to either file is lost on the next import. The same script writes
`ccaf/data/imported_en.json`, the imported half of the English Foundations bank, placed by
`ccaf/data/blueprint.json` and grouped in the bank browser through `ccaf/data/objectives.json`. Each item's domain and
objective come from the `Subdomain X.Y` label CertSafari itself puts on the question, read out of
the captured page snapshot and checked against `objectives.json` before it is trusted.

A few files are not what they look like: `ccaf/sources/mock-exam.txt` is the source for the
60-question mock bank, and the preflight checklist has no markdown source — its content
lives in `scripts/build-pages.mjs` (`PREFLIGHT_ITEMS`, `PREFLIGHT_FACTS`,
`PREFLIGHT_DOMAINS`, `PREFLIGHT_RESOURCES`) and `docs/preflight/` is overwritten on every
build.

## Contributing

- Translation fixes and clarifications are welcome. Keep the heading structure aligned across
  `ccaf/guide_en.md`, `ccaf/guide_es.md`, and `ccaf/guide_pt.md` so question extraction stays consistent.
- Run the validators and both test scripts before opening a PR.
- **Do not commit material from the Partner Academy courses.** That content is partner-gated.
  Guide prose and the Foundations practice items are Ravn-authored; keep it that way. The
  CertSafari archive under `.corpus/certsafari/` is the tracked third-party exception — see
  `scripts/certsafari-collection.md` — and it is the source of the CCAR-P and CCDV-F banks,
  which are regenerated from it by `utils/import_certsafari.py` rather than edited by hand.
- PDFs regenerate automatically on merge to `main` as part of the Pages deploy.

## License

© Ravn. Originating study materials by Paul Larionov, used and adapted under the terms of the
upstream license.
