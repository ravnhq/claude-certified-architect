---
name: ask-ccaf
description: "CCAR-F (Claude Certified Architect – Foundations) exam guide v1.0 plus Anthropic prep-course mechanics. Use for any Foundations exam work: what the exam tests, domain weights, scoring, registration, retakes, policies; answering, writing, reviewing, or grading practice, mock, or sample questions and answer keys; the four preparation exercises; task statement ids (1.1–5.6), chapters, or in/out-of-scope checks; authoring study guides, cheatsheets, or mock exams for it. Also use when a design answer should follow the exam's model of agentic loops and stop_reason, coordinator-subagent orchestration, tool descriptions and error taxonomy, MCP, Claude Code configuration (CLAUDE.md, rules, skills, hooks, permission modes, plugins, headless), structured output and tool_choice, batch, context management, and escalation. Foundations only: for CCAR-P (Professional) it is background, not the blueprint."
---

<!-- argument-hint: [topic, task statement id (e.g. 1.4), or chapter number (e.g. ch05)] -->

# Claude Certified Architect – Foundations Exam Guide
**Publisher**: Anthropic (Certification Program) | **Version**: 1.0, effective July 2026 | **Exam code**: CCAR-F | **Pages**: 39 | **Chapters**: 10 | **Generated**: 2026-08-18

## How to use this skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `escalation`, `tool_choice`, `plan mode`, `batch processing`; I find and read the relevant chapter.
- **With a task statement id** — ask for `1.4` or `5.6`; the Topic Index routes to the chapter.
- **With a chapter** — ask for `ch05`; I load that file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about something not covered below, I read the relevant chapter file before answering.

---

## Core frameworks and decision rules

### The exam in numbers
60 items, 120 minutes (2 min/item), cut score **720** on a 100–1,000 scale, $125, valid 12 months. **4 of 6 scenarios** appear at random. Weights: **Domain 1 Agentic Architecture 27%**, Domain 3 Claude Code 20%, Domain 4 Prompt Engineering 20%, Domain 2 Tool Design & MCP 18%, Domain 5 Context & Reliability 15%. Criterion-referenced: per-domain percentages are diagnostic; only the total scaled score decides pass/fail.

### The one judgment the exam keeps testing
**Deterministic where compliance must be guaranteed; adaptive where judgment must generalize.**
- Rule must never fail (financial, irreversible, required ordering) → **hook or prerequisite gate**. Prompt instructions carry a non-zero failure rate.
- Model must generalize to novel cases → **explicit categorical criteria + 2–4 few-shot examples**. Never "be conservative" or confidence filtering.

### Agentic loop
Send request → inspect **`stop_reason`** → `"tool_use"`: execute tools, append results to history, iterate → `"end_turn"`: finish. Never terminate by parsing natural language, by assistant text presence, or by an arbitrary iteration cap as the primary mechanism.

### Coordinator-subagent orchestration
Hub-and-spoke: route **all** subagent communication through the coordinator. Subagents have **isolated context** — pass complete prior findings explicitly in the prompt. `allowedTools` must include `"Task"`. Parallelism = **multiple Task calls in one response**. The coordinator's decomposition breadth is the ceiling on coverage — correct subagents working wrong subtasks still fail. Specify goals and quality criteria, not step-by-step procedures.

### Tool design
**Tool descriptions are the primary mechanism LLMs use for tool selection.** Fix the description before adding few-shot examples, routing layers, or classifiers. Include input formats, example queries, edge cases, and boundaries ("use this rather than X when…"). Give each agent **4–5 role-relevant tools**, not 18. Add a scoped cross-role tool only for a measured high-frequency case (least privilege).

### Error handling
Return `isError` plus `errorCategory` (transient / validation / business / permission), `isRetryable`, and a human-readable message. Recover transient failures **locally in the subagent**; propagate only the unresolvable, with what was attempted and partial results. Distinguish **access failure** from a **valid empty result**. Never return a generic status, never mark failure as empty success, never kill the workflow on one failure — proceed with partial results and annotate coverage gaps.

### Claude Code configuration = scope selection
"Shared with the team" → project path under version control. "Personal" → `~/.claude/...`. "Always loaded, universal" → CLAUDE.md. "On-demand, task-specific" → a skill. **"Automatic, for files scattered across directories" → `.claude/rules/` with YAML `paths:` globs** — the only mechanism that does this; directory-bound CLAUDE.md and invocation-dependent skills cannot. SKILL.md frontmatter: `context: fork` (isolate verbose output), `allowed-tools` (restrict), `argument-hint` (prompt for parameters). CI: `-p` / `--print`, plus `--output-format json` with `--json-schema`. Rule placement (prep courses): always-on convention → CLAUDE.md; task procedure → skill; must-never-skip rule → **hook** (PreToolUse blocks, exit 2 = block, exit 1 does not); unattended runs → auto mode (intent classifier) + a Stop hook running tests; CI → dontAsk; bypass only in a disposable container.

### Plan mode vs direct execution
Plan mode for large-scale, architectural, multi-approach, multi-file work — and when the requirements *already state* the complexity. Direct execution for a single-file fix with clear scope. Combine: plan to investigate, direct to implement. Use the **Explore subagent** to keep verbose discovery out of the main context.

### Structured output
`tool_use` + JSON schema is the reliable mechanism — it eliminates **syntax** errors, not semantic ones. `tool_choice`: `"auto"` may return text, `"any"` guarantees some tool, forced selection guarantees order. Make fields **optional/nullable when the source may lack them** to prevent fabrication; add `"unclear"` enums and `"other"` + detail strings. Retry by resending the document, the failed extraction, **and** the specific validation errors — retry cannot recover information absent from the source.

### Batch vs synchronous
Message Batches API: **50% savings, up to 24 hours, no latency SLA, no multi-turn tool calling**, `custom_id` correlation. Batch for overnight and weekly work; synchronous for anything blocking. Resubmit only failed `custom_id`s.

### Review architecture
An **independent instance** reviews better than the session that generated the code. Split large multi-file reviews into per-file passes plus a cross-file integration pass — the failure mode is **attention dilution**, which a larger context window does not fix, and consensus voting across passes suppresses real bugs.

### Context and reliability
Extract transactional facts into a persistent **case-facts block outside summarized history**; trim verbose tool output to relevant fields before it accumulates; put key findings **first** with explicit section headers against **lost-in-the-middle**; use scratchpad files, phase summaries, and `/compact` against context degradation; export state manifests for crash recovery. Preserve **claim-source mappings** with publication dates; annotate conflicting credible sources instead of picking one; separate well-established from contested findings.

### Escalation
Escalate on: **explicit human request** (immediately, no investigation first), **policy gap or ambiguity**, **inability to progress**. Ask for more identifiers when tools return multiple matches. Complexity alone, negative sentiment, and self-reported confidence are **not** valid triggers.

---

## Chapter index

| # | Title | Key content |
|---|-------|----------------|
| [ch01](chapters/ch01-exam-overview.md) | Exam overview — credential, blueprint, scenarios | details table, domain weights, the 6 scenarios |
| [ch02](chapters/ch02-domain1-agentic-architecture.md) | Domain 1 — Agentic Architecture & Orchestration (27%) | task statements 1.1–1.7, agentic loop, coordinator-subagent, hooks, decomposition, sessions |
| [ch03](chapters/ch03-domain2-tool-design-mcp.md) | Domain 2 — Tool Design & MCP Integration (18%) | 2.1–2.5, descriptions, error taxonomy, `tool_choice`, MCP scoping, built-in tools |
| [ch04](chapters/ch04-domain3-claude-code-config.md) | Domain 3 — Claude Code Configuration & Workflows (20%) | 3.1–3.6, CLAUDE.md hierarchy, commands, skills, path rules, plan mode, CI |
| [ch05](chapters/ch05-domain4-prompt-engineering.md) | Domain 4 — Prompt Engineering & Structured Output (20%) | 4.1–4.6, explicit criteria, few-shot, JSON schemas, retry, batch, multi-pass review |
| [ch06](chapters/ch06-domain5-context-reliability.md) | Domain 5 — Context Management & Reliability (15%) | 5.1–5.6, context preservation, escalation, error propagation, confidence, provenance |
| [ch07](chapters/ch07-preparation-and-exercises.md) | How to prepare, and the four exercises | 7 study directives, Exercises 1–4 step by step |
| [ch08](chapters/ch08-sample-questions-and-scoring.md) | The 12 sample questions, and scoring | every question, key, distractor reasoning, scaled scoring |
| [ch09](chapters/ch09-logistics-and-policies.md) | Registration, policies, exam day, recertification | scheduling, ID, retake waits, NDA, renewal |
| [ch10](chapters/ch10-appendix-scope-boundaries.md) | Appendix — technologies, in-scope, out-of-scope | named technologies, 18 in-scope topics, 16 out-of-scope |

## Topic index

- **Agentic loop / `stop_reason`** → ch02, ch10
- **`allowedTools` / Task tool** → ch02
- **Anti-patterns (per domain)** → ch02, ch03, ch04, ch05, ch06
- **Batch processing / Message Batches API** → ch05, ch08, ch10
- **Blueprint weights** → ch01
- **Built-in tools (Read, Write, Edit, Bash, Grep, Glob)** → ch03
- **CI/CD integration (`-p`, `--json-schema`)** → ch04, ch08
- **CLAUDE.md hierarchy / `@import`** → ch04
- **`.claude/rules/` path globs** → ch04, ch08
- **Confidence calibration / stratified sampling** → ch06, ch05
- **Context degradation / scratchpad / `/compact`** → ch06
- **Coordinator-subagent / hub-and-spoke** → ch02
- **Error taxonomy / structured errors** → ch03, ch06
- **Escalation criteria** → ch06, ch08
- **Exam details, fee, cut score** → ch01, ch08
- **Exercises (preparation)** → ch07
- **Few-shot prompting** → ch05
- **`fork_session` / `--resume`** → ch02
- **Hooks (PostToolUse, interception)** → ch02
- **JSON schema design / nullable fields** → ch05
- **Lost in the middle / summarization loss** → ch06
- **MCP servers (`.mcp.json`, `~/.claude.json`)** → ch03
- **MCP resources** → ch03
- **Multi-pass / independent review** → ch05, ch08
- **Out-of-scope topics** → ch10
- **Plan mode vs direct execution** → ch04, ch08
- **Policies, retakes, recertification** → ch09
- **Programmatic enforcement / prerequisite gates** → ch02, ch08
- **Prompt chaining / task decomposition** → ch02, ch05
- **Provenance / claim-source mappings** → ch06
- **Sample questions (1–12)** → ch08
- **Scenarios (the 6)** → ch01
- **Scoring, scaled score, standard setting** → ch08
- **Skills frontmatter (`context: fork`, `allowed-tools`, `argument-hint`)** → ch04
- **Slash commands (project vs user)** → ch04, ch08
- **Task statements (1.1–5.6)** → ch02–ch06
- **`tool_choice`** → ch03, ch05
- **Tool descriptions / differentiation** → ch03, ch08
- **Tool distribution / least privilege** → ch03
- **Validation-retry loops** → ch05

Prep-course supplements (each chapter's closing section, plus patterns/glossary/cheatsheet):

- **Permission modes (default/acceptEdits/plan/auto/dontAsk/bypass)** → ch04
- **Hook events, exit codes, `updatedInput`** → ch04, ch02
- **CLAUDE.md discipline (dilution, imports, phrasing, memory stack)** → ch04
- **Plugins / marketplaces** → ch04
- **Routines / headless / GitHub Action / managed code review** → ch04
- **Verifying unsupervised runs / Stop-hook test gate** → ch04
- **Steering: /compact with instructions, rewind, worktrees** → ch04, ch06
- **MCP primitives (tool/resource/prompt control model), transports, Inspector** → ch03
- **Tool-result wire mechanics (`tool_use_id`, `is_error`, block handling)** → ch03, ch02
- **Workflow patterns (chaining, routing, parallelization, evaluator-optimizer)** → ch02
- **Prompt construction order / diagnose-before-reprompting** → ch05
- **Eval workflow, graders, LLM-as-judge calibration** → ch05
- **Retriable vs terminal / prompt-injection action boundary** → ch06

## Supporting files

- [glossary.md](glossary.md) — every named term, flag, and command with a definition
- [patterns.md](patterns.md) — 24 guide techniques plus 5 prep-course patterns, with when-to-use, how, and trade-offs
- [cheatsheet.md](cheatsheet.md) — answer-selection rules, thresholds, tells, and the scope boundary

---

## Scope and limits

This skill covers the CCAR-F Exam Guide v1.0 (July 2026) — the authoritative source for exam answers — enriched with clearly marked "prep-course supplement" sections synthesized from Anthropic's official CCAR-F prep courses (Claude Code in Action, Claude with the Anthropic API, Introduction to Model Context Protocol) and, secondarily, the Developer Foundations modules. Supplements add mechanics the guide only gestures at; where a supplement and the guide differ, the guide's model is the tested one. From the guide itself, it covers: the blueprint, task statements, the 12 published sample questions, the 4 preparation exercises, program policies, and the scope lists. It is a synthesized study reference, not exam content — the guide states that actual exam items are confidential, and it is itself "subject to change without notice", so verify the current version before you sit.

For hands-on practice, combine it with the real tools it describes (Agent SDK, MCP servers, Claude Code configuration in a live project); the guide prescribes building, not reading. Product behavior beyond this guide — current Claude Code flags, SDK APIs, model names — belongs to the official documentation, which moves faster than a certification blueprint.

Extraction note: the source PDF split ligatures (`con fi guration`) and repeated a running header; both were normalized during generation. No images were dropped.
