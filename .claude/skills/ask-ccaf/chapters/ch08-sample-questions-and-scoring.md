# Chapter 8: The 12 Sample Questions, and How the Exam Is Scored

*Covers guide sections 9–10. The answer explanations are the only place this guide reveals its own judgment criteria — study the distractor reasoning, not just the keys.*

## Core Idea
Every explanation applies the same three tests: **does it fix the root cause, is it proportionate to the problem, and does it exist?** Distractors fail by blaming a downstream component, over-engineering ahead of cheaper fixes, solving a different problem, or referencing features that do not exist.

## The five recurring distractor types
| Type | Signature | Examples |
|---|---|---|
| **Probabilistic where deterministic is required** | prompt or few-shot for a rule that must never fail | Q1 B, Q1 C |
| **Over-engineered ahead of the cheap fix** | classifier, routing layer, extra infrastructure before prompt/description work | Q2 A, Q2 C, Q3 B, Q3 C |
| **Blames a working component** | fixes downstream when the log points upstream | Q7 A, Q7 C, Q7 D |
| **Solves a different problem** | plausible mechanism, wrong root cause | Q1 D, Q3 D, Q6 B, Q12 C |
| **Does not exist** | invented flags, env vars, config files | Q10 B, Q10 D, Q4 D |

## Question-by-question

### Scenario: Customer Support Resolution Agent
**Q1 — Agent skips `get_customer`, calls `lookup_order` from a stated name; misidentified accounts and incorrect refunds (12% of cases).** → **A. Programmatic prerequisite blocking `lookup_order`/`process_refund` until `get_customer` returns a verified customer ID.** Required tool sequences for critical business logic need deterministic guarantees. B (system prompt) and C (few-shot) rely on probabilistic compliance, insufficient when errors have financial consequences. D (routing classifier) addresses tool *availability*, not *ordering* — not the actual problem.

**Q2 — Agent calls `get_customer` for order queries; both tools have minimal descriptions and similar identifier formats. Most effective *first step*?** → **B. Expand each description with input formats, example queries, edge cases, and boundaries.** Descriptions are the primary selection mechanism; this is the low-effort, high-leverage root-cause fix. A (5–8 few-shot examples) adds token overhead without fixing the cause. C (keyword routing layer) is over-engineered and bypasses the LLM's language understanding. D (consolidate into `lookup_entity`) is a *valid architectural choice* but more effort than a "first step" warrants.

**Q3 — 55% first-contact resolution vs 80% target; escalates straightforward cases, attempts complex policy exceptions.** → **A. Explicit escalation criteria in the system prompt with few-shot examples of escalate vs resolve.** Root cause is unclear decision boundaries; this is the proportionate first response. B fails because LLM self-reported confidence is poorly calibrated — the agent is already wrongly confident on hard cases. C (trained classifier) is over-engineered before prompt optimization. D (sentiment analysis) solves a different problem; sentiment does not correlate with complexity.

### Scenario: Code Generation with Claude Code
**Q4 — A `/review` command available to every developer on clone or pull. Where?** → **A. `.claude/commands/` in the project repository.** Version-controlled and automatically available to all developers. B (`~/.claude/commands/`) is personal, not shared via VCS. C (CLAUDE.md) holds instructions and context, not command definitions. D (`.claude/config.json` with a commands array) **does not exist**.

**Q5 — Monolith to microservices, dozens of files, service-boundary and dependency decisions.** → **A. Enter plan mode to explore, understand dependencies, and design before changing anything.** Plan mode targets large-scale changes, multiple valid approaches, and architectural decisions. B risks costly rework when dependencies surface late. C assumes the right structure is already known. D ignores that the complexity is **already stated in the requirements**, not something that might emerge.

**Q6 — Area-specific conventions; test files beside their sources (`Button.test.tsx` next to `Button.tsx`); all tests must follow the same conventions regardless of location, applied automatically.** → **A. `.claude/rules/` files with YAML frontmatter glob patterns.** Globs like `**/*.test.tsx` apply by path regardless of directory — essential for scattered test files. B (root CLAUDE.md with headers) relies on inference rather than explicit matching. C (skills per code type) needs invocation or Claude choosing to load them, contradicting "automatic". D (CLAUDE.md per subdirectory) cannot handle files spread across many directories, since CLAUDE.md is directory-bound.

### Scenario: Multi-Agent Research System
**Q7 — Every subagent succeeds, but reports cover only visual arts; coordinator logs show decomposition into "AI in digital art creation", "AI in graphic design", "AI in photography".** → **B. The coordinator's task decomposition is too narrow.** The logs name the cause directly: "creative industries" became three visual-arts subtasks, omitting music, writing, and film. The subagents executed their assignments correctly — the problem is **what they were assigned**. A, C, and D each blame a downstream agent working correctly within its assigned scope.

**Q8 — Web search subagent times out; how should the failure reach the coordinator?** → **A. Structured error context: failure type, attempted query, partial results, potential alternatives.** This lets the coordinator retry with a modified query, try an alternative, or proceed with partial results. B's generic "search unavailable" hides context. C (empty result marked successful) suppresses the error and risks incomplete research. D terminates the whole workflow unnecessarily.

**Q9 — Synthesis agent needs verification mid-pass; round-tripping through the coordinator adds 40% latency; 85% are simple fact-checks, 15% need deeper investigation.** → **A. A scoped `verify_fact` tool for the synthesis agent; complex verifications keep delegating through the coordinator.** Applies **least privilege** — the 85% common case handled locally, the coordination pattern preserved for the rest. B (batching verifications) creates blocking dependencies, since later synthesis may depend on earlier verified facts. C (all web search tools) over-provisions and violates separation of concerns. D (speculative caching) cannot reliably predict what synthesis will need.

### Scenario: Claude Code for Continuous Integration
**Q10 — `claude "Analyze this pull request..."` hangs waiting for interactive input.** → **A. Add `-p`: `claude -p "..."`.** `-p` / `--print` is the documented non-interactive mode: processes the prompt, writes to stdout, exits. B (`CLAUDE_HEADLESS=true`) and D (`--batch`) **do not exist**; C (stdin from `/dev/null`) is a Unix workaround that does not properly address the command syntax.

**Q11 — Move both a blocking pre-merge check and an overnight technical debt report to the Message Batches API for 50% savings?** → **A. Batch for the technical debt reports only; keep real-time for pre-merge checks.** Batch offers 50% savings but up to 24 hours with no latency SLA — unsuitable for a blocking check, ideal for overnight jobs. B relies on "often faster", unacceptable for blocking work. C reflects a misconception — `custom_id` correlates batch results. D adds unnecessary complexity when matching each API to its use case is simpler.

**Q12 — 14-file PR; single-pass review gives uneven depth, misses obvious bugs, and contradicts itself across files.** → **A. Split into per-file passes for local issues, then a separate integration pass for cross-file data flow.** Addresses the root cause, **attention dilution**. B shifts burden to developers without improving the system. C misunderstands that a larger context window does not fix attention *quality*. D (consensus across three passes) would suppress real bugs caught only intermittently.

## How the exam is scored
- **Criterion-referenced**: each candidate is measured against a fixed performance standard, not against other candidates. You pass by demonstrating the blueprint's knowledge and skills, not by outperforming a percentage of peers.
- **Passing standard**: set by a formal **standard-setting study** in which trained subject matter experts judged the performance expected of a **minimally qualified candidate**. Reported on a scaled range of **100–1,000** with a **cut score of 720**.
- **Why scaled**: scaled scoring equates scores across multiple exam forms with slightly different difficulty.
- **Result reporting**: pass/fail plus the scaled score, plus **percent-correct per content domain**. Section-level percentages are informational — **your pass/fail result depends only on the total scaled score**.

## Key Takeaways
1. When ordering must be guaranteed and consequences are financial, choose programmatic enforcement.
2. "Most effective **first step**" rules out valid-but-expensive answers — read that qualifier carefully.
3. When logs name an upstream cause, the answer is upstream; correct downstream agents are not the bug.
4. Structured context beats generic status, and never mark a failure as a successful empty result.
5. Least privilege wins tool-distribution items: scope for the common case, delegate the exception.
6. Verify a flag or file exists before selecting it — invented surface is a standard distractor.
7. A larger context window does not fix attention quality, and consensus voting suppresses real findings.
8. 720 of 1,000 is the cut score; per-domain percentages are diagnostic only.

## Connects To
- **ch01**: the scenarios these questions sit inside, and the scoring row of the details table.
- **ch02–ch06**: Q1/Q7/Q8/Q9 → Domains 1–2 and 5; Q4/Q5/Q6/Q10 → Domain 3; Q11/Q12 → Domain 4.
- **cheatsheet.md**: these explanations condensed into decision rules.
