# Chapter 1: Exam Overview — Credential, Blueprint, and Scenarios

*Covers guide sections 1–5.*

## Core Idea
The exam measures **practical judgment about tradeoffs** in production Claude systems, not recall of API surface. Every item is framed inside one of 6 fixed production scenarios, and domain weights tell you exactly where to spend study time.

## Reference Tables

### Exam details at a glance
| Attribute | Value |
|---|---|
| Credential | Claude Certified Architect – Foundations |
| Exam code | CCAR-F |
| Items | 60 |
| Item format | Multiple-choice and multiple-response; each item states how many responses to select |
| Structure | 4 scenarios drawn from a bank of 6 |
| Time limit | 120 minutes |
| Delivery | Proctored — online proctored and/or test center, per program policy |
| Passing score | Scaled 720 on a 100–1,000 scale |
| Fee | $125 USD |
| Validity | 12 months from award date |
| Result reporting | Pass/fail with scaled score, plus percent-correct by domain |

Derived pacing: 60 items / 120 minutes = **2 minutes per item**.

### Blueprint weights
| Domain | Content domain | Weight | Task statements |
|---|---|---|---|
| 1 | Agentic Architecture & Orchestration | 27% | 7 (1.1–1.7) |
| 2 | Tool Design & MCP Integration | 18% | 5 (2.1–2.5) |
| 3 | Claude Code Configuration & Workflows | 20% | 6 (3.1–3.6) |
| 4 | Prompt Engineering & Structured Output | 20% | 6 (4.1–4.6) |
| 5 | Context Management & Reliability | 15% | 6 (5.1–5.6) |

Weights are set by job task analysis and indicate the approximate proportion of scored items per domain. At 60 items: Domain 1 ≈ 16 items, Domain 3 ≈ 12, Domain 4 ≈ 12, Domain 2 ≈ 11, Domain 5 ≈ 9.

### The 6 scenarios (4 appear, chosen at random)
| # | Scenario | Primary domains |
|---|---|---|
| 1 | **Customer Support Resolution Agent** — Agent SDK agent for returns, billing disputes, account issues; MCP tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`; target 80%+ first-contact resolution | 1, 2, 5 |
| 2 | **Code Generation with Claude Code** — team use for generation, refactoring, debugging, docs; custom slash commands, CLAUDE.md, plan mode vs direct execution | 3, 5 |
| 3 | **Multi-Agent Research System** — coordinator delegating to web search, document analysis, synthesis, and report subagents; produces cited reports | 1, 2, 5 |
| 4 | **Developer Productivity with Claude** — codebase exploration, legacy systems, boilerplate; built-in tools (Read, Write, Bash, Grep, Glob) plus MCP servers | 2, 3, 1 |
| 5 | **Claude Code for Continuous Integration** — automated code review, test generation, PR feedback; prompts that give actionable feedback and minimize false positives | 3, 4 |
| 6 | **Structured Data Extraction** — extraction from unstructured documents, JSON schema validation, high accuracy, graceful edge cases | 4, 5 |

## Key Concepts
- **Task statement** — a tested objective, split into "Knowledge of" and "Skills in" bullets; exam items are written directly against these.
- **Job task analysis** — the study that set domain weights from real practitioner work.
- **Criterion-referenced** — you are measured against a fixed standard, not against other candidates (see ch08).
- **Scenario framing** — a production context that frames a set of items; the same technical fact can be tested differently depending on which scenario wraps it.
- **Intended audience** — a solution architect with **6+ months** hands-on experience across Claude API, Agent SDK, Claude Code, and MCP.

## Frameworks & Patterns Named
- **Four core technologies tested**: Claude Code, Claude Agent SDK, Claude API, Model Context Protocol (MCP). Anything outside these four is likely out of scope (ch10).
- **Scenario-to-domain mapping** (table above): use it to predict which domain a question is testing from its opening context. Support agent → escalation and enforcement; research system → orchestration and provenance; CI → prompt precision and non-interactive Claude Code.

## Anti-patterns
- **Studying the four technologies evenly**: Domain 1 is 27% of the exam — nearly double Domain 5's 15%.
- **Treating the exam as API recall**: items reward the *proportionate* fix (see the "first step" reasoning in ch08), not the most sophisticated one.
- **Ignoring the scenario preamble**: it names the tools and the target metric that make one answer correct.

## Worked Example
Scenario 1 states its own success criterion: "Your target is 80%+ first-contact resolution while knowing when to escalate." Sample Question 3 (ch08) then reports an agent at **55%** first-contact resolution that escalates straightforward cases while attempting complex policy exceptions autonomously. The scenario's stated metric *is* the grading rubric for the item: the correct answer (explicit escalation criteria with few-shot examples) is the one that moves first-contact resolution by fixing decision boundaries, not the one that adds infrastructure (a trained classifier) or measures the wrong signal (sentiment). Read every scenario preamble for its stated target — it tells you what "most effective" means for that item.

## Key Takeaways
1. 60 items, 120 minutes, cut score 720 of 1,000 — budget 2 minutes per item.
2. Domain 1 (27%) is the single heaviest domain; Domains 3 and 4 tie at 20%.
3. Only 4 of the 6 scenarios appear, chosen at random — prepare all 6.
4. Items are written against task statements, so the task statement list in ch02–ch06 is the real syllabus.
5. Section-level percentages appear on your score report but do not determine pass/fail — only the total scaled score does.
6. The candidate profile assumes hands-on production experience; the exam tests tradeoff judgment, not definitions.

## Connects To
- **ch02–ch06**: the detailed objectives behind each blueprint weight.
- **ch08**: sample questions, and how scoring converts them into a scaled score.
- **ch10**: in-scope and out-of-scope lists — the boundary of everything above.
