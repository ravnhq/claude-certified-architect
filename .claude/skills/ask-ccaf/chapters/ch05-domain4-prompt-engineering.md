# Chapter 5: Domain 4 — Prompt Engineering & Structured Output (20%)

*6 task statements. At 20%, roughly 12 of 60 items (derived from the weight).*

## Core Idea
Replace vague instruction with **explicit criteria, concrete examples, and schema enforcement**. Confidence language ("be conservative", "only high-confidence findings") does not improve precision; categorical criteria and few-shot examples do, and `tool_use` with a JSON schema is what actually guarantees well-formed output.

## Task Statements

### 4.1 Design prompts with explicit criteria to improve precision and reduce false positives
**Knowledge of:** explicit criteria over vague instructions — "flag comments only when claimed behavior contradicts actual code behavior" beats "check that comments are accurate"; that general instructions like "be conservative" or "only report high-confidence findings" fail to improve precision compared to specific categorical criteria; the impact of false positive rates on developer trust — high false-positive categories undermine confidence in the accurate ones.
**Skills in:** writing specific review criteria defining which issues to report (bugs, security) versus skip (minor style, local patterns) rather than relying on confidence-based filtering; **temporarily disabling high false-positive categories** to restore developer trust while improving those prompts; defining explicit severity criteria with concrete code examples per level for consistent classification.

### 4.2 Apply few-shot prompting to improve output consistency and quality
**Knowledge of:** few-shot examples as the **most effective technique** for consistently formatted, actionable output when detailed instructions alone are inconsistent; their role in demonstrating ambiguous-case handling (tool selection for ambiguous requests, branch-level coverage gaps); how they let the model **generalize judgment to novel patterns** rather than matching only pre-specified cases; their effectiveness at reducing hallucination in extraction (informal measurements, varied document structures).
**Skills in:** creating **2–4 targeted examples** for ambiguous scenarios that show the reasoning for choosing one action over plausible alternatives; examples demonstrating the desired output format (location, issue, severity, suggested fix); examples distinguishing acceptable code patterns from genuine issues to cut false positives while preserving generalization; examples covering varied document structures (inline citations vs bibliographies, methodology sections vs embedded details); examples that fix empty/null extraction of required fields.

### 4.3 Enforce structured output using tool use and JSON schemas
**Knowledge of:** `tool_use` with JSON schemas as **the most reliable approach** for guaranteed schema-compliant output, eliminating JSON syntax errors; `tool_choice` `"auto"` (may return text) vs `"any"` (must call a tool, chooses which) vs forced selection (must call a named tool); that strict schemas eliminate **syntax** errors but not **semantic** ones (line items that don't sum to the total, values in the wrong fields); schema design considerations — required vs optional fields, enum fields with `"other"` + detail string patterns for extensible categories.
**Skills in:** defining extraction tools whose input parameters are the JSON schema, then reading the structured data from the `tool_use` response; `tool_choice: "any"` to guarantee structured output when multiple extraction schemas exist and the document type is unknown; forcing `{"type": "tool", "name": "extract_metadata"}` so a particular extraction runs before enrichment; designing fields as **optional/nullable when documents may not contain the information, preventing fabrication** to satisfy required fields; adding `"unclear"` enum values for ambiguity and `"other"` + detail fields for extensible categorization; including format normalization rules in the prompt alongside the strict schema.

### 4.4 Implement validation, retry, and feedback loops for extraction quality
**Knowledge of:** **retry-with-error-feedback** — append the specific validation errors to the prompt on retry; the limits of retry — ineffective when the required information is **absent from the source** (as opposed to format or structural errors); feedback loop design — tracking which code constructs trigger findings via a `detected_pattern` field to analyze dismissal patterns; semantic validation errors (values don't sum, wrong field placement) vs schema syntax errors (already eliminated by tool use).
**Skills in:** follow-up requests containing the original document, the failed extraction, **and** the specific validation errors for self-correction; identifying when retries cannot succeed (information exists only in an external document not provided) versus when they will (format mismatches, structural errors); adding `detected_pattern` fields to findings to analyze false positives when developers dismiss them; designing self-correction flows — extract `calculated_total` alongside `stated_total` to flag discrepancies, add a `conflict_detected` boolean for inconsistent source data.

### 4.5 Design efficient batch processing strategies
**Knowledge of:** the **Message Batches API — 50% cost savings, up to a 24-hour processing window, no guaranteed latency SLA**; batch suits non-blocking latency-tolerant workloads (overnight reports, weekly audits, nightly test generation) and is unsuitable for blocking workflows (pre-merge checks); the batch API **does not support multi-turn tool calling within a single request**; `custom_id` fields for correlating request/response pairs.
**Skills in:** matching API to latency requirement — synchronous for blocking pre-merge checks, batch for overnight/weekly analysis; calculating submission frequency from SLA constraints (4-hour submission windows to guarantee a 30-hour SLA against 24-hour batch processing); handling failures by resubmitting **only** failed documents identified by `custom_id`, with modifications such as chunking documents that exceeded context limits; refining the prompt on a sample set before batching large volumes to maximize first-pass success and cut resubmission cost.

### 4.6 Design multi-instance and multi-pass review architectures
**Knowledge of:** **self-review limitations** — a model retains its generation reasoning context and is less likely to question its own decisions in the same session; **independent review instances** without that context catch subtle issues better than self-review instructions or extended thinking; **multi-pass review** — per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings.
**Skills in:** using a second independent Claude instance to review generated code; splitting large multi-file reviews into per-file passes for local issues plus separate integration passes for cross-file data flow; running verification passes where the model self-reports confidence alongside each finding to enable calibrated review routing.

## Reference Tables

### Structured-output mechanism by problem
| Problem | Mechanism |
|---|---|
| Malformed JSON | `tool_use` with a strict JSON schema |
| Model returns prose instead of data | `tool_choice: "any"` |
| A specific extraction must run first | `tool_choice: {"type":"tool","name":"..."}` |
| Model fabricates missing values | make fields optional/nullable |
| Ambiguous category values | enum with `"unclear"`; `"other"` + detail string |
| Totals that don't add up | semantic validation — extract `calculated_total` and `stated_total` |
| Inconsistent source formatting | format normalization rules in the prompt, alongside the schema |

### Synchronous vs Message Batches API
| Dimension | Synchronous | Batch |
|---|---|---|
| Cost | full | **50% savings** |
| Latency | immediate | up to **24 hours**, no SLA |
| Multi-turn tool calling | supported | **not supported** |
| Correlation | per-request | `custom_id` |
| Fits | blocking pre-merge checks | overnight reports, weekly audits, nightly test generation |

### Precision levers, most to least effective
| Lever | Effect |
|---|---|
| Explicit categorical criteria | defines what to report vs skip |
| Few-shot examples (2–4) | format consistency, ambiguous-case judgment, generalization |
| Disabling a high-FP category temporarily | restores developer trust while its prompt is fixed |
| "Be conservative" / confidence filtering | **ineffective** |

## Anti-patterns
- **Confidence-based filtering as a precision strategy** — "only report high-confidence findings" does not work; self-reported confidence is poorly calibrated.
- **Vague criteria** — "check that comments are accurate" instead of a contradiction test.
- **Required fields for information documents may not contain** — invites fabrication.
- **Assuming a strict schema prevents semantic errors** — it eliminates syntax errors only.
- **Retrying when the information is absent from the source** — retry fixes format and structure, not missing data.
- **Retrying without including the specific validation errors** — the model has nothing to correct against.
- **Batch API for blocking workflows** — no latency SLA; "often faster" is not acceptable for a pre-merge gate.
- **Batch API for multi-turn tool calling** — unsupported within a single request.
- **Resubmitting an entire batch after partial failure** — resubmit only the failed `custom_id`s.
- **Single-pass review of a large multi-file PR** — attention dilution yields inconsistent depth and contradictory findings.
- **Self-review in the generating session**, or reaching for a larger context window to fix attention quality.
- **Consensus voting across independent passes** — suppresses real bugs caught intermittently.

## Worked Example
**Sample Question 11 (Scenario 5).** Two workflows — a blocking pre-merge check and an overnight technical debt report — and a proposal to move both to the Message Batches API for 50% savings.

| Option | Verdict | Reasoning |
|---|---|---|
| A. Batch for the overnight reports only; keep real-time for pre-merge | **Correct** | Matches each API to its latency tolerance |
| B. Both to batch with status polling | Wrong | "Often faster" is unacceptable for a blocking workflow |
| C. Keep both real-time to avoid ordering issues | Wrong | Misconception — `custom_id` correlates batch results |
| D. Both to batch with a real-time timeout fallback | Wrong | Unnecessary complexity when matching API to use case is simpler |

**Sample Question 12 (Scenario 5)** covers 4.6: a 14-file PR reviewed in one pass gives detailed feedback on some files, superficial comments on others, misses obvious bugs, and contradicts itself — flagging a pattern in one file while approving identical code elsewhere. Correct answer: **split into per-file local passes plus a separate cross-file integration pass**. Requiring developers to split PRs shifts burden without improving the system; a larger context window does not fix **attention quality**; consensus across three full passes would suppress real bugs detected intermittently. The named root cause is **attention dilution**.

**Preparation Exercise 3** runs the domain end to end: a schema with required, optional, nullable, and `"other"` + detail enum fields verified to return null rather than fabricate; a validation-retry loop sending the document, the failed extraction, and the specific error, tracking which errors retry can fix; few-shot examples for varied document formats; a 100-document batch with `custom_id` failure handling, chunking oversized documents, and processing time computed against the SLA; and confidence-based human review routing with accuracy analyzed by document type and field.

## Key Takeaways
1. Categorical criteria beat confidence language every time.
2. 2–4 few-shot examples showing the *reasoning* for a choice generalize to novel cases.
3. `tool_use` + JSON schema eliminates syntax errors; semantic validation is still your job.
4. `"auto"` may return text, `"any"` guarantees some tool, forced selection guarantees a specific tool.
5. Nullable/optional fields prevent fabrication; `"unclear"` and `"other"` + detail absorb ambiguity.
6. Retry with the specific errors appended — and recognize when the data simply is not there.
7. Batch = 50% cheaper, up to 24 hours, no SLA, no multi-turn tool calling, `custom_id` correlation.
8. Independent review instances beat self-review; per-file plus integration passes beat one big pass.
9. High false-positive categories damage trust in accurate ones — disable and fix rather than tolerate.

## Prep-course supplement — prompt construction and the eval workflow

*Source: Anthropic Partner Academy prep courses (Claude with the Anthropic API; Developer Foundations M2/M4). Supplements the guide — where the two differ, answer from the guide.*

### Building a prompt, in order of leverage
1. **First line — clear and direct**: an action verb, the task, and the expected output ("Generate a one-day meal plan for an athlete that meets their dietary restrictions"). The first line is the highest-leverage line in the prompt.
2. **Be specific** with two kinds of structure: **guidelines** (qualities the output must have — length, structure, required attributes; use on almost every prompt) and **steps** (a process the model should follow; use for complex analysis where you must force breadth it would not naturally consider).
3. **XML tags** delimit interpolated content (`<my_code>`, `<docs>`, `<sales_records>`) — invented, descriptive tag names; they stop instruction/data confusion when large content is pasted into a prompt.
4. **Examples** (one-shot / multi-shot): for corner cases (sarcasm in sentiment work) and complex output formats. Wrap in `<sample_input>` / `<ideal_output>` tags; appending *why* the output is ideal reinforces the pattern. Mine your highest-scoring eval outputs as examples instead of writing them from scratch.
5. **Prefill + stop sequences** — the lightweight alternative for raw structured output: prefill the assistant message with a fenced ` ```json ` opener and set the closing fence as a stop sequence, stripping headers, footers, and commentary; the prefill text itself can steer ("Here are all three commands in a single block without comments:"). `tool_use` + schema remains the guide's reliable mechanism (4.3); prefill suits quick pipelines and eval harnesses.
6. **Temperature**: low → deterministic extraction and classification; high → creative variety. Not a substitute for any technique above.

### Diagnose before re-prompting
Match the failure to the missing piece, then add exactly that:
- Output in the wrong **shape** (prose where you wanted a label/JSON) → missing **output constraint**.
- Content or scope **drifts** across turns → underspecified **system prompt** (the behavioral contract).
- Task right, **structure invented** → missing **few-shot examples** — a model cannot infer an exact structure from description alone.
- Happy path fine, **edge cases break** → add a constraint or example naming the variant.
The smell: a prompt that grows longer every revision without getting more precise. Six passes of richer description cannot substitute for one output constraint plus two examples — and long, unfocused prompts also produce long, unfocused output (a latency regression with no accuracy gain).

### The eval workflow
Pipeline: draft prompt → generate a **test dataset** (Claude with a fast model generates input cases from a spec; spot-check them) → run the prompt per case → grade each output → average → change **one thing** → rerun. Write the eval before polishing the feature, or you end up rationalizing whatever the model produces.

| Grader | Fits | Caveat |
|---|---|---|
| **Code grader** | one correct form or a structural rule — JSON parses, Python AST compiles, regex compiles, length/keyword checks; score 10 or 0 | near-free, run on every change; says nothing about content quality |
| **Model grader (LLM-as-judge)** | open-ended quality — faithfulness, instruction-following, completeness | demand strengths, weaknesses, and **reasoning before the score**, or judges drift to a safe middle (~6); **calibrate against human-labeled cases** before trusting; one extra API call per case |
| **Human grading** | anything, most flexible | slow and tedious — reserve for the calibration set |

Merge graders where both apply (average the model score with the syntax score). Read **per-case results**, not just the average — a flat average hides a change that fixed three cases and broke three. **Coverage beats rubric perfection**: more cases with slightly noisier grading catches more regressions than a few hand-polished ones. This is the calibration machinery behind the guide's 5.5 (labeled validation sets, accuracy by segment).

## Connects To
- **ch03 (Domain 2)**: `tool_choice` and tool schemas are the same mechanism used for tool selection.
- **ch04 (Domain 3)**: CI review prompts (`--json-schema`, independent review instance) apply 4.1 and 4.6.
- **ch06 (Domain 5)**: confidence calibration and human review routing (5.5) continue 4.4 and 4.6.
- **ch08**: Sample Questions 11 and 12.
