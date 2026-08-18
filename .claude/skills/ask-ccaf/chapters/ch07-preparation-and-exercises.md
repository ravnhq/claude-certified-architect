# Chapter 7: How to Prepare, and the Four Hands-On Exercises

*Covers guide sections 7–8.*

## Core Idea
The guide prescribes **build-it preparation**, not reading. Seven study directives and four exercises together cover all five domains; the exercises are the closest thing to exam conditions because each one forces the same tradeoff decisions the items test.

## The seven preparation directives
1. **Build an agent with the Agent SDK** — a complete agentic loop with tool calling, error handling, and session management. Practice spawning subagents and passing context between them. *(Domain 1)*
2. **Configure Claude Code for a real project** — CLAUDE.md hierarchy, path-specific rules in `.claude/rules/`, custom skills with frontmatter (`context: fork`, `allowed-tools`), and at least one MCP server. *(Domain 3)*
3. **Design and test MCP tools** — descriptions that clearly differentiate similar tools; structured error responses with categories and retryable flags; test selection reliability with **ambiguous** requests. *(Domain 2)*
4. **Build a structured data extraction pipeline** — `tool_use` with JSON schemas, validation-retry loops, optional/nullable schema fields, batch processing with the Message Batches API. *(Domain 4)*
5. **Practice prompt engineering** — few-shot examples for ambiguous scenarios, explicit review criteria to reduce false positives, multi-pass review architectures for large reviews. *(Domain 4)*
6. **Study context management patterns** — extracting structured facts from verbose tool outputs, scratchpad files for long sessions, subagent delegation to manage context limits. *(Domain 5)*
7. **Review escalation and human-in-the-loop patterns** — when to escalate (policy gaps, customer requests, inability to progress) versus resolve autonomously; human review workflows with confidence-based routing. *(Domain 5)*

## Reference Table — exercise to domain coverage
| Exercise | Focus | Domains reinforced |
|---|---|---|
| 1. Multi-Tool Agent with Escalation Logic | agentic loop, tool integration, structured errors, escalation | 1, 2, 5 |
| 2. Claude Code for a Team Development Workflow | CLAUDE.md hierarchy, commands, path rules, MCP, plan mode | 3, 2 |
| 3. Structured Data Extraction Pipeline | JSON schemas, `tool_use`, validation-retry, batch | 4, 5 |
| 4. Multi-Agent Research Pipeline (design and debug) | subagent orchestration, context passing, error propagation, provenance | 1, 2, 5 |

Coverage note: Domain 3 appears in only one exercise despite carrying 20% of the exam — pair Exercise 2 with the ch04 anti-patterns list.

## Exercise 1: Build a Multi-Tool Agent with Escalation Logic
**Objective:** practice designing an agentic loop with tool integration, structured error handling, and escalation patterns.
1. Define **3–4 MCP tools** with detailed descriptions differentiating purpose, expected inputs, and boundary conditions — including **at least two with similar functionality** that require careful description to avoid selection confusion.
2. Implement an agentic loop checking `stop_reason` to decide whether to continue tool execution or present the final response; handle both `"tool_use"` and `"end_turn"` correctly.
3. Add structured error responses: `errorCategory` (transient/validation/permission), `isRetryable` boolean, human-readable descriptions. Test that the agent retries transient errors and explains business errors to the user.
4. Implement a **programmatic hook intercepting tool calls** to enforce a business rule (blocking operations above a threshold amount), redirecting to an escalation workflow when triggered.
5. Test with **multi-concern messages** and verify the agent decomposes the request, handles each concern, and synthesizes a unified response.

## Exercise 2: Configure Claude Code for a Team Development Workflow
**Objective:** practice CLAUDE.md hierarchies, custom slash commands, path-specific rules, and MCP server integration for a multi-developer project.
1. Create a **project-level** CLAUDE.md with universal coding standards and testing conventions; verify project-level instructions apply consistently across all team members.
2. Create `.claude/rules/` files with YAML frontmatter glob patterns per code area (`paths: ["src/api/**/*"]`, `paths: ["**/*.test.*"]`); test that rules load **only** when editing matching files.
3. Create a project-scoped skill in `.claude/skills/` with `context: fork` and `allowed-tools` restrictions; verify it runs in isolation without polluting the main conversation context.
4. Configure an MCP server in `.mcp.json` with environment variable expansion for credentials; add a personal experimental server in `~/.claude.json` and verify both are available simultaneously.
5. Test plan mode versus direct execution across three task sizes — a single-file bug fix, a multi-file library migration, and a new feature with multiple valid implementation approaches — and observe when plan mode provides value.

## Exercise 3: Build a Structured Data Extraction Pipeline
**Objective:** practice JSON schema design, `tool_use` for structured output, validation-retry loops, and batch strategy.
1. Define an extraction tool whose schema mixes **required, optional, and nullable fields** plus an **enum with `"other"` + detail string**. Process documents missing some fields and verify the model returns null rather than fabricating values.
2. Implement a **validation-retry loop**: on Pydantic or JSON schema validation failure, send a follow-up containing the document, the failed extraction, and the specific error. Track which errors retry resolves (format mismatches) versus which it cannot (information absent from source).
3. Add few-shot examples covering varied document formats (inline citations vs bibliographies, narrative descriptions vs structured tables); verify improved handling of structural variety.
4. Design a batch strategy: submit **100 documents** via the Message Batches API, handle failures **by `custom_id`**, resubmit failures with modifications (chunking oversized documents), and compute total processing time against SLA constraints.
5. Implement human review routing: field-level confidence scores from the model, low-confidence extractions routed to humans, and accuracy analyzed **by document type and field** to verify consistent performance.

## Exercise 4: Design and Debug a Multi-Agent Research Pipeline
**Objective:** practice subagent orchestration, context passing, error propagation, and synthesis with provenance tracking.
1. Build a coordinator delegating to at least two subagents (web search, document analysis). Ensure the coordinator's `allowedTools` includes `"Task"` and that each subagent receives findings **directly in its prompt** rather than relying on automatic context inheritance.
2. Implement **parallel execution** by emitting multiple Task calls in a single coordinator response; measure the latency improvement over sequential execution.
3. Design subagent output that separates content from metadata — each finding carries a claim, evidence excerpt, source URL/document name, and publication date. Verify synthesis **preserves source attribution**.
4. Implement error propagation: simulate a subagent timeout, verify the coordinator receives structured error context (failure type, attempted query, partial results), and test that it proceeds with partial results and annotates the final output with **coverage gaps**.
5. Test with **conflicting source data** (two credible sources, different statistics) and verify synthesis preserves both values with attribution rather than arbitrarily selecting one, structuring the report to distinguish well-established from contested findings.

## Key Takeaways
1. Every directive is a build instruction — reading the guide alone does not cover the skills bullets.
2. Deliberately build **two similar tools** and observe misrouting; that experience answers several Domain 2 items.
3. Verify each configuration mechanism's loading behavior yourself — that is exactly what Domain 3 items test.
4. Exercise 3's null-vs-fabrication test and Exercise 4's conflicting-source test map directly to sample questions.
5. Measure things the guide quantifies: parallel-vs-sequential latency, batch time against SLA, accuracy per segment.
6. Domain 3 is under-represented in the exercises relative to its 20% weight — supplement it.

## Connects To
- **ch02–ch06**: each exercise step traces to specific task statements.
- **ch08**: the sample questions test the same decisions these exercises produce firsthand.
