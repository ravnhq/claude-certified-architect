# Patterns — techniques named in the CCAR-F exam guide

## Agentic loop (stop_reason control flow)
**When to use**: any autonomous agent that calls tools until a task completes.
**How**: send request → inspect `stop_reason` → if `"tool_use"`, execute the requested tools, append results to conversation history, iterate → if `"end_turn"`, present the final response.
**Trade-offs**: model-driven next-tool selection adapts to context but is less predictable than a fixed decision tree. Iteration caps belong as a safety net, never as the primary termination condition.

## Coordinator-subagent (hub-and-spoke)
**When to use**: work decomposable across specialized agents needing observability and consistent error handling.
**How**: coordinator decomposes the task, selects which subagents to invoke by query complexity, routes all inter-agent communication, aggregates results. `allowedTools` must include `"Task"`.
**Trade-offs**: all traffic through the hub adds round trips (see scoped cross-role tools) but gives one place for error handling and logging. Decomposition breadth caps total coverage.

## Explicit context passing to subagents
**When to use**: always — subagents have isolated context and no shared memory.
**How**: include complete prior findings in the subagent's prompt; use structured formats separating content from metadata (source URLs, document names, page numbers).
**Trade-offs**: prompt size grows; mitigate by passing structured facts and citations instead of verbose reasoning chains.

## Parallel subagent spawning
**When to use**: independent subtasks that can run concurrently.
**How**: emit multiple Task tool calls in a **single** coordinator response.
**Trade-offs**: no cross-subagent coordination mid-flight; unsuitable when one subtask's output feeds another.

## Iterative refinement loop
**When to use**: open-ended research where first-pass coverage is uncertain.
**How**: coordinator evaluates synthesis output for gaps → re-delegates targeted queries to search and analysis subagents → re-invokes synthesis until coverage is sufficient.
**Trade-offs**: extra latency and cost per cycle; needs an explicit sufficiency criterion or it does not terminate.

## Programmatic prerequisite gate
**When to use**: a required tool ordering with financial, legal, or irreversible consequences.
**How**: block downstream tool calls until the prerequisite returns a verified result (block `process_refund` until `get_customer` returns a verified customer ID).
**Trade-offs**: deterministic but rigid; every legitimate exception needs its own path.

## Hook-based interception
**When to use**: business rules requiring guaranteed compliance, or heterogeneous tool output needing normalization.
**How**: **PostToolUse** hooks transform results before the model reads them (Unix timestamps, ISO 8601, numeric status codes → one format). Tool-call interception hooks block policy violations (refunds over $500) and redirect to escalation.
**Trade-offs**: deterministic where prompts are probabilistic; hook logic lives outside the prompt, so it is invisible to the model's reasoning unless surfaced in the redirect.

## Structured handoff protocol
**When to use**: mid-process escalation to a human who cannot see the transcript.
**How**: compile customer ID, root cause analysis, amount, and recommended action into one payload.
**Trade-offs**: costs a synthesis step; without it the human restarts the investigation.

## Prompt chaining vs dynamic decomposition
**When to use**: chaining for predictable multi-aspect work (per-file analysis, then a cross-file pass); dynamic decomposition for open-ended investigation.
**How**: chaining fixes the sequence up front; dynamic decomposition generates subtasks from what each step discovers — map structure, identify high-impact areas, build a prioritized plan that adapts as dependencies appear.
**Trade-offs**: chaining is predictable and cheap to reason about but blind to surprises; dynamic decomposition adapts but is harder to bound.

## Session resumption vs fresh start with summary
**When to use**: resumption when prior context is mostly valid; fresh start when tool results are stale.
**How**: `--resume <session-name>` for named continuation, informing the agent which files changed for targeted re-analysis. Otherwise start new and inject a structured summary. `fork_session` branches divergent approaches from one baseline.
**Trade-offs**: resuming preserves nuance but risks acting on stale reads; a fresh session is reliable but loses unwritten context.

## Differentiated tool descriptions
**When to use**: whenever two tools could plausibly serve one request.
**How**: state input formats, example queries, edge cases, and boundaries ("use this instead of X when…"). Rename to remove overlap (`analyze_content` → `extract_web_results`); split generic tools into purpose-specific ones with defined contracts.
**Trade-offs**: longer descriptions cost tokens, but far less than misrouting. Check system prompts for keyword-sensitive wording that overrides them.

## Structured error responses
**When to use**: every MCP tool.
**How**: set `isError`, return `errorCategory` (transient/validation/permission/business), `isRetryable` / `retriable: false`, and a human-readable description. Distinguish access failures from valid empty results.
**Trade-offs**: more schema surface to maintain; without it the agent cannot choose between retry, explain, and escalate.

## Local recovery, selective propagation
**When to use**: multi-agent systems with transient failure modes.
**How**: subagents retry transient failures themselves; propagate only unresolvable errors, including what was attempted and any partial results. Coordinator proceeds with partial results and annotates coverage gaps.
**Trade-offs**: hides recoverable noise from the coordinator, which is the point — but log locally or failures become invisible.

## Scoped tool access with cross-role exceptions
**When to use**: specialized agents where round-tripping dominates latency for a common case.
**How**: give each agent only role-relevant tools; add one constrained cross-role tool for a high-frequency need (a `verify_fact` tool for the synthesis agent), routing complex cases through the coordinator. Replace generic tools with validated alternatives (`fetch_url` → `load_document`).
**Trade-offs**: least privilege preserved; each exception is a small breach of separation of concerns, so justify it with measured frequency.

## Path-scoped rules
**When to use**: conventions that must apply automatically to files spread across directories.
**How**: `.claude/rules/*.md` with YAML frontmatter `paths:` globs (`paths: ["**/*.test.*"]`, `paths: ["terraform/**/*"]`).
**Trade-offs**: loads only on matching files, cutting context; glob maintenance is on you. Directory-bound CLAUDE.md cannot cover scattered files, and skills cannot guarantee automatic loading.

## Structured output via tool_use and JSON schema
**When to use**: any extraction or machine-consumed output.
**How**: define an extraction tool whose input schema is the output contract; read data from the `tool_use` response. `tool_choice: "any"` when the document type is unknown among several schemas; forced selection when one extraction must run first. Make fields optional/nullable where the source may lack them; add `"unclear"` enums and `"other"` + detail strings.
**Trade-offs**: eliminates syntax errors, not semantic ones — pair with validation.

## Validation-retry with error feedback
**When to use**: extraction pipelines with semantic validation.
**How**: on failure, resend the original document, the failed extraction, and the specific validation errors. Extract `calculated_total` alongside `stated_total`; add a `conflict_detected` boolean.
**Trade-offs**: retries fix format and structure, never absent information — detect that case and route to human review instead.

## Batch processing strategy
**When to use**: non-blocking, latency-tolerant volume (overnight reports, weekly audits, nightly test generation).
**How**: Message Batches API for 50% savings within a 24-hour window; correlate with `custom_id`; resubmit only failed IDs with modifications (chunk oversized documents); refine the prompt on a sample first; size submission windows from the SLA (4-hour windows to guarantee 30 hours).
**Trade-offs**: no latency SLA and no multi-turn tool calling — never for blocking pre-merge checks.

## Multi-pass and multi-instance review
**When to use**: large multi-file reviews, and reviewing code the same session generated.
**How**: per-file passes for local issues plus a separate integration pass for cross-file data flow; a second independent Claude instance without the generator's reasoning context; verification passes that self-report confidence per finding for routing.
**Trade-offs**: more calls and cost; a larger context window does not substitute, and consensus voting across passes suppresses intermittently caught bugs.

## Explicit criteria over confidence filtering
**When to use**: any precision problem — code review, extraction, escalation.
**How**: define categorically what to report versus skip; define severity levels with concrete code examples; add 2–4 few-shot examples showing why one action was chosen over plausible alternatives. Temporarily disable a high false-positive category while fixing its prompt.
**Trade-offs**: criteria need maintenance as the codebase evolves; self-reported confidence and "be conservative" do not work at all.

## Context preservation layer
**When to use**: long conversations, multi-issue sessions, verbose tool output.
**How**: extract transactional facts into a persistent "case facts" block outside summarized history; trim tool results to relevant fields before they accumulate; place key findings at the beginning of aggregated inputs with explicit section headers; keep scratchpad files across boundaries; summarize each phase before spawning the next subagents; `/compact` when discovery output fills context; export state manifests for crash recovery.
**Trade-offs**: an extra maintained layer, but the only defense against summarization loss and lost-in-the-middle effects.

## Escalation criteria with few-shot examples
**When to use**: agents with a human fallback path.
**How**: escalate on explicit human request (immediately, without investigating first), policy gaps or ambiguity, and inability to progress. Ask for additional identifiers when tool results return multiple matches. Acknowledge frustration while offering resolution when the issue is within capability.
**Trade-offs**: needs upkeep as policy changes; sentiment and self-reported confidence are unreliable substitutes.

## Provenance-preserving synthesis
**When to use**: multi-source research with citation requirements.
**How**: subagents emit claim-source mappings (URL, document name, excerpt, publication date) that downstream agents preserve; reports separate well-established from contested findings; conflicting values are annotated with attribution rather than resolved arbitrarily; render financial data as tables, news as prose, technical findings as structured lists.
**Trade-offs**: heavier payloads and longer reports, in exchange for attribution that survives summarization.

## Human review routing with calibrated confidence
**When to use**: before reducing human review on an extraction pipeline.
**How**: field-level confidence scores calibrated on labeled validation sets; stratified random sampling of high-confidence output for ongoing error measurement; accuracy analyzed by document type and field; route low-confidence or contradictory-source cases to humans.
**Trade-offs**: needs labeled data and ongoing sampling cost; aggregate accuracy alone hides segment failures.

---

# Supplementary patterns — from the Partner Academy prep courses

*Not named in the Exam Guide; drawn from Anthropic's official CCAR-F prep courses. Where a supplementary pattern and the guide differ, answer from the guide.*

## Workflow patterns (chaining, routing, parallelization, evaluator-optimizer)
**When to use**: you know the steps in advance — default to a workflow over an agent; reliability beats flexibility.
**How**: chaining = fixed sequence of focused calls (generate, then a rewrite pass enforcing violated constraints); routing = classify the input, forward to a specialized prompt; parallelization = independent subtask calls run concurrently, merged by an aggregator call; evaluator-optimizer = producer → grader loop, feedback returning to the producer until criteria pass.
**Trade-offs**: workflows are easier to test and eval and complete more reliably; agents (task + abstract tools, Claude plans) adapt to unknown tasks but complete less reliably and resist evaluation.

## Hook-gated verification of unsupervised runs
**When to use**: any run nobody watched — unattended sessions, CI, headless jobs.
**How**: verify in proportion to autonomy. Read the diff, not the summary of it; wire tests as a Stop hook that refuses end-of-turn on failure (exit 2 feeds the failure back and the agent fixes it); check headless runs by JSON result and exit code; take a cold review from a fresh session or subagent with no memory of how the code was built.
**Trade-offs**: setup cost once; pays back the first time it catches something on a run you were not watching. An intent classifier (auto mode) never judges correctness — the hook does.

## Prefill + stop-sequence extraction
**When to use**: raw structured output in lightweight pipelines and eval harnesses, where full `tool_use` schema machinery is overkill.
**How**: prefill the assistant message with the opening fence (```` ```json ````) and set the closing fence as a stop sequence — the model believes it already wrote the wrapper and emits only the payload; prefill prose also steers ("Here are all three commands without comments:").
**Trade-offs**: no schema guarantee — `tool_use` + JSON schema remains the reliable mechanism (guide 4.3); prefill is incompatible with schema-constrained output modes.

## Calibrated eval loop
**When to use**: before trusting any prompt in production, and before every prompt change after that.
**How**: generate a test dataset with a fast model from an input spec (spot-check it) → run the prompt per case → grade → average → change one variable → rerun. Code graders (parse/AST/regex-compile, 10-or-0) for form; an LLM judge for open-ended quality — demand strengths, weaknesses, and reasoning before the score or it drifts to a safe ~6, and calibrate it against human-labeled cases first; merge scores where both apply.
**Trade-offs**: judges cost one extra call per case — grade form with code on every change, reserve the judge for scheduled quality passes. Read per-case results; averages hide fixed-three-broke-three. Coverage beats rubric perfection.

## Environment inspection
**When to use**: any agent whose actions change state it cannot directly see.
**How**: give the agent an observation path beyond tool return values — read a file before editing it, re-check state after a mutation, extract frames or captions to verify generated media — and prompt it to use that path to gauge progress.
**Trade-offs**: extra calls per action; without it the agent reasons about an environment it is only guessing at.
