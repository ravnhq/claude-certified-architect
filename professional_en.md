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
| Credential validity | **12 months** from the date the credential is awarded |
| Prerequisites | **None.** The credential is awarded on exam performance alone |
| Score report | Pass/fail, scaled score, and percent correct by domain |

The schedule allows about 1 minute 54 seconds per item. Treat that as a pacing signal, not a target for every question: direct knowledge checks should leave time for architecture scenarios and multiple-response items.

Registration starts on the [Anthropic Partner Academy certification page](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification). Scheduling and delivery then move to Pearson VUE.

### Scoring

The exam is **criterion-referenced**: you are measured against a fixed performance standard, not against other candidates. The 720 cut score came from a formal standard-setting study in which subject-matter experts judged the performance expected of a minimally qualified candidate.

The score report shows percent correct per domain. Those **section percentages do not determine pass or fail** — only the total scaled score does. Use them to direct a retake, not to predict one.

### Policies worth knowing before you register

| Policy | Detail |
|---|---|
| Eligibility | Employees of Claude Partner Network organizations, registering with a recognized company email domain. Personal email addresses are rejected; adding a domain takes 7-10 days |
| Attempts | Up to **4 per rolling 12-month period**, at full fee each time |
| Retake waits | **14 days** after a first failure, **30 days** after a second, **90 days** after a third |
| Delivery | Pearson VUE, online proctored or at a test center; **closed book** |
| Time on site | About **135 minutes** including check-in, for a 120-minute exam |
| Language | **English only.** Browser translation tools are prohibited during proctored testing |
| Accommodations | Request through Pearson at least **10 days** before your exam date |
| Reschedule | Free up to **24 hours** before the appointment; changes inside 24 hours forfeit the fee |
| Results | Scaled score shown immediately; Credly badge invitation follows within minutes for online delivery |
| Renewal | Review what changed and complete a complimentary **non-proctored** assessment |

Corporate networks must allow Pearson's domains for online proctoring. If your device is locked down, a test center is the safer choice.

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

Take these seven domains from the official exam guide only. Published prep pages describe the Architect exam as five domains and 60 questions, which is the Foundations shape, not the seven-domain 63-item Professional blueprint — never let an outside blueprint replace this one.

Integration carries the largest individual weight, but the exam is deliberately broad. Domains 1, 3, and 4 account for 52% together; Domains 5 and 6 add the governance and organizational judgment that separates this track from a purely technical implementation exam.

## Domain Guidance

### 1. Solution Design & Architecture - 17%

**Official objectives.** Exam items are written against these six task statements:

1. Translate business problems into Claude-based AI solutions
2. Design end-to-end architectures (input → processing → output → feedback loops)
3. Select appropriate architectural patterns (workflow, agentic, augmented LLM)
4. Design multi-agent systems and orchestration strategies
5. Apply decomposition techniques for complex problem solving
6. Align solutions to business value pillars (efficiency, transformation, productivity, cost, performance SLAs)

Prepare to start with the business outcome, not the model. A sound answer connects users, inputs, data boundaries, processing stages, outputs, feedback, failure handling, and measurable value.

**Decomposition comes before architecture.** Split the request three ways before choosing anything: work that suits language understanding, planning, drafting, or tool-mediated action; work an existing system already does reliably; and work a person must retain. Over-assigning to the model is the most expensive early mistake, because it is also the easiest one to defend in a demo.

Justify each assignment on three questions — can a wrong call be undone, what does a wrong call cost, and who has to answer for it. The classic error is handing a deterministic business rule to a probabilistic system. A threshold that must hold on every case, enforced by something that holds on most cases, fails on the untidy inputs nobody thought to test, produces no error signal, and surfaces in an audit rather than in monitoring.

**Choose the pattern by elimination, not by preference.** Three shapes sit on one spectrum: a single augmented call, a workflow whose control flow lives in your code, and an agent whose control flow lives inside the model. Walk five factors in order and let the first one that rules a shape out decide.

1. **Predictability.** Can the steps be enumerated in advance? If yes, an agent is paying for flexibility you will not use.
2. **Error cost.** A retry, an audit finding, or a lawsuit? Deterministic guards can only sit between steps you wrote.
3. **Observability.** Can operations reconstruct what happened? A workflow logs like ordinary software. With an agent, the trajectory *is* the control flow, and most tooling was never built to raise alerts on one.
4. **Latency budget.** An agent's runtime has no natural ceiling, so budget the worst case rather than the median.
5. **Cost.** Iterative reasoning, retries, and accumulating context add up. What actually drives cost is context growth and call count, not the pattern label — a careless workflow can outspend a disciplined agent.

Within a workflow, pick the sub-shape by how the steps relate: chain them when each stage consumes the last one's output; route them when inputs differ in kind and need different handling; run them in parallel when the sub-tasks are genuinely independent; and add a generate-then-critique loop when quality is verifiable but one pass is not reliable enough. Most production systems combine more than one.

Choosing an agent because the work "feels open-ended" is not the same as being unable to write the steps down. Teams that mine their traces often find a handful of recurring paths — a router and a few chains, rebuilt expensively inside a loop, minus the logging an auditor will eventually ask for.

**Multi-agent systems fail asymmetrically.** A coordinator owns the goal, decomposes the work, and synthesizes; workers each carry one scoped unit in their own context. Reach for this only when the work genuinely exceeds a single context, because every added agent is another boundary to observe and govern.

| Failure | Recoverable? | Design response |
|---|---|---|
| A worker returns nothing, or something malformed | Yes, at the worker boundary | Check every returned result; retry the unit or send it elsewhere, and record the gap rather than dropping it |
| Two workers disagree | Yes, at synthesis | Give the coordinator an explicit tie-breaking rule, or send the disagreement to a person |
| The coordinator loses track of the goal, or of what it has already merged | Usually not | Protect and checkpoint coordinator state so a failed run resumes rather than restarts |
| Traces fragment across roles | Cross-cutting | Propagate one trace identifier so a single run reconstructs end to end |

The dangerous failure is silent: results come back for most units, the coordinator summarizes confidently, and the fluency of the summary hides the missing work. Reconcile coverage at synthesis: the number of completed units must match the number dispatched, and any shortfall is raised before the summary reaches a reader.

**Human checkpoints belong in the orchestration design**, not bolted on afterwards. Gate before any irreversible or high-consequence action; sample the rest. Domain 5 covers how to set that routing rule.

**Reference architectures carry known failure modes.** Treat them as shapes to adapt rather than blueprints to copy, and know where each one breaks:

- **Tool-using agent** — unbounded autonomy: state-changing tools with no turn limit, no review gate, and no measure of whether the goal was met.
- **Retrieval over a stable corpus** — asked to answer questions about live state, where the index is a snapshot and the answer is confidently stale.
- **Document processing with a verification pass** — no exception path, so low-confidence extractions flow through the same route as clean ones.
- **Classify-then-route** — retrieval standing in for a transactional lookup, no escalation path to a person, or an agent variant shipped before the simpler routed version was measured.
- **Coding agent** — edits and commits with no human gate, and no regression set per language or framework.

Combine two patterns when two parts of the problem break in different ways. Reaching for a second pattern because the problem itself is still undefined defers a decision rather than applying one.

**Feasibility is a verdict plus the constraint that makes it true.** Three outcomes are defensible: feasible as scoped; feasible only under stated constraints; or not feasible at all. A constrained verdict must name the boundary condition explicitly — the input size, the refresh cadence, the review gate — because an undocumented constraint becomes an infeasible system the moment production violates it. A well-argued "not feasible" is the cheapest finding in the project.

**Tie the design to the value pillars.** Efficiency, transformation, productivity, solution cost, and performance service levels are the language the blueprint and the budget holder share. Build the case as a comparison: the baseline measured in a unit the business already tracks, the projected state in the same unit, minus the run cost from your own sizing model, expressed as a payback period with sensitivity. Three errors recur — a baseline estimated rather than measured, a projection that models full automation while the design still routes work to a reviewer, and a run cost taken from an average when the input distribution has a heavy tail.

Be able to:

- Decide when deterministic workflow steps are enough and when agentic behavior earns its added cost and risk
- Break a complex task into bounded components with explicit contracts and ownership
- Design coordinator-worker and specialist-agent patterns without creating unnecessary orchestration
- Trace an end-to-end request through ingestion, model calls, tools, validation, delivery, and feedback
- Express trade-offs against service levels for quality, latency, reliability, throughput, and cost

**Practice artifact:** draw one production architecture and annotate every boundary with its trust level, failure mode, fallback, owner, and observable signal.

### 2. Claude Models, Prompting & Context Engineering - 13%

**Official objectives.** Exam items are written against these five task statements:

1. Select appropriate Claude models based on trade-offs
2. Design system prompts, templates, and guardrails
3. Apply prompt engineering techniques (zero-shot, few-shot, chain-of-thought)
4. Optimize context windows and manage token usage
5. Implement prompt reuse strategies (caching, modular prompts, Skills)

Model choice is a system decision. Match capability, speed, and cost to the work instead of defaulting every stage to the same model.

**Start at the balanced tier and move on evidence.** Move up only when an evaluation says the default misses your quality bar, and down only when an evaluation confirms the trade is acceptable for that specific task. Declining to choose is itself a choice, and it defaults to the most expensive option at every step — usually discovered weeks after launch, when the conversation has moved from design into change management. Per-step routing only becomes possible when per-step evaluations exist.

**Treat a model swap as a release.** Three things must be in place: a curated set covering the real distribution of work, a grading function, and a rollback threshold agreed *before* the run. Setting the threshold afterwards is writing the acceptance criteria to match the result. The payoff is more than a pass or a fail. Results broken out by input type frequently expose a partial migration that one averaged number conceals — send the classes that regressed to the stronger model and route the rest to the cheaper one.

**Keep four context mechanisms distinct.** The context window is the model's active attention space and resets between calls. Retrieval fetches external knowledge at query time and augments that window. Persistent application state lives in your systems and needs a tool call. Memory and summaries are continuity your application stores and passes back in. Conflating them is where context designs go wrong.

Then choose how context reaches each call. The four strategies below are poles for teaching; production systems layer them.

| Strategy | Earns its place when | Breaks down when |
|---|---|---|
| Load everything up front | Input size is bounded and predictable, and a stable prefix can be cached | Context accumulates turn over turn; attention quality can degrade well before the hard limit |
| Carry recent state forward | Multi-turn dialogue, agent loops, staged workflows with narrow handoffs | Decisions depend on detail dropped earlier; caching is harder when the prefix mutates |
| Fetch just in time | The corpus exceeds any window, changes faster than redeploys, or citations are required | Synthesis spans many documents, or the right one never reaches the top results |
| Compact into summaries | Long sessions where keeping every turn is wasteful yet recent state still matters | Summaries drop load-bearing detail — identifiers, values, prior decisions — and the loss is one-way |

Ask four separate questions: what the model needs at the start, what it needs from recent steps, what it might fetch on demand, and what earlier material compresses without losing decision-relevant detail. Sizing the window and choosing the strategy are related decisions, not the same one, and the window is a ceiling rather than a target: size it for the largest conversation you actually expect, then add retrieval, the system prompt, and headroom.

**Extended reasoning is a measured decision.** It bills tokens and adds latency on every call where it is engaged. Run the evaluation without it, work on the prompt first, and turn it on when a measured accuracy gap justifies the cost — not on the assumption that more thinking cannot hurt. Enabling it on a step that does no reasoning, such as a classifier, is a recurring tax for nothing.

**A reused prompt is an asset with structure.** At scale it needs a stated role and scope, the constraints it must hold, and an output contract naming the shape of the response. The skill worth practicing is spotting what a prompt leaves unsaid. Wherever it is silent, the model improvises, and differently each time. A well-built template makes the guarded path the path of least resistance — the fixed scaffolding carries the guarantees, and filling a slot cannot remove a constraint. A guardrail written as one more line of role description can be drifted past. The same rule expressed as a structural requirement of the output cannot be quietly skipped.

**Use the lightest technique that clears the bar.** Start with instruction alone. Add examples when showing the desired shape is easier than specifying it. Add explicit step-by-step reasoning only when the path genuinely determines the answer. Each step costs tokens and latency on every call. Note that identical wording does not produce identical behavior across tiers or generations — a prompt tuned on one model is a draft for the next rather than a finished artifact, which is a further reason a swap is gated by evaluation. Watch for bias introduced by construction: leading phrasing, an example set drawn from one kind of case, and instructions that presume the answer they are supposed to elicit. No single output reveals that skew; it shows up only across many.

**Caching is a prefix decision.** The saving depends on an unchanging prefix that is identical byte for byte across requests, so the fixed content goes first and the per-request content last. Putting the variable content at the top means the prefix changes every time and the cache never hits — the mechanism is ordering, not configuration. Where the cached content must reflect live state, caching introduces a consistency window that may disqualify it.

**Reuse across a team is a governance choice.** A shared prompt library suits fragments engineers assemble and tweak inside one codebase. A versioned, self-contained package suits a stable procedure that runs the same way every time, travels across teams or products, and needs approval and rollback. Ungoverned prompts copied between teams drift into many slightly different versions, each behaving slightly differently.

Be able to:

- Route tasks by complexity and risk, with a clear reason for each model choice
- Separate stable instructions from dynamic user and retrieved content
- Use zero-shot and few-shot prompting where each is justified
- Design structured system prompts, reusable templates, Skills, and guardrails
- Reduce repeated input cost with prompt caching and modular prompt design
- Control context growth through retrieval, summarization, compaction, and selective history

**Practice artifact:** create a model-routing table that states the task class, chosen model, fallback, quality threshold, latency budget, and cost ceiling.

### 3. Integration - 19%

**Official objectives.** Exam items are written against these eight task statements:

1. Evaluate tool/agent configuration for capability bloat
2. Analyze authentication and authorization requirements to identify security gaps
3. Evaluate accuracy-latency trade-offs and justify configuration decisions
4. Analyze observability challenges and select monitoring strategies at scale
5. Design a RAG pipeline with appropriate chunking and indexing strategies
6. Apply retrieval strategies matched to data shape and query pattern
7. Evaluate connection protocols and select the appropriate integration mechanism (MCP, API/CLI, agent-to-agent)
8. Evaluate progressive discovery vs. monolithic context strategy

Integration is the highest-weighted domain, and it carries the most objectives. Expect to reason about more than whether a connection works: the exam emphasizes capability scope, authorization, retrieval quality, latency, observability, and protocol choice.

**Hold three connection decisions apart.** Blurred vocabulary produces muddled integration answers. An *entry point* is what a person or a system touches. A *build-time interface* is what your engineers write code against. A *delivery route* is where the request terminates and whose contract covers it. Every deployment involves all three, and settling one layer seldom settles the other two.

| Layer | The question it answers | What decides it |
|---|---|---|
| Entry point | Who talks to the system, and what may they reach? | The user and the shape of the work |
| Build-time interface | What does our code call? | Team skills, breadth of reuse, whether the model must act across turns |
| Delivery route | Whose infrastructure and contract carries the traffic? | Cloud commitments, region rules, audit posture, procurement |

Each layer is negotiated with a different stakeholder, so a strong answer names which layer the question is actually about before it recommends anything.

**Eliminate on constraint, then optimize on preference.** A governing obligation — a privacy regime, a residency rule, an authorization level, an approved-vendor list — removes options before cost, ergonomics, or build effort are worth discussing. An answer that picks the cheapest or fastest route and checks compliance afterwards has the order backwards. When a stem names a regulation, the discriminator is usually that one option was already ruled out.

**Protocol choice turns on reuse, not familiarity.** Work down this list and stop at the first fit:

- A direct API call or a language SDK when one product owns the integration. The SDK is the default; drop to raw HTTP only for a capability it has not exposed yet.
- A shared tool protocol when the *same* tool surface must be reachable from more than one client. Reuse across clients is what pays for the extra layer.
- A managed agent runtime when the model must iterate over tools inside your own application and you do not want to own the loop.
- A coding-agent entry point only when the user is an engineer working in a repository.

The failure to recognize is a protocol carried forward out of habit from the last project. A shared protocol layer with exactly one client buys integration cost and no reuse. The mirror-image failure is placing a developer-facing surface in front of users who are not developers, on the grounds that the underlying model is the same.

**Retrieval design follows the corpus shape and the query pattern.** Neither is a default you can carry between projects.

| What you observe | Design response | What it costs |
|---|---|---|
| Section-numbered contracts, manuals, or policies | Preserve document structure and retrieve at the level that answers the question | Ingestion complexity; the structure must parse reliably |
| Long-form prose with no structural anchors | Split on meaning boundaries so each retrieved unit stands alone | Variable unit sizes complicate context budgeting |
| Homogeneous text with weak natural boundaries | Uniform spans with overlap | Arguments and tables get cut mid-idea |
| Queries that hinge on identifiers, codes, or citations | Keyword matching | Paraphrased questions miss |
| Queries phrased differently from the source | Semantic matching | Exact-token lookups miss |
| Both query kinds in one system, which is the usual case | Run both and merge the ranked lists with a standard rank-fusion rule | More retrieval compute and latency on every request |

Every retrieval design trades three things against each other: whether the right unit comes back, what retrieval adds to each request, and what the pipeline costs to keep accurate as the corpus expands. No setting is universally correct. There is only the one you can defend for this corpus and these queries.

**Retrieval is for knowledge that holds still.** Anything whose current value is owned by another system needs a tool call, not an index lookup. The symptoms are recognizable: answers that contradict the database, results that shift with each refresh, staleness no embedding upgrade repairs. Expect stems where the data changes independently of the index and the credited answer calls the system of record.

**Expose capability progressively.** A monolithic tool catalog or a preloaded corpus costs tokens on every request, degrades selection accuracy as the catalog grows, and enlarges the space of actions you never tested. Stage what the model can see and reach, and let the next step pull what it needs.

**Five layers decide whether an enterprise integration survives review.**

| Layer | The architect's decision | What breaks when it is wrong |
|---|---|---|
| Compliance | Which routes and surfaces remain permitted once the obligation applies | The design passes engineering review and fails legal review, after the build is paid for |
| Identity | Where authentication happens relative to the model call | A user asserts a role inside their own message and the system believes it |
| Authorization | Which capabilities and data this role may reach | The model becomes a path around the access policy the underlying systems enforce |
| Data handling | Which fields genuinely need to enter the context window | Sensitive values land in your own request logs and surface at the next audit |
| Observability | What you must be able to reconstruct afterwards | An unlogged path is an uninvestigable one |

**Where integrations go wrong**

- Identity supplied by the user instead of injected by the server after authentication.
- Fields passed because they were convenient. Necessity is the filter: if the language task does not need the value, a reference identifier usually suffices.
- One shared API key across tenants, so a rate-limit breach cannot be attributed and every tenant absorbs it.
- Tools kept because removal felt like scope reduction. Audit the tool set the way you audit permissions and record why each removal was safe.
- Reliability controls placed at the wrong layer. Retries sit beside the call itself, circuit breakers guard the service boundary, and fallback routing belongs with orchestration.
- Observability deferred to after launch. Security reviewers increasingly treat an agent action that produces no audit record as an action that cannot be permitted at all.

Be able to:

- Remove tools an agent does not need instead of relying only on instructions or confirmations
- Keep authentication, authorization, tenant isolation, and auditability distinct
- Choose among direct APIs, MCP, CLI integration, and agent-to-agent communication
- Design RAG ingestion, chunking, indexing, metadata, retrieval, reranking, and freshness controls around the data shape and query pattern
- Expose capabilities progressively so the model does not carry a monolithic tool or context catalog
- Instrument the path across model calls, retrieval, tools, queues, and downstream services

**Practice artifact:** threat-model a tool-enabled RAG system, then explain how you would detect stale retrieval, excessive tool scope, cross-tenant access, and downstream timeouts.

### 4. Evaluation, Testing & Optimization - 16%

**Official objectives.** Exam items are written against these six task statements:

1. Define evaluation metrics (accuracy, latency, cost, safety, security)
2. Design evaluation datasets and test frameworks using mixed methodologies
3. Conduct A/B testing and iterative improvements
4. Diagnose system issues (prompt failure, hallucinations, model mismatch)
5. Optimize token usage, latency, and cost-performance trade-offs
6. Monitor system performance using logging and observability tools

Evaluation should tell you whether the system is fit for its business purpose, why it failed, and whether a change improved the right thing without damaging another dimension.

**Write the evaluation before the production code.** Doing it first forces three things that are otherwise deferred indefinitely: a measurable definition of success, an early confrontation with design assumptions while changing them is still cheap, and a gate that can judge every later change. A behavior you cannot write an evaluation for is a behavior you cannot claim the system has.

The workflow runs in stages, and each stage produces the input to the next: define the behavior and its pass criteria, build a labeled dataset that matches the input distribution you will actually see, run automated checks, score the interpretive cases with a judge, then read the results per category rather than in aggregate.

**Grade at the cheapest reliable level.** Climb only when the behavior forces you to.

| Method | Use it for | Its limit |
|---|---|---|
| Code-based check | Anything unambiguous: schema, exact match, numeric threshold, presence of a required field, comparison against an authoritative value | Cannot judge tone, reasoning quality, or edge-case appropriateness |
| Model-based judge | Behaviors needing interpretation: faithfulness, instruction following, policy compliance, handling of ambiguous input | Inconsistent on borderline cases, and one model call per item |
| Human review | High-stakes or novel behaviors with no trusted rubric yet, and calibration of the judge itself | Slowest and least scalable; viable only on samples |

Two rules make the ladder work. A judge has failure modes of its own, so calibrate it against human-labeled outputs and grade using a model other than the one being tested. And prefer breadth: many cheap automatically graded cases catch more regressions than a handful of meticulously built ones, because the cheap set can run on every change.

Watch for the common misgrade in exam scenarios. A high-stakes check is not automatically an interpretive one. Whether a prohibited action was taken is binary, and whether a summary invents facts is not. Stakes decide how much you care; ambiguity decides the method.

**Turn a business requirement into a threshold.** "Summarize accurately" is not measurable. Name the specific behavior, set the passing number from the business requirement rather than from whatever the prototype happened to score, enumerate the failure modes as dataset categories, and include adversarial and malformed inputs. A dataset built only from clean examples produces scores that do not predict production.

**A stale evaluation suite is worse than none.** It reports stable scores while measuring behavior the system no longer produces. Update the dataset whenever the prompt, retrieval strategy, or model changes. Single-turn sets also say nothing about conversation: multi-turn behavior needs its own dataset of full transcripts.

**Diagnose the failure class before proposing a fix.** These four are separable, and the exam rewards separating them.

| Failure class | What you see | Where the fix lives |
|---|---|---|
| Prompt failure | The instruction was ambiguous and the model filled the gap its own way | The prompt, not the model |
| Hallucination | Fluent, confident content with no basis in the input or any cited source | Grounding: retrieval, tool calls, verification. No amount of stronger wording fixes it |
| Model mismatch | The tier does not fit the work, or it changed without anyone re-measuring | Model selection, gated by an evaluation |
| Orchestration failure | A subagent dropped work, or a coordinator lost its thread | Failure boundaries and a trace that spans both roles |

When a metric moves, attribute the cause before acting. Model drift means behavior changed on stable inputs. Data drift means the input distribution changed. A model update means the version changed underneath you. The three have different fixes, and confusing them produces the wrong one.

**Design experiments that can be believed.** Four elements must exist before the run, not after:

1. A falsifiable hypothesis naming the treatment, the expected direction, and the constraint on secondary metrics.
2. Random assignment that stays consistent per user or session.
3. One primary metric chosen in advance. Choosing it afterwards is outcome-shopping.
4. A sample size computed from the effect you want to detect. Model outputs vary more than deterministic ones, so the required sample is larger than intuition suggests.

Then read the result honestly. Statistical significance and practical significance are different questions, and a win on the primary metric that degrades cost or latency may not be a win at all. Watch for interaction effects: a change that helps typical inputs can hurt an edge case that is rare during the test window and common in a seasonal peak.

**Shadow testing is the alternative when exposure is unacceptable.** Run the candidate on a copy of live traffic, serve everyone the current version, and score the shadow outputs offline. You give up downstream behavioral signal, because no user ever sees the new response. You gain a deployment decision made before anyone is exposed — often the only permissible option in a regulated deployment, and the right one when a single bad output is too costly or traffic is too thin for a live split.

**Optimize against the tail, not the average.** Median latency is not what breaches a service level; the slow end is. Token distributions are usually skewed, so a cost model built on an average can understate spend by a wide margin. Aggregate dashboards can look healthy while a small share of requests consumes most of the budget and produces most of the wrong answers, which is why per-request decomposition sits alongside the aggregate view.

Be able to:

- Define metrics for task quality, safety, security, latency, reliability, and cost
- Combine curated cases, production samples, regression sets, human review, and model-based grading
- Segment results by use case, risk tier, language, customer group, and failure type
- Diagnose whether a failure comes from prompts, retrieval, tools, orchestration, model fit, or data
- Run controlled comparisons and make iterative changes with explicit acceptance thresholds
- Monitor drift and operational behavior after deployment

**Practice artifact:** build an evaluation matrix with representative, edge, adversarial, and regression cases. For every metric, name the decision it informs.

### 5. Governance, Safety & Risk Management - 14%

**Official objectives.** Exam items are written against these five task statements:

1. Implement guardrails and safety controls
2. Identify risks, limitations, and failure modes of LLM systems
3. Apply human-in-the-loop validation strategies
4. Ensure compliance with regulations (e.g., GDPR, HIPAA, FedRAMP)
5. Address ethical AI considerations (bias, fairness, transparency)

Treat safety and compliance as architecture inputs. A policy statement is not a control until the system enforces it and produces evidence.

**Draw the alignment boundary explicitly.** Training reduces broad classes of harmful output for every request, without configuration. It never saw this deployment's own policy, its rules for handling data, or its access model. A request can sit comfortably inside general safety behavior and still violate a rule specific to this system — disclosing another business unit's record, advising outside an approved script. The most dangerous safety failure is a quiet one: a rule everybody believes is being enforced that exists in no layer at all. Nothing can enforce a policy it was never handed.

Read the stack as four layers, each covering what the one below cannot:

| Layer | Reliably covers | Blind spot | Owner |
|---|---|---|---|
| Trained behavior | Broad harm classes, on every request | Your domain policy, data rules, authorization model | The model provider |
| System instructions | Role, tone, and stated constraints inside one request | Anything an adversarial input talks the model out of; instructions are not enforcement | You |
| Screening | Disallowed content on the way in and on the way out | Actions with side effects, and novel attacks a classifier misses | You |
| Action authorization | Whether *this* caller may take *this* action now | Content quality and fairness | You |

**Name the risk categories, then walk the paths.** Direct prompt injection overrides your instructions from user input. Indirect injection arrives through retrieved documents and tool responses that the model treats as trustworthy — the dominant vector wherever retrieval or tools exist, and the one input screening alone never sees. Token-budget exhaustion truncates work or inflates cost through oversized input. Tool and action abuse induces a side-effecting call outside policy. Data exposure puts sensitive fields into the context window or the logs regardless of how the model behaves. Walk the request path and the data path together, and at every entry point ask what an attacker could attempt there and which control would stop them.

**Three control points, three different questions.** Input screening decides whether a request reaches the model. Output screening decides whether a response reaches the user. Action authorization decides whether a side-effecting call may run. One filter sitting at the far end of the path covers exactly one of these, and it sits downstream of the only step that cannot be undone. Expect at least one exam scenario built on that gap.

Choose the check type by the question, not by the stakes. Screening for fuzzy intent needs a model-based classifier because the patterns cannot be enumerated. Crisp rules — formats, blocklists, schemas, known strings — belong in deterministic code, which is faster and cannot be argued with. Authorization should be deterministic almost without exception, because it must be provable and replayable: an allowlist plus identity and scope. Because a classifier can be evaded and a rule can be brittle, chain them and know what each one misses.

**Decide the failure direction deliberately.** A screening service that errors and passes traffic through gives you the appearance of protection with none of its function. If you have not chosen, the surrounding code chooses for you, and that default nearly always resolves toward passing the request on. Where an unscreened request would cause harm, fail closed. This applies to the controls your team builds and operates.

**Audit reusable capability before you trust it.** A packaged, distributable procedure is a supply-chain surface: the risk arrives in the bundle, upstream of anything your conversation-level screening watches. Read it for calls that do not match its stated purpose — network requests, shell execution, filesystem access, credential reads — and treat that stated purpose as the audit baseline. Then run it with least privilege in a sandbox anyway, because a clean bundle can still fetch code at runtime. End every audit in a recorded verdict of approve, reject, or remediate, and restrict where such packages may come from at all.

**Unequal outcomes enter at points you own.** Fairness is not a property that arrives with the model. Four points are yours to instrument: a retrieval corpus that over- or under-represents groups, prompt framing that encodes an assumption, few-shot examples carrying the same skew, and downstream routing that sends some groups along different paths. An aggregate outcome metric can look healthy while harm concentrates in one subgroup.

Transparency then depends on who is asking. An affected person needs the driving inputs and the reason, phrased so they can act on it. A regulator needs evidence that comparable cases were treated comparably and that one decision can be reconstructed on demand. Your own team needs the full trace. All three draw on the same decision-level logging — the inputs, the retrieved context, the output, and every routing step — governed differently. That log falls inside the compliance register too: minimize it, bound its retention, and control who can read it.

**Route to human review by stakes, not by volume.** Two things set the stakes: how easily a mistake can be undone, and what it costs when it is not. Confidence estimates how likely this particular output is to be wrong, which decides how much of that volume you can safely let through — and it is only useful to the degree it is calibrated. When the signals disagree, weight reversibility and cost.

| Placement | What it buys | What it costs |
|---|---|---|
| Approval before the action | Nothing irreversible happens unreviewed | Latency on every routed decision, and a reviewer who must be available |
| Audit after the action | Throughput stays high | The wrong action already took effect; only suits reversible, low-cost decisions |
| Sampled review | Quality monitoring without slowing the flow | Individual bad decisions slip through unsampled |

Two independent failures collapse review into rubber-stamping, and either alone is enough. Volume beyond what a person can read produces consent fatigue: oversight that covers everything reviews nothing. And handing someone a bare output with a single approve button leaves them nothing to weigh it against. Give the reviewer the inputs, the output, and the reason this item was flagged. Requiring sign-off on every step adds friction without a matching safety gain; concentrate review where it carries information, such as approving a plan or handling an exception.

**Turn each obligation into a control, an owner, and evidence.** Regulations state outcomes and leave the implementation to you. Choosing a compliant delivery route is a prerequisite, not proof. A reviewer accepts a countersigned agreement, a screenshot of the live setting, an authorization record, or a query that returns the expected rows. A design document is none of these. A control with no named owner and no living artifact stops operating quietly, and the gap turns up in an audit instead of a design review, which is the costliest possible place to find it. Revalidate the register on a cadence, because configurations drift after the design is signed off.

Be able to:

- Identify misuse, hallucination, privacy, security, bias, and automation risks
- Place preventive, detective, and corrective controls at the right system boundary
- Use human review where impact, uncertainty, or regulation demands it
- Connect requirements such as GDPR, HIPAA, or FedRAMP to data handling, access, logging, retention, and deployment choices
- Explain residual risk and who accepts it

**Practice artifact:** create a risk register with likelihood, impact, control, evidence, owner, residual risk, and review cadence.

### 6. Stakeholder Communication & Lifecycle Management - 14%

**Official objectives.** Exam items are written against these five task statements:

1. Conduct structured discovery and requirement gathering
2. Communicate architectural decisions and trade-offs
3. Manage stakeholder feedback loops and expectation alignment (including SLAs)
4. Document architectures and provide implementation guidance
5. Support lifecycle phases (discovery, design, handoff, monitoring, iteration)

Professional architects must discover the real problem and make decisions legible. The strongest technical design can still fail when requirements, ownership, rollout, or expectations remain implicit.

**Discovery is structured elicitation, not conversation.** Listen to the goal in the stakeholder's own business language, translate it into requirements and named assumptions, and write both down before the discussion moves on. Skip the translation and the design silently inherits your assumptions instead of their constraints.

The core move is converting a preference into a constraint. Experience words — seamless, fast, simple, intuitive — are signals that more questions are needed, never requirements themselves. Ask which failures would puncture it, which mechanics must stay invisible to the user, and what has to remain true on the unhappy path. "Seamless" then resolves into a latency target, an integration boundary, a rule for how work passes to a person, and a failure state that exposes nothing — each of which the system can be built and measured against.

Force every vague statement through four categories:

1. **What the system must do** — capabilities stated as business outcomes, split across the model, existing systems, and people.
2. **What the system must not do** — prohibited actions and the cases that must route to a person. Stakeholders rarely volunteer these, so ask directly.
3. **What the system must cost** — the latency target, the per-interaction ceiling, the volume forecast.
4. **What the system must prove** — the evidence obligations. Finding these in discovery is far cheaper than finding them in a legal review weeks later.

Record one row per item across four columns: the stakeholder's own words, the constraint sitting underneath them, the design decision that constraint compels, and whatever you are still assuming until someone confirms it. The characteristic discovery failure is sketching an architecture mid-call. The sketch is plausible, and its plausibility is the danger — a stakeholder who sees a confident design assumes the questions were already asked, and the questions stop.

**Present a trade-off in three elements.** The benefit, the concession, and the price of undoing the choice after the rest of the system has been built on top of it. In regulated settings, add its effect on the compliance posture. That third element is routinely left out, and it is usually the one that decides the room, because it converts "which option is technically better" into "which option is the better business decision." Approving a per-call figure without understanding the unwind cost is not an informed decision, and the stakeholder will say so when the invoice arrives.

Package the decision so it can be defended upward: the options considered, the criteria you weighed, your recommendation, and the risks that survive it. Open on the business consequence instead of the design, and state the limits plainly; naming them is what earns a security reviewer's confidence.

**Observability collects signals; a feedback loop decides what they mean.** The loop runs signals, triage, decision, action, review — and it must exist as a table before launch, pairing every signal with the condition that fires it, the person who acts, and the action expected of them. Without it, the failure is characteristic: a metric drifts slowly for weeks, never crosses a hard alert threshold, and nobody hears about it until a stakeholder mentions the output "feels less useful." Every metric was collected. Nothing was mapped to a trigger.

Include the slow drifts alongside the hard failures, and include the reviews that fire on a schedule rather than a threshold. A residency confirmation or a periodic output audit happens whether or not anything looks wrong, and building that in later costs far more than building it in at design time.

**Service levels must trace to a source.** A latency threshold comes from the user-experience expectation captured in discovery, an availability threshold from how central the deployment is to the business, and a quality threshold from the evaluation acceptance criteria. A number that traces to none of these is a target someone found reasonable. Cost is the expectation that most often fails to survive launch, because production volume routinely runs orders of magnitude above the pilot: give the sponsor a consumption forecast and a spend-control posture before the first invoice, not after it.

**Documentation serves three readers at once.** The engineer inheriting the system needs the decisions, the options that were turned down, and the trade-off each rejection settled. The compliance reviewer needs each obligation paired with the control that satisfies it, the person accountable, and the artifact proving it runs. The architect returning months later needs dated decisions, assumptions marked as assumptions instead of woven in as facts, and open items with owners and resolution criteria.

| Field | What it captures |
|---|---|
| Decision | The choice made, with its date |
| Rejected alternatives | What was considered and not chosen |
| Trade-off resolved | The gain, the cost, and what reversal would take |
| Owner | Who is responsible for the decision or control going forward |
| Evidence artifact | What demonstrates the control is actually operating |
| Audit-ready status | Whether that evidence is current and sufficient |

The completeness test is practical: could an equally capable architect who missed every design session change this system safely on the strength of the document alone? A diagram records the shape of the system. With no rationale attached, a successor cannot tell which choices carry weight and which were merely preference, and will overturn a sound one for a reason that looks sound at the time.

**Manage the lifecycle as named phases** — discovery, design, handoff, monitoring, iteration — and know which phase a decision belongs to, because that is what tells you when one phase is ready to close. When a deployment spans more than one route or entry point, write down which one owns which task before integration begins; otherwise routing drifts and a surface chosen for one job quietly acquires another.

**Close with an outcome document, not a dashboard export.** Volume, latency, and error rate say the system runs. A sponsor justifying expansion needs the use case with its scope boundary, the business metric before, the same metric measured the same way after, the control that makes that comparison checkable rather than merely asserted, the owner of ongoing measurement, and a note on where the pattern transfers. Capture the "before" number at the start; there is no way to reconstruct it at the end.

Be able to:

- Turn stakeholder goals into prioritized functional and non-functional requirements
- Surface assumptions, conflicts, dependencies, and decision owners during discovery
- Explain architectural choices in terms of business value and operational consequences
- Record trade-offs in architecture decision records and implementation guidance
- Define feedback loops, handoff criteria, service levels, monitoring, and iteration plans

**Practice artifact:** present the same architecture twice: a five-minute executive version centered on value and risk, and a technical version centered on interfaces, controls, and operations.

### 7. Developer Productivity & Operational Enablement - 7%

**Official objectives.** Exam items are written against these three task statements:

1. Configure Claude tools and environments for teams (e.g., Claude Code)
2. Improve developer workflows using AI-assisted tooling
3. Support debugging and operational issue resolution

This smaller domain checks whether teams can use and operate the architecture effectively. At 7% it is roughly four scored items — worth an evening, not a week.

**Separate what shapes the agent from what governs it.** Standing project instructions, packaged procedures, scoped subagents, and connected tool servers shape what the agent knows and how it works. Lifecycle hooks, permission modes, approval flows, and sandboxing govern what it is allowed to touch. The distinction matters because a guarantee that must hold has to come from code and configuration, not from wording in an instructions file.

**Configure for a team, not for a person.** A team environment means one shared baseline everyone starts from — agreed project instructions, an agreed tool set, one permission posture — so configuration can be reviewed and improved once instead of drifting across individual setups. Choose the distribution mechanism by who needs the asset and how much control you must retain. Organization-wide availability reaches everyone but offers the least version control. Group-scoped packages target specific teams and carry versioned updates and rollback. Repository-scoped artifacts version alongside the code that uses them. Programmatic reuse pins an explicit version. Each trades reach against governance. Set spend guardrails deliberately rather than inheriting defaults: default model, allowed models, effort guidance, and per-user or rate caps. Unmanaged model choice compounds across everyone on the team and every request they make.

**Engineer adoption rather than announcing it.** Enable one champion per team first, let them convert a real workflow and absorb the early friction, then seed adoption in batches. Two failure modes are worth naming: lumpy adoption, where a few people use the tooling heavily and the practice never standardizes, and stalling at basic chat, where the team has access but never reaches repository-aware assistance or packaged procedures. Access is not adoption.

**Raise how the team works without lowering what it ships.** Assistance pays off where the work already happens — while code is being written, during review, inside the test cycle — rather than in a chat tab someone visits occasionally. Pair each stage with the discipline it still needs: whoever ships generated code must be able to explain it, a flagged finding is an input to judgment rather than a verdict, and a proposed diagnosis is checked against evidence before anyone acts on it. Capture that as an explicit verification checklist covering correctness, security, maintainability, and human understanding, then automate whatever can be automated so the gate fires on every change instead of relying on a reviewer's attention.

**Support means translating symptoms into causes, then handing the path over.**

| Symptom | Likely cause | First action |
|---|---|---|
| Quality slid gradually, and nobody shipped code | A changed model or prompt, or an index drifting as the corpus grew | Re-run the evaluation set, then diff what actually moved |
| Response times jumped | Context grew, a dependency slowed, or cached prefixes stopped matching | Trace the slowest span; read per-request token counts and cache hits |
| A tool fails intermittently | Credentials, throttling, or an error path nobody handled | Follow one failing call all the way through and check that tool's scope |
| Spend rose while usage held flat | Requests drifting to a costlier tier, or caching quietly regressing | Compare the observed tier mix and cache behavior against the sizing model |

Resolving one incident yourself is firefighting. Leave behind a runbook of known symptom-to-action paths and an escalation path naming who owns what, so you are called for genuinely new problems rather than ones the team has already seen.

Be able to:

- Configure Claude Code and related tooling with shared project guidance and bounded permissions
- Standardize repeatable development workflows without hiding important decisions
- Use AI-assisted tooling for code exploration, implementation, tests, debugging, and incident investigation
- Design adoption, support, and troubleshooting paths for a team

**Practice artifact:** define a team rollout for Claude tooling that covers configuration ownership, access, review gates, usage guidance, telemetry, and support.

## The Official Prep Path

Anthropic publishes a Professional prep path on the Partner Academy. It is **not required** — the exam guide states there is no single required course and that no resource guarantees a pass — but it is the only preparation material written against this blueprint.

| # | Course | Length | Primary domains |
|---|---|---:|---|
| 1 | Claude Platform & Solution Design | 238 min | 1, 2 |
| 2 | Enterprise Integration & Production | 158 min | 3 |
| 3 | Responsible AI, Safety & Risk for Architects | 114 min | 5 |
| 4 | Stakeholder Engagement, Lifecycle & GTM | 178 min | 6 |
| 5 | Team Enablement & Operational Productivity | 45 min | 7 |

Total run time is about **12 hours 15 minutes**.

Two things to notice. First, the course hours do not track the domain weights: Solution Design gets the most video time but Integration is the heaviest domain at 19%, and **Domain 4 (Evaluation, Testing & Optimization, 16%) has no dedicated course**. Second, that gap is yours to close with hands-on work — evaluation design is the domain where reading substitutes least well for having built the thing.

Access: [prep course path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional) · [all prep courses](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses)

## What the Official Sample Questions Teach

Section 8 of the exam guide contains three sample items with full rationale. Read them in the source rather than a summary — the reasoning in the answer key is the most direct signal available about how items are constructed. What they demonstrate:

- **Sample 1 (Integration).** An agent holds tools its users never need. The credited answer *removes* the unneeded tools. Logging them and adding a confirmation prompt are offered as plausible distractors, and both are rejected: they are detective and compensating controls, not removal of privilege. Using a larger model is rejected as unrelated to authorization scope. This is the least-privilege tool audit from Domain 3 in item form — ask of each connected tool whether the task requires it or merely benefits from it, and remove the rest.
- **Sample 2 (Models, Prompting & Context).** A large static prefix is re-sent on every request, and both latency and cost matter. The credited answer puts the stable content first and enables prompt caching. Truncating loses required policy; blind downsizing risks quality; moving the content into a few-shot block does not create a reusable cacheable prefix. The mechanism under test is ordering. A cache hit requires an unchanged prefix, so any per-request content placed ahead of the fixed block changes that prefix on every call and nothing is ever reused.
- **Sample 3 (Evaluation & Optimization).** Answers become confident but wrong right after a document refresh, with model and latency unchanged. The credited answer investigates retrieval and indexing first. The distractors invite you to suspect model weights, temperature, or the context window — none of which a document refresh would change. Run it through the failure taxonomy: the symptom is grounding, the trigger is a corpus change, and the model was never the variable that moved.

The shared pattern: **the stem contains a discriminator** (only support staff need those tools; the prefix is identical every time; only the documents changed). The credited answer is the one that acts on it. Several distractors are defensible engineering practices that simply do not address what the stem describes.

Two habits follow from this. Read the stem for the variable that changed and the constraint that is binding before reading any option. Then check each attractive distractor against the discriminator: if it would be equally reasonable advice with the discriminator removed, it is almost certainly not the credited answer.

## Ravn Practice Exam

This repository ships a **Professional practice exam** you can run in the browser:

- **126-question bank**, every item written against one of the 38 official objectives
- Each attempt draws **63 questions weighted to the blueprint** — 11/8/12/10/9/9/4 across the seven domains
- **Multiple-response items** included, scored all-or-nothing, each stating how many responses to select
- **Study mode** (rationale reveals per question) and **exam mode** (results at the end)
- Per-domain breakdown against the 720 cut score, and progress saved in the browser

> These are **Ravn-authored practice items, not real exam content**, and no third party can reproduce the live item bank. They are written to rehearse the reasoning the blueprint rewards. Treat a passing practice score as a readiness signal, never as a prediction.

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

Use the [Ravn practice exam](#ravn-practice-exam) in **exam mode** for the timed run, then re-run the same domains in **study mode** to read the rationale for every option you got wrong — including why the distractor you picked was attractive.

## Exam Decision Framework

When several options look plausible, prefer the answer that:

1. Solves the stated business requirement and respects every explicit constraint.
2. Uses the least complex architecture that meets the need.
3. Removes unnecessary capability and privilege at the source.
4. Produces measurable evidence through evaluation and observability.
5. Handles failure, fallback, human review, and ownership explicitly.
6. Makes cost, latency, quality, security, and maintainability trade-offs visible.

Several tie-breakers recur often enough to be worth memorizing:

- **A stated constraint eliminates before a preference chooses.** When a regulation, residency rule, or authorization level appears in the stem, it removes options first; cost and ergonomics only decide among what survives.
- **A rule that must be right every time belongs in deterministic code.** Authorization, thresholds, and schema checks are provable and replayable. Interpretation is what a model is for.
- **Match the mechanism to the data.** Stable reference knowledge is retrieved; a value another system owns is fetched with a tool call.
- **Place the control where the harm occurs.** A check after an irreversible action does not protect against it, and a control that passes traffic when it errors protects nothing.
- **Prefer the change that produces evidence.** Set the acceptance threshold before the measurement, and diagnose the failure class before proposing the fix.
- **Name the reversal cost.** Between two workable designs, the defensible answer is the one whose consequences you can state if it turns out to be wrong.

Avoid answers that rely on a larger model to solve an authorization or architecture problem, add monitoring without reducing avoidable risk, optimize one metric while ignoring the stated service level, or introduce agentic complexity without a clear benefit. Be equally wary of answers that add a plausible control at the wrong point in the path, treat a policy statement as an enforced rule, or route every decision to human review — the last one looks conservative and reliably degrades the review it claims to add.

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
- Complete 63 mixed-format practice items within 120 minutes — the [Ravn practice exam](#ravn-practice-exam) in exam mode is one way to rehearse this

## Resources

### Official — certification program

Everything in this guide's tables traces to one of these.

- [Claude Certified Architect - Professional Exam Guide (PDF)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf) — the authoritative blueprint, and the source of the 38 objectives above
- [Professional certification registration page](https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification)
- [All certifications and exam guides](https://anthropic-partners.skilljar.com/page/partner-certifications) — Associate, Developer, Architect Foundations, Architect Professional
- [Professional prep course path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional) (5 courses, ~12h)
- [Certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) — eligibility, retakes, validity, proctoring, badging
- [Certification policies](https://anthropic-partners.skilljar.com/page/policies-certifications)
- [Computer and network setup](https://anthropic-partners.skilljar.com/page/computer-and-network-setup) — check this before booking online proctoring
- [Claude Partner Network learning path](https://anthropic-partners.skilljar.com/page/claude-partner-network-learning-path)

### Official — product documentation

The exam guide directs candidates to the Claude API, models, prompt engineering, MCP, and Skills documentation.

- [Claude API documentation](https://platform.claude.com/docs/en/api/overview)
- [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Tool use](https://platform.claude.com/docs/en/build-with-claude/tool-use/overview)
- [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code documentation](https://code.claude.com/docs/en/overview)

Review the official exam guide again before registration. It contains the current policies for identification, accommodations, retakes, rescheduling, exam conduct, confidentiality, renewal, support, and appeals — and Anthropic marks it subject to change without notice.
