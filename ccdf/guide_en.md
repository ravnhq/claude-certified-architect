# Claude Certified Developer – Foundations

## Study guide for exam CCDV-F

> Based on the [official Developer – Foundations Exam Guide, version 1.0](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542875%2FClaude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf), effective July 2026. Anthropic marks the guide as subject to change, so confirm the current blueprint before scheduling.

The Developer – Foundations track tests whether you can build, integrate, and ship production-grade applications, agents, and workflows on Anthropic's Claude platform at a foundational level. It sits below the Architect – Professional exam in scope: it rewards hands-on mechanics — the API, the agent loop, tool schemas, streaming, context engineering, model and cost selection, debugging, security, and MCP — more than architecture or stakeholder negotiation.

This guide turns the official blueprint into a practical preparation plan. It does not reproduce or predict live exam content. Any practice material named here is Ravn-authored, not real exam content, and no third party can reproduce the live item bank.

## Exam at a glance

| Parameter | Official detail |
|---|---|
| Credential | **Claude Certified Developer – Foundations** |
| Exam code | **CCDV-F** |
| Items | **53** |
| Item format | Multiple-choice and multiple-response; each item states how many responses to select |
| Time limit | **120 minutes** |
| Delivery | Proctored, online or at a Pearson VUE test center, per program policy |
| Passing score | **720** on a 100–1,000 scaled score |
| Exam fee | **$125 USD** list; the amount at checkout reflects any partner-tier discount |
| Credential validity | **12 months** from the date the credential is awarded |
| Prerequisites | **None.** No course is required; the credential is awarded on exam performance alone |
| Score report | Pass/fail, scaled score, and percent correct by domain |

The schedule allows about 2 minutes 16 seconds per item. That is a pacing signal, not a target for every question: direct knowledge checks should leave time for multi-step scenarios and the multiple-response items that ask for a specific number of selections.

Registration starts on the [Anthropic Partner Academy certification page](https://anthropic-partners.skilljar.com/page/partner-certifications). Scheduling and delivery then move to Pearson VUE.

### Scoring

The exam is **criterion-referenced**: you are measured against a fixed performance standard, not against other candidates. The 720 cut score came from a formal standard-setting study in which subject-matter experts judged the performance expected of a minimally qualified candidate.

The score report shows percent correct per domain. Those **section percentages do not determine pass or fail** — only the total scaled score does. Use them to direct a retake, not to predict one.

### Policies worth knowing before you register

| Policy | Detail |
|---|---|
| Identification | A valid, unexpired, government-issued photo ID whose name matches your registration exactly. Correct the name through certifications-support@anthropic.com before scheduling |
| Attempts | Up to **4 per rolling 12-month period**, per exam; the fee applies to each attempt |
| Retake waits | **14 days** after a first failure, **30 days** after a second, **90 days** after a third |
| Delivery | Pearson VUE, online proctored or at a test center; **closed book** |
| Language | **English only.** Browser translation tools are prohibited during proctored testing |
| Accommodations | Request through Pearson VUE and be approved **before** you schedule |
| Reschedule | Free up to **24 hours** before the appointment; changes inside 24 hours, or a no-show, forfeit the fee |
| Confidentiality | You must accept a non-disclosure agreement before the exam begins; declining ends the session with no refund |
| Renewal | Review what changed and complete a complimentary **non-proctored** assessment on time; a lapsed credential means retaking the full exam at full fee |

Online proctoring needs Pearson's domains allowed on your network. If your device is locked down, a test center is the safer choice.

## Who the exam is for

Anthropic targets technical professionals who build, integrate, and ship production-grade AI solutions on Claude. The intended audience is AI and ML engineers, technical leads, and senior software engineers at the intersection of business requirements and implementation. The minimally qualified candidate profile recommends:

- One to five years of software engineering experience
- At least six months of hands-on work with Claude or a comparable LLM system
- Proficiency in Python and/or TypeScript
- Fluency with REST APIs and CLI tools
- A working understanding of LLM fundamentals, agents, context management, and MCP

These are recommendations, not prerequisites. The credential is not intended for non-technical or casual users, or for roles limited to prompt writing without broader application responsibility. Exam performance alone determines certification.

## The eight-domain blueprint

| Domain | Weight | What the exam expects |
|---|---:|---|
| 1. Agents and Workflows | **14.7%** | Build Claude agents and workflows with the Agent SDK, custom loops, and frameworks; decide workflow versus agent; use subagents and memory. |
| 2. Applications and Integration | **33.1%** | Integrate Claude through the API and SDKs with streaming, batch, vision, and caching; apply software-engineering foundations; design applications and manage configuration. |
| 3. Claude Code | **3.1%** | Operate Claude Code: Rules, Skills, Commands, Agents, memory, slash commands, modes, CLAUDE.md hierarchy, and settings.json. |
| 4. Eval, Testing, and Debugging | **2.6%** | Identify error types, choose recovery strategies, and isolate failure origin between the integration layer and model output through trace analysis. |
| 5. Model Selection and Optimization | **16.8%** | Reason about LLM fundamentals, model tiers and tradeoffs, technical substrate, and token/cost management including caching and batch. |
| 6. Prompt and Context Engineering | **11.0%** | Engineer prompts and context: instruction clarity, few-shot, placement, output constraints, context drift and compaction, and structured output handling. |
| 7. Security and Safety | **8.1%** | Apply secure-by-design principles, prompt-injection defense, guardrails and hooks, secrets and identity management. |
| 8. Tools and MCPs | **10.6%** | Implement tools and function calling, build MCP servers, and choose among built-in tools, custom tools, Skills, and MCPs. |

Take these eight domains and their weights from the official exam guide only. The exam is deliberately lopsided: **Domain 2 alone is a third of the exam**, and Domains 2 and 5 together are half. Domains 3 and 4 together are under 6%, so invest there lightly. The credential's purpose statement also lists designing and running evals as a capability, but on this blueprint evals sit inside the lightly weighted Domain 4 alongside debugging — do not over-invest in eval design the way the Architect track does.

## Domain guidance

### 1. Agents and Workflows — 14.7%

**Official objectives.** The guide groups this domain into three skills:

- **Agent Architecture (4.5%)** — workflow-versus-agent decision criteria, manager/supervisor hierarchies, and the role of subagents in task execution.
- **Agent Construction with Claude (5.3%)** — the Claude Agent SDK, custom agent loops and harnesses, managed deployment models (self-hosted vs. Anthropic-hosted), and hooks for deterministic actions.
- **Agent Patterns and Frameworks (4.9%)** — tool-use loops, sub-agents, memory, context-window management, and agentic abstraction frameworks such as Strands, LangGraph, and PydanticAI.

Decide workflow versus agent before you write the first line, because the wrong choice is the most expensive early mistake and the easiest to defend in a demo.

| Choose a workflow when… | Choose an agent when… |
|---|---|
| You can enumerate the exact steps in code | You can state the goal and the tools but not the path |
| Error cost is real and step-level guardrails matter | The path cannot be enumerated in advance |
| Standard observability is required | Non-determinism is acceptable and actions are bounded by the toolset |
| Inputs are well-constrained to a known set | User inputs vary unpredictably in content and structure |

The safe default is the cheapest pattern that survives your inputs: a single API call, then a workflow, then an agent. Promote one tier only when the current one cannot absorb the input variety you actually see. Mismatch the other way and you pay for it — a workflow chosen where an agent was needed collapses on the first input that leaves the coded path, and an agent chosen where a workflow suffices buys nondeterminism you never use.

**The agent is the pattern; the wiring path is an implementation choice.** Once you decide the task needs an agent, the pattern is constant: a loop that calls tools, manages context, and runs until a goal is met. Three wiring paths differ in how much runtime you own.

| Path | Who runs the loop | What you own | Choose when |
|---|---|---|---|
| Raw loop against the Messages API | Your code, every iteration | Full loop, tool execution, context, retries, exit conditions | You need full control or are learning the loop |
| Agent SDK | The SDK, inside your process | Tool execution and the surrounding application | You want the loop, context handling, and tool scaffolding in your own Python or TypeScript environment |
| Claude Managed Agents | Anthropic runs the loop and sandbox | The application layer and a versioned agent definition | Long-running execution in minutes or hours, or you want a managed sandbox and no loop to build |

Set `settingSources` explicitly in the Agent SDK rather than relying on a default: it decides whether filesystem-based configuration such as CLAUDE.md and Skills load into the agent. Managed Agents sessions are stateful and stored server-side, which currently rules them out for Zero Data Retention or HIPAA BAA workloads no matter how well they fit operationally — the governing constraint picks the path before convenience gets a say.

**Wire the loop the same four ways on every path.** Register tools, set a scoped system prompt, handle the tool-use loop by returning a `tool_result` block for every `tool_use` block the model issues, and define explicit exit conditions. A loop without exit conditions keeps requesting tool calls past what the task needs. Every `tool_use` block in an assistant turn must be answered by a matching-ID `tool_result` in the immediately following user turn; mismatched or missing IDs fail request validation, and no prompt fixes that.

**Place the human-in-the-loop gate by worst-case cost.** The question that decides where to insert a checkpoint is: what is the worst outcome if this step runs without a person checking it?

| Insertion point | What it addresses |
|---|---|
| Before a destructive tool call | Irreversible writes, deletes, or sends |
| After a planning step | A wrong plan executed correctly still produces the wrong outcome |
| On unexpected output | Error flags, empty results, or out-of-bound values that retry alone will not fix |

The characteristic failure is a loop that worked in a scratch directory and then edited a production file: validation passed on the file the agent edited, but no checkpoint sat between "validation passed" and "write committed to the live environment." If a tool can take an irreversible action in production, it needs a checkpoint before it runs, registered at design time.

**Pick the memory scope at design time, not under production pressure.** Four scopes trade cost against continuity.

| Scope | What persists | When it fits |
|---|---|---|
| In-context | State in the active conversation, survives turns | Short sessions that fit the window and need no cross-session continuity |
| External storage | State written to a database, read at session start | State that must survive across sessions, users, or agent instances |
| Summarized memory | A condensed prior conversation injected at start | Long-running dialogue where full history would outgrow the budget |
| Stateless | Nothing; each session independent | Self-contained jobs that finish and close out |

Too much in-context state inflates every call because the model re-reads the full history each turn; too little persistent state strips memory across sessions. Measure expected state size — history plus system prompt plus tool schemas — against the window before choosing in-context as the default. Tool outputs in production are often three to five times larger than test fixtures, so a window that held twenty turns in development can fill at turn eight in production.

Be able to:

- Decide workflow versus agent from the predictability and error cost of the task
- Choose a wiring path — raw loop, Agent SDK, or Managed Agents — on deployment and compliance constraints
- Wire the four-step loop with correct tool-use block pairing and explicit exit conditions
- Place human-in-the-loop checkpoints by the worst-case cost of an unchecked step
- Choose a memory scope that matches whether state must survive the session

**Practice artifact:** take a multi-step task and write three designs for it — a workflow, a single agent, and an orchestrator-worker — then state which you would ship and the constraint that decides it.

### 2. Applications and Integration — 33.1%

**Official objectives.** The largest domain splits into six skills:

- **Understanding Requirements (3.4%)** — functional and infrastructure requirements from business requirements and solution architecture.
- **Systems Life Cycle (2.8%)** — lifecycle concepts for developing, implementing, operating, and maintaining the system.
- **Claude API Mechanics (6.8%)** — messages, tools, streaming, vision, thinking, caching, third-party vendors, Messages API data-access patterns, the Batch API, and realtime-versus-batch tradeoffs.
- **Software Engineering Foundations (7.4%)** — REST APIs, JSON, asynchronous programming, version control, SDLC integration, code review, and small- and large-scale refactoring.
- **Claude Application Design (8.6%)** — how Claude interprets instructions across interfaces (Claude Code, Desktop, claude.ai, API, SDKs), content boundaries, schema design, session hygiene, and plugin management.
- **Configuration Management (4.1%)** — CLAUDE.md files, settings.json, model version pinning, prompt versioning, and plugin dependencies.

A third of the exam lives here, so weight your study accordingly. The unifying skill is turning a business requirement into running, configured, production-shaped code against the API.

**Capture requirements before you wire.** A business problem yields two kinds of requirement. Functional requirements name what the system must do, split across the model, existing systems, and people. Infrastructure requirements name where it runs: which cloud, which region, which identity model, which compliance posture. The expensive failure is sketching the architecture mid-discovery; a stakeholder who sees a confident design assumes the questions were already asked, and the questions stop. Write the constraint down — a residency rule, a retention rule, an approval gate — because an undocumented constraint becomes an infeasible system the moment production violates it.

**Choose the request shape by who is waiting.** The API offers three response shapes that solve different problems.

| Shape | When it fits |
|---|---|
| Synchronous (one complete response) | Short responses and backend jobs where no one is waiting |
| Streaming (server-sent events, pieces as the model generates) | Long responses or a user watching, so output appears immediately instead of after a blank-screen wait |
| Asynchronous client (async/await in the SDK) | You need concurrency without blocking your application thread; the request still returns in real time |
| Message Batches API | Bulk offline workloads where no user is waiting; submits a large set, returns within a 24-hour window at lower per-token cost |

Streaming and batch never compete for the same request: a request is either user-facing or it is not. Streaming changes how latency is perceived; batching changes the bill. On the newest models, sampling parameters such as `temperature`, `top_p`, and `top_k` return a 400 error and behavior is steered through prompting — confirm current parameter support in the API reference at build time.

**Handle a stream without corrupting state.** Acting on a half-built block is the bug to avoid. SSE chunks a `tool_use` block across several delta events; the block is whole only after the stream closes. Buffer the deltas by index, rebuild the tool call from the finished block, and only then execute it. Touch a partial `tool_use` and you feed malformed arguments downstream with no error signal. A dropped stream is not data to salvage — treat it as transient, retry the request in full, and discard anything you buffered.

**Match multimodal input to its cost.** Every image and PDF consumes context budget before the model reads a character of your prompt. A base64 payload inflates request size on every call, so a one-off image is fine but the same image sent repeatedly should be passed as a URL. Calculate image token cost before you commit a multimodal pipeline.

**Apply software-engineering foundations as you would for any production service.** REST and JSON are the substrate; the SDK is a thin convenience layer over the same REST API that handles authentication, request construction, retries, and parsing. Asynchronous programming keeps your application responsive while calls are in flight. Version control, code review, SDLC integration, and staged refactoring are scored as engineering discipline, not as Claude-specific trivia — the exam treats a Claude application as a system that must survive its own lifecycle.

**Design the application around how Claude reads instructions.** The same instruction is interpreted differently across interfaces — Claude Code, Desktop, claude.ai, the API, and SDKs — so a prompt that works in one surface is a draft for another, not a finished artifact. Hold content boundaries explicitly: separate trusted instructions from untrusted content the agent fetches. Keep session hygiene by trimming or summarizing history before each call; the window is a ceiling, not a target. Design schemas for the outputs you consume, and manage plugins as versioned dependencies rather than ad hoc copies.

**Configuration is a production artifact, not a convenience.** Five configuration surfaces recur, and each is a governance choice.

| Surface | What it controls | Where it lives |
|---|---|---|
| CLAUDE.md | Project instructions loaded into every session | Repo root |
| settings.json | Permission mode, allow and deny rules, hooks | User, project, local, and enterprise levels |
| Model version pin | Which model snapshot the code calls | In code, by full model ID |
| Prompt versioning | Which prompt the code sends | Alongside the code |
| Plugin dependencies | Which packaged capabilities are installed | Versioned and tracked |

**Pin the model version, not the alias.** A model alias such as Opus or Sonnet is convenient but resolves to a moving target; an upstream update then becomes a silent production change with nothing to roll back to. Pin the full model ID to a fixed snapshot, keep the prior version available, and gate promotion through your eval. The same discipline applies to prompts and plugins: version them alongside the code so a regression is a rollback rather than a hotfix.

Be able to:

- Derive functional and infrastructure requirements from a business problem and a solution architecture
- Choose synchronous, streaming, async-client, or batch request shapes by who is waiting and whether the work is realtime or bulk
- Consume a stream safely and recover from a dropped stream without committing partial tool calls
- Separate trusted instructions from untrusted content and design content boundaries across interfaces
- Configure CLAUDE.md, settings.json, pinned model versions, versioned prompts, and plugin dependencies
- Place configuration at the right scope — user, project, local, or enterprise — and explain which overrides which

**Practice artifact:** write the configuration files for one Claude application — a pinned model ID, a scoped settings.json with a deny rule, a CLAUDE.md held to the rules that change behavior, and a plugin declared as a versioned dependency — and state where each file lives and who can override it.

### 3. Claude Code — 3.1%

**Official objectives.** One skill:

- **Claude Code Operation (3.1%)** — core components (Rules, Skills, Commands, Agents, Agent Memory), features (session management, built-in and custom slash commands, headless mode, streaming mode, auto-mode), the CLAUDE.md hierarchy, repository initialization, and settings.json configuration.

At roughly one and a half scored items, this domain is worth an evening, not a week. Know the names and what each does; do not chase depth.

Claude Code runs the same agent loop in your terminal and adds a permission layer that gates every action. It works through a task in three phases — explore, plan, code — and plan mode holds it in the read-only explore phase, blocking edits and shell commands until you release a plan.

**Permission modes trade speed against oversight.** Default prompts before nearly every edit or command and is the baseline for any new or unfamiliar codebase. acceptEdits auto-approves reads, file edits, and common filesystem commands inside the working directory but still gates other shell commands and writes outside it. plan mode reads and proposes only. A bypass mode silences every confirmation prompt and also skips the protected-path guard the other modes keep, so it belongs only inside an isolated container. An allow-list mode pre-approves a named tool set and auto-denies everything else, built for locked-down CI.

**Configuration layers by scope, and deny wins.** User settings apply to every project on the machine; project settings apply to everyone who clones the repo; local settings are personal overrides that are git-ignored; enterprise managed settings cannot be overridden by users or projects. A deny rule always wins over an allow rule regardless of mode, and an enterprise-level deny is the most durable governance control because no individual developer can remove it.

**Keep CLAUDE.md short.** It loads into every session unconditionally, so every line you add reduces the weight of every other line. A file that grows to hundreds of lines dilutes the one rule that catches a real mistake. Hold it to the constraints that change behavior, and move path-specific guidance into rules files scoped by a `paths` glob in their frontmatter. Skills are the third mechanism: a SKILL.md file loads only when a request matches its description, so task-specific expertise inflates only the sessions that need it.

Be able to:

- Name the core components and what each carries into a session
- Pick a permission mode from the worst-case cost of an unchecked action
- Place a setting at the right scope and explain the deny-over-allow precedence
- Keep CLAUDE.md to behavior-changing rules and move the rest to rules files or Skills

**Practice artifact:** assemble a settings.json for a trusted local refactor that auto-approves edits, never runs destructive shell commands, and denies reads to `.env.production`, then state where the human gate sits for a change to a deployment config.

### 4. Eval, Testing, and Debugging — 2.6%

**Official objectives.** One skill:

- **Debugging and Error Handling (2.6%)** — error type identification, recovery strategy selection, trace analysis to identify failure modes, and problem origin isolation between the integration layer and the model output.

Despite the domain name, the single scored skill is debugging and error handling, not eval design. Treat evals as supporting material, not as the center of this domain.

**Every failure starts with one question: is it retriable or terminal?** If waiting and retrying the identical request could plausibly work, the failure is retriable; if not, it is terminal. On the Anthropic API, the status code tells you the bucket.

| Status | Class | Handling |
|---|---|---|
| 429 (rate limit) | Retriable | Exponential backoff with jitter, honor `retry-after`, cap attempts |
| 529 (overloaded) | Retriable | Backoff; reflects Anthropic-side load, not a rate-limit signal |
| 5xx server errors, 504 timeout | Retriable | Anthropic-side faults that typically clear on retry |
| 400 (bad request) | Terminal | No retry; the identical request will fail again — fix or reject the input |
| 401 (auth failure), 403 (forbidden) | Terminal | No retry; a permissions or auth problem that time cannot fix |
| Tool result error | Depends on the cause | Return it to Claude with `is_error: true` so the model can react |
| Refusal (200, stop_reason `refusal`) | Terminal | No retry; the model made a content decision. Raise it and log it |

Retrying a terminal error wastes the retry budget and hides the real problem behind a wall of identical failures. When unsure, the safe default is to treat an error as terminal and raise it: a failure wrongly classed as terminal fails loudly and gets fixed, while one wrongly classed as retriable hammers a service.

**Know what the SDK already retries before you write your own.** The Anthropic client libraries retry transient failures with progressive delays up to a configurable cap. Two retry loops wrapped around the same call multiply attempts against a rate limit rather than capping them, so decide where retry lives: let the SDK handle transient cases and reserve your code for application-specific fallback, or turn the SDK down and own the whole path. Honor `retry-after` when present; treat your own backoff as the fallback when it is not.

**Tool errors must come back to Claude explicitly, never silenced.** Swallowing a tool failure is what manufactures a confident, wrong answer: the model reads an empty result as legitimate data and builds reasoning on it. Surface the failure instead — return it with `is_error: true`, which gives the model the signal to change tack, ask for clarification, or halt. An empty result is never neutral; silence is what turns a tool bug into a plausible-sounding response.

**Use a trace to isolate the origin.** Tests tell you a failure exists; a trace tells you which step produced it. Four test levels each catch a different break: unit tests isolate one function, functional tests check one Claude call's shape, integration tests exercise the handoff between two components, and end-to-end tests run the whole flow. Most silent production breaks live at the integration level, where each side passes its own tests while the handoff between them is broken. A trace turns "the case failed" into "step four raised a KeyError on a field the model did not return," which is the difference between a five-minute fix and a day spent tracing by hand.

Be able to:

- Sort an error as retriable or terminal from its status code and behavior
- Place retry at one layer and avoid double-retrying the same call
- Return tool errors explicitly so the model can react
- Read a trace to localize a failure between the integration layer and the model output

**Practice artifact:** take a failing end-to-end run, read the trace, name the failing step, and classify the error as retriable or terminal with the handling that follows.

### 5. Model Selection and Optimization — 16.8%

**Official objectives.** Four skills:

- **LLM Fundamentals (5.2%)** — tokens, context windows, sampling, non-determinism, next-token generation; model options (fast mode, extended thinking, adaptive thinking, effort levels); and prompting techniques (zero-shot, single-shot, multi-shot).
- **Technical Fundamentals (6.1%)** — foundational engineering practices, including integrating with SDKs that wrap REST APIs and websockets.
- **Model Selection and Tradeoffs (2.7%)** — Opus vs. Sonnet vs. Haiku use cases, adaptive thinking support, tradeoffs across quality, latency, and cost, and breaking behavior changes across model releases.
- **Cost and Token Management (2.8%)** — token usage tracking, cost modeling, and caching techniques (prompt caching, cache checkpointing) for cost optimization.

This domain and Domain 2 together are half the exam. The fundamentals are the shared vocabulary the rest of the exam builds on.

**Tokens are the unit of input, output, and cost.** Claude reads tokens, not characters or words, and the characters-per-token average depends on the tokenizer and differs between model generations. Everything the model processes — prompt, history, tool definitions, tool results, and the response — is counted in tokens, and tokens are what the API bills and the context window measures. Think and budget in tokens, not words.

**The context window is a fixed budget, not a free resource.** Everything in a request shares it: system prompt, conversation history, documents, tool results, and the generated output. Two limits bite in different places. An input that already overflows fails validation before generation ever starts. An input that fits can still overflow while the model is generating — current models then halt and hand back what they produced so far, flagged with a `model_context_window_exceeded` stop reason, not an error. In neither case does the API quietly drop your oldest tokens; staying under the ceiling is your code's responsibility, which means trimming or summarizing history before every call.

**Sampling makes generation non-deterministic.** At each step the model produces a probability distribution over possible next tokens and samples from it; settings such as temperature shape that distribution. Because the choice is sampled, the same prompt run twice can return different wording even when both answers are correct. That changes how you test: a test that asserts the exact text of a response will be inconsistent, so assert on the property that must hold — a required field, a value in range, a structure that parses. On the newest Claude models, non-default sampling parameters are not accepted and behavior is steered through prompting; confirm current support at build time.

**Separate model choice from reasoning mode.** Two decisions, set independently: which model answers, and whether it thinks before it answers. On current models the thinking is adaptive — the model picks when and how deeply to reason, and you steer that depth with an effort setting, not a token allotment. The legacy `budget_tokens` field is deprecated and 400s on the newest generations. Spend the thinking budget where it pays:

| Reasoning | Worth it | Wasted |
|---|---|---|
| On | Hard, multi-step problems | Lookups, classification |
| Off | A capable model, fast and direct | A small model that needs the extra reasoning to compete |

Compose the levers: a strong model with thinking off is quick and straight; a smaller model with thinking on trades tokens for deliberation. The **carry-back rule** governs any turn that mixes reasoning with tools: every thinking block goes back to the API verbatim on the next turn. Its signature is the proof the reasoning was not altered; drop the block to save context and the following request fails.

**Start at the balanced tier and move on evidence.** The guide frames the model family around Opus, Sonnet, and Haiku. Sonnet is the balanced default for most production workloads; Haiku is built for speed and cost on tasks that fit its envelope; Opus handles demanding work above the Sonnet envelope. Move up only when an eval shows Sonnet missing your quality bar, and down only when an eval shows the quality drop is acceptable for the task — not merely to save cost. A model change is a release, gated by an eval against your cases, not a preference.

> **Guide-versus-course note.** The exam guide's Domain 5 objective names three tiers — Opus, Sonnet, and Haiku. The current prep-course material describes a four-tier family that adds Fable as the most capable tier. The exam is written against the blueprint, so the three-tier framing is the exam-relevant one; the course's Fable tier reflects a lineup that has since evolved. Confirm the current family and identifiers at platform.claude.com before scheduling, and treat any tier count as version-sensitive.

**Routing lets one system use more than one model.** Before building a router, ask whether every request looks the same: if it does, pin one model and stop. The pattern earns its keep only when request types differ — send the bulk to a balanced default and divert the few categories that need a larger or smaller model, keyed off a cheap signal read from the request. The whole point is to pay for capability only on the calls that justify it.

**Manage cost against the tail, not the average.** A cost or latency problem almost always traces to a few measurable levers: model selection, prompt and context size, number of tool calls, and streaming versus batch. Instrument three metrics per call — token usage, latency, and error rate — from the start, so a cost spike becomes a row you can sort instead of a mystery on the invoice. Token distributions are usually skewed, so a cost model built on an average can understate spend by a wide margin.

**Prompt caching reuses work already done on a stable prefix.** The first request writes the prefix to a cache; follow-up requests that send identical content up to a marked breakpoint read from it at a fraction of the cost. The cache matches on an exact prefix, so a single changed character before the breakpoint invalidates it — which is why caching fits stable content such as a long system prompt or a large tool schema and works against anything that must reflect live state. The default lifetime is five minutes, refreshed on each read; a one-hour lifetime is available at additional cost. Caching only applies above a minimum token threshold, so short prompts see no benefit. Place the stable content first and the per-request content last: ordering is the mechanism, not configuration, and putting variable content at the top means the prefix changes every time and the cache never hits.

**The Batch API trades latency for a lower bill.** For non-urgent, high-volume work, submit a large set of requests and receive results within an asynchronous window at lower per-token cost. Batching and prompt caching compound when a scheduled job reuses the same context across many requests.

Be able to:

- Explain tokens, the context window, sampling, and non-determinism and what each means for testing
- Separate model choice from reasoning mode and decide when extended thinking earns its cost
- Start at Sonnet and move tiers only on eval evidence
- Choose synchronous, streaming, async, or batch by who is waiting
- Use prompt caching and the Batch API to cut cost on stable and latency-tolerant workloads
- Instrument token usage, latency, and error rate per call

**Practice artifact:** build a cost model for one workload that names the model tier, the per-request token budget, the cacheable prefix, and whether each request is realtime or batch, then state which lever you would pull first if the bill tripled.

### 6. Prompt and Context Engineering — 11.0%

**Official objectives.** Three skills:

- **Context Engineering (3.8%)** — context window management, prevention of context drift and bloat (tool output pruning, compaction), and context isolation through subagents or multi-step agentic workflows.
- **Prompt Engineering (4.6%)** — instruction clarity, few-shot examples, system versus user placement, output constraints, prompt and instruction placement across components, iterative refinement, prompt adjustment, and input sanitization.
- **Output Handling (2.6%)** — structured output patterns, response validation, defensive parsing, and skepticism toward confident output.

Context engineering is deciding in advance what enters the context window, what comes back out as a summary, and what never enters at all.

**Four strategies keep a session in budget.** Each loses a different kind of continuity.

| Strategy | What it does | What you lose |
|---|---|---|
| Pruning | Jump back to an earlier message and continue from there | The work done after the rewind point |
| Compaction | Summarize history into a condensed version that preserves key information | Details the summarizer did not capture |
| Clearing | Start a new conversation with empty context | All session context; persist what matters elsewhere |
| Subagent handoff | Delegate a scoped task to an isolated context that returns a summary | Visibility into how the subagent reached its conclusion |

What compaction preserves depends on how you write the summarizer. An under-specified summarizer drops task-critical state — which files were modified, which decision was made at a branch point, which error was resolved — and that loss is one of the most common sources of multi-session agent failure. Context isolation through subagents keeps per-turn cost low and makes long-horizon tasks tractable, but only worth the overhead where context cost is a real constraint; a short workflow does not need it.

**Use the lightest prompting technique that clears the bar.** Start with instruction alone. Add examples when showing the desired shape is easier than specifying it. Add explicit step-by-step reasoning only when the path genuinely determines the answer. Each step costs tokens and latency on every call.

| Mode | When it fits |
|---|---|
| Zero-shot | The task is simple and the output shape is obvious |
| One-shot | A single example pins a structure a description keeps missing |
| Multi-shot (few-shot) | The output has a specific structure, casing, or edge case that needs several examples |

Model capability and prompting mode are the same optimization: a stronger model clears a task zero-shot that a smaller one only passes with a few examples. Run both down at once — start from the cheapest model and the fewest shots that satisfy your eval, then escalate capability or example count only where the eval demands it.

**Diagnose before you re-prompt.** Three failed revision passes is the cutoff for adding words: stop and ask which technique is absent instead. The trap is a prompt that swells rather than sharpens — six rounds, each longer than the last, none supplying the output constraint that was missing all along. Bloated prompts return bloated output and a latency hit for no accuracy gain. The fix is usually two lines: pin the exact format with an output constraint, and cover the ambiguous case with a single few-shot example.

**Move output control from the prompt into the API when it must hold.** A JSON-only instruction in the prompt passes the cases you tested and fails on the one you did not. Structured output closes that hole: pass the API a JSON schema and the grammar is enforced at generation, so a schema-violating response cannot be emitted. Two forms serve different surfaces — JSON outputs bind the final answer, and strict tool use validates the arguments bound for your tools before your code runs them. The cost is real and worth naming: the first request on a fresh schema is slower while the grammar compiles, an injected format prompt adds input tokens, and a guaranteed schema still does not guarantee success. A refusal or a `max_tokens` cut returns non-matching text, so your code reads `stop_reason` before it treats any response as parseable.

**Treat confident output with skepticism.** A model that produces fluent, confident content can still be wrong, with no error signal. Validate the response against the contract it must hold: parse defensively, check required fields, and do not trust confidence as a proxy for correctness. Validation confirms a value is the right shape; it cannot confirm it is the right value, which is why the eval — not the parser alone — guards the cases you did not think to test.

Be able to:

- Choose among pruning, compaction, clearing, and subagent handoffs by what continuity you can afford to lose
- Write a summarizer that preserves task-critical state
- Pick zero-shot, one-shot, or multi-shot by the cost and quality trade-off
- Diagnose a drifting prompt by the technique it is missing rather than by adding words
- Decide when structured outputs earn their cost over a prompt-level instruction
- Parse defensively and check `stop_reason` rather than trusting confidence

**Practice artifact:** take a classification prompt that returns the wrong shape, write the two-line fix (an output constraint and a covering few-shot example), then rewrite it with a JSON schema and name when the schema is worth its cost.

### 7. Security and Safety — 8.1%

**Official objectives.** Four skills:

- **AI Application Security (3.2%)** — prompt injection awareness and mitigation, jailbreak defense, untrusted input handling, data leakage prevention, PII handling, and authentication, authorization, confidentiality, privacy, and integrity.
- **Guardrails and Safe Deployment (2.3%)** — content policy, guardrail layering, and secure-by-design principles (privacy, identity and access management, least privilege).
- **Claude Hooks (1.0%)** — hooks for guardrails and safety controls to prevent destructive actions.
- **Identity, Secrets, and Key Management (1.6%)** — managing secrets, credentials, and API keys across development and production; identity validation and authentication; access approval and level verification; and authorized access monitoring.

Treat security as architecture, not as a prompt you add later. A rule that lives only in a prompt is a convention; a control that holds is one the system enforces and produces evidence for.

**Prompt injection is the core threat for any agent that reads content it did not write.** Trusting the human at the keyboard does not help, because the hostile instruction almost always hitches a ride inside content the agent retrieves — a fetched page, a document, a tool result — rather than arriving in the user's message. The model flattens its entire context into a single token stream with no native trusted/untrusted line, so buried instructions read as commands alongside your own prompt. The defense is structural: mark fetched and user-supplied content as data to inspect, never instructions to obey; fence it with delimiters; and gate any consequential action through constrain-and-log regardless of what that data says. No agent that ingests untrusted content is fully immune — the application has to hold the boundary as well.

**Jailbreaks and prompt injections are different threats with the same defense.** The two aim at different targets:

| Threat | What it attacks |
|---|---|
| Jailbreak | The model's own safety guardrails — get it to ignore them |
| Prompt injection | Your application's instructions — get it to follow the attacker's instead |

One defense covers both: validate and constrain what reaches the model, and separately cap what the model is permitted to do as a consequence. Guarding the prompt while leaving the action open is the common gap — once the model is steered, the unconstrained action is where the damage lands.

**Least privilege is the control that holds when every other defense fails.** The same injection, run under two identities, lands as two different outcomes: with an identity that can write anywhere and read every secret, it is an incident; with an identity scoped to one output directory and its given input, it is a denied action and a line in the log. So scope every production agent to the narrowest permission set the task needs. The blast radius of a steered agent is bounded by what its identity can touch, which makes the auth configuration itself a target — anything that can rewrite it acts with that identity, so guard that configuration as tightly as the secret.

**Secrets never travel with the configuration that references them.** Once a key leaks, rotation is the only remedy — and a credential baked into committed code (a `.mcp.json`, a settings file, source) cannot be rotated, because overwriting the file never erases it from history. Keep the two apart: the config carries a variable reference, and the value is injected at execution time from an environment variable or a managed secret store. When several services share the value, a store centralizes it so one rotation reaches every consumer and every read is logged.

**A hook is enforcement, not convention.** A PreToolUse hook runs before a tool call executes and can exit with a non-zero code to block it, writing the reason to stderr the agent sees. A PostToolUse hook runs after the call and is the right place for automated side effects and audit logging. When multiple rules apply to the same action, the precedence is deny over ask over allow — a single deny rule blocks the action regardless of how many allow rules are present. The distinction that matters in a regulated environment: a rule in a prompt can be followed inconsistently, while a hook fires at every relevant tool call without exception. Use both layers — a CLAUDE.md instruction communicates intent, and a hook enforces it deterministically.

**Screen at the right point in the path.** Input screening decides whether a request reaches the model. Output screening decides whether a response reaches the user. Action authorization decides whether a side-effecting call may run. One filter at the far end of the path covers exactly one of these, and it sits downstream of the only step that cannot be undone. Choose the failure direction deliberately: a screening service that errors and passes traffic through gives the appearance of protection with none of its function, so where an unscreened request would cause harm, fail closed.

Be able to:

- Treat untrusted content as data and constrain actions regardless of what it says
- Distinguish jailbreak from prompt injection and defend both with the same layered shape
- Scope an identity to the narrowest access the task needs and protect the auth configuration
- Keep secrets out of committed files and rotate them through a store or environment variable
- Place a PreToolUse hook to block and a PostToolUse hook to log, and apply deny-over-allow precedence
- Place input, output, and action controls at the points in the path where each harm occurs

**Practice artifact:** write the minimal secure configuration for an agent that fetches untrusted web pages and writes to one protected path — a hook that blocks writes triggered by untrusted input, a deny rule on sensitive paths, a secret referenced by environment variable, and an audit-log line on every privileged action.

### 8. Tools and MCPs — 10.6%

**Official objectives.** Three skills:

- **Tool Implementation (4.4%)** — tool use and function calling, configuration for external system interaction, tool description writing, error handling, tool usage patterns (agentic harness dispatch, client-side vs. server-side tools, approval patterns), and tool set construction best practices.
- **MCP Server Development (2.1%)** — server authoring, deployment, integration, MCP resources, tools, and prompts, and communication patterns (stdio, sockets, client vs. server).
- **Agentic Customization (4.1%)** — tradeoffs among built-in tools, custom tools, Skills, and MCPs for selecting and applying the appropriate approach for a given use case.

**Claude does not run your tools; it selects them and tells your code what to call.** The tool-use loop has a boundary that is where most bugs live: your code defines a schema, the model reads it and decides whether and when to call the tool, your code executes the tool and returns a `tool_result`, and the model continues. If your application does not handle the return correctly, the model never gets the data it asked for and the loop breaks.

**The schema is what drives selection.** Tool selection is driven almost entirely by what you wrote in the schema — the name, the description, and the input schema. Write descriptions that name what the tool does and when to use it; a vague or overlapping description produces erratic routing. Too many tools with overlapping descriptions degrade selection quality as the surface grows, so start with the minimum set the task needs and add tools only when a specific gap is confirmed. Too few tools force the agent to hallucinate a path or return an incomplete result.

| Failure | Fix |
|---|---|
| Wrong tool selected | The description, not the model — name the task and when the tool applies |
| Malformed tool arguments | Strict tool use with an input schema, validated before your code runs |
| Tool error silenced | Return `is_error: true` so the model can react |
| Over-tooled agent | Remove tools the task does not need; audit the set as you audit permissions |

**An MCP server separates tool definitions from any one application.** Build the capability once as a process that exposes tools, resources, and prompts, and every MCP client that connects gets access without re-implementing the integration. Resources are read-only data the client fetches into context by address, useful when pulling it in directly is cheaper and more predictable than a tool call. Prompts are vetted instruction templates the client invokes by name, useful when specific wording produces materially better results than whatever a user would type.

**Transport and scope are independent decisions that interact.** Transport is how the client talks to the server; scope is who loads it.

| Transport | When it fits |
|---|---|
| stdio | A local process on the same machine as the client — personal tools and dev servers |
| HTTP | Any server that does not run locally — shared team servers and hosted integrations (recommended) |
| SSE | Legacy; superseded by HTTP, not recommended for new servers |

| Scope | Who loads it | Where it lives |
|---|---|---|
| Local | Only you, one project | `~/.claude.json` under the current project |
| User | You, across all your projects | Personal Claude settings |
| Project | Everyone who clones the repo | `.mcp.json` committed to the repo root |
| Enterprise | All users, admin-controlled | Managed settings that cannot be overridden |

A stdio server cannot be project-scoped for sharing because it runs only on one machine, so match transport to where the server runs before choosing scope. Each connected server adds its tool definitions to the context pool, so connect only the servers a task needs.

**Secrets in MCP configuration follow the same rule as everywhere else.** An API key committed inline to `.mcp.json` enters repository history and cannot be removed by overwriting the file in a later commit; it must be treated as compromised and rotated. The configuration holds a variable reference, and the value lives in an environment variable. GitHub MCP authenticates with a personal access token passed as a header; Linear MCP uses an OAuth browser sign-in flow that issues and stores a token without anyone copying a secret. OAuth redirect URIs are registered per host, so a working staging connection does not mean production is configured — add the new host's redirect URI before moving an OAuth integration into a new environment.

**Permission rules can target a single MCP tool, not the whole server.** An MCP tool is identified as `mcp__server__tool`; an allow rule on one tool lets it run without a prompt while every other tool on the server still prompts, and a deny on one tool overrides an allow on the server. The API MCP connector adds an `enabled` flag per tool: the flag decides whether the model sees the tool at all, while a permission rule decides whether an exposed tool may run — a context-cost control and a governance control, often used together.

**Choose among built-in tools, custom tools, Skills, and MCPs by reuse.** Work down the list and stop at the first fit.

| Approach | When it fits |
|---|---|
| Built-in tool | The platform already provides the capability you need |
| Custom tool, wired directly | One application owns the integration and reuses nothing |
| Skill (SKILL.md) | A reusable instruction set that loads on demand for a recurring task |
| MCP server | The same tool surface must be reachable from more than one client and maintained independently |

Hard-coding logic into a prompt is neither reusable nor maintainable; pasting live data into the context window gives no live access and wastes context; relying on a built-in tool to reach an arbitrary internal API does not work. The failure to recognize is a protocol carried forward out of habit: a shared MCP layer with exactly one client buys integration cost and no reuse, and the mirror-image failure is a developer-facing surface placed in front of users who are not developers.

Be able to:

- Define a tool schema whose description drives correct selection
- Return tool errors explicitly and use strict tool use to validate arguments
- Choose stdio versus HTTP transport and local, user, project, or enterprise scope
- Keep secrets out of committed MCP configuration and pick the right auth pattern
- Target a single MCP tool with a permission rule and use the enabled flag for context cost
- Choose among built-in tools, custom tools, Skills, and MCPs by reuse and maintenance

**Practice artifact:** for one internal REST service, write two designs — a custom tool wired into one application and an MCP server shared across several — and state which you would ship and the reuse signal that decides it.

## The official prep path

Anthropic publishes a Developer – Foundations prep path on the Partner Academy. It is **not required** — the exam guide states there is no single required course and that no resource guarantees a pass — but it is the only preparation material written against the developer material. The five modules and their run times:

| # | Module | Length | Primary domains |
|---|---|---:|---|
| 1 | MSO Foundations | 59 min | 5, 6 |
| 2 | Production-Grade Prompting, Agents & Tool Use | 209 min | 1, 2, 6, 8 |
| 3 | Claude Code, MCP & Integration | 142 min | 3, 8, 2, 7 |
| 4 | Production Engineering, Evals & Security | 211 min | 4, 5, 7, 1 |
| 5 | Accelerators & IP Contribution | 139 min | 2, 7 |

Total run time is about **12 hours 40 minutes**.

Two things to notice. First, the course modules are organized by topic, not by exam domain, so no module maps one-to-one to a blueprint domain. Second, the module hours do not track the domain weights: Module 4 spends 211 minutes on evals, tracing, errors, cost, and security, yet Domain 4 (Eval, Testing, and Debugging) is only 2.6% and Domain 7 (Security and Safety) is 8.1%; meanwhile Domain 2 (Applications and Integration, 33.1%) is spread across Modules 2, 3, and 5 with no single home. Use the blueprint weights, not the module minutes, to budget your time.

Access: [prep course path](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses) · [all prep courses](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses)

## What the official sample questions teach

Section 8 of the exam guide contains three sample items with full rationale. Read them in the source rather than a summary — the reasoning in the answer key is the most direct signal available about how items are constructed. What they demonstrate:

- **Sample 1 (Applications and Integration).** Ten thousand documents must be processed overnight for a non-urgent report where cost is the primary concern. The credited answer uses the Message Batches API, which processes large asynchronous workloads within a 24-hour window at reduced cost. Sending requests synchronously in parallel does not reduce per-token cost; lowering `max_tokens` or blindly downsizing the model does not address the batch-versus-realtime tradeoff. The discriminator is that no user is waiting and cost, not turnaround, is the constraint.
- **Sample 2 (Security and Safety).** A summarizer reads a web page with hidden text instructing it to ignore previous instructions and reveal its system prompt. The credited answer treats retrieved page content as untrusted input, keeps it separate from trusted instructions, and uses guardrails or hooks so injected instructions cannot trigger sensitive actions. Raising temperature is irrelevant to injection; a polite request in the system prompt is not an enforceable control; a more instruction-following model can be more susceptible, not less. The mechanism under test is that the threat arrives through content, not through the user.
- **Sample 3 (Tools and MCPs).** An internal inventory REST service must be reusable across several Claude applications and maintained independently of any one. The credited answer builds an MCP server that exposes the inventory operations as tools so multiple applications can connect. Hard-coding logic into prompts is neither reusable nor maintainable; pasting data gives no live access and wastes context; built-in tools do not automatically reach arbitrary internal APIs. The discriminator is reuse across clients.

The shared pattern: **the stem contains a discriminator** — only cost matters and no user waits; the threat arrives through fetched content; the capability must be reusable across clients. The credited answer is the one that acts on it. Several distractors are defensible engineering practices that simply do not address what the stem describes.

Two habits follow. Read the stem for the variable that changed and the constraint that is binding before reading any option. Then check each attractive distractor against the discriminator: if it would be equally reasonable advice with the discriminator removed, it is almost certainly not the credited answer.

## Ravn practice material

This study guide is **Ravn-authored** and is not real exam content. Any practice items Ravn publishes for this track are written to rehearse the reasoning the blueprint rewards, and no third party can reproduce the live item bank. Treat a passing practice score as a readiness signal, never as a prediction.

The repository already ships a browser practice exam, but it targets the **Architect – Foundations** blueprint (exam code CCAR-F, 60 items, five domains) — a different exam from CCDV-F. Its domain mix and item count do not represent Developer – Foundations coverage, so do not treat it as Developer practice. For item-style calibration specific to this exam, the authoritative reference is the three sample questions in Section 8 of the official exam guide.

## A four-phase preparation plan

### Phase 1: Map your gaps

Copy the eight domains into a scorecard. Rate every domain from 0 to 3:

- **0 — unfamiliar:** you cannot explain the objective
- **1 — conceptual:** you can explain it but have not applied it
- **2 — practiced:** you have built or reviewed it with guidance
- **3 — defensible:** you can choose among alternatives and explain the evidence

Calculate `(3 - rating) × domain weight` for each domain. Use the result to prioritize study time instead of reading every topic equally. Domain 2 dominates this scorecard; Domains 3 and 4 barely move it.

### Phase 2: Build one reference application

Build or deeply review one end-to-end Claude application that includes:

- A business requirement turned into functional and infrastructure requirements
- API integration with streaming, a tool, and a batch or cached path
- A pinned model version and a versioned prompt
- A scoped agent loop with a human-in-the-loop checkpoint and a memory scope
- Error handling that sorts retriable from terminal and returns tool errors explicitly
- A security boundary: untrusted content as data, least privilege, a hook, and a secret in an environment variable
- An MCP server or custom tool chosen by reuse
- A trace that localizes a failure between the integration layer and the model

One coherent application exposes cross-domain trade-offs better than eight disconnected demos.

### Phase 3: Rehearse decisions

For each major design choice, practice this sequence:

1. State the requirement and constraints.
2. Name two or three viable options.
3. Compare quality, latency, cost, security, and operability.
4. Choose one and explain the evidence that would invalidate it.
5. Describe the fallback and who owns it.

This mirrors the judgment the blueprint rewards.

### Phase 4: Run timed items

Practice mixed-format items under the 120-minute limit. Include multiple-response items and force yourself to verify the requested number of selections. Review misses by failure type, not just topic: overlooked constraint, wrong request shape, misclassified error, misread discriminator, or a control placed at the wrong point in the path. Re-read the three official sample questions and their rationale before the run, because the answer key is the clearest available signal about how items are constructed.

## Exam decision framework

When several options look plausible, prefer the answer that:

1. Solves the stated requirement and respects every explicit constraint.
2. Uses the least complex pattern that meets the need — a single call before a workflow before an agent.
3. Matches the request shape to who is waiting — realtime or batch, streaming or synchronous.
4. Removes unnecessary capability and privilege at the source.
5. Places the control where the harm occurs — input, output, or action.
6. Makes cost, latency, quality, and security trade-offs visible and measured.

Several tie-breakers recur often enough to be worth memorizing:

- **A stated constraint eliminates before a preference chooses.** When a regulation, residency rule, or authorization level appears in the stem, it removes options first; cost and ergonomics only decide among what survives.
- **A rule that must be right every time belongs in deterministic code.** Authorization, schema validation, and deny rules are provable and replayable. A prompt instruction is a convention, not a control; if it must hold, enforce it with a hook.
- **Match the mechanism to the data.** Stable reference knowledge is retrieved or cached; a value another system owns is fetched with a tool; a reusable capability across clients is an MCP server.
- **Classify the error before you handle it.** Retriable failures back off with a cap; terminal failures fail fast. A tool error returns to the model with `is_error` set.
- **Pin the version, then gate promotion on the eval.** An alias is a moving target; a full model ID is a fixed snapshot with a rollback.
- **Treat untrusted content as data.** The threat arrives through what the agent reads, not through the user, so constrain actions regardless of what the content says.

Avoid answers that rely on a larger model to solve an authorization or schema problem, add monitoring without reducing avoidable risk, optimize one metric while ignoring the stated service level, or introduce agentic complexity without a clear benefit. Be equally wary of answers that silence a tool error, commit a secret to a config file, retry a terminal error, or place a screening check after the irreversible action it was meant to prevent.

## Readiness checklist

You are ready when you can do all of the following without notes:

- Decide workflow versus agent from predictability and error cost, and wire the four-step loop
- Choose a wiring path — raw loop, Agent SDK, or Managed Agents — on deployment and compliance constraints
- Pick synchronous, streaming, async-client, or batch request shapes by who is waiting
- Consume a stream safely and recover from a dropped stream without committing partial tool calls
- Configure CLAUDE.md, settings.json, a pinned model version, and plugin dependencies at the right scope
- Explain tokens, the context window, sampling, and non-determinism and what each means for testing
- Start at Sonnet and move tiers only on eval evidence, and use caching and batch to cut cost
- Choose among pruning, compaction, clearing, and subagent handoffs by what continuity you can lose
- Diagnose a drifting prompt by the technique it is missing, and decide when structured outputs earn their cost
- Sort an error as retriable or terminal and read a trace to isolate the failure origin
- Treat untrusted content as data, apply least privilege, and enforce the boundary with a hook
- Keep secrets out of committed files and choose the right MCP auth pattern
- Choose among built-in tools, custom tools, Skills, and MCPs by reuse
- Complete 53 mixed-format practice items within 120 minutes, verifying the requested number of selections on every multiple-response item

## Resources

### Official — certification program

Everything in this guide's tables traces to one of these.

- [Claude Certified Developer – Foundations Exam Guide (PDF)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542875%2FClaude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf) — the authoritative blueprint, and the source of the eight domains and their sub-skills above
- [All certifications and exam guides](https://anthropic-partners.skilljar.com/page/partner-certifications) — Associate, Developer, Architect Foundations, Architect Professional
- [Developer prep course path](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses) (5 modules, ~12h 40m)
- [Certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) — eligibility, retakes, validity, proctoring, badging
- [Certification policies](https://anthropic-partners.skilljar.com/page/policies-certifications)
- [Computer and network setup](https://anthropic-partners.skilljar.com/page/computer-and-network-setup) — check this before booking online proctoring

### Official — product documentation

The exam guide directs candidates to the Claude API, models, prompt engineering, Claude Code, Skills, and MCP documentation.

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
