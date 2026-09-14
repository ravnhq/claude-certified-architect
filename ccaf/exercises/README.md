# Build Exercises

Source: https://claudecertificationguide.com/learn/exercises

30 hands-on build exercises across 5 certification domains, copied verbatim from each lesson's `#build-exercise` section.

## Domain 1 · Agentic Architecture & Orchestration

### 1.1. Build a Multi-Tool Agent Loop
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-1-agentic-loops#build-exercise)

1. Set up a Claude API client with two tools: a calculator tool (accepts expression, returns result) and a web search stub (accepts query, returns mock results)
   *Why:* Multi-tool setups expose model-driven decision-making — Claude must select the right tool based on context, which is core to agentic architecture.
   **You should see:** Two tool definitions registered with proper JSON Schema input_schema, each with name, description, and parameters.
2. Implement the agentic loop that sends requests to Claude and inspects stop_reason after each response
   *Why:* The agentic loop is the core execution pattern — the exam tests whether you use stop_reason (deterministic) versus content-type checks or natural language parsing (unreliable).
   **You should see:** A while loop that calls client.messages.create() and checks response.stop_reason after each iteration.
3. Handle the tool_use stop_reason by executing the requested tool, creating a tool result message, and appending it to conversation history
   *Why:* This is the critical handoff in the loop — the exam specifically tests whether you correctly extract tool calls, execute them, and return results in the right message format.
   **You should see:** When Claude requests a tool, your code extracts the tool_use block, runs the corresponding function, and appends both the assistant response and a user message with tool_result to the conversation.
4. Handle the end_turn stop_reason by extracting and returning the final response
   *Why:* end_turn is Claude signal that it has completed the task — extracting the final text response correctly closes the loop and returns the result to the user.
   **You should see:** When stop_reason is end_turn, your loop exits and returns the text content from the final response.
5. Test with a prompt that requires multiple sequential tool calls (e.g., search for a value then calculate something with it) and verify the loop continues correctly through all iterations
   *Why:* Sequential tool calls test the full loop lifecycle — the agent must complete one tool call, receive the result, reason about it, and decide to call another tool before finally returning.
   **You should see:** At least two tool call iterations before end_turn. The agent searches first, uses the search result in a calculation, then returns the combined answer.
6. Add a safety iteration cap of 20 as a maximum bound (not the primary stopping mechanism) and log a warning if it triggers
   *Why:* The exam distinguishes safety caps (acceptable as a fallback) from using caps as the primary stopping mechanism (an anti-pattern). Your cap should never trigger in normal operation.
   **You should see:** A MAX_ITERATIONS constant, a counter that increments each loop, and a warning log if the cap is hit. Normal queries should terminate via stop_reason well before reaching 20.
### 1.2. Build a Hub-and-Spoke Research Coordinator
**Difficulty:** Intermediate · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-2-orchestration-patterns#build-exercise)

1. Create a coordinator agent that accepts a broad research topic as input
   *Why:* The coordinator is the central hub in hub-and-spoke architecture. The exam tests whether you understand that the coordinator owns task decomposition, subagent selection, and result aggregation — not the subagents.
   **You should see:** A coordinator function that accepts a topic string and returns a structured research report. It should have a system prompt defining its role as the orchestrating hub.
2. Implement task decomposition logic that breaks the topic into at least 5 distinct subtopics covering the full breadth of the subject
   *Why:* Narrow decomposition is a specific exam failure pattern. The coordinator that only assigns solar and wind for renewable energy misses entire categories. The exam expects you to recognise that incomplete output traces back to the coordinator decomposition.
   **You should see:** A decomposition function that produces 5 or more subtopics for any broad topic. For renewable energy, it should cover solar, wind, geothermal, tidal, biomass, and fusion at minimum.
3. Spawn two subagents (web search and document analysis) with explicit context passing — include all relevant information in each subagent prompt
   *Why:* Subagent isolation means no shared memory and no inherited context. The exam heavily tests this: if a subagent produces poor results, check whether the coordinator gave it sufficient context, not whether the subagent itself is flawed.
   **You should see:** Two subagent invocations where each receives the full assigned subtopic, the research goal, and any relevant context from prior agents — all explicitly included in the prompt.
4. Aggregate results from both subagents and evaluate coverage completeness
   *Why:* The coordinator must evaluate whether the combined results cover the full breadth of the original topic. This is where iterative refinement starts — gaps detected here trigger re-delegation.
   **You should see:** An aggregation function that combines results from both subagents and produces a coverage assessment listing which subtopics are well-covered, partially covered, or missing.
5. Implement an iterative refinement loop: if the coordinator identifies coverage gaps, re-delegate to subagents with targeted queries and re-invoke until coverage is sufficient
   *Why:* Iterative refinement is a core coordinator responsibility the exam tests. A single-shot delegation is not enough — the coordinator must evaluate output and re-delegate for gaps. This distinguishes a coordinator from a simple dispatcher.
   **You should see:** A loop that checks coverage, identifies gaps, sends targeted follow-up queries to subagents for the missing subtopics, and re-evaluates until a coverage threshold is met or a maximum iteration count is reached.
6. Test with the topic renewable energy technologies and verify that the final output covers solar, wind, geothermal, tidal, biomass, and fusion
   *Why:* This specific test case maps to the exam narrow decomposition failure pattern. If your output only covers solar and wind, the root cause is the coordinator decomposition — the exact diagnostic the exam expects you to make.
   **You should see:** A final research report with substantive sections on all six energy types: solar, wind, geothermal, tidal, biomass, and fusion. The coverage evaluation should show 100% completeness.
### 1.3. Implement Context Passing with Structured Metadata
**Difficulty:** Intermediate · **Estimate:** 50 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-3-subagent-invocation-context#build-exercise)

1. Create a coordinator agent with Task (or Agent) in its allowedTools
   *Why:* Task is the hard gate for subagent spawning (renamed Agent in current Claude Code v2.1.63; Task still works as an alias). Without it in allowedTools, the coordinator cannot invoke any subagent. The exam tests this as a binary requirement — it is not optional or configurable at runtime.
   **You should see:** A query() call whose options include allowedTools explicitly containing Agent (or Task) alongside any other tools the coordinator needs directly, plus the subagent definitions under options.agents.
2. Define two subagents: a web search agent that returns results with source URLs and titles, and a document analysis agent that returns analysis with page references
   *Why:* Each subagent needs scoped tool access matching its role. The exam tests whether you define subagents with proper AgentDefinition fields: description, system prompt, and tool restrictions.
   **You should see:** Two AgentDefinition objects, each with a description, system prompt, and restricted tool set. The web search agent has search tools only; the document analysis agent has file reading tools only.
3. Design a structured output format that separates content from metadata: each finding includes claim, source_url, document_name, page_number, and confidence
   *Why:* The exam specifically tests the attribution failure pattern: when a synthesis agent produces unsourced claims, the root cause is that the coordinator passed content without structured metadata. Separating content from metadata is the fix.
   **You should see:** A TypeScript interface or JSON schema defining the Finding type with both content fields (claim, analysis) and metadata fields (source_url, document_name, page_number, confidence, retrieved_by).
4. Pass complete structured results from both subagents to a synthesis subagent, preserving all metadata
   *Why:* This is the critical step the exam targets. Stripping metadata before passing to the synthesis agent is the root cause of attribution failures. The coordinator must pass the full structured output, not just the claim text.
   **You should see:** The coordinator passes the complete findings array (with all metadata intact) to the synthesis agent prompt. No metadata fields are stripped or summarised away.
5. Verify that the synthesis agent can attribute every claim in its output to a specific source with URL and page number
   *Why:* This verification step confirms the context passing worked. If any claim lacks attribution, trace back to whether the metadata was actually passed — do not blame the synthesis agent prompt.
   **You should see:** A synthesis report where every factual claim includes a citation with source URL and page number. No orphaned claims without attribution.
6. Refactor the coordinator to spawn both research subagents in parallel using multiple Task tool calls in a single response
   *Why:* The exam tests latency awareness. Sequential spawning of independent subagents wastes time. Parallel spawning via multiple Task tool calls in a single coordinator response is the correct pattern for independent tasks.
   **You should see:** Both the web search and document analysis subagents invoked simultaneously via parallel Task tool calls, with the coordinator waiting for both to complete before proceeding to synthesis.
### 1.4. Build a Prerequisite Gate for Financial Operations
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-4-workflow-enforcement-handoff#build-exercise)

1. Create a customer support agent with three tools: get_customer (returns customer ID and verification status), lookup_order (returns order details), and process_refund (processes a refund for a given amount)
   *Why:* These three tools create the exact scenario the exam uses for the 8% failure rate question. The workflow dependency between get_customer and process_refund is where programmatic enforcement becomes essential.
   **You should see:** Three tool definitions with proper JSON Schema input_schema. get_customer accepts a name or email, lookup_order accepts an order ID, and process_refund accepts a customer ID and amount.
2. Implement a programmatic prerequisite gate that blocks process_refund from executing until get_customer has returned a verified customer ID in the current session
   *Why:* This is the core exam concept: prompt instructions work 92% of the time but fail 8%. A prerequisite gate provides 100% deterministic enforcement. The exam always rejects prompt-based solutions for financial operations.
   **You should see:** A session-level state tracker that records whether get_customer has returned a verified customer. The process_refund handler checks this state before executing and returns an error if verification has not occurred.
3. Test that the gate works by prompting the agent to skip verification and process a refund directly — verify the gate blocks the attempt
   *Why:* Testing the bypass attempt demonstrates the difference between prompt-based and programmatic enforcement. Even when the model decides to skip verification, the gate blocks the action — which is the entire point of deterministic enforcement.
   **You should see:** The agent attempts to call process_refund without prior verification. The gate returns a blocked error message. The agent then calls get_customer before retrying the refund successfully.
4. Implement a structured handoff protocol: when the agent cannot resolve an issue, it compiles a self-contained summary with customer ID, conversation summary, root cause analysis, refund amount, and recommended action
   *Why:* Human agents do NOT have access to the conversation transcript. The handoff summary is the only information they receive. The exam tests whether you include all five required fields: customer ID, summary, root cause, amount, and recommended action.
   **You should see:** A handoff function that produces a structured object with all five fields populated. No field should be empty or contain placeholder text.
5. Test the handoff with a multi-concern request (return plus billing dispute plus account update) and verify the handoff summary is complete and self-contained
   *Why:* Multi-concern requests test whether the agent decomposes the request into distinct items and addresses all of them. The exam expects decomposition, parallel investigation, and unified resolution — not sequential handling or forgetting items.
   **You should see:** The agent identifies all three concerns, investigates each one, and produces a handoff summary that covers all three issues with specific details for each. No concern is omitted.
### 1.5. Implement Agent SDK Hooks for Normalisation and Policy Enforcement
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-5-agent-sdk-hooks#build-exercise)

1. Create an agent with three MCP tools that return data in different formats: Tool A returns Unix timestamps and numeric status codes, Tool B returns ISO 8601 dates and string statuses, Tool C returns DD/MM/YYYY dates and single-character status codes
   *Why:* This recreates the data format chaos example from the exam. Without normalisation, the model must interpret three different date formats and three different status representations, leading to inconsistent parsing across iterations.
   **You should see:** Three tool implementations that each return data with distinct date and status formats. Tool A uses epoch seconds and numeric codes, Tool B uses ISO strings and English statuses, Tool C uses DD/MM/YYYY and single characters.
2. Implement a PostToolUse hook that intercepts all tool results and normalises dates to ISO 8601 format and status codes to human-readable English strings
   *Why:* PostToolUse hooks run after execution but before the model processes the result. This is the correct hook direction for data normalisation — the exam tests whether you know that PostToolUse transforms data after execution, not before.
   **You should see:** A hook function that detects the format of each field and converts it: Unix timestamps to ISO 8601, DD/MM/YYYY to ISO 8601, numeric status codes to English strings, and single-character codes to full words.
3. Verify the model receives consistent data by testing with queries that require results from all three tools
   *Why:* Consistent data eliminates interpretation errors. Without normalisation, the model might confuse day/month order in DD/MM/YYYY or misinterpret status code P as processed instead of pending. Verification proves the hook works across all tool outputs.
   **You should see:** Three tool results that all use ISO 8601 dates and English status strings, regardless of which tool produced them. The model response should reference dates and statuses consistently without confusion.
4. Add a PreToolUse hook that blocks process_refund when the amount exceeds $500 and redirects to a human escalation workflow
   *Why:* A PreToolUse hook runs before execution — the refund never processes. The exam specifically warns against using PostToolUse for blocking, because by that point the action has already occurred. Pre-execution interception is the only correct hook direction for policy enforcement.
   **You should see:** A pre-execution hook that inspects process_refund calls, checks the amount parameter, and blocks the call with a redirect message if the amount exceeds 500. The refund tool never executes for blocked calls.
5. Add a second PreToolUse hook that blocks transfer_funds until aml_check has returned a pass result in the current session
   *Why:* This is the AML compliance scenario from the exam. Prompt instructions achieve 95% compliance, but regulatory requirements demand 100%. The hook provides deterministic enforcement that no prompt can match — a single missed AML check can result in legal penalties.
   **You should see:** A pre-execution hook that checks session state for a completed AML check before allowing transfer_funds to execute. Without a prior passing aml_check, the transfer is blocked with a descriptive error.
6. Test both hooks by attempting to trigger the blocked operations and verify they are prevented before execution
   *Why:* Testing confirms that the hooks provide deterministic enforcement. The key verification is that blocked tools never execute — the hook prevents the call, not just logs a warning after the fact.
   **You should see:** Both blocked operations return interception messages without the underlying tool executing. After satisfying prerequisites (completing AML check, reducing refund amount), the operations succeed.
### 1.6. Build a Multi-Pass Code Review Pipeline
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-6-task-decomposition#build-exercise)

1. Create a code review agent that accepts a directory path containing at least 10 source files
   *Why:* The 10+ file threshold is where attention dilution becomes observable. The exam uses a 14-file example where detailed feedback for early files degrades to superficial analysis for later files. Your setup must replicate this scale.
   **You should see:** A code review function that reads all files in a directory and prepares them for analysis. It should handle at least 10 TypeScript or JavaScript source files.
2. Implement a single-pass review that processes all files at once and record the results
   *Why:* The single-pass approach is the baseline that demonstrates attention dilution. The exam expects you to recognise the symptoms: thorough analysis for early files, shallow analysis for later files, and contradictory pattern evaluation.
   **You should see:** A review result where early files receive detailed feedback with specific line references and bug identification, while later files receive increasingly brief or missing feedback. This is the attention dilution pattern.
3. Implement per-file local analysis passes that produce structured feedback for each file individually (bug count, severity, specific line references)
   *Why:* Per-file passes give each file the full attention budget. This is the first layer of multi-pass architecture. The exam contrasts this with single-pass to show that structural decomposition solves attention dilution, not better prompts or larger context windows.
   **You should see:** Consistent analysis depth across all files. The last file receives the same level of detail as the first. Each review includes bug count, severity ratings, and specific line references in a structured format.
4. Implement a cross-file integration pass that checks for data flow issues, API consistency, and pattern usage consistency across all files
   *Why:* Per-file passes catch local issues but miss cross-cutting concerns. The exam tests whether you include a cross-file integration pass — batching without it still misses data flow issues and pattern inconsistencies across files.
   **You should see:** A separate analysis that takes the per-file summaries and checks for cross-file issues: inconsistent API usage, data flow problems between modules, and patterns used differently across files.
5. Compare results: document which issues the single-pass review caught versus the multi-pass approach, paying special attention to consistency of analysis depth across all files
   *Why:* This comparison demonstrates the exam argument quantitatively. Attention dilution is not a model capability problem — it is an architectural problem. The same model produces better results with multi-pass architecture, proving the fix is structural.
   **You should see:** A comparison table showing: more total issues found by multi-pass, consistent issue counts across files (no drop-off for later files), and cross-file issues caught only by the integration pass.
6. Record any cases where the single-pass review flagged a pattern in one file but approved identical code in another — these are attention dilution artefacts
   *Why:* Contradictory pattern evaluation is the clearest symptom of attention dilution. The exam uses the forEach example: flagged as inefficient in File 3, approved without comment in File 11. Documenting these artefacts proves the structural nature of the problem.
   **You should see:** At least one case where the single-pass review treated identical code patterns differently across files. The multi-pass review should treat the same pattern consistently.
### 1.7. Implement Session Management Strategies
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/1-agentic-architecture/1-7-session-state-resumption#build-exercise)

1. Create a Claude Code session that analyses a 10-file codebase and name it with --name for later resumption
   *Why:* Named sessions resumed with --resume enable continuation of work across breaks. The exam tests when resume is appropriate (no files changed) versus when it creates the stale context problem (files have been modified since the last session).
   **You should see:** A named Claude Code session that reads and analyses 10 source files. The session name should be memorable for later resumption. The agent should produce findings about each file.
2. Record the key findings from the initial analysis as a structured summary (file names, issues found, recommendations)
   *Why:* This structured summary is the knowledge you will inject into the fresh session later. The exam tests whether you preserve prior findings without carrying stale tool results. A good summary captures conclusions without raw tool output.
   **You should see:** A structured document listing each file name, the issues found in it, severity ratings, and specific recommendations. This should be concise enough to inject into a prompt but complete enough to preserve all key findings.
3. Modify 3 files in the codebase to fix some of the identified issues
   *Why:* Modifying files after a session creates the conditions for stale context. The old file contents remain as tool results in the session history while the actual files now contain different code. This is the exact scenario that triggers the contradictory advice bug.
   **You should see:** Three files modified with fixes for the issues identified in the initial analysis. The changes should be substantive enough that the old and new versions would produce different analysis results.
4. Attempt to resume the session with --resume and observe any stale context issues (contradictory advice, references to old code)
   *Why:* This demonstrates the stale context problem. The resumed session contains old tool results showing the unfixed code. The agent may recommend fixing issues that are already fixed, or give contradictory advice by referencing both old and new file contents.
   **You should see:** The agent giving contradictory advice: recommending fixes for issues already resolved, referencing code that no longer exists, or providing inconsistent guidance about the modified files. These are the hallmarks of stale context.
5. Start a fresh session with the structured summary injected into the initial prompt, specifying the 3 changed files for targeted re-analysis
   *Why:* Fresh start with summary injection is the correct approach when files have changed. The exam specifically tests this: no stale tool results, preserved knowledge from the prior session, and targeted re-analysis of only the changed files instead of wasteful full re-exploration.
   **You should see:** A clean session that knows about the prior findings (from the injected summary), targets only the 3 changed files for re-analysis, and produces consistent advice without contradictions.
6. Compare the quality and consistency of advice between the stale resume and the fresh start with targeted re-analysis
   *Why:* This comparison demonstrates why the exam favours fresh start with summary injection over naive resume after file changes. The fresh start produces consistent, accurate advice while the resume produces contradictions from stale context.
   **You should see:** A clear quality difference: the resume session gives contradictory or outdated advice about the modified files, while the fresh session gives accurate, consistent analysis based on the current file contents.
## Domain 2 · Tool Design & MCP Integration

### 2.1. Design Tool Descriptions That Eliminate Misrouting
**Difficulty:** Beginner · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/2-tool-design-mcp/2-1-tool-schema-design#build-exercise)

1. Create two MCP tools with intentionally ambiguous descriptions (e.g. get_customer: Retrieves customer information and lookup_order: Retrieves order details)
   *Why:* Reproducing a misrouting scenario first-hand builds intuition for why minimal descriptions fail. The exam tests your ability to identify ambiguous descriptions as the root cause of tool selection errors.
   **You should see:** Two tool definitions registered with your MCP server, each having a single-sentence description that does not mention input formats, example queries, or boundaries.
2. Test with 10 queries covering different user intents and log which tool the model selects for each
   *Why:* Quantifying selection accuracy before and after description changes gives you concrete evidence of the impact. The exam expects you to know that description quality directly affects selection reliability.
   **You should see:** A log showing at least 2-3 misrouted queries where the model selected get_customer for order-related queries or vice versa, demonstrating the ambiguity problem.
3. Rewrite both descriptions to include: purpose, expected inputs with formats, example queries, edge cases, and explicit boundaries against the other tool
   *Why:* This is the core exam skill — the lowest-effort, highest-leverage fix for misrouting. Production-grade descriptions include all five elements: purpose, inputs, examples, edge cases, and boundaries.
   **You should see:** Each tool description is 3-5 sentences long, explicitly states accepted identifier formats, gives example queries, and includes a boundary statement like "Do NOT use for order-specific queries — use lookup_order for those."
4. Re-run the same 10 queries and compare selection accuracy before and after
   *Why:* Measuring improvement validates that description quality is the root cause. The exam expects you to understand that better descriptions produce measurably better selection without any architectural changes.
   **You should see:** Selection accuracy improves to 9/10 or 10/10 correct, with previously misrouted queries now hitting the correct tool. A clear before/after comparison showing the improvement.
5. Review your system prompt for keyword-sensitive instructions that could override the improved descriptions
   *Why:* System prompt conflicts are a subtle failure mode the exam tests. Keywords like "always check customer details" can create unintended tool associations that override even well-written descriptions.
   **You should see:** A list of any keyword-sensitive phrases in your system prompt that could trigger incorrect tool associations, along with rewritten versions that avoid the conflict.
### 2.2. Build Structured Error Responses for All Four Categories
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/2-tool-design-mcp/2-2-structured-error-responses#build-exercise)

1. Create an MCP tool that queries a mock customer database with simulated failure modes
   *Why:* Simulating failure modes in a controlled environment lets you observe how agents behave when errors lack structure. The exam tests your understanding of how poor error responses cause wasted retries and incorrect escalations.
   **You should see:** An MCP server running with a customer_lookup tool that accepts a customer identifier and a failure_mode parameter to trigger specific error conditions on demand.
2. Implement four error response types: transient (simulated timeout), validation (invalid input format), business (refund exceeds policy limit), and permission (access denied)
   *Why:* Each error category demands a different recovery strategy. The exam tests whether you can identify which category an error belongs to and what recovery action is appropriate. Transient errors are retryable; business errors never are.
   **You should see:** Four distinct error responses, each with isError: true, a specific errorCategory value, the correct isRetryable boolean, and a descriptive message explaining what went wrong and what to do next.
3. Include structured metadata in each error: errorCategory, isRetryable boolean, and a human-readable description
   *Why:* Structured metadata is what enables intelligent recovery. Without these fields, the agent cannot distinguish a transient timeout from a permanent policy violation. The exam specifically tests whether you know that isRetryable: false means the agent must take an alternative path, not retry.
   **You should see:** Each error response parses to a JSON object containing exactly three fields: errorCategory (one of transient, validation, business, permission), isRetryable (boolean), and description (a sentence explaining the error and suggesting recovery).
4. Implement a valid empty result response (isError: false, resultCount: 0) clearly distinguished from an access failure
   *Why:* This is one of the most critical distinctions in Domain 2. Confusing access failures with valid empty results causes wasted retries and incorrect escalations. The exam tests this directly — an agent retrying a successful empty query is the canonical anti-pattern.
   **You should see:** Two structurally different responses: a valid empty result with isError: false and resultCount: 0 (indicating the query ran successfully but found nothing), and an access failure with isError: true, errorCategory: transient, and isRetryable: true.
5. Write an agent loop that reads the error metadata and takes appropriate action: retry for transient, fix input for validation, escalate for business, and request credentials for permission
   *Why:* The agent loop demonstrates the practical outcome of structured error metadata. Each error category maps to a specific recovery action, and the loop must branch correctly. This is exactly the kind of decision logic the exam expects you to design.
   **You should see:** An agent loop that parses the error metadata, branches on errorCategory, retries transient errors up to 3 times with backoff, reformats input for validation errors, escalates business errors to a human, and requests elevated credentials for permission errors.
### 2.3. Configure Tool Distribution Across a Multi-Agent System
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/2-tool-design-mcp/2-3-tool-distribution-choice#build-exercise)

1. Design three agent roles (web search, document analysis, synthesis) and assign 4-5 tools to each, scoped to its role
   *Why:* Tool overload degrades selection reliability. The exam tests the principle that each agent should have 4-5 tools scoped to its specific role. Giving a single agent 18 tools is a known anti-pattern that causes misrouting.
   **You should see:** A configuration object or table listing three agents, each with exactly 4-5 tools. No tool appears in more than one agent role (except scoped cross-role tools added later). Tool names clearly indicate their purpose and scope.
2. Add a scoped verify_fact tool to the synthesis agent that handles simple lookups directly
   *Why:* Routing every fact verification through the coordinator adds 2-3 round trips and up to 40% latency. The exam tests the scoped cross-role tool pattern — give the agent a constrained version of a capability for the 85% simple case, routing only complex cases to the coordinator.
   **You should see:** A verify_fact tool added to the synthesis agent toolset with a description that explicitly limits it to simple single-source lookups and states that complex multi-source verifications should be escalated to the coordinator.
3. Configure tool_choice forced selection on the document analysis agent to ensure extract_metadata runs as the mandatory first step
   *Why:* Forced selection enforces workflow ordering. The exam tests your knowledge of all three tool_choice modes: auto lets the model choose freely, any guarantees a tool call, and forced selection guarantees a specific tool call. This prevents the model from skipping mandatory steps.
   **You should see:** A document analysis agent configuration where the first API call uses tool_choice with type: tool and name: extract_metadata, and subsequent calls switch to tool_choice: auto for the remaining analysis steps.
4. Replace a generic fetch_url tool with a constrained load_document that validates document URLs only
   *Why:* This applies the principle of least privilege to tool design. A generic fetch_url tool can fetch anything from anywhere, enabling misuse. A constrained load_document that validates URLs prevents the agent from fetching arbitrary resources. The exam tests this pattern directly.
   **You should see:** A load_document tool definition that includes URL validation logic (checking for document file extensions or trusted domains) and rejects non-document URLs with a clear error message.
5. Test with a query that requires all three agents and verify that no cross-role tool misuse occurs
   *Why:* End-to-end testing validates that your tool distribution works in practice. Cross-role misuse — such as a synthesis agent running its own web searches instead of using provided results — is a common failure the exam expects you to prevent through proper scoping.
   **You should see:** A test run log showing: the web search agent using only its tools, the document analysis agent starting with extract_metadata (forced), and the synthesis agent using compile_report plus verify_fact for simple checks. No agent calls a tool outside its assigned set.
### 2.4. Configure MCP Servers with Scoping and Environment Variables
**Difficulty:** Beginner · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/2-tool-design-mcp/2-4-mcp-server-integration#build-exercise)

1. Create a .mcp.json file in your project root configuring a community MCP server (e.g. GitHub) with command and args
   *Why:* Project-level .mcp.json is version-controlled and shared with every team member who clones the repository. The exam tests whether you know that team-wide servers belong here, not in ~/.claude.json. Using community servers for standard integrations is always the correct first choice.
   **You should see:** A .mcp.json file at the project root containing an mcpServers object with at least one server entry specifying command (e.g. npx) and args (e.g. -y @modelcontextprotocol/server-github).
2. Use ${GITHUB_TOKEN} environment variable expansion for authentication credentials
   *Why:* Committing credentials directly in .mcp.json is a security risk the exam penalises. The ${VARIABLE_NAME} syntax lets the configuration file reference environment variables without containing the actual values, keeping secrets out of repository history.
   **You should see:** The env section of your server configuration contains ${GITHUB_TOKEN} (not an actual token value). Running git diff confirms no secrets are staged for commit. Each developer sets their own token locally.
3. Add a personal or experimental MCP server to ~/.claude.json for user-level configuration
   *Why:* User-level configuration in ~/.claude.json is personal, not version-controlled, and not shared with teammates. The exam tests whether you know the scoping hierarchy: .mcp.json for team servers, ~/.claude.json for personal or experimental servers.
   **You should see:** A ~/.claude.json file with an mcpServers entry for a personal server (e.g. an experimental integration you are testing). This file is NOT in your project repository and NOT in version control.
4. Expose a content catalogue (e.g. a documentation hierarchy or database schema) as an MCP resource
   *Why:* MCP resources give agents visibility into available data without requiring exploratory tool calls. Without resources, an agent might call list_tables then describe_table for every table, wasting multiple tool calls. A schema resource makes that information available immediately.
   **You should see:** An MCP resource definition that exposes structured data (e.g. a list of database tables with column types, or a documentation table of contents) accessible at a URI like db://schema/main. The resource should have a name, description, and mimeType.
5. Enhance the tool descriptions for your configured MCP server to explain capabilities and outputs in detail, preventing the agent from preferring built-in tools
   *Why:* When an MCP tool has a sparse description, the agent prefers built-in tools like Grep because their descriptions are richer and more detailed. The exam tests whether you know that enhanced MCP descriptions are required to compete with built-in tools for selection priority.
   **You should see:** Tool descriptions that are 3-5 sentences long, explaining what the tool does, what it returns, when to use it, and how it compares to built-in alternatives. For example, a search_codebase tool description that explicitly states it is more accurate than Grep for semantic searches.
### 2.5. Trace and Refactor a Deprecated Function Using Built-in Tools
**Difficulty:** Intermediate · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/2-tool-design-mcp/2-5-built-in-tools#build-exercise)

1. Use Grep to search for all callers of a target function (e.g. processLegacyOrder) across the codebase
   *Why:* Grep searches file contents — it is the correct tool for finding function callers. Using Glob here would fail because Glob matches file paths, not contents. The exam tests this distinction directly and penalises candidates who confuse the two.
   **You should see:** A list of file paths containing calls to processLegacyOrder, with line numbers and matching lines showing the exact call sites. For example: src/OrderProcessor.ts:42: await processLegacyOrder(orderId).
2. Use Glob to find test files matching the caller filenames (e.g. `**/*.test.tsx`)
   *Why:* Glob matches file paths by naming pattern — it is the correct tool for finding test files by extension or naming convention. This completes the Grep-then-Glob pattern: content search to find callers, then path matching to find their tests.
   **You should see:** A list of test file paths matching the pattern, such as src/OrderProcessor.test.tsx and src/RefundHandler.test.tsx. These correspond to the caller files found by Grep in the previous step.
3. Use Read to examine each caller file and understand the usage pattern and context
   *Why:* Reading files incrementally — only after Grep identifies which files matter — is the correct approach. Reading all source files upfront is a context-budget killer that the exam explicitly penalises. Each Read should be justified by what you discovered in the previous step.
   **You should see:** The full contents of each caller file, showing how processLegacyOrder is called, what parameters are passed, how the return value is used, and whether the function is imported directly or through a wrapper module.
4. Use Edit to replace the deprecated function call with the new API in each caller file
   *Why:* Edit is the preferred modification tool because it targets specific text and uses less context than Read + Write. The exam penalises defaulting to Read + Write for every modification. Always try Edit first — it is faster and more precise.
   **You should see:** Each caller file updated with the new API call replacing the deprecated one. For example, processLegacyOrder(orderId) replaced with processOrder(orderId, { validate: true }). The Edit tool confirms the replacement was made successfully.
5. When Edit fails with a non-unique match, widen old_string with more surrounding lines until it pins down one location (or set replace_all: true if you actually want every occurrence updated). Only fall back to Read + Write if neither option can disambiguate the target
   *Why:* Edit fails when the target text appears multiple times in the file — this is a safety mechanism, not a bug. Per the Edit tool documentation, the documented recovery is to expand the anchor with more surrounding context until it matches one place, or to use replace_all for global replacements. Both keep you on Edit and cost almost nothing in context. Read + Write loads the entire file for what is usually a single-line change — keep it as a last resort.
   **You should see:** On the first try, Edit fails with an error like: old_string matches 3 locations. On the retry with a wider old_string that includes the surrounding function name or unique adjacent line, Edit succeeds and changes exactly one occurrence. If replace_all: true was the right call, every occurrence is updated atomically.
## Domain 3 · Claude Code Configuration & Workflows

### 3.1. Build a Multi-Level CLAUDE.md Configuration
**Difficulty:** Beginner · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/3-claude-code-config/3-1-claude-md-hierarchy#build-exercise)

1. Create a project-level .claude/CLAUDE.md with universal coding standards: naming conventions, error handling patterns, and a code review checklist
   *Why:* Project-level configuration is the foundation of team-wide standards. The exam tests whether you place shared conventions here rather than in user-level config, which is the most common misconfiguration scenario.
   **You should see:** A .claude/CLAUDE.md file at the repository root containing at least three sections: naming conventions, error handling patterns, and a code review checklist. Running /context in the project root lists this file under Memory files.
2. Create a directory-level CLAUDE.md in a /packages/api/ subdirectory with API-specific conventions (REST endpoint naming, request/response schema requirements)
   *Why:* Directory-level configuration scopes conventions to a specific package. The exam tests whether you know that directory-level CLAUDE.md applies only within that directory, not across the entire project.
   **You should see:** A CLAUDE.md file inside /packages/api/ containing REST-specific conventions. When you run /context while working in /packages/api/, both the project-level and directory-level files appear under Memory files.
3. Create .claude/rules/testing.md with test-specific conventions (test naming pattern, assertion style, fixture usage)
   *Why:* The .claude/rules/ directory holds topic-specific rule files that can optionally include YAML frontmatter for path scoping. Understanding this mechanism is tested alongside path-specific rules in Task Statement 3.3.
   **You should see:** A testing.md file inside .claude/rules/ containing at least three test conventions. Running /context lists this rules file under Memory files.
4. Use an @ path import in the project-level CLAUDE.md to reference a shared standards file at ./standards/naming.md
   *Why:* The @ import syntax enables modular organisation of conventions. There is no @import keyword — a path prefixed with @ on its own line is the import. Each package can import only relevant standards, reducing duplication and drift in the source files. The exam tests whether you know the mechanism exists and how the syntax actually looks.
   **You should see:** The project-level .claude/CLAUDE.md contains a line beginning with @ pointing to ./standards/naming.md. A separate file at .claude/standards/naming.md (or standards/naming.md relative to the CLAUDE.md) exists with naming conventions. Running /context confirms the imported content is loaded inline.
5. Run /context in different directories to verify the correct files are loaded in each context
   *Why:* The exam tests that the diagnostic command reveals loaded files but does not trigger loading — configuration loads automatically based on location. The guide names /memory for this; current Claude Code reports the loaded set under /context, so that is what you run here.
   **You should see:** In the project root, /context shows the project-level CLAUDE.md and rules files under Memory files. In /packages/api/, it additionally shows the directory-level CLAUDE.md. The imported standards file content appears as part of the project-level configuration.
6. Move one convention from project-level to user-level (~/.claude/CLAUDE.md) and verify that a different user session does NOT pick it up — confirming the scoping boundary
   *Why:* This is the exam favourite trap scenario. When conventions live in user-level config, new team members who clone the repo do not receive them. Proving this boundary experimentally cements the concept.
   **You should see:** After moving a convention to ~/.claude/CLAUDE.md, your own /context shows it loaded. A simulated second user session (or a fresh clone without your home directory config) does NOT show that convention. This confirms the scoping boundary.
### 3.2. Create Custom Commands and Skills
**Difficulty:** Intermediate · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/3-claude-code-config/3-2-slash-commands-skills#build-exercise)

1. Create a project-scoped /review command in .claude/commands/review.md containing a team code review checklist
   *Why:* Project-scoped commands are shared via git so every developer gets them on clone. The exam tests whether you place team commands in .claude/commands/ (project) vs ~/.claude/commands/ (personal).
   **You should see:** A file at .claude/commands/review.md in the repository. Running /review in Claude Code triggers the code review checklist. The command appears when any developer clones the repository.
2. Create a personal /brainstorm skill in ~/.claude/skills/brainstorm/SKILL.md with context: fork in the frontmatter
   *Why:* The context: fork frontmatter option isolates verbose skill output from the main conversation. Without it, codebase analysis output fills the context window and degrades subsequent responses. The exam directly tests this concept.
   **You should see:** A SKILL.md file at ~/.claude/skills/brainstorm/SKILL.md with YAML frontmatter containing context: fork. The skill is available only in your sessions, not shared with teammates.
3. Add allowed-tools to the brainstorm skill, restricting it to Read, Grep, and Glob (read-only operations)
   *Why:* The exam guide describes allowed-tools as restricting which tools a skill can access, and that is the expected exam answer. In current Claude Code it pre-approves the listed tools so they run without a permission prompt (disallowed-tools is the actual boundary), but the intent is the same: a read-only analysis skill should never be using Write or Bash.
   **You should see:** The SKILL.md frontmatter now includes an allowed-tools list with exactly Read, Grep, and Glob. Under the exam-guide model the skill cannot use Write or Bash; in current Claude Code the list pre-approves those three tools for promptless use.
4. Add argument-hint to the brainstorm skill: "Provide a feature description or codebase area to explore"
   *Why:* The argument-hint prompts developers for required parameters when invoking the skill without arguments. This improves developer experience and is one of the three SKILL.md frontmatter options tested on the exam.
   **You should see:** The SKILL.md frontmatter now includes argument-hint. When a developer invokes /brainstorm without arguments, they see a prompt asking for a feature description or codebase area.
5. Test that /review appears for all project users (shared via git) and /brainstorm only for you
   *Why:* This verifies the scoping boundary that the exam repeatedly tests: .claude/ is project-scoped and shared via git, while ~/.claude/ is user-scoped and personal. Confirming this experimentally solidifies the concept.
   **You should see:** Running /review works in any clone of the repository. Running /brainstorm works only in your session. A colleague or fresh clone without your home directory config does not see /brainstorm as an available command.
6. Invoke the brainstorm skill and verify that its verbose output does not appear in the main conversation context
   *Why:* The context: fork option runs the skill in an isolated sub-agent. The main conversation receives only the summary, not the full verbose output. This is critical for preserving context window tokens during exploratory tasks.
   **You should see:** After invoking /brainstorm with a codebase area, the main conversation shows a concise summary of findings. The verbose file listings, code excerpts, and analysis notes are not visible in the main conversation history. Subsequent responses remain high quality because the context window is not filled with exploration output.
### 3.3. Configure Path-Specific Rules with Glob Patterns
**Difficulty:** Intermediate · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/3-claude-code-config/3-3-path-specific-rules#build-exercise)

1. Create .claude/rules/testing.md with YAML frontmatter paths: [`"**/*.test.ts"`, `"**/*.test.tsx"`, `"**/*.spec.ts"`] and test conventions (naming, assertions, mocking patterns)
   *Why:* Path-specific rules with glob patterns are the correct solution for conventions that apply to a file type spread across many directories. The exam favourite scenario is test files co-located with source files across 50+ directories.
   **You should see:** A file at .claude/rules/testing.md with YAML frontmatter containing a paths array with glob patterns. The body contains at least three test conventions covering naming, assertions, and mocking.
2. Create .claude/rules/api-conventions.md with paths: [`"src/api/**/*"`, `"**/routes/**/*"`] and API conventions (response shape, validation, error handling)
   *Why:* Separating API conventions into their own path-scoped rule means they only load when editing API files. This avoids consuming tokens with irrelevant context when working on frontend or infrastructure code.
   **You should see:** A file at .claude/rules/api-conventions.md with YAML frontmatter paths targeting API directories. The body contains at least three API conventions.
3. Create .claude/rules/terraform.md with paths: [`"terraform/**/*"`, `"**/*.tf"`] and infrastructure conventions
   *Why:* Infrastructure conventions are completely irrelevant when editing application code. Path-scoped rules ensure Terraform rules never consume tokens during React or API development sessions.
   **You should see:** A file at .claude/rules/terraform.md with YAML frontmatter paths matching Terraform files. The body contains infrastructure-specific conventions.
4. Edit a test file and use /memory to verify that testing rules are loaded but API and Terraform rules are not
   *Why:* This proves the conditional loading mechanism works. The exam tests whether you understand that path-specific rules load only for matching files, and /memory is the diagnostic tool to verify this.
   **You should see:** When editing a .test.ts file, /memory output lists .claude/rules/testing.md as loaded. The .claude/rules/api-conventions.md and .claude/rules/terraform.md files do NOT appear in the /memory output.
5. Edit an API handler and verify that API rules load while testing and Terraform rules do not
   *Why:* This is the complementary verification. Switching contexts should swap which rules are loaded, confirming that the glob patterns correctly scope each rule file.
   **You should see:** When editing a file in src/api/, /memory output lists .claude/rules/api-conventions.md as loaded. The testing and Terraform rule files do NOT appear.
6. Compare the token footprint when all conventions are in root CLAUDE.md versus split into path-specific rules
   *Why:* Token efficiency is a key exam concept. Root CLAUDE.md loads all conventions for every session regardless of relevance. Path-specific rules load only matching conventions, reducing irrelevant context and preserving token budget for actual work.
   **You should see:** With all conventions in root CLAUDE.md, /memory shows the full set of conventions loaded even when editing a simple utility file. With path-specific rules, /memory shows only the relevant subset. The token count for loaded configuration is measurably smaller when using path-specific rules for targeted editing sessions.
### 3.4. Practice Plan Mode vs Direct Execution Decision-Making
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/3-claude-code-config/3-4-plan-mode-execution#build-exercise)

1. Identify a complex multi-file task in a codebase (refactoring, migration, or restructuring) and use plan mode to explore dependencies and design an approach
   *Why:* Plan mode is for tasks with multiple valid approaches, architectural decisions, or multi-file modifications. The exam tests whether you choose plan mode upfront when complexity is stated in the requirements rather than waiting for surprises.
   **You should see:** Claude Code explores the codebase without modifying any files. The output includes: identified dependencies between modules, multiple possible approaches with tradeoffs, and a recommended implementation strategy. No files are changed during the planning phase.
2. Identify a simple single-file bug and use direct execution to fix it — observe the efficiency gain over planning
   *Why:* Direct execution is correct when the problem, location, and solution are all clear. The exam tests that you do not over-plan well-understood changes. The decision is about ambiguity, not difficulty.
   **You should see:** Claude Code makes the fix immediately without a planning phase. The change is confined to a single file or function. The total time from prompt to fix is noticeably shorter than the plan mode task above.
3. Use the hybrid approach: plan mode to design a migration strategy for a library change across multiple files, then switch to direct execution to implement the plan
   *Why:* The plan-then-execute hybrid is a specific pattern tested on the exam. Plan mode designs the strategy; direct execution applies it consistently. This is the correct approach for tasks like library migrations affecting many files.
   **You should see:** Phase 1 (plan): Claude identifies all files importing the old library, maps API differences, and produces a migration pattern. Phase 2 (execute): Claude applies the migration pattern file by file using the planned approach. The implementation is consistent across all files.
4. Use the Explore subagent for a verbose codebase discovery task and observe how it keeps the main conversation context clean
   *Why:* The Explore subagent isolates verbose discovery output so the main conversation context stays focused. Without isolation, extensive file listings and analysis fill the context window and degrade subsequent responses.
   **You should see:** The Explore subagent runs the discovery task and returns a concise summary to the main conversation. The full verbose output (file listings, dependency graphs, code excerpts) is not visible in the main conversation. Subsequent responses in the main conversation remain high quality.
5. Create a written decision framework: list your criteria for choosing plan mode vs direct execution, with examples for each
   *Why:* Internalising the decision criteria is essential for the exam. The framework should cover the key distinction: ambiguity determines the mode, not difficulty. A difficult but well-defined fix is direct execution; a simple-sounding feature with multiple approaches is plan mode.
   **You should see:** A clear decision framework with at least four criteria for plan mode and three for direct execution. Each criterion has a concrete example. The framework explicitly addresses the ambiguity-vs-difficulty distinction.
### 3.5. Practice Iterative Refinement Techniques
**Difficulty:** Beginner · **Estimate:** 30 minutes · [article](https://claudecertificationguide.com/learn/3-claude-code-config/3-5-iterative-refinement#build-exercise)

1. Describe a code transformation in prose and run it three times, noting how interpretation varies across runs
   *Why:* This demonstrates the core problem that concrete examples solve. Prose descriptions rely on interpretation, and interpretation varies across runs. Observing this inconsistency firsthand makes the case for switching to examples.
   **You should see:** Three different outputs from the same prose description. The variations may be subtle (different naming choices, different edge case handling) or significant (different structural approaches). This proves that prose alone produces inconsistent results.
2. Provide 2-3 concrete input/output examples of the same transformation and run it three times — compare the consistency
   *Why:* Concrete examples are the documented first-line technique for inconsistent interpretation. The model generalises from examples more reliably than from prose. This step proves the effectiveness difference experimentally.
   **You should see:** Three outputs that are consistent with each other and match the pattern established by the examples. The variation observed in the prose-only step is eliminated or drastically reduced.
3. Write a test suite for a function with happy path, edge cases, and error cases, then iterate by sharing test failures with Claude Code
   *Why:* Test-driven iteration is the most effective technique for complex transformations. Test failures provide unambiguous feedback — "Expected X, got Y" leaves no room for interpretation. This technique complements examples for more complex scenarios.
   **You should see:** After sharing test failures, Claude Code makes targeted fixes that address the specific failing assertions. Each iteration reduces the number of failing tests. The feedback loop is faster and more precise than prose-based corrections.
4. Use the interview pattern for a task outside your expertise — ask Claude to pose questions before implementing and note what considerations surface
   *Why:* The interview pattern is for unfamiliar domains where you might miss important requirements. It surfaces considerations an expert would know to address. The exam tests whether you can distinguish this from the examples technique — they solve different problems.
   **You should see:** Claude asks 5-10 targeted questions about requirements, edge cases, and constraints you had not considered. The questions reveal considerations like cache invalidation strategies, consistency requirements, failure modes, or security implications that would have been missed.
5. Practice batching: give Claude three interdependent issues in one message and observe whether the fix is coherent across all three
   *Why:* When issues interact, batching them in one message lets the model see all constraints simultaneously. Sequential fixing of interdependent issues causes the model to fix one issue in a way that conflicts with the others. The exam tests this distinction.
   **You should see:** A single coherent fix that addresses all three interdependent issues consistently. The error response shape, the logging format, and the type definitions all align with each other. Compare this to fixing them sequentially, where each fix might conflict with the next.
### 3.6. Set Up a CI/CD Pipeline with Claude Code
**Difficulty:** Advanced · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/3-claude-code-config/3-6-cicd-integration#build-exercise)

1. Write a CI script that runs Claude Code with the -p flag for non-interactive PR analysis
   *Why:* The -p flag is the single most directly testable fact in Domain 3. Without it, the CI job hangs indefinitely waiting for interactive input. This is Question 10 in the official sample questions.
   **You should see:** A CI script (GitHub Actions YAML, GitLab CI, or similar) that invokes claude -p with a review prompt. The job completes successfully without hanging. The output is printed to stdout and captured by the CI system.
2. Add --output-format json and --json-schema to produce structured findings with file, line, severity, and message fields
   *Why:* CI output must be machine-parseable. Automated systems need structured JSON to post inline PR comments, filter by severity, and track findings across runs. Human-readable text output cannot be reliably parsed by downstream tools.
   **You should see:** The Claude Code output is a JSON envelope whose structured_output field conforms to the specified schema. Each finding has file, line, severity, and message fields. Piping the output to jq .structured_output extracts the validated data without errors.
3. Configure the pipeline to parse the JSON output and post findings as inline PR comments
   *Why:* Inline PR comments at exact file and line numbers provide actionable feedback. Generic PR-level comments are ignored. Structured JSON output makes precise inline commenting possible.
   **You should see:** Each finding from the JSON output appears as an inline comment on the PR at the exact file and line number. Severity levels are visible. Developers can see the finding in context alongside the code it references.
4. Add a section to CLAUDE.md documenting testing standards, available fixtures, and review criteria for CI-invoked Claude Code
   *Why:* Claude Code reads CLAUDE.md in CI just as in interactive mode. Without project context, CI-invoked test generation produces low-value boilerplate. With testing standards and fixture documentation, generated tests follow team patterns.
   **You should see:** The CLAUDE.md file contains a clearly marked CI-relevant section with testing standards, available fixture paths, and review severity criteria. CI-invoked Claude Code produces tests using the documented factories and fixtures rather than generic boilerplate.
5. Set up two separate Claude Code invocations: one for code generation and an independent one for review (no shared session context)
   *Why:* The same session that generated code is less effective at reviewing it because it retains reasoning context that biases it toward its own decisions. Independent review instances evaluate code on its own merits without prior justification bias.
   **You should see:** Two distinct claude -p invocations in the CI script: one for generation and one for review. They share no session context. The review invocation analyses the generated code independently. The review findings are more thorough than self-review in the same session.
6. Implement incremental review: store previous findings, include them in the next review run, and instruct Claude to report only new or still-unaddressed issues
   *Why:* Without incremental context, each review run analyses the entire PR from scratch and produces duplicate comments. Duplicate comments erode developer trust — when the same five issues appear on every push regardless of fixes, developers stop reading them.
   **You should see:** The first review run produces findings and stores them (as a JSON artifact or file). Subsequent runs include the previous findings in context. The output contains only new issues or issues that remain unaddressed. Previously fixed issues do not reappear as comments.
## Domain 4 · Prompt Engineering & Structured Output

### 4.1. Build an Explicit Criteria Code Review Prompt
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/4-prompt-engineering/4-1-system-prompts#build-exercise)

1. Write a system prompt with vague instructions (be conservative, only flag important issues) and test it against 5 code snippets containing known bugs, security issues, and style nitpicks
   *Why:* Establishing a baseline with vague instructions demonstrates the false positive problem the exam tests. You need empirical evidence that phrases like be conservative give the model no actionable decision boundary.
   **You should see:** Inconsistent classification across the 5 snippets: some style nitpicks flagged as critical, some genuine bugs missed or marked minor, and different results if you run the same snippets twice.
2. Rewrite the prompt with explicit categorical criteria: define exactly which issues to report (bugs, security vulnerabilities) and which to skip (style preferences, local patterns)
   *Why:* Explicit categorical criteria are the correct approach tested on the exam. This step demonstrates that concrete categories eliminate the ambiguity that causes false positives.
   **You should see:** The rewritten prompt has clear categories: report bugs and security vulnerabilities, skip style preferences and local patterns, flag comments only when claimed behaviour contradicts actual code behaviour.
3. Add concrete code examples for each severity level — critical, major, minor — showing actual code patterns, not prose descriptions
   *Why:* The exam specifically tests that code examples outperform prose descriptions for severity calibration. Prose like issues that could cause system failures forces the model to interpret, while code examples remove ambiguity entirely.
   **You should see:** Your prompt now contains at least one code snippet per severity level, each showing the actual pattern that defines that severity, not a prose description of what that severity means.
4. Compare false positive rates between the two versions on the same test set and document which approach produces more consistent classification
   *Why:* Quantifying the improvement validates the explicit criteria approach and builds the evaluation skill the exam expects. You should be able to articulate why one approach outperforms the other with data, not intuition.
   **You should see:** A clear reduction in false positives with the explicit criteria version. The vague prompt should produce 30-50% inconsistency while the explicit criteria version should be below 15%. Classification should be stable across repeated runs.
5. Temporarily disable any category with above 25% false positive rate and document the criteria refinements needed before re-enabling
   *Why:* The trust recovery strategy is a key exam concept: high false positive rates in one category destroy developer trust in ALL categories. Disabling problematic categories restores system-wide trust while you iterate on their criteria.
   **You should see:** A document listing which categories exceed the 25% threshold, what specific criteria refinements are needed (e.g., add code examples for edge cases), and a re-enablement plan with target false positive rates.
### 4.2. Build a Few-Shot Enhanced Extraction Prompt
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/4-prompt-engineering/4-2-few-shot-prompting#build-exercise)

1. Create a base extraction prompt with detailed instructions but no examples and test it against 10 documents with varied structures: tables, narrative paragraphs, mixed formats
   *Why:* Establishing a baseline without examples demonstrates the consistency problem the exam tests. Detailed instructions alone produce inconsistent output across varied document structures, which is the exact trigger for deploying few-shot examples.
   **You should see:** Inconsistent extraction results across the 10 documents: fields extracted correctly from tables but empty or wrong from narrative paragraphs, different output formats across runs, and inconsistent handling of edge cases.
2. Record which fields are consistently empty or inconsistent across document structures
   *Why:* Identifying the specific failure patterns tells you exactly what your few-shot examples need to demonstrate. The exam tests whether you can diagnose the problem before prescribing the solution.
   **You should see:** A table or log showing which fields fail on which document types. Typical pattern: dates extracted correctly from tables but missed in narrative text, amounts inconsistent when written in words rather than digits, line items empty when embedded in paragraphs.
3. Create 3 few-shot examples targeting the failing patterns — each must include reasoning explaining why the extraction was done that way
   *Why:* Examples with reasoning teach the model to generalise to novel patterns, not just match specific cases. Without reasoning, the model learns only surface-level pattern matching. The exam specifically tests that reasoning-included examples outperform input-output pairs.
   **You should see:** Three examples, each showing a different document structure (table, narrative, mixed), with the correct extraction AND a reasoning section explaining how the data was located and why the extraction decisions were made.
4. Re-run the same 10 documents with the few-shot enhanced prompt and compare: empty field rate, format consistency, and extraction accuracy
   *Why:* Quantifying the improvement demonstrates the effectiveness of few-shot examples as the first-choice technique for consistency problems. The exam expects you to know that few-shot examples outperform additional instructions for this class of problem.
   **You should see:** A measurable reduction in empty fields (especially on narrative documents), improved format consistency across document types, and higher overall extraction accuracy. The improvement should be most dramatic on the document types that previously failed.
5. Document which structural patterns benefit most from few-shot examples and which require different techniques like schema changes
   *Why:* The exam tests whether you can match the right technique to the right problem. Few-shot examples fix consistency and structural variety issues, but malformed JSON needs tool_use, fabricated values need nullable schemas, and sum discrepancies need validation loops.
   **You should see:** A decision matrix showing which problem types improved with few-shot examples and which still need other interventions. Narrative extraction and format consistency should improve. Fabrication of missing data should not improve and needs schema changes instead.
### 4.3. Build a Structured Extraction Tool with JSON Schema
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/4-prompt-engineering/4-3-structured-output#build-exercise)

1. Define an extraction tool with a JSON schema: 3 required fields, 3 optional/nullable fields, an enum with unclear and other options, and a detail string field for the other category
   *Why:* Schema design directly prevents fabrication. Required fields pressure the model to invent values when information is absent. Optional/nullable fields allow honest null responses. This is the root cause fix for hallucinated extraction data.
   **You should see:** A valid JSON schema with required array containing only the 3 always-present fields, nullable type definitions for optional fields, and an enum array including unclear and other alongside the standard categories.
2. Test with tool_choice auto and observe cases where the model returns text instead of calling the tool
   *Why:* The exam tests the distinction between auto, any, and forced tool_choice. Auto allows the model to respond conversationally instead of calling a tool, which means no guaranteed structured output. You need to see this failure mode firsthand.
   **You should see:** At least one response where the model returns a text message describing the document contents instead of calling the extraction tool. This demonstrates why auto is unsuitable when you need guaranteed structured output.
3. Switch to tool_choice any and verify the model always returns structured output via a tool call
   *Why:* tool_choice any guarantees a tool call while letting the model choose which tool. This is the correct setting for guaranteed structured output when the document type is unknown, a key exam distinction from auto.
   **You should see:** Every response has stop_reason of tool_use and contains a valid tool call with structured output conforming to your schema. No text-only responses.
4. Force a specific tool with tool_choice {type: tool, name: extract_metadata} and verify the mandatory extraction step runs
   *Why:* Forced tool selection ensures a mandatory first step executes regardless of the model decision. The exam tests this for scenarios like metadata extraction that must run before enrichment steps.
   **You should see:** The response always calls the exact tool you specified, even when the document content might suggest a different tool would be more appropriate. The model has no flexibility in tool selection.
5. Process 5 documents — 3 with complete data and 2 with missing fields — and verify nullable fields return null rather than fabricated values
   *Why:* This validates the most important schema design principle: optional/nullable fields prevent fabrication. The exam specifically tests the scenario where required fields pressure the model to invent plausible-looking data for absent information.
   **You should see:** For the 3 complete documents, all fields populated with correct values. For the 2 documents missing information, the nullable fields return null instead of fabricated values. No invented dates, amounts, or identifiers.
### 4.4. Build a Validation-Retry Loop for Document Extraction
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/4-prompt-engineering/4-4-validation-retry-loops#build-exercise)

1. Define an extraction tool with calculated_total and stated_total fields, a conflict_detected boolean, and detected_pattern fields for tracking which constructs trigger findings
   *Why:* Self-correction fields like calculated_total vs stated_total enable automatic discrepancy detection without external logic. conflict_detected booleans and detected_pattern fields create the data foundation for systematic prompt improvement.
   **You should see:** A JSON schema with separate calculated_total and stated_total number fields, a total_discrepancy boolean, a conflict_detected boolean, and a detected_pattern string field on each finding in the line_items array.
2. Implement validation logic that checks: field completeness, numerical consistency (calculated sum matches stated total), enum validity, and date ordering
   *Why:* Semantic validation catches errors that tool_use cannot. The exam distinguishes schema syntax errors (eliminated by tool_use) from semantic errors (wrong sums, misplaced values) that require validation logic and retry loops.
   **You should see:** A validation function that returns an array of specific, actionable error messages. Each error should state what was expected versus what was found, not just that validation failed.
3. Build the retry loop: on validation failure, construct a follow-up message containing the original document, the failed extraction, and the specific validation error
   *Why:* Retry-with-error-feedback is dramatically more effective than naive retries. Without the specific error, the model has no guidance and typically reproduces the same mistake. With the error, the model can target its self-correction.
   **You should see:** A retry message that includes all three elements: the original document text, the JSON of the failed extraction, and the specific validation error string. The model should produce a corrected extraction on retry.
4. Test with 5 documents: 2 with fixable errors (misplaced values, wrong totals) and 3 with unfixable errors (absent information) — verify the loop retries only fixable cases
   *Why:* The retry effectiveness boundary is the most aggressively tested concept in this task statement. Retries fix format mismatches and structural errors but cannot create information absent from the source. The exam presents both scenarios and expects you to identify which is fixable.
   **You should see:** The 2 fixable documents succeed after 1-2 retries with corrected totals or field placements. The 3 unfixable documents are correctly identified as having absent information and flagged for human review rather than retried.
5. Log detected_pattern data for each finding and analyse which patterns are most frequently dismissed to identify prompt refinement priorities
   *Why:* detected_pattern fields create a systematic improvement loop. When developers consistently dismiss findings triggered by a specific pattern, that pattern likely needs prompt refinement. This turns dismissal data into actionable prompt improvement priorities.
   **You should see:** A log or table showing each detected_pattern, its frequency, its dismissal rate, and a prioritised list of patterns needing prompt refinement. Patterns with high dismissal rates should be at the top.
### 4.5. Design a Batch Processing Strategy
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/4-prompt-engineering/4-5-batch-processing#build-exercise)

1. List 5 workflows in a hypothetical organisation and categorise each as blocking (synchronous) or latency-tolerant (batch-eligible) with justification
   *Why:* The matching rule between synchronous and batch API is the most tested concept in this task statement. The exam presents a scenario where a manager proposes switching everything to batch for cost savings, and you must identify which workflows cannot tolerate the 24-hour processing window.
   **You should see:** A table with 5 workflows, each clearly categorised with justification. Blocking workflows have someone or something waiting for the result. Batch-eligible workflows consume results later with no real-time dependency.
2. Define a batch submission for 20 documents using the Message Batches API format with unique custom_id fields for each document
   *Why:* custom_id fields are the mechanism for correlating request-response pairs in batch results. Without unique identifiers, you cannot determine which documents succeeded or failed, making failure handling impossible.
   **You should see:** A valid batch request object with 20 entries, each containing a unique custom_id, model specification, max_tokens, and a messages array with the document content.
3. Implement failure handling: parse batch results, identify failures by custom_id, and construct a retry batch containing only failed documents with increased max_tokens
   *Why:* Resubmitting only failures with targeted modifications is the correct batch failure pattern. Resubmitting the entire batch wastes cost on already-successful documents. The exam tests that you understand custom_id correlation and targeted retry.
   **You should see:** A failure handler that filters results by error status, extracts the custom_id values of failures, looks up the original documents, and creates a retry batch with modifications like increased max_tokens or chunked content.
4. Calculate the batch submission frequency needed to guarantee a 30-hour SLA given the 24-hour maximum processing window
   *Why:* SLA calculation with the 24-hour batch processing window is a direct exam test point. You must work backwards from the SLA deadline to determine when to submit, accounting for the maximum processing time plus a safety margin.
   **You should see:** A calculation showing: 30-hour SLA minus 24-hour maximum processing window equals 6 hours of buffer. Submission must occur at least 30 hours before the deadline, with batches submitted every 4-6 hours to guarantee the SLA with margin.
5. Create a 5-document sample set and refine extraction prompts iteratively before submitting the full batch of 20 documents
   *Why:* Prompt refinement on a sample set before batch submission is the most cost-effective batch processing strategy. A 90% first-pass success rate means 2 retries on 20 documents. A 60% first-pass rate means 8 retries, four times the resubmission cost.
   **You should see:** A sample set covering the range of document types and edge cases, 2-3 prompt iterations improving accuracy on the sample, and then the full batch submission achieving a high first-pass success rate.
### 4.6. Build a Multi-Pass Code Review System
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/4-prompt-engineering/4-6-multi-pass-review#build-exercise)

1. Create a single-pass review prompt and run it against a 10-file mock PR — document instances of inconsistent depth, missed issues, and contradictory findings
   *Why:* Establishing the single-pass baseline demonstrates the three symptoms of attention dilution: inconsistent depth across files, missed bugs in the middle of the review, and contradictory findings flagging the same pattern differently in different files.
   **You should see:** Detailed feedback on some files (typically first and last) but superficial comments on others, at least one obvious bug missed in a middle file, and at least one contradictory finding where the same code pattern is flagged as problematic in one file but approved in another.
2. Implement per-file local analysis: iterate over each file with a focused review prompt that examines only that file for bugs, security issues, and logic errors
   *Why:* Per-file analysis ensures every file receives consistent, focused attention. Each invocation examines only one file, eliminating the attention dilution that causes inconsistent depth and missed bugs in single-pass reviews.
   **You should see:** Consistent review depth across all 10 files. Bugs that were missed in the single-pass review should now be caught, especially those in the middle files. Each review should be focused and thorough.
3. Implement a cross-file integration pass: feed all per-file findings into a separate prompt that checks for data flow inconsistencies, contradictory findings across files, and API contract violations
   *Why:* Per-file analysis catches local issues but misses cross-file concerns: data flow between modules, consistent API usage, and contradictions in per-file findings. The integration pass is a separate invocation that receives all findings and checks for systemic issues.
   **You should see:** A synthesis output identifying cross-file issues that no single-file review could catch: data passed between modules in incompatible formats, contradictory findings from per-file reviews, and API contracts violated across service boundaries.
4. Add confidence scoring to each finding (0.0-1.0) and implement routing: high confidence findings go directly to the developer, low confidence findings go to a human review queue
   *Why:* Confidence-based routing directs limited human reviewer attention to the findings that need it most. The exam distinguishes raw uncalibrated confidence from calibrated thresholds validated against labelled sets.
   **You should see:** Each finding annotated with a confidence score, reasoning for the score, and a routing decision (direct_report or human_review). The routing threshold should separate clear-cut findings from uncertain ones.
5. Use a separate Claude instance (fresh session, no prior context) to review a subset of the generated findings and compare its assessment to the original confidence scores for calibration
   *Why:* Independent review instances approach output fresh without the bias of I chose this because reasoning. This step calibrates confidence thresholds by comparing self-reported confidence against independent assessment, the method the exam identifies as the correct approach.
   **You should see:** A calibration dataset showing the relationship between reported confidence scores and independent verification results. Some high-confidence findings may be overturned, revealing calibration gaps that adjust your routing thresholds.
## Domain 5 · Context Management & Reliability

### 5.1. Build a Persistent Case Facts Context Manager
**Difficulty:** Intermediate · **Estimate:** 45 minutes · [article](https://claudecertificationguide.com/learn/5-context-management/5-1-context-window-management#build-exercise)

1. Create a case facts extractor that identifies transactional data (amounts, dates, order numbers, statuses) from tool results
   *Why:* The persistent case facts block is the single most important pattern in context window management. Extracting transactional facts into a structured block that is never summarised prevents the progressive summarisation trap from destroying critical numerical values and identifiers.
   **You should see:** A function that takes raw tool output and returns a structured object containing only the transactional facts: customer ID, order numbers, amounts, dates, and statuses. Non-transactional narrative content should be excluded.
2. Implement a persistent case facts block that is prepended to every prompt, outside summarised history
   *Why:* The case facts block must persist across every turn regardless of what happens to the conversation history. It sits outside the summarised portion of the context, ensuring amounts, dates, and order numbers survive even when earlier conversation turns are compressed.
   **You should see:** A prompt construction function that always includes the case facts block at the top of every message, followed by any summarised history, followed by the current turn. The case facts block should be clearly delimited with a section header.
3. Build a tool result trimmer that filters order lookup responses from 40+ fields to only the 5 relevant return-related fields
   *Why:* Untrimmed tool results are a silent context budget killer. An order lookup returning 40+ fields consumes tokens in every subsequent turn as conversation history grows. Trimming to relevant fields before results enter context is essential, not optional.
   **You should see:** A trimming function that takes a raw tool result object and returns only the fields needed for the current task. The trimmed result should be 80-90% smaller than the original.
4. Test with a multi-turn conversation where summarisation occurs and verify that transactional facts survive intact across all turns
   *Why:* This validates that the persistent case facts pattern actually works. The exam tests whether you understand that progressive summarisation destroys specific amounts and dates, and the case facts block is the fix. You need to verify this empirically.
   **You should see:** A 6-8 turn conversation where summarisation occurs after turn 4. After summarisation, the agent should still reference the exact refund amount ($247.83), order number (#8891), and date (March 3rd) from the case facts block. Without the block, these values would be lost to summarisation.
5. Add key findings placement logic that positions summaries at the beginning of aggregated inputs to mitigate the lost-in-the-middle effect
   *Why:* Models process information at the beginning and end of long inputs reliably, but findings buried in the middle may be missed. Placing key findings summaries at the start of aggregated inputs is a structural fix for this well-documented phenomenon.
   **You should see:** An aggregation function that places a Key Findings Summary section at the top of combined inputs, followed by detailed results with explicit section headers. The key findings should be concise bullet points drawn from the detailed content.
### 5.2. Build an Escalation Decision Engine
**Difficulty:** Intermediate · **Estimate:** 40 minutes · [article](https://claudecertificationguide.com/learn/5-context-management/5-2-escalation-ambiguity#build-exercise)

1. Create a system prompt with explicit escalation criteria covering all three valid triggers: explicit human request, policy exceptions/gaps, and inability to make progress
   *Why:* Explicit escalation criteria in the system prompt are the proportionate first response before adding infrastructure like classifier models or sentiment analysis. The exam tests that prompt optimisation should always precede architectural changes for escalation calibration.
   **You should see:** A system prompt with three clearly defined escalation triggers, each with a description and decision rule. The prompt should also explicitly list the two anti-patterns (sentiment-based and confidence-based escalation) as things to avoid.
2. Add few-shot examples showing: immediate escalation for explicit human request, autonomous resolution for a frustrated customer with a straightforward issue, and escalation for a policy gap
   *Why:* Few-shot examples demonstrating when to escalate versus when to resolve autonomously directly address unclear decision boundaries. This is the exact technique the exam identifies as the correct improvement for a support agent with poor first-contact resolution rates.
   **You should see:** Three examples in the system prompt, each showing a different scenario with the correct decision and reasoning. The frustrated-but-resolvable example should show the agent acknowledging frustration and offering the resolution directly.
3. Implement ambiguous customer matching logic that requests additional identifiers (email, phone, order number) instead of selecting heuristically
   *Why:* Selecting from ambiguous matches using heuristics (most recent, most active) risks privacy violations and incorrect actions. The exam tests that the only safe response to multiple customer matches is to ask for additional identifiers to disambiguate.
   **You should see:** A matching function that detects when multiple records are returned and immediately asks for disambiguation rather than applying any selection heuristic. The disambiguation request should suggest specific identifier types.
4. Test with four scenarios: frustrated customer with simple issue, calm customer requesting policy exception, customer explicitly requesting a human, and ambiguous customer match
   *Why:* These four scenarios cover all critical decision boundaries the exam tests: the frustration nuance, policy gap versus violation distinction, absolute rule for explicit human requests, and privacy-safe disambiguation.
   **You should see:** Correct handling of all four scenarios: resolution offered for the frustrated customer, escalation for the policy gap, immediate escalation for the explicit human request (no investigation first), and disambiguation request for the ambiguous match.
5. Verify the agent never attempts investigation before honouring an explicit human request and never selects from ambiguous matches using heuristics
   *Why:* These are the two absolute rules the exam tests with no exceptions. Any attempt to investigate before escalating on an explicit human request, or any heuristic selection from ambiguous matches, is a critical failure that would cost marks on the exam.
   **You should see:** For explicit human requests: the escalation happens in the very first response with zero investigation steps. For ambiguous matches: the response always asks for additional identifiers, never selects a record. Both rules should hold across multiple phrasings and edge cases.
### 5.3. Build a Structured Error Propagation System
**Difficulty:** Advanced · **Estimate:** 50 minutes · [article](https://claudecertificationguide.com/learn/5-context-management/5-3-error-propagation#build-exercise)

1. Define a structured error schema with fields: failureType (transient/validation/business/permission), attemptedAction (tool, query, parameters), partialResults (array of any retrieved data), and alternativeApproaches (suggested recovery strategies)
   *Why:* Structured error context enables intelligent coordinator recovery. The four elements give the coordinator everything it needs to decide: retry, try an alternative, proceed with partial results, or escalate. Generic error messages like search unavailable prevent all informed recovery.
   **You should see:** A TypeScript interface or JSON schema with failureType as an enum of the four categories, attemptedAction as an object with tool/query/parameters, partialResults as an array, and alternativeApproaches as a string array. Each field should have a description explaining its purpose.
2. Implement a subagent that distinguishes access failures (timeout, connection error) from valid empty results (successful query, no matches) in its error reporting
   *Why:* Conflating access failures with valid empty results is a critical error the exam tests directly. Access failures mean the query did not execute and should be retried. Valid empty results mean the query succeeded and found nothing, which IS the answer. Treating them the same leads to either never retrying when you should or wasting time retrying queries that will always return nothing.
   **You should see:** A subagent function that catches exceptions (timeouts, connection errors) and reports them as access failures with shouldRetry: true, while successful queries returning no results are reported as success with an empty results array and shouldRetry: false.
3. Build local retry logic for transient failures within the subagent (3 retries with exponential backoff) before propagating to the coordinator
   *Why:* Subagents should handle their own transient failures locally before escalating. This reduces coordinator complexity as the coordinator does not need to manage retry logic for every possible transient failure across every subagent. Only persistent failures that survive local retry should propagate.
   **You should see:** A retry wrapper with exponential backoff (e.g., 1s, 2s, 4s) that attempts the operation up to 3 times before propagating the structured error to the coordinator. Partial results gathered before failure should be preserved across retries.
4. Create a coordinator that receives structured errors and decides between retry with modified query, alternative approach, or proceed with partial results
   *Why:* The coordinator is the intelligent recovery decision-maker. With structured error context, it can make informed choices rather than applying blanket policies. This is the correct middle ground between silent suppression (ignoring failures) and workflow termination (killing the pipeline on one failure).
   **You should see:** A coordinator function that examines the failure type, checks partial results, evaluates alternative approaches, and selects the appropriate recovery strategy. It should handle all four failure types differently and never silently suppress errors.
5. Add coverage annotations to synthesis output noting which findings are well-supported versus which topic areas have gaps due to unavailable sources
   *Why:* Coverage annotations let the consumer know what the report covers fully and where there are known limitations. Without them, a gap looks like the topic was not relevant rather than the source being unavailable. This transparency is far better than silently omitting topics.
   **You should see:** A synthesis output that includes a coverage section listing each topic area with its data quality status: well-supported, limited (with reason), or unavailable (with reason). Failed subagent topics should be explicitly noted, not silently omitted.
### 5.4. Build a Context-Resilient Codebase Explorer
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/5-context-management/5-4-codebase-exploration#build-exercise)

1. Create a coordinator agent that delegates specific codebase exploration tasks to subagents (e.g., find test files, trace dependency chains, identify external integrations)
   *Why:* Subagent delegation is primarily about context isolation, not parallelisation. The main agent context stays clean for high-level coordination while subagents handle verbose exploration. This directly prevents context degradation by keeping verbose file contents and search results out of the coordinator context.
   **You should see:** A coordinator function that spawns subagents with specific, focused investigation prompts. Each subagent returns a structured summary (key findings, file paths, class names) rather than raw verbose output. The coordinator context should remain clean.
2. Implement scratchpad file management: agents write key findings (class names, file paths, dependency chains) to a known file and read it before subsequent exploration steps
   *Why:* Scratchpad files are the primary mitigation for context degradation. They persist knowledge outside the conversation context, making it immune to the attention shift that causes the model to reference typical patterns instead of specific class names and file paths it discovered earlier.
   **You should see:** An agent that writes structured findings to a scratchpad file after each exploration step and reads the scratchpad at the start of each subsequent step. The scratchpad should contain specific class names, file paths, and dependency chains, not summaries.
3. Build summary injection logic: after Phase 1 exploration, summarise findings and inject the summary into Phase 2 subagent prompts
   *Why:* Summary injection prevents the cold start problem where Phase 2 subagents duplicate Phase 1 exploration because they were not given previous findings. It ensures Phase 2 agents have the architectural understanding needed to ask the right questions without rediscovering the system structure.
   **You should see:** A Phase 1 summary document that captures the high-level architecture, key concerns, and specific investigation targets for Phase 2. This summary is injected into the initial prompt of every Phase 2 subagent.
4. Implement crash recovery: each agent exports structured state (explored paths, key findings, next steps) to a manifest file that the coordinator loads on resume
   *Why:* Extended exploration sessions can fail from crashes, network interruptions, or context exhaustion. Without recovery mechanisms, all progress is lost. Structured state manifests enable the coordinator to resume from the last checkpoint rather than restarting from scratch.
   **You should see:** A manifest file in JSON format containing the session ID, current phase, explored paths, key findings, and next steps. On resume, the coordinator loads this manifest and injects it into agent prompts so exploration continues from where it left off.
5. Test context degradation by running an extended exploration session across multiple modules and verify that scratchpad files preserve specific class names and file paths that would otherwise degrade to generic descriptions
   *Why:* This validates that the scratchpad mitigation actually works against context degradation. The observable symptom is the model referencing typical patterns instead of specific classes and paths. You need to confirm that scratchpad files prevent this degradation.
   **You should see:** Two comparison runs: one without scratchpad files where the agent degrades to generic references after exploring 4-5 modules, and one with scratchpad files where the agent maintains specific class names and file paths throughout the entire session.
### 5.5. Build a Confidence-Calibrated Review Router
**Difficulty:** Advanced · **Estimate:** 50 minutes · [article](https://claudecertificationguide.com/learn/5-context-management/5-5-human-review-calibration#build-exercise)

1. Create a mock extraction system that outputs field-level confidence scores for different document types (invoices, receipts, scanned PDFs, international documents)
   *Why:* Field-level confidence scores are the foundation of intelligent review routing. The exam tests that raw model confidence is not calibrated and must be validated against ground truth before use. Building the mock system gives you data to calibrate against.
   **You should see:** An extraction function that returns each field with its value and a confidence score between 0.0 and 1.0. The system should process at least 4 document types with noticeably different confidence distributions per type.
2. Implement accuracy tracking broken down by document type and field segment — not just aggregate metrics
   *Why:* The aggregate metrics trap is the most dangerous misconception in production extraction systems. 97% overall accuracy can hide catastrophic failure rates on specific document types because standard invoices dominate the volume. The exam tests that you must validate by document type AND field segment before automating.
   **You should see:** An accuracy table showing each document type and field combination separately. Standard invoices should show 95%+ accuracy while handwritten receipts and international documents show 40-70%. The aggregate should look excellent (90%+) despite the poor per-type numbers.
3. Build a calibration module that takes a labelled validation set (ground truth) and produces calibrated confidence thresholds per field type per document type
   *Why:* Raw model confidence scores are not calibrated. A model reporting 0.90 confidence might actually be correct 94% of the time on date fields but only 82% on amount fields. Calibration using labelled validation sets is required before confidence scores can drive automated routing decisions.
   **You should see:** A calibration curve for each field type per document type, mapping reported confidence ranges to actual accuracy percentages. The curve should reveal that the same confidence score means different things for different field-document combinations.
4. Implement stratified random sampling that selects high-confidence extractions for ongoing verification, sampling proportionally across all document types
   *Why:* High-confidence extractions are automated and not reviewed. If the model develops a novel error pattern affecting high-confidence items, only stratified sampling will catch it. Sampling only low-confidence items leaves you blind to systematic errors in automated extractions.
   **You should see:** A sampling function that selects a representative subset from each stratum (document type and confidence band), including samples from the high-confidence automated extractions. The sample should be proportional to the volume in each stratum.
5. Build a review router that prioritises limited reviewer capacity on the highest-uncertainty items, dynamically reordering the review queue as new extractions arrive
   *Why:* Human reviewers are expensive and limited. Spreading capacity evenly across all extractions wastes time on high-confidence items while leaving insufficient capacity for uncertain items that need human judgement. Dynamic priority ordering ensures the most uncertain items are always reviewed first.
   **You should see:** A priority queue that orders items by uncertainty (lowest confidence first), dynamically reorders as new extractions arrive, and serves the next-highest-uncertainty item to each available reviewer. The queue should never serve items in chronological order.
### 5.6. Build a Provenance-Preserving Synthesis Pipeline
**Difficulty:** Advanced · **Estimate:** 60 minutes · [article](https://claudecertificationguide.com/learn/5-context-management/5-6-information-provenance#build-exercise)

1. Define a structured claim-source mapping schema with fields: claim, sourceUrl, documentName, relevantExcerpt, publicationDate
   *Why:* Every finding in a multi-agent research system must carry its provenance. Without structured claim-source mappings, attribution dies during summarisation and the final output becomes untraceable plausible-sounding text with no verifiable sources.
   **You should see:** A TypeScript interface or JSON schema with all five required fields: claim (the assertion), sourceUrl (where found), documentName (title), relevantExcerpt (supporting passage), and publicationDate (when published or data collected). Each field should be required, not optional.
2. Implement two research subagents that output findings using the claim-source mapping schema, including publication dates
   *Why:* Subagents must output in the structured format from the start. If subagents return unstructured prose, attribution is already lost before synthesis begins. Requiring structured output at the subagent level is the foundation of end-to-end provenance.
   **You should see:** Two subagent functions that each return an array of ClaimSourceMapping objects with all fields populated, including publication dates. Each subagent should research a different aspect of the same topic.
3. Build a synthesis agent that merges findings from both subagents while explicitly preserving all claim-source mappings through the merge process
   *Why:* Step 3 (synthesis) is the most common failure point for attribution. The synthesis agent naturally compresses and paraphrases, destroying claim-source mappings unless explicitly instructed to preserve them. The exam tests whether you understand that attribution must be explicitly maintained through every synthesis step.
   **You should see:** A synthesis output where every claim is traceable to its source. The synthesis should combine related findings but maintain inline citations or a reference section linking each claim to its original source URL, document name, and publication date.
4. Handle conflicting sources by annotating both values with full attribution and possible explanations, without arbitrarily selecting one value
   *Why:* When two credible sources report different statistics, arbitrarily selecting one destroys information and presents false certainty. The exam tests that the correct approach is to annotate both values with source attribution and let the consumer decide. Different publication dates often explain different numbers as trends, not contradictions.
   **You should see:** A conflict handling function that detects overlapping claims with different values, preserves both with full attribution, and adds a possible explanation noting temporal or methodological differences. The output should never silently pick one value.
5. Implement content-appropriate rendering in the final output: format financial data as tables, news findings as prose, and technical findings as structured lists
   *Why:* The exam tests that synthesis should not flatten everything into a uniform format. Financial data is most readable as tables, news context reads naturally as prose, and technical findings are clearest as structured lists. Forcing all content into one format degrades readability.
   **You should see:** A rendering function that detects the content type of each section and applies the appropriate format. Financial data should appear in tables with columns for year, value, and source. News should be prose paragraphs. Technical findings should be bulleted lists.
## Fill-in exercises (custom additions)

Four exercises written to cover gaps found by cross-checking the scraped set against the Ravn study guide (fork_session, Explore-subagent isolation, @path depth limit, /compact + /memory). Format matches the scraped set.

### F1. Compare Approaches in Parallel with fork_session
**Difficulty:** Intermediate · **Estimate:** 40 minutes · [guide](https://ravnhq.github.io/claude-certified-architect/guides/en.html)

[full file](exercise-fill-in-1.md)

1. Start a Claude Code session that investigates a shared problem, for example: "This React app re-renders too often. Map the component tree and identify where state lives."
   *Why:* fork_session branches from *shared* context. You need a completed investigation phase first so both forks inherit the same discoveries. Without shared groundwork, you are not forking — you are just starting two independent sessions.
   **You should see:** A session that has mapped the component tree and located the state-holding components, with the findings present in context. No new code written yet.
2. Fork the session twice: fork A gets the prompt "Implement a fix using Redux", fork B gets "Implement a fix using Context API".
   *Why:* Both forks inherit everything up to the branch point and then diverge independently. This is the exact exam use case: comparing viable implementation approaches from a common understanding without re-explaining the investigation to either branch.
   **You should see:** Two independent sessions whose contexts both contain the original investigation. Neither fork sees the other's work. Each pursues only its assigned approach.
3. Let each fork complete a minimal implementation and record the results: lines changed, new dependencies, and any trade-offs each fork surfaced.
   *Why:* The value of forking is a like-for-like comparison. Because both branches started from identical context, differences in the outcome are attributable to the approach, not to uneven information.
   **You should see:** Two implementations you can compare directly: same investigation baseline, different solutions. Each fork's summary lists files touched, new dependencies (Redux adds one; Context API adds none), and discovered trade-offs.
4. Decide which approach to keep and discard the losing branch.
   *Why:* Forking is explicitly for exploring alternatives in parallel — the losing branch costs nothing and leaves no trace in the winning session. The exam contrasts this with the alternative: serially trying approach A, then reverting and trying B, which pollutes one session's context with a dead end.
   **You should see:** One surviving session with the chosen implementation. The abandoned approach's context is gone — no dead-code exploration lingering in the session you continue in.
5. Write down when you would fork versus when you would start a fresh session or use --resume, in three rules.
   *Why:* The exam tests the boundary between the three session strategies. fork_session is for branching alternatives from shared context; --resume is for continuing work when files are unchanged; fresh-start-with-summary is for when prior tool results have gone stale.
   **You should see:** Three written rules. Example: fork when comparing approaches from a shared investigation; resume when continuing unchanged work; fresh-start when files changed since the last session. Each rule names the trap it avoids.

### F2. Isolate Verbose Discovery with an Explore Subagent
**Difficulty:** Intermediate · **Estimate:** 40 minutes · [guide](https://ravnhq.github.io/claude-certified-architect/guides/en.html)

[full file](exercise-fill-in-2.md)

1. Pick a verbose codebase discovery task, for example: "Trace every import chain that reaches the payments module." Estimate its raw output size before running it.
   *Why:* The Explore subagent exists for one reason: verbose discovery output exhausts the main context window and degrades every later response in the session. You need a task chatty enough that running it inline would visibly pollute context — file listings, import chains, code excerpts across a dozen files.
   **You should see:** A task whose full raw output would span dozens of files and thousands of tokens, and a rough token estimate of that output written down before you run anything.
2. Run the task inline in the main session and note the effect on the conversation.
   *Why:* You need the baseline failure mode firsthand. Inline discovery dumps every intermediate file and search result into the main context, where it stays for the rest of the session. The exam treats "main agent reads 15 files directly" as the anti-pattern this exercise replaces.
   **You should see:** The main conversation context filled with file contents and search results. Ask a follow-up question afterwards and note that the model's answers now compete with a large volume of discovery noise.
3. Repeat the same task delegated to an Explore subagent and compare what enters the main context.
   *Why:* The Explore subagent isolates verbose output and returns only a summary. The main agent keeps one line — "Payments depends on AuthService, OrderModel, and the external PaymentGateway API" — instead of 15 files. The exam names this as the correct defence against context-window exhaustion in multi-phase tasks.
   **You should see:** The main conversation receives a concise structured summary: key findings, file paths, class names. The raw listings and excerpts never appear in the main context. A follow-up question is answered without degradation.
4. Check the context budget difference between the two runs.
   *Why:* Quantifying it proves the mechanism. The exam expects you to know *why* delegation works, not just that it works: subagents operate in their own context budget, and only their return value costs tokens in the coordinator session.
   **You should see:** A measurable difference in context usage between the inline run and the delegated run, roughly matching the size of the raw output you estimated in step 1. The delegated run's main-context cost is the summary only.
5. Add the pattern as a standing rule: in your CLAUDE.md or a skill with context: fork, require verbose discovery to run in an isolated subagent that returns a summary.
   *Why:* One-off discipline does not survive long sessions. The guide's standard mechanism is a skill with `context: fork` frontmatter (exercise 3.2) or an explicit team convention, so every discovery task gets isolation by default rather than by remembering.
   **You should see:** A written rule or skill frontmatter entry that routes verbose exploration through an isolated context. The rule states what the subagent must return: a structured summary, not raw output.

### F3. Modular CLAUDE.md with @path Imports and the Depth-5 Limit
**Difficulty:** Beginner · **Estimate:** 30 minutes · [guide](https://ravnhq.github.io/claude-certified-architect/guides/en.html)

[full file](exercise-fill-in-3.md)

1. Split a monolithic CLAUDE.md into topic files and import them with @path: coding standards in @./standards/coding-style.md, test requirements in @./standards/testing-requirements.md, project overview in @README.md.
   *Why:* The @path syntax is what makes CLAUDE.md modular. Each topic lives in one file, edited once, imported wherever relevant — avoiding the duplication-and-drift problem of copying conventions into multiple files. The exam tests the exact syntax: `@` immediately before the path, on its own line, no `@import` keyword.
   **You should see:** A short CLAUDE.md whose imports resolve inline — run /context and confirm the imported file contents appear as part of the loaded configuration. A standards/ directory containing the split-out files.
2. Verify that a relative @path resolves relative to the file containing the import, not the project root.
   *Why:* Resolution-relative-to-importer is the detail that breaks nested configurations. A CLAUDE.md in packages/api/ that writes @standards/api.md resolves against packages/api/, not the repo root. The exam tests whether you place imports correctly in multi-level setups.
   **You should see:** An import inside a directory-level CLAUDE.md that resolves correctly relative to that file's location. Moving the referenced file without updating the path breaks the import, confirming the resolution root.
3. Build an import chain five levels deep: CLAUDE.md imports A.md, A.md imports B.md, and so on to E.md. Confirm the chain loads.
   *Why:* The maximum import nesting depth is 5 — an explicit exam fact. You need a working depth-5 chain as the boundary case before you can demonstrate the failure at depth 6.
   **You should see:** Five levels of nesting resolving: content from E.md (the fifth hop) appears in the loaded configuration when you run /context.
4. Add a sixth level (E.md imports F.md) and observe what happens.
   *Why:* Knowing the limit exists is different from seeing the boundary behaviour. The exam tests the number 5 because it is an easy detail to get wrong — candidates who guess "unlimited" or "3" lose the point.
   **You should see:** The depth-6 import not resolved: F.md content does not appear in the loaded configuration. The chain silently stops at the depth limit rather than recursing further.
5. Refactor the over-deep chain: hoist the deepest shared files so no import chain exceeds the limit, and re-verify all content loads.
   *Why:* The practical skill is designing a modular layout that stays inside the constraint: keep shared standards near the top of the import graph and let leaf files import them, rather than chaining imports through intermediate files.
   **You should see:** A restructured layout where every file's content loads under /context, with the longest chain at 5 levels or fewer. Shared files are imported directly by the files that need them instead of being relayed through multiple hops.

### F4. Use /compact and /memory Without Losing Critical Facts
**Difficulty:** Beginner · **Estimate:** 30 minutes · [guide](https://ravnhq.github.io/claude-certified-architect/guides/en.html)

[full file](exercise-fill-in-4.md)

1. Run a long investigation session (10+ turns of file reads and searches) until the context window is heavily used, with specific facts discovered along the way: exact line numbers, amounts, dates, identifiers.
   *Why:* You need real context pressure to see what /compact actually does. The exam tests the risk, not just the command: summarisation compresses prior history, and exact numeric values, dates, and specific details can be lost in the process.
   **You should see:** A session with concrete discovered facts recorded somewhere you can check later — for example "refund amount $247.83, order #8891, March 3rd, bug at auth.ts:42". Several of these facts should live only in the conversation so far.
2. Before compacting, extract the critical facts into a persistent location: a case-facts block in your prompt, a scratchpad file, or CLAUDE.md via /memory.
   *Why:* This is the exam's required pairing: /compact frees the context window, but you must first protect transactional facts outside the summarised history. Compacting without extraction is the progressive-summarisation trap; compacting after extraction is the intended workflow.
   **You should see:** The key facts now exist outside raw conversation history — in a delimited facts block, a scratchpad file, or a CLAUDE.md entry. Each fact is specific (exact values), not a summary ("a refund of some amount").
3. Run /compact, then ask the agent questions that require the protected facts.
   *Why:* This is the verification that the pattern works. After summarisation, the conversation history no longer contains the original turns verbatim — only the facts you protected survive intact. The exam tests that lossy summarisation is acceptable *because* critical facts were extracted first.
   **You should see:** Correct, specific answers post-compact: the exact amount, order number, date, and line number come back. Try the same questions on a control run where you compacted *without* step 2 and observe degraded answers ("around $250", "early March").
4. Use /memory to persist a project convention or preference you want available next session, then confirm it loads in a fresh session.
   *Why:* /memory is the guide's designated command for cross-session persistence: it opens the CLAUDE.md file for editing, and the saved information loads automatically on startup. The exam contrasts this with re-explaining the same instructions every session.
   **You should see:** An entry added to CLAUDE.md through /memory (for example a testing convention or a frequently used command). A new session in the same project has that entry in its loaded configuration under /context, with zero re-explanation.
5. Write a two-line rule for your team: when to /compact, and what must be true before you do it.
   *Why:* The exam rewards knowing the conditions, not the keystroke. The rule should bind the two commands together: /compact is for long sessions filling with verbose tool output; before running it, critical facts must live in a persistent block, scratchpad, or memory.
   **You should see:** A written rule a teammate could apply without asking you. Example: "Long investigation filling context? Extract facts to scratchpad or /memory first, then /compact. Never compact with unprotected specifics in history."
