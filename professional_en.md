# Claude Certified Architect - Professional

## Study Guide for Exam CCAR-P

> Based on the [official Professional Exam Guide, version 1.0](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf), effective July 2026. Anthropic marks the guide as subject to change, so confirm the current blueprint before scheduling.

The Professional track tests whether you can own the architecture and lifecycle of a production Claude system. It goes beyond implementation mechanics: you must connect business requirements to technical decisions, defend trade-offs, evaluate quality, manage operational risk, and communicate the design to technical and non-technical stakeholders.

This guide turns the official blueprint into a practical preparation plan. It does not reproduce or predict live exam content.

## Exam at a Glance

| Parameter | Official detail |
|---|---|
| Exam code | **CCAR-P** |
| Items | **63** |
| Formats | Multiple choice and multiple response; each item tells you how many responses to select |
| Time | **120 minutes** |
| Delivery | Proctored online or at a test center, subject to program policy |
| Passing score | **720** on a 100-1,000 scaled score |
| Fee | **$175 USD** |
| Credential validity | **12 months** |
| Score report | Pass/fail, scaled score, and percent correct by domain |

The schedule allows about 1 minute 54 seconds per item. Treat that as a pacing signal, not a target for every question: direct knowledge checks should leave time for architecture scenarios and multiple-response items.

Registration starts on the [Anthropic Partner Academy certification page](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification). Scheduling and delivery then move to Pearson VUE.

## Who the Exam Is For

Anthropic targets mid- to senior-level solution architects, AI/ML engineers, technical leads, and senior software engineers who design end-to-end AI systems. The official candidate profile recommends:

- A strong base in modular software design, scalability, and separation of concerns
- Three or more years in systems architecture or platform engineering
- At least six months operating Claude or a comparable LLM system in production
- Experience taking a system from discovery through deployment and operations

These are recommendations, not prerequisites. Exam performance alone determines certification.

## The Seven-Domain Blueprint

| Domain | Weight | What the exam expects |
|---|---:|---|
| 1. Solution Design & Architecture | **17%** | Turn business needs into an end-to-end Claude architecture and choose suitable workflow, agentic, or augmented-LLM patterns. |
| 2. Claude Models, Prompting & Context Engineering | **13%** | Select models and shape prompts, context, caching, and reusable instructions around quality, latency, and cost. |
| 3. Integration | **19%** | Design secure integrations, RAG pipelines, tool surfaces, protocols, retrieval strategies, and production observability. |
| 4. Evaluation, Testing & Optimization | **16%** | Build mixed-method evaluation systems, diagnose failures, and optimize quality, latency, safety, and cost. |
| 5. Governance, Safety & Risk Management | **14%** | Identify failure modes and apply guardrails, human review, compliance controls, and responsible-AI practices. |
| 6. Stakeholder Communication & Lifecycle Management | **14%** | Lead discovery, explain trade-offs, document decisions, align SLAs, and manage feedback throughout the lifecycle. |
| 7. Developer Productivity & Operational Enablement | **7%** | Configure Claude tooling for teams and improve development, debugging, and operational workflows. |

Integration carries the largest individual weight, but the exam is deliberately broad. Domains 1, 3, and 4 account for 52% together; Domains 5 and 6 add the governance and organizational judgment that separates this track from a purely technical implementation exam.

## Domain Guidance

### 1. Solution Design & Architecture - 17%

Prepare to start with the business outcome, not the model. A sound answer connects users, inputs, data boundaries, processing stages, outputs, feedback, failure handling, and measurable value.

Be able to:

- Decide when deterministic workflow steps are enough and when agentic behavior earns its added cost and risk
- Break a complex task into bounded components with explicit contracts and ownership
- Design coordinator-worker and specialist-agent patterns without creating unnecessary orchestration
- Trace an end-to-end request through ingestion, model calls, tools, validation, delivery, and feedback
- Express trade-offs against service levels for quality, latency, reliability, throughput, and cost

**Practice artifact:** draw one production architecture and annotate every boundary with its trust level, failure mode, fallback, owner, and observable signal.

### 2. Claude Models, Prompting & Context Engineering - 13%

Model choice is a system decision. Match capability, speed, and cost to the work instead of defaulting every stage to the same model.

Be able to:

- Route tasks by complexity and risk, with a clear reason for each model choice
- Separate stable instructions from dynamic user and retrieved content
- Use zero-shot and few-shot prompting where each is justified
- Design structured system prompts, reusable templates, Skills, and guardrails
- Reduce repeated input cost with prompt caching and modular prompt design
- Control context growth through retrieval, summarization, compaction, and selective history

**Practice artifact:** create a model-routing table that states the task class, chosen model, fallback, quality threshold, latency budget, and cost ceiling.

### 3. Integration - 19%

Integration is the highest-weighted domain. Expect to reason about more than whether a connection works: the exam emphasizes capability scope, authorization, retrieval quality, latency, observability, and protocol choice.

Be able to:

- Remove tools an agent does not need instead of relying only on instructions or confirmations
- Keep authentication, authorization, tenant isolation, and auditability distinct
- Choose among direct APIs, MCP, CLI integration, and agent-to-agent communication
- Design RAG ingestion, chunking, indexing, metadata, retrieval, reranking, and freshness controls around the data shape and query pattern
- Expose capabilities progressively so the model does not carry a monolithic tool or context catalog
- Instrument the path across model calls, retrieval, tools, queues, and downstream services

**Practice artifact:** threat-model a tool-enabled RAG system, then explain how you would detect stale retrieval, excessive tool scope, cross-tenant access, and downstream timeouts.

### 4. Evaluation, Testing & Optimization - 16%

Evaluation should tell you whether the system is fit for its business purpose, why it failed, and whether a change improved the right thing without damaging another dimension.

Be able to:

- Define metrics for task quality, safety, security, latency, reliability, and cost
- Combine curated cases, production samples, regression sets, human review, and model-based grading
- Segment results by use case, risk tier, language, customer group, and failure type
- Diagnose whether a failure comes from prompts, retrieval, tools, orchestration, model fit, or data
- Run controlled comparisons and make iterative changes with explicit acceptance thresholds
- Monitor drift and operational behavior after deployment

**Practice artifact:** build an evaluation matrix with representative, edge, adversarial, and regression cases. For every metric, name the decision it informs.

### 5. Governance, Safety & Risk Management - 14%

Treat safety and compliance as architecture inputs. A policy statement is not a control until the system enforces it and produces evidence.

Be able to:

- Identify misuse, hallucination, privacy, security, bias, and automation risks
- Place preventive, detective, and corrective controls at the right system boundary
- Use human review where impact, uncertainty, or regulation demands it
- Connect requirements such as GDPR, HIPAA, or FedRAMP to data handling, access, logging, retention, and deployment choices
- Explain residual risk and who accepts it

**Practice artifact:** create a risk register with likelihood, impact, control, evidence, owner, residual risk, and review cadence.

### 6. Stakeholder Communication & Lifecycle Management - 14%

Professional architects must discover the real problem and make decisions legible. The strongest technical design can still fail when requirements, ownership, rollout, or expectations remain implicit.

Be able to:

- Turn stakeholder goals into prioritized functional and non-functional requirements
- Surface assumptions, conflicts, dependencies, and decision owners during discovery
- Explain architectural choices in terms of business value and operational consequences
- Record trade-offs in architecture decision records and implementation guidance
- Define feedback loops, handoff criteria, service levels, monitoring, and iteration plans

**Practice artifact:** present the same architecture twice: a five-minute executive version centered on value and risk, and a technical version centered on interfaces, controls, and operations.

### 7. Developer Productivity & Operational Enablement - 7%

This smaller domain checks whether teams can use and operate the architecture effectively.

Be able to:

- Configure Claude Code and related tooling with shared project guidance and bounded permissions
- Standardize repeatable development workflows without hiding important decisions
- Use AI-assisted tooling for code exploration, implementation, tests, debugging, and incident investigation
- Design adoption, support, and troubleshooting paths for a team

**Practice artifact:** define a team rollout for Claude tooling that covers configuration ownership, access, review gates, usage guidance, telemetry, and support.

## A Four-Phase Preparation Plan

### Phase 1: Map your gaps

Copy the seven domains into a scorecard. Rate every domain from 0 to 3:

- **0 - unfamiliar:** you cannot explain the objective
- **1 - conceptual:** you can explain it but have not applied it
- **2 - practiced:** you have built or reviewed it with guidance
- **3 - defensible:** you can choose among alternatives and explain the evidence

Calculate `(3 - rating) × domain weight` for each domain. Use the result to prioritize study time instead of reading every topic equally.

### Phase 2: Build one reference system

Build or deeply review one end-to-end Claude solution that includes:

- A measurable business outcome and explicit non-functional requirements
- Model selection and prompt/context strategy
- Tool use or RAG with authentication and authorization
- Automated evaluation and human review
- Logging, tracing, dashboards, and operational alerts
- Safety, privacy, compliance, and rollback controls
- Architecture decisions and a stakeholder handoff

One coherent system exposes cross-domain trade-offs better than seven disconnected demos.

### Phase 3: Rehearse decisions

For each major design choice, practice this sequence:

1. State the requirement and constraints.
2. Name two or three viable options.
3. Compare quality, latency, cost, security, operability, and maintainability.
4. Choose one option and explain the evidence that would invalidate it.
5. Describe monitoring, fallback, and ownership.

This mirrors the judgment the Professional blueprint rewards.

### Phase 4: Run timed scenarios

Practice mixed architecture questions under the 120-minute limit. Include multiple-response items and force yourself to verify the requested number of selections. Review misses by failure type, not just topic: overlooked constraint, weak trade-off, unsafe default, confused metric, or incomplete lifecycle thinking.

## Exam Decision Framework

When several options look plausible, prefer the answer that:

1. Solves the stated business requirement and respects every explicit constraint.
2. Uses the least complex architecture that meets the need.
3. Removes unnecessary capability and privilege at the source.
4. Produces measurable evidence through evaluation and observability.
5. Handles failure, fallback, human review, and ownership explicitly.
6. Makes cost, latency, quality, security, and maintainability trade-offs visible.

Avoid answers that rely on a larger model to solve an authorization or architecture problem, add monitoring without reducing avoidable risk, optimize one metric while ignoring the stated service level, or introduce agentic complexity without a clear benefit.

## Readiness Checklist

You are ready when you can do all of the following without notes:

- Sketch and defend an end-to-end Claude architecture from a short business scenario
- Choose workflow, agentic, RAG, and direct-model patterns based on constraints
- Explain model routing, prompt reuse, caching, and context-management trade-offs
- Design least-privilege tools and secure authentication and authorization boundaries
- Diagnose retrieval, prompt, model, tool, and orchestration failures separately
- Define evaluation data and metrics that drive a release decision
- Map major safety and compliance risks to enforceable controls and evidence
- Communicate the same decision to executives, engineers, security, and operations
- Define rollout, monitoring, incident, feedback, iteration, and ownership plans
- Complete 63 mixed-format practice items within 120 minutes

## Official Resources

- [Claude Certified Architect - Professional Exam Guide (PDF)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf)
- [Professional certification registration page](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification)
- [Claude API documentation](https://platform.claude.com/docs/en/api/overview)
- [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code documentation](https://code.claude.com/docs/en/overview)

Review the official exam guide again before registration. It contains the current policies for identification, accommodations, retakes, rescheduling, exam conduct, confidentiality, renewal, support, and appeals.
