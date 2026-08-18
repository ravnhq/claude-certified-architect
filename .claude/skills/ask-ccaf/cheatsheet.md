# Cheatsheet — CCAR-F decision rules

## Answer-selection rules (from the sample-question explanations)
- **If a rule must never fail (financial, irreversible, ordering) → programmatic enforcement.** Prompts and few-shot are probabilistic; hooks and prerequisite gates are deterministic.
- **If the question says "first step" or "most effective first" → pick the cheapest root-cause fix.** A valid but heavier architectural answer is scored wrong.
- **If the logs name an upstream cause → answer upstream.** Correct downstream agents are never the bug.
- **If an option cites a flag, env var, or config file → verify it exists.** `CLAUDE_HEADLESS`, `--batch`, and `.claude/config.json` do not.
- **If an option adds a classifier, routing layer, or ML infrastructure before prompt work → over-engineered.**
- **If an option relies on self-reported confidence or sentiment → wrong.** Both are unreliable proxies for complexity.
- **If an option marks failure as an empty success, or kills the whole workflow → wrong.** Both are named anti-patterns.
- **If an option offers a bigger context window for uneven attention → wrong.** Context size ≠ attention quality.

## Thresholds and numbers
| Value | Meaning |
|---|---|
| 60 items / 120 min | 2 minutes per item |
| **720** of 100–1,000 | cut score (total scaled score only decides pass/fail) |
| 27 / 20 / 20 / 18 / 15 % | Domains 1 / 3 / 4 / 2 / 5 weights |
| 4 of 6 scenarios | appear, at random |
| 4–5 tools per agent | reliable; **18** degrades selection |
| 2–4 few-shot examples | the prescribed count |
| 2–3 input/output examples | for clarifying a transformation |
| 50% savings, ≤24 h, no SLA | Message Batches API |
| 4-hour submission windows | to guarantee a 30-hour SLA |
| $500 refund cap, 12% skip rate, 40% latency, 85/15 split, 97% aggregate | numbers quoted in the sample items |
| 14 / 30 / 90 days | retake waits; 4 attempts per rolling 12 months |
| 12 months | credential validity; free non-proctored renewal if not lapsed |

## Where does it go? (Claude Code)
| Requirement | Location |
|---|---|
| Shared with the team | project path, version-controlled |
| Personal only | `~/.claude/...` |
| Always loaded, universal | CLAUDE.md |
| On-demand, task-specific | skill in `.claude/skills/` |
| **Automatic + files scattered across directories** | `.claude/rules/` with `paths:` globs |
| Verbose skill output isolated | `context: fork` |
| Restrict a skill's tools | `allowed-tools` |
| Prompt for missing parameters | `argument-hint` |
| Shared MCP server | `.mcp.json` with `${VAR}` |
| Personal MCP server | `~/.claude.json` |
| Diagnose loaded memory | `/memory` |

## Plan mode vs direct execution
- Multi-file, architectural, multiple valid approaches → **plan mode** (do not wait for complexity to "emerge" when the requirements already state it).
- Single-file fix, clear stack trace, one conditional → **direct execution**.
- Investigate then build → plan mode, then direct execution.

## tool_choice
`"auto"` may return text · `"any"` guarantees some tool (unknown document type) · `{"type":"tool","name":"X"}` forces order (`extract_metadata` before enrichment).

## Sync vs batch
Blocking (pre-merge gate) → synchronous. Overnight/weekly, latency-tolerant → batch. Needs multi-turn tool calling → synchronous, batch cannot.

## Escalate or resolve
Escalate: explicit human request (immediately, no investigation first) · policy gap or ambiguity · no meaningful progress. Ask for identifiers on multiple matches. Not triggers: complexity alone, negative sentiment, low self-reported confidence.

## Error taxonomy → agent behavior
transient → retry (locally in the subagent) · validation → fix input · business → `retriable: false` + explain/escalate · permission → escalate · **valid empty result → success, not failure**.

## Tells and smells
- Two tools with near-identical descriptions → misrouting incoming; rewrite descriptions first.
- Reports coherent but topic coverage lopsided → coordinator decomposition too narrow.
- Contradictory review feedback across files in one PR → attention dilution; split into per-file + integration passes.
- Model fabricates values → a required field should be nullable.
- Retries never converge → the information is absent from the source; route to human review.
- Agent answers with "typical patterns" instead of the classes it found → context degradation; scratchpad, phase summary, or `/compact`.
- 97% aggregate accuracy quoted → demand per-document-type and per-field segmentation.
- Numbers or dates missing after a long conversation → progressive summarization; add a case-facts block.
- Two credible sources disagree → annotate both with attribution; never pick one silently.

## Scope boundary (fastest study cut)
**In**: using Claude Code, Agent SDK, Claude API, MCP — configure, orchestrate, prompt, manage context.
**Out**: fine-tuning, model internals, RLHF/Constitutional AI, embeddings and vector DBs, computer use, vision, streaming/SSE, rate limits and pricing math, OAuth and key rotation, cloud provider config, benchmarking, prompt caching internals, tokenization. Configuring an MCP server is in scope; **deploying or hosting one is not**. Batch cost/SLA arithmetic is the one pricing-adjacent exception.

---

# Prep-course selectors (supplementary — guide wins on any conflict)

## Permission mode → job
default = unfamiliar codebase · acceptEdits = trusted local iteration (still gates shell beyond common fs commands) · plan = research only · auto = unattended-at-work (classifier checks intent, never correctness — add a Stop hook running tests) · dontAsk = CI/pipelines (auto-deny, never hangs) · bypassPermissions = disposable container/VM only. Deny > ask > allow at every level; enterprise deny survives everything.

## Instruction surface → rule type
Always-on convention → CLAUDE.md · task procedure/reference → skill · must-never-skip rule → hook (instructions the model follows vs code that runs). "Never push to main" = PreToolUse hook.

## Hook event selector
Block or rewrite a call → PreToolUse (deny / updatedInput) · react after a call (format, lint, audit) → PostToolUse · refuse "done" until tests pass → Stop (exit 2) · re-inject state after compaction → SessionStart + compact matcher. Exit 0 = success, exit 2 = block + stderr to Claude, **exit 1 does not block**.

## MCP primitive selector
Model needs a capability → tool (model-controlled) · app needs data for UI/context → resource (app-controlled; direct URI vs templated) · user invokes a vetted workflow → prompt (user-controlled, slash command). stdio = local subprocess · HTTP = shared/remote · SSE = legacy.

## Workflow vs agent
Steps known → workflow (chaining · routing · parallelization · evaluator-optimizer); steps unknowable → agent with abstract, composable tools. Default to workflows — testability and completion rate.

## Grader selector
One correct form → exact match · structural rule → code grader (parse/AST/regex, 10-or-0) · open-ended quality → LLM judge (reasoning before score; calibrate on human labels). Change one variable per eval run; read per-case results.

## Additional stop_reason values
`max_tokens` = truncated (possibly mid-structure) · `refusal` = content decision — terminal, never blind-retry. Loop test stays `stop_reason != "tool_use"` → done.
