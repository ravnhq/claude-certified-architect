# Claude Certified Associate – Foundations (CCAO-F) Study Guide

This guide follows the **official Version 1.0 blueprint, effective July 2026**. It is for professionals who use Claude as a productivity tool for research, analysis, drafting, planning, and workflow improvement. The exam does **not** expect API development or advanced software engineering.

Use the [official exam guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542847%2FClaude+Certified+Associate+%E2%80%93+Foundations+Exam+Guide.pdf) as the authority. Product features and policies change, so verify current behavior in Anthropic's documentation before the exam.

> This is an independent study aid. The accompanying question bank comes from a public third-party practice site; it is not live exam content, and its answer keys have not been independently verified by Anthropic or Ravn.

## Exam at a glance

| Fact | Official value |
|---|---:|
| Exam code | CCAO-F |
| Questions | 60 multiple-choice and multiple-response items |
| Time | 120 minutes |
| Delivery | Proctored online or at a test center |
| Passing score | 720 on a 100–1,000 scale |
| List fee | $99 USD per attempt |
| Validity | 12 months |
| Prerequisites | None |

The official score report gives pass/fail, a scaled score, and percentage performance by domain. Treat the cut score as a scaled result rather than assuming that exactly 72% raw is sufficient.

### Blueprint and practice-exam draw

| Domain | Weight | Practice draw |
|---|---:|---:|
| 1. Prompting and Task Execution | 14% | 8 |
| 2. Output Evaluation and Validation | 21% | 13 |
| 3. Product and Model Selection | 12% | 7 |
| 4. Workflow Integration and Solution Design | 16% | 10 |
| 5. Configuration and Knowledge Management | 12% | 7 |
| 6. Governance, Risk, and Responsible Use | 15% | 9 |
| 7. Troubleshooting and Optimization | 10% | 6 |
| **Total** | **100%** | **60** |

The practice draw uses largest-remainder apportionment. Domain 2 is the largest target: spend roughly one fifth of preparation time learning how to evaluate, verify, and refine outputs.

## The decision pattern the exam rewards

Across all seven domains, the strongest answer usually does five things:

1. starts from the user's outcome and constraints;
2. chooses the lightest product, model, or process that can meet them;
3. grounds important work in relevant evidence;
4. puts human review before a consequential or irreversible action; and
5. measures the result, diagnoses misses, and improves the smallest relevant layer.

Be suspicious of answers that rely on confidence, make a capability claim without evidence, send sensitive data without checking policy, or add complexity before identifying the actual failure.

# Domain 1 — Prompting and Task Execution (14%)

## 1.1 Create effective prompts for business and technical tasks

An effective prompt is a compact work contract. State the task, relevant context, constraints, intended audience, output format, and success criteria. Delimit source material clearly, identify what may and may not be inferred, and request uncertainty or missing information explicitly.

Use examples when they demonstrate a shape or edge case more efficiently than prose. More words are not automatically better: irrelevant instructions compete with the request.

**Practice:** turn a vague request such as “analyze this report” into a prompt that names the decision, evidence, audience, format, and validation rule.

## 1.2 Apply task decomposition techniques to structure complex requests

Break complex work at natural verification points. A useful sequence is: understand requirements, gather or organize evidence, perform the analysis, draft the deliverable, then review against criteria. Check intermediate outputs before later stages depend on them.

Decomposition is not ceremony. A simple rewrite rarely needs five stages; a research-backed recommendation usually does.

## 1.3 Iterate prompts to improve output quality

Iteration is diagnosis, not repetition. Identify the exact defect—missing evidence, wrong audience, weak structure, excess length, inconsistent tone, or misunderstood constraint—then change the smallest relevant instruction or context and compare again using the same rubric.

“Try again” supplies no new information. Specific feedback such as “retain the three verified findings, remove implementation detail, and put the decision in the first paragraph” does.

## 1.4 Adapt prompting strategies based on task type

| Task | Prompt emphasis |
|---|---|
| Analysis | decision, criteria, evidence, assumptions, trade-offs |
| Research | scope, date, primary sources, citations, conflicting evidence |
| Drafting | audience, purpose, voice, length, required facts |
| Brainstorming | breadth, distinct categories, constraints, defer ranking |

Research needs traceability; brainstorming needs variety before convergence. Do not treat creative possibilities as verified findings.

### Domain 1 checklist

- Can I write a prompt with task, context, constraints, audience, format, and success criteria?
- Can I choose where to split a complex request and what to verify at each stage?
- Can I diagnose a weak result before revising the prompt?
- Can I explain why research and brainstorming require different instructions?

# Domain 2 — Output Evaluation and Validation (21%)

## 2.1 Evaluate Claude-generated outputs for accuracy and completeness

Evaluate against a rubric, not against how polished the answer sounds. Check factual accuracy, requirement coverage, relevance, internal consistency, audience fit, and the requested format. Reconcile totals, dates, names, and citations. A response that answers a nearby question fluently is still wrong.

## 2.2 Identify hallucinations, inconsistencies, and biases

A hallucination is a claim without adequate support. Warning signs include plausible but untraceable citations, invented quotations, precise numbers with no source, and details that exceed the supplied evidence. Inconsistencies may appear across sections or between prose and tables.

Bias can enter through the prompt, source set, framing, examples, or what is omitted. Ask whose perspective is represented, who could be excluded, and whether a proxy variable changes the result unfairly.

## 2.3 Apply fact-checking and validation techniques

Match evidence to the claim:

- laws and policies → the official text and effective date;
- current business facts → the authoritative system of record;
- calculations → reproduce them from inputs;
- research claims → primary sources, with independent corroboration when stakes are high;
- quotations → the original source and surrounding context.

Search snippets and Claude's citations are leads to inspect, not proof by themselves.

## 2.4 Determine when human review or additional verification is required

Require qualified review for regulated, safety-critical, financial, legal, medical, employment, privacy-sensitive, or otherwise consequential work. Review also belongs where ambiguity is real, evidence conflicts, or the action is difficult to reverse.

Put the gate before publication, sending, payment, access change, or other side effect. A review after the action is an audit, not a safeguard.

## 2.5 Edit, adapt, refine, and compare outputs for the intended audience

Separate factual correction from style adaptation. Preserve verified meaning while changing structure, tone, vocabulary, and detail. Compare alternatives against named criteria such as clarity, evidence, actionability, and audience fit.

When summarizing for executives, retain uncertainty, impact, and the decision required. “Shorter” must not mean “less honest.”

## 2.6 Organize and curate information and select appropriate output formats

Choose the format from the next action:

- **inline response** for a short answer or conversational iteration;
- **table or structured data** for comparison, sorting, or downstream processing;
- **artifact** for substantial, self-contained content that will be edited, reused, presented, or shared.

Anthropic describes artifacts as reusable deliverables that open beside the conversation and can include documents, code, diagrams, dashboards, and small tools. See [What are artifacts?](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them).

### Official sample-question lesson

The guide asks how to handle a response citing a specific regulation subsection. The correct move is to verify the cited language in the official regulation. Confidence, plausibility, or asking Claude to repeat the claim is not validation.

### Domain 2 checklist

- Can I score an answer against accuracy and completeness separately?
- Can I distinguish unsupported claims, internal inconsistency, and bias?
- Do I know which primary source can verify each claim type?
- Can I place human review before the consequential action?
- Can I select inline, structured, or artifact output from the use case?

# Domain 3 — Product and Model Selection (12%)

## 3.1 Select appropriate Claude product features

- **Chat:** focused questions, drafting, analysis, and iterative dialogue.
- **Projects:** recurring work that benefits from persistent project instructions and curated knowledge. Chats do not automatically share context unless information is placed in project knowledge. See [Create and manage projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).
- **Research mode:** evidence-heavy, multi-source investigation where current sources and citations matter.
- **Artifacts:** substantial deliverables intended for editing, reuse, or sharing.

Choose the lightest surface that keeps the needed context and produces the right deliverable.

## 3.2 Differentiate between Claude model types

The blueprint uses the stable tier framing:

- **Haiku:** fastest and lowest cost; good for simple, high-volume work inside a proven quality envelope.
- **Sonnet:** balanced capability, speed, and cost; a strong default for most knowledge work.
- **Opus:** highest capability for the hardest reasoning and quality-sensitive tasks, at greater cost and latency.

Exact versions and availability change. Verify what the product currently offers instead of memorizing one model number.

## 3.3 Align model selection with task requirements

Define the quality threshold, latency need, request volume, and cost boundary. Test representative examples on the least expensive model likely to meet the bar. Escalate hard cases rather than routing every request to the largest model.

The official sample asks about high-volume short customer reply drafts. The expected choice is the faster, lower-cost model that meets the task's modest complexity.

## 3.4 Manage context limitations and memory considerations

Every message, file, instruction, and retrieved result uses context. Restart when stale history creates confusion or the task changes. Summarize when continuity matters but full detail does not. Persist stable knowledge in a Project or another approved source of truth.

Project knowledge can switch to retrieval when it grows large; retrieval finds relevant portions rather than loading everything at once. See [RAG for projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects).

Do not use chat history as the only record of an important decision.

# Domain 4 — Workflow Integration and Solution Design (16%)

## 4.1 Analyze requirements and use cases

Map the current workflow before choosing a feature. Identify the outcome, users, inputs, decisions, constraints, risk, systems of record, review points, and success metrics. Separate work Claude can assist from decisions people must own.

## 4.2 Support research, planning, and process optimization

Claude can synthesize evidence, expose dependencies, draft plans, and propose alternatives. People remain responsible for validating sources and choosing actions. Ask for assumptions, missing information, alternatives, and risks to avoid accepting a single polished path too early.

## 4.3 Support solution design, development, and iteration

Use an iterative loop: clarify requirements, generate candidate designs, test against constraints, prototype, collect feedback, and revise. Keep acceptance criteria visible throughout. A design that violates a hard data or policy constraint is not rescued by creativity.

## 4.4 Integrate Claude into existing workflows

Design the whole handoff, not just the prompt. Specify inputs, access, source provenance, error handling, review, approval, output destination, fallback, monitoring, and ownership. Augmentation keeps a person in an existing step; redesign changes the process. Either can be correct when justified by evidence.

## 4.5 Communicate value and limitations to stakeholders

State what was tested, on which cases, with what quality, time, cost, and residual risk. Explain required review and excluded use cases. Avoid claiming universal capability from a small pilot or presenting limitations as reasons to reject every use.

### Domain 4 checklist

- Can I map a process before selecting Claude features?
- Can I identify human-owned decisions and irreversible actions?
- Can I define success with quality, time, cost, and risk measures?
- Can I explain a pilot without hype or false certainty?

# Domain 5 — Configuration and Knowledge Management (12%)

## 5.1 Configure Projects with instructions and knowledge sources

Use project instructions for stable behavior specific to the work: audience, role, evidence rules, tone, formatting, and escalation. Put authoritative reference material in project knowledge with clear filenames and dates. Anything uploaded may be used across chats in that Project.

Keep instructions concise and non-conflicting. A large knowledge base is not automatically a relevant one.

## 5.2 Manage uploaded knowledge and connectors

Connect only approved sources and the minimum permissions required. Check provenance, freshness, ownership, and data classification before upload or connection. A connector expands the accessible surface; the prompt is not an access-control boundary.

Prefer a narrow Drive folder over a broad workspace. Remove stale, duplicated, or superseded files.

## 5.3 Create effective system-level instructions

System or project instructions should express durable rules; task prompts should express the current job. Good instructions are specific, testable, ordered, and clear about uncertainty and escalation. Keep untrusted source content visibly separate from instructions.

## 5.4 Maintain configurations, knowledge sources, and instructions

Assign an owner and a review cadence. Date sources, record changes, remove obsolete documents, and rerun representative tasks after meaningful updates. If a policy changes, updating one prompt while leaving the Project knowledge stale is not maintenance.

# Domain 6 — Governance, Risk, and Responsible Use (15%)

## 6.1 Identify appropriate and inappropriate use cases

Assess impact, reversibility, supervision, and whether the output can be validated. Low-risk drafting with review is a strong fit. Unsupervised decisions about rights, access, employment, credit, health, or safety require much stronger controls and may be inappropriate.

## 6.2 Apply data sensitivity, regulatory, and privacy considerations

Follow purpose limitation and data minimization. Check classification, authorization, approved product, contractual terms, retention, residency, and applicable law. Consumer and commercial products can have different terms; use the policy that governs the actual account and workspace.

The official sample asks about customer names and account numbers that policy classifies as restricted. The correct action is to anonymize or remove identifiers before use, following policy—not to rely on a prompt asking Claude to ignore them.

Anthropic's privacy documentation is product-specific and changes over time; begin with its [Privacy Center](https://privacy.claude.com/).

## 6.3 Follow organizational AI policies and governance standards

Know the approved tools, data classes, reviewers, logging requirements, exception process, and incident path. Organizational policy outranks convenience and cannot be waived by a user instruction. Controls should produce evidence that they operated.

## 6.4 Understand ethical implications

Ethical analysis includes fairness, transparency, autonomy, accessibility, affected stakeholders, and how benefits and harms are distributed. Ask who may be excluded, whether people know AI is involved, how they can challenge a result, and who remains accountable.

### Domain 6 checklist

- Can I classify a use case by impact, reversibility, and reviewability?
- Can I minimize or anonymize sensitive data before use?
- Do I know where policy, approvals, and incident procedures live?
- Can I analyze fairness and transparency beyond minimum compliance?

# Domain 7 — Troubleshooting and Optimization (10%)

## 7.1 Diagnose underperforming prompts or poor outputs

Reproduce the failure and classify it before editing anything. Common causes are:

- unclear task or success criterion;
- missing, stale, or low-quality context;
- conflicting instructions;
- unsuitable feature, model, or output format;
- context overload or contamination from old history;
- a task whose certainty or authority exceeds what Claude can provide.

Change one meaningful variable, then verify against the original criteria.

## 7.2 Adjust approach based on feedback and results

Translate feedback into an observable requirement. Update the smallest relevant layer—task prompt, project instruction, knowledge source, workflow step, or model choice—and test across representative cases. A fix that only memorizes one example is overfitting.

## 7.3 Optimize workflows for efficiency and effectiveness

Measure the baseline before optimizing. Useful levers include removing redundant context, reusing stable Project configuration, selecting a cheaper model that passes the eval, batching similar work, standardizing output formats, and focusing human review where risk is highest.

Optimize quality, time, cost, and operational effort together. Faster wrong work is not efficiency.

# Official sample questions: what they test

The official guide includes one sample each for Domains 2, 3, and 6:

1. **Verify a cited regulation in the official source.** This tests validation, not prompt refinement.
2. **Choose a faster, lower-cost model for high-volume simple drafts.** This tests task-model fit, not “largest model wins.”
3. **Anonymize restricted customer data before use.** This tests policy-based minimization, not whether Claude can technically process the data.

The pattern is consistent: choose the direct control that addresses the actual risk or requirement.

# Four-week study plan

## Week 1 — Prompting and products

- Study Domains 1 and 3.
- Rewrite ten real work requests using the prompt contract.
- Perform one task in chat, one in a Project, and one as an artifact; explain why each surface fits.
- Compare a simple task across available model tiers using the same quality rubric.

## Week 2 — Evaluation and governance

- Spend most time on Domains 2 and 6.
- Fact-check five Claude outputs against primary sources.
- Build a review checklist and identify where approval must occur.
- Map your organization's approved tools, data classes, and escalation path.

## Week 3 — Workflows and knowledge

- Study Domains 4 and 5.
- Map one current business process end to end.
- Configure a Project with curated sources, durable instructions, and representative tests.
- Draft a stakeholder update containing measured value, limitations, and residual risk.

## Week 4 — Troubleshooting and timed practice

- Study Domain 7 and revisit weak objectives.
- Diagnose five deliberately weak prompts without immediately rewriting them.
- Take two timed 60-question practice attempts on different days.
- Review every distractor, then drill weak domains rather than repeating only full exams.

# Exam-day strategy

- Budget two minutes per item, but answer direct governance and product-fit questions faster to preserve time for scenarios.
- For multiple-response items, select exactly the requested number; this practice exam scores them all-or-nothing.
- Translate the scenario into task, constraint, risk, and required control before comparing options.
- Prefer the answer that directly satisfies the stated requirement with the fewest unsupported assumptions.
- Flag difficult items and return after completing the rest.

# Registration and retake policies

The Version 1.0 guide states:

- up to four attempts in a rolling 12-month period;
- waits of 14, then 30, then 90 days after successive failures;
- a fee for each attempt;
- reschedule or cancel at least 24 hours before the appointment or forfeit the fee;
- valid government photo ID matching the registration name;
- accommodations requested before scheduling;
- closed-book, proctored conditions and no copying or recording exam content;
- a free, non-proctored renewal assessment when completed on time; otherwise retake the full exam;
- appeals filed within 14 days.

Confirm current rules in the official guide before registration.

# Practice bank and sources

The local bank contains **770 unique public practice records** collected through the [CertSafari Associate browser interface](https://www.certsafari.com/anthropic/claude-certified-associate-foundations): all 30 objective quizzes plus the public sample pool and its variants. The source site advertised 757 questions; the export is larger because public sample variants add distinct records. All 30 official objectives are represented.

Use the bank to rehearse reasoning and locate weak objectives. Do not treat a third-party answer key as authority; when an answer conflicts with the official guide, Anthropic documentation, or a primary source, follow the authoritative source and report the discrepancy.

## Primary references

- [Official CCAO-F Exam Guide, Version 1.0](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542847%2FClaude+Certified+Associate+%E2%80%93+Foundations+Exam+Guide.pdf)
- [Create and manage Claude Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)
- [RAG for Projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)
- [Artifacts](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them)
- [Anthropic Privacy Center](https://privacy.claude.com/)

**Last reviewed:** October 15, 2026.
