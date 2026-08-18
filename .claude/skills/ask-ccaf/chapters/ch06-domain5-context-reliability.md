# Chapter 6: Domain 5 — Context Management & Reliability (15%)

*6 task statements. At 15%, roughly 9 of 60 items (derived from the weight).*

## Core Idea
Protect the facts that matter from summarization, position effects, and verbose tool output — by **extracting them into a structured layer that survives compression**. Reliability comes from explicit criteria and structured error context, never from the model's self-assessment.

## Task Statements

### 5.1 Manage conversation context to preserve critical information across long interactions
**Knowledge of:** **progressive summarization risks** — condensing numerical values, percentages, dates, and customer-stated expectations into vague summaries; the **"lost in the middle" effect** — models reliably process the beginning and end of long inputs but may omit findings from middle sections; how tool results accumulate and consume tokens disproportionately to relevance (40+ fields per order lookup when 5 are relevant); the importance of passing complete conversation history in subsequent API requests for coherence.
**Skills in:** extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent **"case facts" block** included in each prompt, outside summarized history; persisting structured issue data into a separate context layer for multi-issue sessions; **trimming verbose tool outputs to only relevant fields before they accumulate**; placing key findings summaries at the **beginning** of aggregated inputs and using explicit section headers to mitigate position effects; requiring subagents to include metadata (dates, source locations, methodological context) in structured outputs; modifying upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning chains when downstream agents have limited context budgets.

### 5.2 Design effective escalation and ambiguity resolution patterns
**Knowledge of:** appropriate escalation triggers — **customer requests for a human, policy exceptions/gaps (not merely complex cases), and inability to make meaningful progress**; escalating immediately on explicit demand versus offering to resolve when the issue is straightforward; why **sentiment-based escalation and self-reported confidence scores are unreliable proxies** for case complexity; that multiple customer matches require clarification (requesting additional identifiers) rather than heuristic selection.
**Skills in:** adding explicit escalation criteria with few-shot examples showing when to escalate versus resolve autonomously; honoring explicit requests for a human immediately, without first attempting investigation; acknowledging frustration while offering resolution when the issue is within capability, escalating only if the customer reiterates; escalating when policy is ambiguous or silent (competitor price matching when policy addresses only own-site adjustments); instructing the agent to ask for additional identifiers when tool results return multiple matches.

### 5.3 Implement error propagation strategies across multi-agent systems
**Knowledge of:** **structured error context** (failure type, attempted query, partial results, alternative approaches) as what enables intelligent coordinator recovery; access failures (timeouts needing a retry decision) vs valid empty results (successful query, no matches); why generic statuses ("search unavailable") hide valuable context from the coordinator; why silently suppressing errors (empty results marked successful) and terminating whole workflows on a single failure are **both** anti-patterns.
**Skills in:** returning failure type, what was attempted, partial results, and potential alternatives; distinguishing access failures from valid empty results in reporting; local recovery in subagents for transient failures with propagation only of the unresolvable, including what was attempted and partial results; structuring synthesis output with **coverage annotations** marking which findings are well-supported versus which topic areas have gaps from unavailable sources.

### 5.4 Manage context effectively in large codebase exploration
**Knowledge of:** **context degradation in extended sessions** — models start giving inconsistent answers and referencing "typical patterns" rather than the specific classes discovered earlier; the role of **scratchpad files** for persisting key findings across context boundaries; subagent delegation to isolate verbose exploration while the main agent coordinates high-level understanding; **structured state persistence for crash recovery** — each agent exports state to a known location and the coordinator loads a manifest on resume.
**Skills in:** spawning subagents for specific questions ("find all test files", "trace refund flow dependencies") while the main agent preserves coordination; maintaining scratchpad files of key findings and referencing them later to counteract degradation; summarizing findings from one exploration phase before spawning subagents for the next, injecting summaries into initial context; designing crash recovery with structured state exports (manifests) the coordinator loads on resume and injects into agent prompts; using **`/compact`** when context fills with verbose discovery output.

### 5.5 Design human review workflows and confidence calibration
**Knowledge of:** the risk that **aggregate accuracy metrics (e.g. 97% overall) mask poor performance** on specific document types or fields; **stratified random sampling** for measuring error rates in high-confidence extractions and detecting novel error patterns; field-level confidence scores **calibrated with labeled validation sets** for routing review attention; validating accuracy by document type and field segment before automating high-confidence extractions.
**Skills in:** stratified random sampling of high-confidence extractions for ongoing error-rate measurement and novel pattern detection; analyzing accuracy by document type and field to verify consistent performance across segments before reducing human review; having models output field-level confidence, then calibrating thresholds with labeled validation sets; routing low-confidence or ambiguous/contradictory-source extractions to human review to prioritize limited reviewer capacity.

### 5.6 Preserve information provenance and handle uncertainty in multisource synthesis
**Knowledge of:** how **source attribution is lost during summarization** when findings are compressed without preserving claim-source mappings; the importance of structured **claim-source mappings** that the synthesis agent preserves and merges; how to handle conflicting statistics from credible sources — **annotate the conflict with source attribution rather than arbitrarily selecting one value**; temporal data — require publication/collection dates in structured outputs so temporal differences are not misread as contradictions.
**Skills in:** requiring subagents to output structured claim-source mappings (source URLs, document names, relevant excerpts) preserved through synthesis; structuring reports with explicit sections distinguishing **well-established from contested findings**, preserving original source characterizations and methodological context; completing document analysis with conflicting values included and explicitly annotated, letting the coordinator decide reconciliation before synthesis; requiring publication or collection dates for correct temporal interpretation; rendering content types appropriately in synthesis output — financial data as tables, news as prose, technical findings as structured lists — rather than forcing one uniform format.

## Reference Tables

### Context preservation techniques
| Threat | Technique |
|---|---|
| Progressive summarization loses numbers and dates | persistent "case facts" block outside summarized history |
| Lost in the middle | key findings summary **first**; explicit section headers |
| Verbose tool results accumulate | trim to relevant fields before they enter context |
| Context degradation in long sessions | scratchpad files; phase summaries; subagent delegation; `/compact` |
| Downstream agent has limited budget | upstream returns structured facts, citations, relevance scores |
| Crash mid-workflow | structured state exports plus a coordinator-loaded manifest |

### Escalate vs resolve
| Situation | Action |
|---|---|
| Customer explicitly asks for a human | **escalate immediately**, no prior investigation |
| Policy is silent or ambiguous on the request | escalate (policy gap) |
| No meaningful progress possible | escalate |
| Straightforward issue, customer frustrated | acknowledge, offer resolution; escalate only if they reiterate |
| Tool returns multiple customer matches | ask for additional identifiers |
| Case merely feels complex | **not** an escalation trigger on its own |
| Sentiment is negative / self-reported confidence is low | **unreliable proxies** — do not route on these |

## Anti-patterns
- **Summarizing away transactional facts** — amounts, dates, order numbers, customer-stated expectations.
- **Burying key findings in the middle** of a long aggregated input.
- **Letting full tool payloads accumulate** when 5 of 40+ fields are relevant.
- **Sentiment-based escalation** — sentiment does not correlate with case complexity.
- **Self-reported confidence as an escalation gate** — the agent is already wrongly confident on hard cases.
- **Heuristic selection among multiple customer matches** — ask for another identifier.
- **Investigating first when the customer has demanded a human.**
- **Generic error statuses** ("search unavailable") — hide recovery-relevant context.
- **Marking a failure as an empty successful result** — prevents any recovery and risks silently incomplete output.
- **Terminating the whole workflow on one subagent failure** — proceed with partial results plus coverage annotations.
- **Trusting a 97% aggregate accuracy figure** — segment by document type and field first.
- **Uncalibrated confidence thresholds** — calibrate against labeled validation sets.
- **Arbitrarily picking one of two conflicting credible statistics** — annotate both with attribution.
- **Compressing findings without claim-source mappings** — provenance cannot be reconstructed later.
- **Forcing one uniform output format** across financial, news, and technical content.

## Worked Example
**Sample Question 8 (Scenario 3).** The web search subagent times out; how should the failure reach the coordinator?

| Option | Verdict | Reasoning |
|---|---|---|
| A. Structured error context — failure type, attempted query, partial results, potential alternatives | **Correct** | Gives the coordinator what it needs to retry with a modified query, try an alternative, or proceed with partial results |
| B. Internal retry with backoff, then a generic "search unavailable" | Wrong | The generic status hides context and prevents informed decisions |
| C. Catch the timeout, return an empty result marked successful | Wrong | Suppresses the error; prevents recovery; risks incomplete research |
| D. Propagate to a top-level handler that terminates the workflow | Wrong | Terminates unnecessarily when recovery could succeed |

**Sample Question 3 (Scenario 1)** is the escalation-calibration item: an agent at 55% first-contact resolution against an 80% target escalates straightforward damage replacements with photo evidence while attempting policy exceptions autonomously. Correct answer: **explicit escalation criteria with few-shot examples** — the proportionate first response to unclear decision boundaries. Self-reported confidence (B) fails because LLM confidence is poorly calibrated and the agent is already confident on hard cases; a trained classifier (C) is over-engineered before prompt optimization; sentiment analysis (D) solves a different problem, since sentiment does not correlate with complexity.

**Preparation Exercise 4** exercises 5.3 and 5.6 directly: simulate a subagent timeout and verify the coordinator receives structured error context, can proceed on partial results, and annotates coverage gaps; then feed two credible sources with different statistics and verify synthesis preserves both with attribution and separates well-established from contested findings.

## Key Takeaways
1. Extract facts into a persistent layer outside summarized history — summaries lose numbers.
2. Put key findings at the beginning; use section headers against the lost-in-the-middle effect.
3. Trim tool output to relevant fields *before* it accumulates.
4. Escalate on: explicit human request, policy gap or ambiguity, no meaningful progress. Nothing else.
5. Sentiment and self-reported confidence are unreliable routing signals.
6. Structured error context (type, attempt, partial results, alternatives) beats both generic statuses and silent suppression.
7. Recover transient failures locally; propagate the rest with partial results; annotate coverage gaps.
8. Scratchpad files, phase summaries, subagent delegation, and `/compact` counteract context degradation; manifests give crash recovery.
9. Segment accuracy by document type and field — aggregates hide failures; calibrate confidence with labeled sets.
10. Preserve claim-source mappings and dates; annotate conflicts rather than resolving them arbitrarily.

## Prep-course supplement — context and failure-handling notes

*Source: Anthropic Partner Academy prep courses. Supplements the guide — where the two differ, answer from the guide.*

- **Direct your compaction**: `/compact` accepts instructions ("keep the API changes, drop the resolved debugging") that control what the summary preserves — undirected compaction is exactly where the numbers, dates, and decisions of 5.1 vanish.
- **Re-inject state after compaction**: a SessionStart hook with the `compact` matcher runs right after compaction and can print a summary of working files back into context, so the agent resumes warm instead of cold (mechanics in ch04).
- **Retriable or terminal — one question**: would the identical request plausibly succeed later? Transient faults, rate limits, overload → yes: back off with a cap, honor a server-supplied retry-after. Malformed request, auth failure, refusal → no: retrying changes nothing, wastes the retry budget, and hides the real cause. When unsure, fail loudly as terminal — a mislabeled terminal error gets noticed and fixed; a mislabeled retriable one hammers the service and buries the fault. Do not stack your own retry loop on top of SDK built-in retries. (Extends the guide's transient/validation/business/permission taxonomy in 2.2/5.3.)
- **A dropped tool error is worse than a loud one**: an error returned as an empty success makes the model treat missing data as valid and continue confidently on a false premise — the guide's anti-pattern, mechanized.
- **Untrusted content is data, not instructions**: anything the agent reads that someone else can write — fetched pages, shared documents, tool output — can carry injected instructions, and the model has no built-in trusted/untrusted boundary. Delimiters help but are soft; the reliable boundary is the **action side**: least-privilege tools, deny rules, and hooks that gate consequential actions regardless of what the text says. (The security rationale behind 1.4/1.5 programmatic enforcement.)

## Connects To
- **ch02 (Domain 1)**: subagent context isolation (1.3) is why provenance must be passed explicitly.
- **ch03 (Domain 2)**: structured error responses at the tool boundary (2.2) feed 5.3.
- **ch05 (Domain 4)**: confidence calibration and human review continue 4.4 and 4.6.
- **ch04 (Domain 3)**: the Explore subagent and `/compact` are the Claude Code surfaces for 5.4.
- **ch08**: Sample Questions 3 and 8.
