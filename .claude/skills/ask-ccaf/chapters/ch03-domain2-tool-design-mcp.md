# Chapter 3: Domain 2 — Tool Design & MCP Integration (18%)

*5 task statements. At 18%, roughly 11 of 60 items (derived from the weight).*

## Core Idea
**Tool descriptions are the primary mechanism LLMs use for tool selection**, and every agent should hold the smallest tool set its role needs. Most Domain 2 items reduce to: fix the description or narrow the scope before adding machinery around the model.

## Task Statements

### 2.1 Design effective tool interfaces with clear descriptions and boundaries
**Knowledge of:** descriptions as the primary selection mechanism — minimal descriptions make selection among similar tools unreliable; the need to include input formats, example queries, edge cases, and boundary explanations; how ambiguous or overlapping descriptions cause misrouting (`analyze_content` vs `analyze_document` with near-identical text); the impact of system prompt wording — keyword-sensitive instructions can create unintended tool associations.
**Skills in:** writing descriptions that differentiate purpose, inputs, outputs, and when to use this tool versus similar alternatives; renaming tools and rewriting descriptions to remove functional overlap (`analyze_content` → `extract_web_results` with a web-specific description); splitting generic tools into purpose-specific tools with defined input/output contracts (`analyze_document` → `extract_data_points`, `summarize_content`, `verify_claim_against_source`); reviewing system prompts for keyword-sensitive instructions that might override good descriptions.

### 2.2 Implement structured error responses for MCP tools
**Knowledge of:** the MCP **`isError` flag** for communicating failures back to the agent; the four error classes — **transient** (timeouts, service unavailable), **validation** (invalid input), **business** (policy violation), **permission**; why uniform responses ("Operation failed") prevent appropriate recovery; retryable vs non-retryable errors, and how structured metadata prevents wasted retries.
**Skills in:** returning `errorCategory` (transient/validation/permission), an `isRetryable` boolean, and human-readable descriptions; including `retriable: false` plus customer-friendly explanations for business rule violations; implementing **local recovery inside subagents** for transient failures and propagating to the coordinator only what cannot be resolved locally, with partial results and what was attempted; distinguishing **access failures** (need a retry decision) from **valid empty results** (successful query, no matches).

### 2.3 Distribute tools appropriately across agents and configure tool choice
**Knowledge of:** that too many tools degrades selection reliability by increasing decision complexity (**18 tools instead of 4–5**); that agents holding tools outside their specialization misuse them (a synthesis agent attempting web searches); **scoped tool access** — only role-relevant tools, plus limited cross-role tools for specific high-frequency needs; `tool_choice` options — `"auto"`, `"any"`, and forced selection `{"type": "tool", "name": "..."}`.
**Skills in:** restricting each subagent's tool set to its role; replacing generic tools with constrained alternatives (`fetch_url` → `load_document` that validates document URLs); providing scoped cross-role tools for high-frequency needs (a `verify_fact` tool for the synthesis agent) while routing complex cases through the coordinator; forcing a specific tool to run first (`extract_metadata` before enrichment) and handling later steps in follow-up turns; `tool_choice: "any"` to guarantee a tool call rather than conversational text.

### 2.4 Integrate MCP servers into Claude Code and agent workflows
**Knowledge of:** server scoping — **project-level `.mcp.json`** for shared team tooling vs **user-level `~/.claude.json`** for personal/experimental servers; environment variable expansion in `.mcp.json` (`${GITHUB_TOKEN}`) for credentials without committing secrets; that tools from all configured servers are discovered at connection time and available simultaneously; **MCP resources** as a mechanism for exposing content catalogs (issue summaries, documentation hierarchies, database schemas) to reduce exploratory tool calls.
**Skills in:** configuring shared servers in project-scoped `.mcp.json` with env var expansion for tokens; configuring personal servers in user-scoped `~/.claude.json`; enhancing MCP tool descriptions so the agent does not prefer built-in tools (like Grep) over more capable MCP tools; choosing existing community servers for standard integrations (e.g. Jira) and reserving custom servers for team-specific workflows; exposing content catalogs as resources so agents see available data without exploratory calls.

### 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively
**Knowledge of:** **Grep** for content search (file contents — function names, error messages, imports); **Glob** for file path pattern matching (names or extensions); **Read/Write** for full-file operations and **Edit** for targeted modification via unique text matching; using Read + Write as the fallback when Edit fails on non-unique text matches.
**Skills in:** Grep for searching code content across a codebase (all callers of a function, locating error messages); Glob for naming patterns (`**/*.test.tsx`); Read then Write when Edit cannot find unique anchor text; building codebase understanding **incrementally** — Grep for entry points, then Read to follow imports and trace flows, rather than reading all files upfront; tracing usage across wrapper modules by first identifying all exported names, then searching each name.

## Reference Tables

### Error taxonomy
| Category | Examples | Retryable | Agent should |
|---|---|---|---|
| Transient | timeout, service unavailable | yes | retry, possibly with local recovery in the subagent |
| Validation | invalid input format | no (without change) | correct the input and re-call |
| Business | policy violation, refund over limit | no (`retriable: false`) | explain to the customer / escalate |
| Permission | unauthorized access | no | escalate or route elsewhere |
| *Valid empty result* | query succeeded, zero matches | n/a | treat as success, not failure |

### `tool_choice` selection
| Setting | Guarantee | Use when |
|---|---|---|
| `"auto"` | model may return text instead of calling a tool | normal conversational agents |
| `"any"` | must call a tool, chooses which | structured output required, document type unknown among several schemas |
| `{"type":"tool","name":"X"}` | must call tool X | a specific step must run first (`extract_metadata` before enrichment) |

### Built-in tool selection
| Need | Tool |
|---|---|
| Find text inside files | Grep |
| Find files by name/extension pattern | Glob |
| Load a whole file | Read |
| Targeted edit with a unique anchor | Edit |
| Edit failed on non-unique text | Read + Write |

## Anti-patterns
- **Minimal tool descriptions** ("Retrieves customer information") — the root cause of most misrouting.
- **Two tools with near-identical descriptions** — rename and re-scope instead of adding routing logic.
- **Uniform error responses** — a generic "Operation failed" strips the agent of recovery information.
- **Silently returning empty results as success** — hides failure and prevents recovery.
- **Giving one agent 18 tools when 4–5 suffice** — decision complexity degrades selection.
- **Cross-specialization tool access** — a synthesis agent with web search will attempt web searches.
- **A pre-turn keyword routing layer** — over-engineered; bypasses the model's language understanding.
- **Custom MCP servers for standard integrations** — prefer community servers; reserve custom for team-specific workflows.
- **Committing credentials into `.mcp.json`** — use `${VAR}` expansion.
- **Reading all files upfront** to understand a codebase — Grep first, then Read along the trace.

## Worked Example
**Sample Question 2 (Scenario 1).** The agent calls `get_customer` for order queries like "check my order #12345". Both tools have minimal descriptions ("Retrieves customer information" / "Retrieves order details") and accept similar identifier formats.

| Option | Verdict | Reasoning |
|---|---|---|
| B. Expand each description with input formats, example queries, edge cases, and boundaries | **Correct** | Descriptions are the primary selection mechanism; low-effort, high-leverage, addresses the root cause |
| A. Add 5–8 few-shot examples for routing | Wrong | Token overhead without fixing the underlying cause |
| C. Keyword/identifier routing layer before each turn | Wrong | Over-engineered; bypasses the LLM's natural language understanding |
| D. Consolidate into one `lookup_entity` tool | Wrong | A valid architectural choice, but more effort than a "first step" warrants |

Note how D is marked wrong **not because it fails** but because the question asks for the *first step*. Watch for that qualifier.

**Sample Question 9 (Scenario 3)** applies 2.3: the synthesis agent needs verification on 85% simple fact-checks and 15% deep investigation. Correct answer — a **scoped `verify_fact` tool** for the common case, with complex cases still delegated through the coordinator. Giving it all web search tools over-provisions and violates separation of concerns; batching verifications creates blocking dependencies; speculative caching cannot predict what synthesis will need. The principle named is **least privilege**.

## Key Takeaways
1. Fix the description before adding routing, few-shot examples, or classifiers.
2. Include input formats, example queries, edge cases, and boundaries in every description.
3. Structured errors need `errorCategory`, `isRetryable`, and a human-readable message.
4. Distinguish access failure from a valid empty result — they demand opposite agent behavior.
5. Recover transient failures locally in the subagent; propagate only the unresolvable, with partial results.
6. 4–5 role-relevant tools beat 18 general ones.
7. `.mcp.json` = project/shared; `~/.claude.json` = personal/experimental; both load simultaneously.
8. MCP resources expose catalogs and cut exploratory tool calls; tools are for actions.
9. Grep for content, Glob for paths, Edit for unique anchors, Read + Write as the fallback.

## Prep-course supplement — MCP mechanics

*Source: Anthropic Partner Academy prep courses (Introduction to MCP; Claude with the Anthropic API; Developer Foundations M3). Supplements the guide — where the two differ, answer from the guide.*

### The three server primitives — who controls what
| Primitive | Controlled by | Invoked when | Reach for it when |
|---|---|---|---|
| **Tool** | the model | Claude alone decides to call it | adding a capability or action for the model |
| **Resource** | the app | client code fetches it by URI and uses the data — UI lists, autocomplete, or direct context injection | exposing data the application needs (an `@`-mention document list, a document's contents) without a tool round-trip |
| **Prompt** | the user | invoked deliberately — a slash command, button, or menu item | shipping a tested, evaluated prompt for the server's specialty, better than what users type ad hoc |

Rule of thumb: **tools serve the model, resources serve the app, prompts serve the user.** Pre-fetching a mentioned resource injects context up front — no tool call and no reliance on the model choosing to look.

- Resources are **direct** (static URI, e.g. `docs://documents`) or **templated** (URI parameters parsed into function arguments, e.g. `docs://documents/{doc_id}`). Define one resource per distinct read operation. The declared **MIME type** (`application/json` vs `text/plain`) tells the client whether to deserialize.
- Prompts return ready-to-send message lists with arguments interpolated server-side. Write, test, and eval the prompt once on the server; every client inherits the quality.

### Protocol and construction
- MCP is **transport-agnostic**: **stdio** for a server on the same machine (the client launches it as a subprocess), **HTTP** for shared or remote servers; SSE is legacy. A stdio server cannot be a shared team service — each machine spawns its own process, so teammates need the runtime installed.
- Wire flow: client sends a ListTools request → server returns definitions → the app passes them to Claude with the user's query → Claude returns `tool_use` → the app has the client send a CallTool request → the server executes (calling the outside service) → the result comes back → the app appends a `tool_result` and re-calls Claude.
- Server SDKs generate the JSON schema from decorated functions (`@mcp.tool` + typed arguments + per-argument field descriptions) — the same description-quality rules apply; the SDK only removes boilerplate.
- Applications wrap the SDK client session in their own class (connection lifecycle and cleanup); the session exposes `list_tools`, `call_tool`, `read_resource`, `list_prompts`, `get_prompt`.
- The **MCP Inspector** (`mcp dev server.py` → browser UI) lists and invokes a server's tools, resources, and prompts without wiring any application — the standard way to test a server in isolation.
- MCP vs tool use: complementary, not competing. MCP moves schema authoring and execution out of your app into a reusable server; the model-side loop is unchanged. On a normal project you build a client **or** a server, not both.
- Context cost: every connected server contributes tool definitions; Claude Code defers loading and discovers only the tools a task needs. Connect only the servers a task requires.
- Permission rules can pin the agent to a slice of a server: allow `mcp__github__create_issue` while everything else on the server still prompts; a deny on one tool overrides an allow on the whole server.

### Tool-result wire mechanics
- Every `tool_use` block carries an **id**; the reply is a `tool_result` block **in the next user message** with the matching `tool_use_id` — **ids, not ordering**, pair requests with results. Multiple `tool_use` blocks in one assistant message get all their results in one following user message.
- `tool_result.content` is the stringified output (JSON-encode structures). On failure set `is_error: true` with a meaningful message — Claude reads the error text and can retry with corrected arguments. Never return a silent empty result: the model treats it as valid data and reasons from a false premise (the guide's 2.2 anti-pattern, mechanized).
- Keep sending the tool schemas on **every** follow-up request in the conversation, and preserve the **full content array** (text block + tool_use blocks) when appending assistant turns — dropping blocks corrupts the history the model relies on.
- Validate tool inputs and raise meaningful errors ("location cannot be empty") — the error text is the model's repair signal.

### Agent tool design
- Give agents **abstract, composable tools** (bash, read, write, fetch) rather than hyper-specialized ones — Claude Code has no `refactor_file` or `install_dependencies` tool; it composes a small generic set. Reconcile with 2.3's scoping rule: scope the set to the role, keep each tool general within that role.
- **Environment inspection**: after (and often before) acting, the agent needs a way to observe results beyond a tool's return value — read a file before editing it, extract frames or captions to verify generated media, re-check state after a mutation. Build the inspection path into the tool set and prompt; it is how the agent gauges progress and catches its own errors.

## Connects To
- **ch02 (Domain 1)**: hooks intercept these tool calls; error propagation starts at the tool boundary.
- **ch06 (Domain 5)**: 5.3 error propagation is the multi-agent continuation of 2.2.
- **ch05 (Domain 4)**: `tool_choice` and JSON schemas reappear as the structured-output mechanism in 4.3.
- **ch08**: Sample Questions 2 and 9.
