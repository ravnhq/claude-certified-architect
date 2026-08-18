# Chapter 2: Domain 1 — Agentic Architecture & Orchestration (27%)

*Heaviest domain: 7 task statements. At 27%, roughly 16 of 60 items (derived from the weight, not stated in the guide).*

## Core Idea
Build agent control flow on **deterministic signals and explicit context passing**, not on inference about text. The recurring exam judgment: when compliance must be guaranteed, use programmatic enforcement (hooks, prerequisite gates); when adaptability matters, specify goals and quality criteria instead of procedures.

## Task Statements

### 1.1 Design and implement agentic loops for autonomous task execution
**Knowledge of:** the loop lifecycle — send request → inspect `stop_reason` (`"tool_use"` vs `"end_turn"`) → execute requested tools → return results for the next iteration; how tool results append to conversation history so the model can reason about the next action; the distinction between **model-driven decision-making** (Claude reasons about which tool to call next from context) and pre-configured decision trees or fixed tool sequences.
**Skills in:** loop control flow that continues while `stop_reason == "tool_use"` and terminates on `"end_turn"`; adding tool results to context between iterations; avoiding termination by natural-language signal parsing, arbitrary iteration caps as the primary stop mechanism, or presence of assistant text as a completion indicator.

### 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns
**Knowledge of:** **hub-and-spoke architecture** where the coordinator manages all inter-subagent communication, error handling, and routing; that subagents run with **isolated context** and do not inherit the coordinator's history; the coordinator's role in decomposition, delegation, aggregation, and selecting which subagents to invoke by query complexity; the risk of overly narrow decomposition producing incomplete topic coverage.
**Skills in:** coordinators that dynamically select subagents rather than always running the full pipeline; partitioning scope across subagents to minimize duplication (distinct subtopics or source types); **iterative refinement loops** where the coordinator evaluates synthesis output for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage suffices; routing all subagent communication through the coordinator for observability and consistent error handling.

### 1.3 Configure subagent invocation, context passing, and spawning
**Knowledge of:** the **Task tool** as the spawning mechanism, and that `allowedTools` must include `"Task"` for a coordinator to invoke subagents; that subagent context must be provided explicitly in the prompt — no automatic inheritance, no shared memory between invocations; **AgentDefinition** configuration (descriptions, system prompts, tool restrictions per subagent type); **fork-based session management** for divergent approaches from a shared baseline.
**Skills in:** including complete prior findings directly in the subagent's prompt (e.g. passing search results and document analysis into synthesis); using structured formats to separate content from metadata (source URLs, document names, page numbers) to preserve attribution across handoffs; spawning **parallel subagents by emitting multiple Task calls in a single coordinator response** rather than across separate turns; writing coordinator prompts that specify research goals and quality criteria rather than step-by-step procedures, to enable subagent adaptability.

### 1.4 Implement multi-step workflows with enforcement and handoff patterns
**Knowledge of:** **programmatic enforcement** (hooks, prerequisite gates) versus prompt-based guidance for ordering; that when deterministic compliance is required — e.g. identity verification before financial operations — prompt instructions alone carry a non-zero failure rate; structured handoff protocols for mid-process escalation including customer details, root cause, and recommended actions.
**Skills in:** prerequisites that block downstream tool calls until prior steps complete (block `process_refund` until `get_customer` returns a verified customer ID); decomposing multi-concern requests into distinct items, investigating each in parallel over shared context, then synthesizing one unified resolution; compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) for human agents who cannot see the transcript.

### 1.5 Apply Agent SDK hooks for tool call interception and data normalization
**Knowledge of:** hook patterns such as **PostToolUse** that intercept tool *results* for transformation before the model sees them; hooks that intercept outgoing tool *calls* to enforce compliance (blocking refunds above a threshold); hooks as deterministic guarantees versus prompts as probabilistic compliance.
**Skills in:** PostToolUse hooks that normalize heterogeneous formats (Unix timestamps, ISO 8601, numeric status codes) across MCP tools before the agent processes them; interception hooks that block policy-violating actions (refunds over $500) and redirect to an alternative workflow such as human escalation; choosing hooks over prompts whenever a business rule requires guaranteed compliance.

### 1.6 Design task decomposition strategies for complex workflows
**Knowledge of:** fixed sequential pipelines (**prompt chaining**) versus **dynamic adaptive decomposition** driven by intermediate findings; prompt chaining that breaks reviews into sequential steps (analyze each file individually, then a cross-file integration pass); the value of adaptive investigation plans that generate subtasks from what each step discovers.
**Skills in:** matching pattern to workflow — prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation; splitting large code reviews into per-file local passes plus a separate cross-file integration pass to avoid **attention dilution**; decomposing open-ended tasks ("add comprehensive tests to a legacy codebase") by first mapping structure, identifying high-impact areas, then building a prioritized plan that adapts as dependencies surface.

### 1.7 Manage session state, resumption, and forking
**Knowledge of:** named session resumption via `--resume <session-name>`; `fork_session` for independent branches from a shared analysis baseline; the need to inform a resumed agent about files changed since analysis; why starting fresh with a **structured summary** beats resuming with stale tool results.
**Skills in:** `--resume` with session names for continuing named investigations; `fork_session` to compare divergent approaches (two testing strategies, two refactorings) from one codebase analysis; choosing resumption (prior context mostly valid) versus fresh start with injected summary (prior tool results stale); informing a resumed session of specific file changes for targeted re-analysis instead of full re-exploration.

## Frameworks & Patterns Named
- **Agentic loop** — `stop_reason`-driven control flow. Continue on `"tool_use"`, stop on `"end_turn"`.
- **Hub-and-spoke coordinator-subagent** — all communication flows through the coordinator.
- **Iterative refinement loop** — evaluate synthesis for gaps → re-delegate targeted queries → re-synthesize.
- **Programmatic prerequisite gate** — block tool B until tool A has returned a verified result.
- **PostToolUse hook** — normalize or transform tool results before the model reads them.
- **Tool call interception hook** — block and redirect policy-violating calls.
- **Prompt chaining** vs **dynamic adaptive decomposition**.
- **Structured handoff protocol** — the escalation payload for a human with no transcript access.
- **Fork-based session management** — `fork_session` from a shared baseline.

## Anti-patterns
- **Parsing natural language to end the loop** — inspect `stop_reason` instead.
- **Arbitrary iteration caps as the primary stopping mechanism** — a safety net, not a termination condition.
- **Treating assistant text content as a completion signal** — text can accompany a tool call.
- **Prompt instructions for rules that must never fail** — non-zero failure rate; use a hook or gate.
- **Assuming subagents inherit coordinator context** — they do not; pass findings explicitly in the prompt.
- **Spawning parallel subagents across separate turns** — emit multiple Task calls in one response.
- **Overly narrow task decomposition** — the coordinator's subtask list caps the system's coverage no matter how well subagents perform.
- **Step-by-step procedural coordinator prompts** — specify goals and quality criteria to keep subagents adaptable.
- **Resuming a session with stale tool results** — start fresh with a structured summary instead.

## Worked Example
**Sample Question 1 (Scenario 1).** In 12% of cases the agent skips `get_customer` and calls `lookup_order` from the customer's stated name, causing misidentified accounts and incorrect refunds.

| Option | Verdict | Reasoning |
|---|---|---|
| A. Programmatic prerequisite blocking `lookup_order`/`process_refund` until `get_customer` returns a verified ID | **Correct** | Critical business logic needs a deterministic guarantee |
| B. System prompt stating verification is mandatory | Wrong | Probabilistic LLM compliance; insufficient when errors are financial |
| C. Few-shot examples of always calling `get_customer` first | Wrong | Same probabilistic weakness as B |
| D. Routing classifier enabling a tool subset per request | Wrong | Addresses tool *availability*, not tool *ordering* — not the actual problem |

The generalizable rule: **financial or irreversible consequence + required ordering → programmatic enforcement.** Sample Questions 7, 8, and 9 (ch08) extend Domain 1 into coordinator decomposition, error propagation, and scoped tool provisioning.

**Preparation Exercise 1** builds this end to end: 3–4 differentiated MCP tools, a `stop_reason` loop handling both `"tool_use"` and `"end_turn"`, structured error responses, a hook enforcing a threshold rule with escalation redirect, and multi-concern decomposition. **Exercise 4** covers the coordinator side: `allowedTools` including `"Task"`, explicit context passing, parallel Task calls with measured latency improvement, structured error propagation on subagent timeout, and conflict-preserving synthesis.

## Key Takeaways
1. `stop_reason` is the only reliable loop control signal — `"tool_use"` continues, `"end_turn"` terminates.
2. Subagents have isolated context: pass complete prior findings in the prompt, every time.
3. `allowedTools` must include `"Task"` or a coordinator cannot spawn anything.
4. Parallelism comes from multiple Task calls in **one** coordinator response.
5. Guaranteed compliance = hook or prerequisite gate; prompts are guidance only.
6. Coordinator decomposition breadth is the ceiling on system coverage — a correct subagent working a wrong subtask still fails.
7. Prompt chaining for predictable passes; adaptive decomposition for open-ended investigation.
8. Prefer a fresh session with a structured summary over resuming with stale tool results.

## Prep-course supplement — workflows, agents, and loop wiring

*Source: Anthropic Partner Academy prep courses (Claude with the Anthropic API; Developer Foundations M2). Supplements the guide — where the two differ, answer from the guide.*

### Workflow vs agent — the decision before the architecture
Know the exact series of steps → a **workflow** (predefined sequence of Claude calls). Task open-ended, steps unknowable up front → an **agent** (task + tools; Claude plans). Workflows: higher completion rate, each call focused on one thing, far easier to test and eval. Agents: flexible and adaptive, but lower completion rate and harder to eval. **Default to workflows; reach for an agent only when truly required** — reliability, not sophistication, is the goal.

| Pattern | Shape | Use when |
|---|---|---|
| **Chaining** | fixed sequence of focused calls, each output feeding the next | a many-constraint output the model keeps violating in one pass — generate first, then a dedicated rewrite pass enforcing the constraints |
| **Routing** | classify the input → forward to a specialized prompt or pipeline | heterogeneous inputs that deserve per-category prompts |
| **Parallelization** | split into independent subtask calls run concurrently → an aggregator call merges | multi-aspect analysis where one giant prompt dilutes focus; scales by adding subtasks |
| **Evaluator-optimizer** | producer → grader loop; feedback returns to the producer until criteria pass | output quality you can check (render and compare, validate, re-generate) |

These are the API-level ancestors of 1.6's decomposition rules: prompt chaining is the named guide technique, and coordinator-subagent (1.2) is the agentic form of parallelization.

### Loop wiring details
- The practical loop test is `stop_reason != "tool_use"` → done. Beyond `"tool_use"` and `"end_turn"`, handle `"max_tokens"` (truncated — possibly mid-structure) and `"refusal"` (a content decision — terminal; never blind-retry it as if transient).
- The API holds **no conversation state** — resend the full history every iteration, including every block of every assistant message (text blocks alongside tool_use blocks).
- `tool_use`/`tool_result` pairing is by id, results ride in the next user message (wire mechanics in ch03).
- `is_error: true` results are the loop's repair channel: Claude reads the error text and re-calls with corrected arguments — meaningful validation errors are part of loop design, not an afterthought.
- **Environment inspection**: design the loop so the agent can observe the results of its actions (read before write, re-check state after a mutation) — the tool return value alone is often not enough signal.

## Connects To
- **ch03 (Domain 2)**: structured error responses and per-agent tool scoping are the other half of orchestration.
- **ch06 (Domain 5)**: error propagation (5.3), context passing for provenance (5.6), and crash-recovery manifests (5.4) build on 1.2–1.3.
- **ch04 (Domain 3)**: the Explore subagent and `--resume`/`fork_session` as Claude Code surfaces of 1.7.
- **ch08**: Sample Questions 1, 7, 8, 9.
