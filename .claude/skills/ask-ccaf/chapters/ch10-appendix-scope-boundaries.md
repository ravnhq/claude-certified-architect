# Chapter 10: Appendix — Technologies, In-Scope and Out-of-Scope Topics

*Covers guide sections 17–18. The out-of-scope list is the highest-leverage page in the guide: it tells you what to stop studying.*

## Core Idea
Scope is drawn around **using** the four technologies, never around building, hosting, or training them. If a topic is about model internals, infrastructure, authentication, or performance measurement, it is out.

## Technologies and concepts that might appear
| Area | Specifics named |
|---|---|
| **Claude Agent SDK** | agent definitions, agentic loops, `stop_reason` handling, hooks (PostToolUse, tool call interception), subagent spawning via Task tool, `allowedTools` |
| **Model Context Protocol** | MCP servers, tools, resources, `isError` flag, tool descriptions, tool distribution, `.mcp.json`, environment variable expansion |
| **Claude Code** | CLAUDE.md hierarchy (user/project/directory), `.claude/rules/` with YAML frontmatter path-scoping, `.claude/commands/`, `.claude/skills/` with SKILL.md frontmatter (`context: fork`, `allowed-tools`, `argument-hint`), plan mode, direct execution, `/memory`, `/compact`, `--resume`, `fork_session`, Explore subagent |
| **Claude Code CLI** | `-p` / `--print`, `--output-format json`, `--json-schema` |
| **Claude API** | `tool_use` with JSON schemas, `tool_choice` (`"auto"`, `"any"`, forced), `stop_reason` values (`"tool_use"`, `"end_turn"`), `max_tokens`, system prompts |
| **Message Batches API** | 50% cost savings, up to 24-hour window, `custom_id` correlation, polling, no multi-turn tool calling |
| **JSON Schema** | required vs optional fields, enums, nullable fields, `"other"` + detail string, strict mode |
| **Pydantic** | schema validation, semantic validation errors, validation-retry loops |
| **Built-in tools** | Read, Write, Edit, Bash, Grep, Glob — purposes and selection criteria |
| **Few-shot prompting** | targeted examples for ambiguity, format demonstration, generalization |
| **Prompt chaining** | sequential decomposition into focused passes |
| **Context window management** | token budgets, progressive summarization, lost-in-the-middle, context extraction, scratchpad files |
| **Session management** | resumption, `fork_session`, named sessions, session context isolation |
| **Confidence scoring** | field-level confidence, calibration with labeled validation sets, stratified sampling |

## In-scope topics (explicitly tested)
1. **Agentic loop implementation** — control flow on `stop_reason`, tool result handling, termination conditions.
2. **Multi-agent orchestration** — coordinator-subagent patterns, task decomposition, parallel execution, iterative refinement loops.
3. **Subagent context management** — explicit context passing, structured state persistence, crash recovery using manifests.
4. **Tool interface design** — effective descriptions, splitting vs consolidating tools, naming to reduce ambiguity.
5. **MCP tool and resource design** — resources for content catalogs, tools for actions, description quality for adoption.
6. **MCP server configuration** — project vs user scope, env var expansion, multi-server simultaneous access.
7. **Error handling and propagation** — structured responses, transient vs business vs permission errors, local recovery before escalation.
8. **Escalation decision-making** — explicit criteria, honoring customer preferences, policy gap identification.
9. **CLAUDE.md configuration** — hierarchy, `@import` patterns, `.claude/rules/` with glob patterns.
10. **Custom commands and skills** — project vs user scope, `context: fork`, `allowed-tools`, `argument-hint`.
11. **Plan mode vs direct execution** — complexity assessment, architectural decisions, single-file changes.
12. **Iterative refinement** — input/output examples, test-driven iteration, interview pattern, sequential vs parallel issue resolution.
13. **Structured output via `tool_use`** — schema design, `tool_choice`, nullable fields to prevent hallucination.
14. **Few-shot prompting** — ambiguous scenario targeting, format consistency, false positive reduction.
15. **Batch processing** — Message Batches appropriateness, latency tolerance assessment, failure handling by `custom_id`.
16. **Context window optimization** — trimming verbose tool outputs, structured fact extraction, position-aware input ordering.
17. **Human review workflows** — confidence calibration, stratified sampling, accuracy segmentation by document type and field.
18. **Information provenance** — claim-source mappings, temporal data handling, conflict annotation, coverage gap reporting.

## Out-of-scope topics (will not appear)
| # | Topic |
|---|---|
| 1 | Fine-tuning Claude models or training custom models |
| 2 | Claude API authentication, billing, or account management |
| 3 | Detailed implementation in specific languages or frameworks (beyond tool and schema configuration) |
| 4 | Deploying or hosting MCP servers (infrastructure, networking, container orchestration) |
| 5 | Claude's internal architecture, training process, or model weights |
| 6 | Constitutional AI, RLHF, or safety training methodologies |
| 7 | Embedding models or vector database implementation details |
| 8 | Computer use (browser automation, desktop interaction) |
| 9 | Vision / image analysis capabilities |
| 10 | Streaming API implementation or server-sent events |
| 11 | Rate limiting, quotas, or API pricing calculations |
| 12 | OAuth, API key rotation, or authentication protocol details |
| 13 | Specific cloud provider configurations (AWS, GCP, Azure) |
| 14 | Performance benchmarking or model comparison metrics |
| 15 | Prompt caching implementation details (beyond knowing it exists) |
| 16 | Token counting algorithms or tokenization specifics |

## Anti-patterns
- **Studying model internals or training methodology** — items 5 and 6 are explicitly excluded.
- **Preparing MCP server deployment** — configuring a server is in scope; hosting one is not.
- **Learning prompt caching mechanics** — knowing it exists is the whole requirement.
- **Practicing token counting or pricing math** — excluded, *except* the batch API's 50% savings and SLA arithmetic, which is in scope under 4.5.
- **Deep language- or framework-specific implementation study** — only what tool and schema configuration needs.
- **Preparing computer use or vision** — neither appears.

## Boundary cases worth noting
- **Batch cost and timing** are in scope (Domain 4.5) even though "API pricing calculations" is out — the tested judgment is workload fit and SLA arithmetic, not price lists.
- **Pydantic** is named, so schema validation in a specific library is fair game, while broader framework implementation is not.
- **Confidence scoring** is in scope as a *design and calibration* practice, while "performance benchmarking" as model comparison is out.
- **Authentication** appears only as `${VAR}` expansion in `.mcp.json` for credential hygiene; protocol details (OAuth, key rotation) are out.

## Document control
| Version | Summary of change | Date |
|---|---|---|
| 1.0 | Formatting and layout updates | July 2026 |
| 0.2 | Draft revision | June 2026 |
| 0.1 | Initial draft | February 2026 |

Version 1.0 is effective July 2026, exam code CCAR-F, and is subject to change without notice.

## Key Takeaways
1. Sixteen out-of-scope topics let you cut study time — read that list before building a plan.
2. In-scope means *using* the four technologies: configure, design, orchestrate, prompt, manage context.
3. Configure MCP servers, do not deploy them; know that prompt caching exists, nothing more.
4. The named technology list doubles as a checklist of exam-relevant identifiers, flags, and commands.
5. Batch cost/SLA arithmetic is the one pricing-adjacent topic that is in scope.
6. This guide is version 1.0 (July 2026) and can change without notice — re-check before sitting.

## Connects To
- **ch01**: blueprint weights tell you how much of the in-scope list each domain carries.
- **ch02–ch06**: each in-scope bullet maps to a task statement.
- **cheatsheet.md**: the scope boundary condensed for a final review pass.
