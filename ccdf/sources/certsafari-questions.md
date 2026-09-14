# Anthropic Claude Developer Foundations

Source: https://www.certsafari.com/anthropic/claude-developer-foundations/practice-questions

Free sample: 35 questions with answers and explanations. The full bank is 524 questions and is gated by the site quiz mode (Cloudflare Turnstile).

## Question 1

A code-review agent needs to read through 40 files, but the team wants the main conversation to stay short so later turns aren't paying for tokens spent on every file that was opened during the review. Which architecture keeps the main agent's context lean?

- **A.** Delegate the review to a subagent defined with an AgentDefinition; its tool calls and file contents stay in its own context, and only a final summary returns to the parent.
- **B.** Increase max_turns on the main query so Claude has enough budget to read all 40 files directly in the main conversation without the loop stopping early.
- **C.** Set effort to "low" on the main query so each turn that reads a file consumes fewer reasoning tokens, even though all 40 files still load fully into the shared main conversation.
- **D.** Enable include_partial_messages so file contents stream back to the main conversation incrementally as text deltas instead of arriving all at once.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A subagent starts with a fresh context; intermediate tool calls and file contents stay inside the subagent, and only its final message returns to the parent, so the main conversation's context does not grow by the full subtask transcript.
- B: Raising max_turns only permits more tool-use round trips; it does nothing to prevent the contents of all 40 files from accumulating directly in the main conversation's context.
- C: Lower effort reduces reasoning tokens spent per turn, but the file contents themselves are still read directly into the main conversation and accumulate exactly as before.
- D: Partial message streaming changes how output is delivered in real time; it does not change whether tool results accumulate in the conversation's context window.

## Question 2

A long-running agent session is approaching its context window limit. The team wants two things: a full, unabridged copy of the conversation saved before the SDK summarizes older history, and a guarantee that a specific formatting rule survives every compaction event without being paraphrased away. Which combination of mechanisms addresses both needs?

- **A.** Register a PreCompact hook to archive the full transcript first, and put the formatting rule in CLAUDE.md so it reloads on every request instead of living only in the initial prompt.
- **B.** Increase max_turns so compaction never triggers, and repeat the formatting rule at the start of every single user message sent throughout the session.
- **C.** Rely on the automatic compaction summary alone to preserve both the transcript and the formatting rule, since summaries are designed to retain conversation details verbatim.
- **D.** Register a PostToolUse hook to archive the transcript after each tool call completes, and place the formatting rule inside a subagent's AgentDefinition prompt instead of the main session.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A PreCompact hook fires before compaction and is the documented mechanism for archiving the full transcript first, and CLAUDE.md is reloaded and re-injected on every request, so a rule placed there survives compaction rather than being paraphrased away as an early-conversation instruction would be.
- B: Compaction triggers based on the context window approaching its limit, not on turn count, so raising max_turns does not prevent it; manually repeating the rule in every message is also fragile and does not match the documented CLAUDE.md pattern.
- C: Compaction is explicitly described as summarizing older history, which can lose specific instructions from earlier in the conversation; it is not documented as preserving details verbatim.
- D: A PostToolUse hook fires after individual tool calls, not immediately before a compaction event, so it does not reliably archive the transcript at the right moment; placing the rule in a subagent's prompt also does not affect the main session's own compaction behavior.

## Question 3

A long-running research agent needs to preserve findings across many separate sessions without re-loading everything it has ever learned into context at the start of each new task. Which Anthropic capability is designed specifically for this, letting the agent record findings as files and read them back only when needed?

- **A.** The memory tool, which lets Claude create, read, update, and delete files in a memory directory client-side, retrieves relevant content just-in-time rather than loading everything upfront.
- **B.** Server-side compaction automatically summarizes completed research sessions into durable summary files on the server, loading only relevant summaries at the start of each new task for referencing past findings.
- **C.** The clear_tool_uses context editing strategy strips old tool outputs from the active prompt and archives summarized findings to a persistent side file that the agent loads at the start of each new task.
- **D.** The Workflow tool executes a predefined sequence of API calls that archives research findings to external storage between sessions, and the agent retrieves these findings on demand without reloading the conversation context.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The memory tool provides a client-side directory where Claude can create, read, update, and delete files. It supports just-in-time retrieval, so the agent can record findings and only load relevant files when needed, avoiding loading everything into context upfront.
- B: Incorrect. Server-side compaction is designed to summarize a single conversation's context to fit within the limited context window, not to create durable summary files for cross-session reuse. It does not provide a persistent file store that an agent can read back across separate sessions.
- C: Incorrect. The clear_tool_uses strategy removes old tool use blocks from the current conversation's prompt to save context space, but it does not automatically archive findings to a persistent side file for later sessions. It operates within a single session and does not support cross-session persistence.
- D: Incorrect. The Workflow tool is used to orchestrate a sequence of subtasks or API calls in a single run, not specifically for persisting research findings across separate sessions. While it might involve external storage, it is not a dedicated mechanism for just-in-time retrieval of recorded findings like the memory tool.

## Question 4

A software architect is comparing three open-source agent frameworks for a project that requires integration with multiple LLM providers and end-to-end observability via OpenTelemetry. The project's agent logic is linear and does not require the manual specification of execution graphs. The frameworks under consideration are Strands Agents SDK, LangGraph, and Pydantic AI. Based on your knowledge of these frameworks, which of the following statements are true? (Select all that apply.) (Select 2 )

- **A.** The Strands Agents SDK is designed to be model-agnostic and includes first-class support for OpenTelemetry, allowing trace export to observability platforms like AWS CloudWatch.
- **B.** LangGraph can only orchestrate agents that use the Anthropic API because it was developed by Anthropic.
- **C.** LangGraph models agent workflows as directed graphs, giving developers precise control over branching and looping in execution paths.
- **D.** Pydantic AI includes a built-in OpenTelemetry collector that can be configured to send traces to CloudWatch out of the box.
- **E.** Strands Agents SDK enforces that all agents are deployed on AWS and does not permit the use of third-party model APIs. F . LangGraph is best suited for simple, linear agent chains because its graph model restricts the developer to a single execution path.

**Correct answer:** 

**Explanation:**


## Question 5

A team wants higher-confidence answers from a fraud-detection prompt applied to a transaction description. Rather than reviewing different angles, they run the exact same prompt against the same transaction five times and keep whichever verdict -- fraudulent or legitimate -- appears most often across the five runs. Which pattern are they using?

- **A.** Parallelization by sectioning, where five different prompts each examine a distinct aspect of the same transaction independently.
- **B.** Parallelization by voting, where the identical task runs multiple times and the majority verdict is selected.
- **C.** Evaluator-optimizer, where a second LLM call critiques the first verdict and the prompt is revised until the criteria are satisfied.
- **D.** Prompt chaining, where each of the five runs consumes the verdict produced by the run immediately before it.

**Correct answer:** B

**Explanation:**

- A: Incorrect. Parallelization by sectioning breaks a task into independent subtasks that run in parallel, with different prompts each examining a different aspect of the same input. This scenario runs one identical prompt five times against the same transaction, not five different prompts each covering a different aspect, so it does not match sectioning.
- B (correct): Correct. This is the voting variation of parallelization: the identical task is run multiple times to get diverse outputs, and the most common result is treated as the answer. Running the same fraud-detection prompt five times against the same transaction and keeping the verdict that appears most often across the runs is exactly that pattern.
- C: Incorrect. Evaluator-optimizer is an iterative loop in which one LLM call generates a response and a second call critiques or evaluates it, with the response revised across cycles until it satisfies the evaluator's criteria. The scenario has no critique step and no revision between runs; it simply repeats the same prompt and tallies verdicts.
- D: Incorrect. Prompt chaining decomposes a task into a sequence of steps where each LLM call processes the output of the previous one. The five runs in the scenario are independent and identical; none of them consumes another run's verdict as input.
Domain 2: Applications and Integration

## Question 6

A product team needs frontier-level intelligence for code generation, data analysis, and agentic tool use across a large user base, and wants the best balance of speed and intelligence rather than the highest-end, most expensive reasoning model. Which model fits this requirement?

- **A.** Claude Opus 4.8
- **B.** Claude Haiku 4.5
- **C.** Claude Sonnet 5
- **D.** Claude Mythos 5

**Correct answer:** C

**Explanation:**

- A: Opus 4.8 is the most capable option for complex agentic coding and enterprise work, but it is priced and positioned above the balanced speed-and-intelligence tier the requirement asks for.
- B: Haiku 4.5 is the fastest and cheapest option, but it is positioned for high-volume, cost-sensitive workloads rather than frontier-level code generation and data analysis at scale.
- C (correct): Sonnet 5 is explicitly described as frontier intelligence at scale with the best combination of speed and intelligence, fitting code generation, data analysis, and agentic tool use.
- D: Mythos 5 shares Fable 5's premium specs and pricing and is limited-availability through Project Glasswing, not a general-purpose balanced option for a large user base.

## Question 7

A long-running autonomous agent conversation regularly approaches the model's context window limit. The architecture needs the platform to automatically summarize earlier parts of the conversation server-side, and to clear out stale tool results as the token limit approaches, without the client managing this manually. Which two features should the architecture enable? (Select 2 )

- **A.** Compaction
- **B.** Context editing
- **C.** Prompt caching
- **D.** Token counting
- **E.** Batch processing F . Files API

**Correct answer:** 

**Explanation:**


## Question 8

A team wants to build a production billing pipeline's core logic entirely around a platform capability currently labeled Beta in Anthropic's feature-availability table. A tech lead raises a concern before approving the design. What is the most accurate basis for that concern?

- **A.** Beta features are billed at a 50% premium compared to generally available features, making them unsuitable for cost-sensitive billing pipelines.
- **B.** Beta features cannot be used together with prompt caching or batch processing, which would prevent the pipeline from scaling cost-effectively.
- **C.** Beta features are capped at 200k tokens of context regardless of the underlying model, which would limit the pipeline's document processing.
- **D.** Beta features may change significantly or be discontinued based on feedback and are not guaranteed for ongoing production use, unlike GA features.

**Correct answer:** D

**Explanation:**

- A: Incorrect -- Beta classification does not imply a fixed premium pricing rule; pricing varies by feature and model, not by a blanket beta surcharge.
- B: Incorrect -- there's no general rule that beta-classified features are incompatible with caching or batch processing; compatibility depends on the specific feature, not its beta status alone.
- C: Incorrect -- context window limits are tied to the underlying model, not to whether a feature is classified as beta.
- D (correct): Correct -- by definition, Beta features may change significantly or be discontinued based on feedback and are not guaranteed for ongoing production use, which is exactly the risk of anchoring core billing logic to one.

## Question 9

An agent built with the Claude Agent SDK reads an authentication module in one query call, and the team wants a second, later query call to reference 'it' meaning that same module without re-reading or re-explaining context. What should they capture and reuse from the first call to accomplish this?

- **A.** Capture the session_id from the SystemMessage of type 'init' during the first query, then pass it as the resume option on the second query call.
- **B.** Capture the full text of every message from the first query and re-send it as the prompt string prefix on the second query call.
- **C.** Capture the file contents read during the first query and hardcode them into the system prompt used for the second query call.
- **D.** Capture the tool_use_id from the first query's Read tool call and pass it as the model parameter on the second query call.

**Correct answer:** A

**Explanation:**

- A (correct): Correct -- capturing the session_id from the init SystemMessage and passing it to the resume option lets the second query continue with full context from the first, including which file was read.
- B: Incorrect -- manually re-sending message text as a prompt prefix is not how session continuity works in the SDK and would not reliably reconstruct tool state like files already read.
- C: Incorrect -- hardcoding file contents into a new system prompt duplicates work the resume option already handles and doesn't scale to arbitrary prior context.
- D: Incorrect -- tool_use_id identifies a specific tool invocation, not a session, and the model parameter selects which Claude model to use, not which session to resume.

## Question 10

An engineer building an SDLC automation wants an agent to run git status, stage changes, and commit them as part of a scripted workflow, in addition to reading and editing source files. Which built-in Agent SDK tool grants this ability to run version-control commands directly?

- **A.** Bash, which runs terminal commands and scripts, including git operations, in addition to other shell tasks
- **B.** Grep, which searches file contents with regex and has no ability to invoke external commands like git
- **C.** WebFetch, which retrieves and parses web page content and cannot execute local version-control commands
- **D.** AskUserQuestion, which prompts the user with clarifying multiple-choice questions rather than executing shell commands

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Bash is documented as running terminal commands and scripts, explicitly including git operations, which covers status, staging, and committing.
- B: Incorrect. Grep only searches file contents with regex; it cannot invoke git or any other external command.
- C: Incorrect. WebFetch retrieves remote web content; it has no capability to run local shell or git commands.
- D: Incorrect. AskUserQuestion is for gathering clarifying input from the user, not for executing version-control operations.

## Question 11

A batch-processing service runs thousands of independent, single-shot document classification tasks per hour using the Agent SDK. Each task is unrelated to the others, must never be resumable later, and the team wants to avoid unnecessary disk writes for these throwaway sessions in their TypeScript service. What is the correct session configuration?

- **A.** Set `persistSession: false` on each `query()` call, so the session exists only in memory for the duration of that call and nothing is written to disk
- **B.** Set `continue: true` on each call so every task shares a single reusable session instead of creating a new one each time
- **C.** Call `resume` with a randomly generated session ID on each task, which creates a new in-memory-only session and skips disk persistence
- **D.** Use the Python SDK's `ClaudeSDKClient` instead, since only the Python SDK offers an option to skip writing session transcripts to disk

**Correct answer:** A

**Explanation:**

- A (correct): Correct. For a stateless task where nothing should be written to disk, TypeScript's `persistSession: false` option keeps the session in memory only for the duration of the call; this is documented as a TypeScript-only capability since Python always persists sessions to disk.
- B: Incorrect. `continue: true` resumes the most recent session and would incorrectly merge unrelated classification tasks into one shared, growing conversation rather than keeping each task independent and non-persistent.
- C: Incorrect. `resume` is for returning to an existing session by its real ID; supplying a random ID does not create a valid in-memory-only session and is not the documented mechanism for skipping persistence.
- D: Incorrect. It is the TypeScript SDK, not Python, that offers the in-memory-only `persistSession: false` behavior; Python always persists sessions to disk, so switching to Python would not achieve the goal.

## Question 12

A developer resumes a long-running session with `claude --resume` that was previously running on Opus 4.6. Between the original session and the resume, the organization's admin retired Opus 4.6 and it is no longer reachable. What happens when the session resumes?

- **A.** The resumed session falls through to the normal precedence order for selecting a model, since the restored model is unavailable, rather than failing outright
- **B.** The resume command fails immediately with an unrecoverable error, since resumed sessions are hard-locked to their originally saved model with no fallback path
- **C.** The session silently resumes on Opus 4.6 anyway, since Claude Code caches the model's response format locally and does not need to reach the retired model to continue an existing transcript
- **D.** The session automatically and permanently updates its saved `model` setting to whatever the resume happens to fall back to, overwriting the user's prior explicit `/model` choice for all future sessions

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Resumed sessions normally keep the model they were using when the transcript was saved, but if that restored model has been retired or is excluded, the session falls through to the normal precedence order for setting a model rather than resuming on an unreachable model or failing outright.
- B: Incorrect. Resumed sessions are not hard-locked with no fallback; the documented behavior specifically covers the retired/excluded case by falling through to normal model-selection precedence instead of erroring.
- C: Incorrect. Claude Code needs to reach the actual model to process new requests; a retired, unreachable model cannot silently continue serving the session, which is exactly why the fallback to normal precedence exists.
- D: Incorrect. Falling through to normal precedence for one resumed session does not describe a documented behavior of permanently overwriting the user's saved settings file as a side effect.

## Question 13

A team is scoping the operational limits of the Message Batches API before committing to it for a recurring nightly job. Select the statements below that accurately describe these limits. (Select 3 )

- **A.** A single Message Batch is restricted to a maximum of 100,000 requests or 256 MB, and the API will immediately reject any batch exceeding either of these limits.
- **B.** A batch expires if it has not finished processing within 24 hours of creation, and any requests still unprocessed at that point are automatically marked as expired.
- **C.** Batch results remain available for download for 29 days after the batch creation, after which the batch record still exists but results can no longer be downloaded.
- **D.** Batches are visible across every Workspace in an organization by default, so a batch created in one Workspace can be listed and its results downloaded by any other Workspace.
- **E.** A batch can include `stream: true` on individual requests as long as the overall batch call itself is submitted without streaming, letting each request specify its own streaming behavior.

**Correct answer:** 

**Explanation:**


## Question 14

A platform team deploys `.claude/settings.json` to every repository with a `permissions.deny` rule blocking `Bash(curl *)`. An individual developer adds the opposite rule, an `allow` entry for `Bash(curl *)`, in their own `.claude/settings.local.json` because they need curl for a personal debugging script. When that developer runs Claude Code in the repo, what happens to `curl` commands?

- **A.** Curl commands stay blocked, because permission rules merge across scopes instead of one scope overriding another, so a local allow cannot remove a project-level deny
- **B.** Curl commands become allowed, because `settings.local.json` has higher precedence than `settings.json` and its permission rules fully replace the lower-scoped file's rules
- **C.** Curl commands prompt for manual approval every time, because conflicting allow and deny rules across scopes cancel each other out and fall back to interactive confirmation
- **D.** Curl commands stay blocked only until the developer restarts Claude Code, after which the local settings file's allow rule takes effect on the next session

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Permission rules are the documented exception to normal settings precedence: they merge across scopes instead of one scope overriding another, so a deny rule from a higher-precedence project scope remains in effect even when a lower-precedence local scope adds a conflicting allow.
- B: Incorrect. While `settings.local.json` does sit above `settings.json` in general precedence, permission rules specifically merge rather than override, so the local file's allow entry does not erase the project-level deny.
- C: Incorrect. Merging conflicting permission rules does not produce an interactive prompt state; the deny rule simply continues to block the command outright.
- D: Incorrect. Restarting Claude Code does not change how permission rules merge across scopes; the project-level deny remains effective before and after any restart.

## Question 15

A vendor wants to package a set of internal-workflow skills, a custom subagent, an audit-logging hook, and a database MCP server as one reusable unit that different project teams can load into their own Claude Code sessions without copying files into each project. Which design satisfies this requirement?

- **A.** Package the skills, agent, hooks, and MCP server definition into a plugin directory (with `skills/`, `agents/`, `hooks/`, and `.mcp.json`) and have each project load it via the `plugins` option pointing at the plugin's path.
- **B.** Place the skills, subagent, hooks, and MCP config into a base directory; then have each team copy the skills into their `.claude/skills/` folder and manually add the subagent, hooks, and MCP settings to their project configuration.
- **C.** Publish the skills, subagent definition, hook scripts, and MCP server configuration as a single CLAUDE.md file with sections like `## Skills`, `## Agents`, `## Hooks`, and `## MCP`, and have each project load it by adding an import directive in the project configuration.
- **D.** Register the skills, subagent logic, hook scripts, and MCP server configuration as a single custom tool function in the Agent SDK's tool registry, and have each project team enable it by adding the tool to their session's tool-calling loop.

**Correct answer:** A

**Explanation:**

- A (correct): Official Claude Code documentation recommends packaging reusable capabilities as a plugin directory with root-level `skills/`, `agents/`, `hooks/`, and `.mcp.json`, plus the required `.claude-plugin/plugin.json` metadata file. This lets projects load the unit through the `plugins` option or `/plugin install`, with no file copying into each project. Hooks can implement audit logging, and `.mcp.json` centralizes the MCP server definition for consistent reuse.
- B: This approach requires each team to copy files into their own project and manually configure subagents, hooks, and MCP settings, which violates the requirement of loading a single reusable unit without copying files. It also splits the components across project folders and configuration, making updates and consistency harder to maintain.
- C: `CLAUDE.md` is an instruction and memory file, not a plugin packaging format that can declare structured skills, agents, hooks, or MCP servers as loadable components. There is no documented import directive that turns these sections into dynamically loaded agent and MCP capabilities, so this design does not satisfy the requirement.
- D: A single custom tool function cannot package the distinct capabilities of skills, subagents, lifecycle hooks, and MCP server definitions into a reusable plugin. This approach would require manually registering tool logic in each project and cannot provide the automatic skill activation, hook lifecycle execution, or MCP connection handling that the plugin directory structure provides.
Domain 4: Eval, Testing, and Debugging

## Question 16

A team's usage sits well under their published requests-per-minute limit, yet they begin seeing 429 errors after a marketing campaign causes API traffic to triple within a few minutes. Historical usage was steady before the spike. What is the most likely explanation, and what should the team change to avoid recurrence?

- **A.** The spike likely triggered acceleration limits designed to catch sharp usage increases; the team should ramp traffic up gradually and keep usage patterns more consistent
- **B.** The published RPM limit only applies to the Message Batches API, so any spike in synchronous Messages API traffic will always return 429 regardless of pacing
- **C.** The 429 responses indicate the organization's API key was automatically revoked for suspected abuse and must be regenerated in the Console
- **D.** The spike exceeded the request size limit for the Messages API, so each oversized request was individually rejected with a rate-limit error

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The documentation notes that a sharp increase in usage can trigger 429 errors from acceleration limits even while under the standard published limits, and the recommended mitigation is to ramp traffic up gradually and maintain consistent usage patterns.
- B: Published RPM limits apply per model to the Messages API itself; the Message Batches API has its own separate rate limits, so this statement misattributes which endpoint the published limit governs.
- C: A 429 rate_limit_error does not indicate key revocation; a revoked or invalid key produces a 401 authentication_error instead, so this diagnosis points to the wrong error type.
- D: Exceeding the maximum request payload size produces a 413 request_too_large error, not a 429, and is unrelated to the number of requests sent per minute.

## Question 17

An engineer is deciding, for several failing requests, whether simply switching to the streaming API or increasing max_tokens would resolve the failure. Select all of the following scenarios where neither of those two changes would fix the described error. (Select 3 )

- **A.** A request fails with 413 request_too_large because the inlined message content itself exceeds the Messages API's maximum request payload size
- **B.** A request fails with 409 conflict_error because two workers concurrently modified the same underlying resource before this request was sent
- **C.** A response completes with stop_reason set to max_tokens because the generated content reached the configured output token cap
- **D.** A request fails with 401 authentication_error because the API key used to sign the request has expired
- **E.** A request fails with 504 timeout_error because a very large non-streaming generation ran past the idle-connection limit on an unreliable network

**Correct answer:** 

**Explanation:**


## Question 18

A billing-sensitive workload needs to know exactly how many tokens a large prompt will consume before it is sent to Claude, so the team can stay within a budget. What should they use?

- **A.** A token counting call, to determine the number of tokens in a message before sending it
- **B.** The effort parameter set to low, which returns an estimated token count in the response metadata
- **C.** The Files API, since uploaded files automatically report their token size before generation begins
- **D.** The budget_tokens field on extended thinking, which caps and reports total request token usage

**Correct answer:** A

**Explanation:**

- A (correct): Token counting lets you determine the number of tokens in a message before sending it, which is exactly what a pre-send budget check requires.
- B: The effort parameter controls how many tokens Claude spends when responding; it does not return a pre-send token estimate for a prompt.
- C: The Files API manages uploading and reusing files across requests; it does not itself report token counts for a prompt before generation.
- D: Budget_tokens caps thinking token spend during manual extended thinking; it is not a pre-send counting mechanism for the full request.

## Question 19

While streaming a response with extended thinking enabled, a client receives a thinking content block that ends with a signature_delta event immediately before content_block_stop. What is the purpose of this signature_delta event?

- **A.** It provides a signature used to verify the integrity of the thinking block's content.
- **B.** It marks the point at which the thinking block's token usage should be added to the cumulative usage total.
- **C.** It indicates that the thinking block has been redacted for policy compliance and its content should be discarded.
- **D.** It signals that a fallback model has taken over generation for the remainder of the response.

**Correct answer:** A

**Explanation:**

- A (correct): Correct — the signature_delta event carries a signature used to verify the integrity of the preceding thinking content, sent just before the block closes.
- B: Token usage accounting happens through the usage field on message_delta and message_start, not through signature_delta.
- C: Redaction of thinking content is a distinct mechanism and is not what signature_delta communicates; signature_delta is about integrity verification, not content redaction.
- D: Model fallback during streaming is represented by dedicated fallback content blocks at model boundaries, not by a signature_delta on a thinking block.

## Question 20

A junior engineer asks why Claude appears to produce text piece by piece rather than generating the entire response instantly. Which explanation best matches how Claude generates output?

- **A.** Claude autoregressively predicts the next token based on the prompt and previously generated tokens, repeating the process to build the full response.
- **B.** Claude retrieves the entire response from a precomputed lookup table by matching the prompt's embedding to a database of response embeddings and returning the nearest full text.
- **C.** Claude generates the full response as a complete string in one forward pass through the model, then splits it into tokens only for transmission to the client.
- **D.** Claude generates tokens in a random order, then applies a learned reordering function to arrange them into a coherent response before returning it.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Claude's generation is autoregressive, meaning it iteratively predicts the next token conditioned on all preceding tokens and the input prompt. This token-by-token process creates the appearance of text being produced piece by piece, as the model continues until a stop condition is met.
- B: Incorrect. Claude does not use a precomputed lookup table; it actively generates each token through model computations. The response is not retrieved from a database of embeddings but is dynamically predicted one token at a time.
- C: Incorrect. Claude does not generate the entire response in a single forward pass. Instead, it produces output sequentially, with each token prediction step depending on the prior tokens, causing the piece-by-piece display.
- D: Incorrect. Claude predicts tokens in a left-to-right, sequential order, not randomly. There is no learned reordering function applied after generation; the coherence emerges naturally from the autoregressive process.

## Question 21

A support-ticket triage service sends the same 6,000-token system prompt and tool definitions with every request, followed by a unique customer message. Requests arrive in bursts roughly every 30 seconds throughout the day. The team wants to cut input token costs on the repeated prefix without adding infrastructure. Which change addresses this most directly?

- **A.** Mark the system prompt and tool definitions with a 5-minute ephemeral cache_control breakpoint; repeated requests then read the prefix from cache, avoiding the full input price.
- **B.** Move the system prompt and tool definitions into each request's user message so that the fixed 6,000-token prefix is cached per message, cutting input costs across the 30-second burst cycle.
- **C.** Reduce the max_tokens parameter on every request to the minimum needed for a short triage response, so Claude's completions stay brief and the blended token cost per call decreases.
- **D.** Switch the tool definitions to a compact JSON schema with shorter property names and fewer nested objects, so the 6,000-token prefix shrinks and each request consumes fewer input tokens.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The system prompt and tool definitions form a stable prefix that is reused within a short window, making prompt caching ideal. By marking them with a 5-minute ephemeral cache_control breakpoint, subsequent requests in the burst read from cache and pay only a fraction of the full input price, directly cutting costs.
- B: Incorrect. Simply moving the prefix into the user message does not enable caching; prompt caching requires an explicit cache_control breakpoint on the content. Without that, each request is still billed for the full 6,000 tokens, so input costs remain unchanged regardless of role placement.
- C: Incorrect. Reducing max_tokens limits the length of the model's output, which reduces output token spend, but it does nothing to lower the repeated 6,000-token input prefix cost. The scenario targets input cost reduction, so this change is misaligned.
- D: Incorrect. A compact schema reduces the token count of the prefix, but every request still pays full input price for that smaller prefix. Prompt caching would allow repeated reads from cache at a much lower cost per request, making it a more effective solution for the burst pattern.
Domain 6: Prompt and Context Engineering

## Question 22

An engineer is building a research agent that needs to read dozens of files across a large repository to answer one question, without letting all that file content pile up in the main conversation's context. Which design best achieves this?

- **A.** Delegate the file exploration to a subagent, whose fresh context absorbs all the intermediate reads while only its final summary message returns to the parent
- **B.** Read every file directly in the main agent loop, then issue a manual /compact command immediately afterward to shrink the accumulated history
- **C.** Read every file directly in the main agent loop, but set effort to low so the extra file content consumes fewer tokens per turn
- **D.** Store all file contents in a custom MCP resource and have the main agent fetch a single combined resource URI instead of individual files

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A subagent runs in its own fresh conversation; intermediate tool calls and results stay inside the subagent, and only its final message returns to the parent, so the main context grows by a summary rather than every file read.
- B: Incorrect. Reading everything in the main loop still pays the full context cost of every file during exploration; manual compaction afterward summarizes history but doesn't prevent that cost from accumulating first, and it also risks losing detail the task still needs.
- C: Incorrect. The effort setting controls how much reasoning Claude applies per turn; it reduces token usage from reasoning, not the token cost of the file contents themselves being read into context.
- D: Incorrect. Combining file contents into one MCP resource still delivers that same total content into the main agent's context when fetched; it does not isolate it the way a subagent's separate conversation does.

## Question 23

A prompt written for a legal-document summarizer produces inconsistent structure across runs, and engineers on the team disagree about why. Before tuning the prompt further, which practice would most directly reveal ambiguity in the current wording?

- **A.** Show the prompt to a colleague who has minimal context on the task and ask them to follow it exactly as written, since confusion for a human reader tends to predict confusion for Claude
- **B.** Rerun the identical, unedited prompt against the model twenty times and keep only the most common resulting structure, treating majority voting as a substitute for locating the ambiguity
- **C.** Ask Claude to explain its own instructions back in a separate call, treating the model's paraphrase of the prompt as a reliable substitute for a human comprehension check
- **D.** Reduce the temperature to zero for the summarizer's requests, on the assumption that ambiguity in phrasing is resolved by lower-variance sampling rather than by clearer instructions

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The golden rule for clarity is to show the prompt to a colleague with minimal context and have them follow it; if they are confused, Claude is likely to be confused too.
- B: Incorrect. Majority voting across repeated runs of an ambiguous prompt does not locate or fix the ambiguity in the wording itself.
- C: Incorrect. A model's own paraphrase of its instructions is not documented as a reliable substitute for an independent human comprehension check.
- D: Incorrect. Lowering temperature reduces sampling variance but does not address ambiguous or unclear instruction wording, which is a distinct problem from output randomness.

## Question 24

A summarization service parses the response text as JSON. For very long transcripts, the JSON string is occasionally cut off mid-object and the parser raises a decode error. Investigating, the engineer finds stop_reason is "max_tokens" on every one of the failing calls. What should the defensive parsing logic do?

- **A.** Catch the decode error, check stop_reason for max_tokens, and treat the response as incomplete
- **B.** Ignore stop_reason and retry parsing with a lenient JSON parser that tolerates trailing commas
- **C.** Lower max_tokens further so Claude is forced to produce shorter, safer completions
- **D.** Treat every JSON decode error as a transient network issue and resend the identical request

**Correct answer:** A

**Explanation:**

- A (correct): Correct. stop_reason "max_tokens" is the documented signal that the response was cut off before completion; defensive code should branch on it and handle the response as incomplete rather than as malformed JSON.
- B: Incorrect. A lenient parser might mask trailing-comma typos, but it cannot recover data that was never generated because the response was truncated mid-object.
- C: Incorrect. Lowering max_tokens makes truncation more likely, not less, worsening the exact failure being investigated.
- D: Incorrect. The failures are explained by output length, not network transience; blindly resending the same request risks the same truncation again.

## Question 25

During testing, an agent occasionally calls a create_ticket tool while omitting the required priority field. Which of the following are appropriate ways to handle this within the conversation, according to recommended tool-use error handling? (Select all that apply) (Select 3 )

- **A.** Return a tool_result with is_error: true naming the missing field so Claude retries with it supplied
- **B.** Add strict: true to the tool definition so input is validated against the schema before your handler
- **C.** Improve the tool's description so the priority-field requirement is stated more explicitly
- **D.** Automatically terminate the session and require the user to start an entirely new conversation
- **E.** Log the omission silently and proceed with ticket creation using a null priority value F . Rewrite the schema to make priority optional so it can never be reported as missing again

**Correct answer:** 

**Explanation:**


## Question 26

A prompt concatenates two source documents as plain, undifferentiated text, and Claude's responses sometimes misattribute which document a fact came from. What restructuring best fixes this attribution problem?

- **A.** Wrap each document in its own <document> tag with nested <source> and <document_content> subtags, placed inside an outer <documents> tag, thereby providing clear boundaries and metadata.
- **B.** Insert a page-break control character between the two documents, such as a form feed, and prepend a short system note that instructs Claude to treat the page break as a document separator for attribution.
- **C.** Prefix each document with a numbered markdown heading (e.g., "# Document 1") and then include a prompt instruction for Claude to attribute facts based solely on which heading they appear under.
- **D.** Convert both documents into a single CSV file where each row holds one paragraph and the left column labels the source document, so Claude can read the tabular data and attribute facts to the correct source.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Wrapping each document in its own <document> tag with nested <source> and <document_content> subtags, inside an outer <documents> tag, provides clear boundaries and explicit source metadata. This is the documented XML pattern for multi-document prompts, ensuring reliable attribution of facts to the correct source.
- B: Incorrect. A page-break control character like a form feed is not a reliable or documented mechanism for conveying document boundaries to Claude. Even with an explanatory system note, it lacks the structured, machine-readable metadata that dedicated XML tags provide, making misattribution more likely.
- C: Incorrect. While markdown headings create visual separation, they do not carry structured source metadata the way nested XML tags with a <source> subtag do. Relying solely on a prompt instruction to attribute based on headings can be brittle and is not the documented best practice for multi-document attribution.
- D: Incorrect. Converting free-form documents into a single CSV file would destroy the original paragraph structure and narrative flow, harming comprehension. This format is not a documented or effective approach for maintaining source attribution, whereas structured XML tagging preserves document integrity.

## Question 27

A subagent is defined to automatically spawn further subagents to divide up its own workload, and those in turn may spawn more. What governs how deep this nesting can go, and how can a team stop a specific subagent from spawning any children at all?

- **A.** Nesting defaults to three levels below the main agent and can be changed with the `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` setting; omitting `Agent` from a subagent's tools (or adding it to `disallowedTools`) prevents that subagent from spawning children.
- **B.** Nesting has no depth limit as long as each subagent runs in the background, because background execution bypasses the configured depth cap, and to prevent a particular subagent from spawning children, set its effort level to low, which prevents it from spawning children.
- **C.** Nesting is capped at two levels only when the subagent runs in the foreground, because foreground execution limits nesting to two levels, and to prevent a subagent from spawning children, set its `permissionMode` to `plan` to restrict it to read-only and prevent spawning.
- **D.** Nesting is unlimited regardless of execution mode, because there is no built-in depth limit, and to prevent a specific subagent from spawning children, the team must remove the `Bash` tool from its tools list to block the execution of child-spawning commands.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The current default maximum nesting depth is 3 levels below the main agent, and it is configurable via `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` in `settings.json`. To stop a specific subagent from spawning children, omit `Agent` from its `tools` list or add `Agent` to `disallowedTools`; without the `Agent` tool, the subagent cannot create child subagents.
- B: Incorrect. Background execution does not bypass the depth limit; the default maximum of 3 levels (or the configured `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` value) applies regardless of execution mode. Effort level does not control child spawning; use `Agent` omission or `disallowedTools`.
- C: Incorrect. Foreground execution does not impose a two-level cap; the same 3-level default (or configured depth) applies to foreground and background subagents. Setting `permissionMode` to `plan` is not the documented way to prevent spawning; use `Agent` omission or `disallowedTools`.
- D: Incorrect. Nesting is not unlimited; by default it is capped at 3 levels (configurable via `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). Removing `Bash` does not block child spawning because subagents spawn children through the `Agent` tool, not shell commands; use `Agent` omission or `disallowedTools`.
Domain 7: Security and Safety

## Question 28

A support agent built on Claude has access to a customer database tool and forwards conversation transcripts to a third-party analytics vendor for quality monitoring. Transcripts routinely contain customers' full names, emails, and account numbers. Which of these actions should the team take to prevent unnecessary PII exposure? (Select all that apply.) (Select 3 )

- **A.** Redact or mask personally identifiable information in the transcripts before they leave the system, sending the vendor only the fields it actually needs
- **B.** Apply the same PII minimization to data logged internally for debugging, not just to data sent to the external vendor
- **C.** Send the full unredacted transcripts as-is, since the analytics vendor's contract already covers general data handling and confidentiality obligations
- **D.** Compress the transcripts before sending them, since compression is treated as equivalent to redaction for the purpose of protecting personal data
- **E.** Review which fields the analytics vendor's quality-monitoring use case genuinely requires before deciding what to include in each transcript export F . Ask Claude to verbally warn the customer at the start of each chat that their data might be shared externally, then proceed without further changes

**Correct answer:** 

**Explanation:**


## Question 29

A fintech company is deploying a multi-tenant Claude-powered advisor that reads account data for one customer per session and can place trades through an internal API. Which combination of practices best supports authentication, authorization, and confidentiality across tenants? (Select all that apply.) (Select 3 )

- **A.** Scope each session's tool access so it can only read and act on the data belonging to the authenticated customer for that session
- **B.** Screen inbound account notes and support messages for injected instructions before they are returned to Claude as tool results
- **C.** Issue one shared service credential for the trading API that every customer session reuses, to simplify credential rotation
- **D.** Log full account numbers and portfolio balances in plaintext application logs so support staff can search history freely
- **E.** Require a fresh authorization check on the backend before executing any trade action the agent requests, rather than trusting the agent's own judgment alone F . Let a session continue reading a different customer's data mid-conversation if the agent decides it is contextually relevant to the current advice

**Correct answer:** 

**Explanation:**


## Question 30

A healthcare organization with a HIPAA-enabled Claude API organization sends a request that includes the code execution tool. The API responds with a 400 invalid_request_error stating the feature is not available for HIPAA-regulated organizations without Zero Data Retention. What is the most appropriate immediate remediation for this specific request?

- **A.** Remove the code execution tool from the request and use only features listed as eligible for HIPAA readiness in the feature eligibility table
- **B.** Retry the identical request with a higher max_tokens value, since the error is caused by insufficient token budget for the tool call
- **C.** Switch the request to a different, unrelated organization ID without a BAA in place so the feature restriction no longer applies
- **D.** Ignore the error and resubmit the same request repeatedly, since HIPAA feature restrictions are only advisory warnings rather than enforced blocks

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The documented HIPAA error handling behavior is that the API enforces feature restrictions automatically and returns a 400 listing non-eligible features; the resolution is to remove those features and use ones eligible under HIPAA readiness.
- B: Incorrect. The error is about feature eligibility under the HIPAA arrangement, not token budget, so adjusting max_tokens would not resolve it.
- C: Incorrect. Routing PHI-bearing requests through an organization without a BAA would violate HIPAA compliance obligations rather than legitimately resolve the restriction.
- D: Incorrect. HIPAA feature restrictions are enforced by the API, not advisory; the 400 error blocks the request until the non-eligible feature is removed.

## Question 31

Which of the following statements about hook decision priority and configuration scope are accurate according to Anthropic's documentation? (Select 3) (Select 3 )

- **A.** When multiple hooks return conflicting decisions, deny takes priority over defer, which takes priority over ask, which takes priority over allow
- **B.** `.claude/settings.local.json` is gitignored and intended for local-only configuration, not for sharing hooks with a team
- **C.** Managed policy settings apply organization-wide and are admin-controlled, taking precedence in a way project-local settings cannot override
- **D.** A hook matcher of `*` is functionally identical to an omitted matcher, since only `*` fully disables regex evaluation for that hook
- **E.** PostToolUse hooks can block a tool call before it executes, just like PreToolUse hooks F . Async hook outputs can safely block, modify, or inject context into the operation as long as `asyncTimeout` is set high enough

**Correct answer:** 

**Explanation:**


## Question 32

An engineer configuring a Claude Code hook wants it to fire for every Bash, Edit, and NotebookEdit tool call without listing each tool name explicitly. According to Anthropic's documentation on regex-based matchers, which configuration achieves this?

- **A.** A matcher like `Bash|Edit.*` is used; the system falls back to regex evaluation and matches any tool name containing those as substrings.
- **B.** A matcher of `Bash, Edit, NotebookEdit` with commas, which triggers regex evaluation, causing the pattern to match any tool name containing those substrings.
- **C.** Omitting the matcher field entirely, which causes the hook to fire only for tools with names longer than four characters, such as Bash and NotebookEdit.
- **D.** A matcher of `Bash+Edit+NotebookEdit`, where the plus sign acts as a concatenation operator, causing the pattern to be evaluated as a single exact-match string.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Per Claude Code's hook matcher rule, a matcher value that contains any character outside letters, digits, underscores, hyphens, spaces, commas and pipes is evaluated as a JavaScript regular expression, tested with JavaScript's RegExp.prototype.test() — unanchored, so a match anywhere in the tool name counts. `Bash|Edit.*` matches `Bash` through the first alternative, and matches both `Edit` and `NotebookEdit` because `Edit.*` is found starting partway through the string; the documentation's own example confirms `Edit.*` matches both `Edit` and `NotebookEdit`. It is a contains match, not a starts-with match: `NotebookEdit` qualifies because it contains `Edit`, not because it begins with it.
- B: Incorrect. Commas keep a matcher on the exact-match path rather than triggering regex evaluation — a value built only from letters, digits, underscores, hyphens, spaces, commas and pipes is evaluated as a list of exact strings, the same way the documentation shows `Edit, Write` matching either tool exactly. So `Bash, Edit, NotebookEdit` would not fail the way this option claims; it would match `Bash`, `Edit`, and `NotebookEdit` each exactly. The reason this configuration is still wrong for the scenario is that it lists every tool name individually, which is exactly what the engineer is trying to avoid.
- C: Incorrect. There is no such length-based behavior in the documentation. If the matcher field is omitted, the hook may not fire at all or may follow a different default (e.g., match all tools), but it definitely does not use a character-length rule. This option describes a fictional behavior.
- D: Incorrect. In regex, `+` means "one or more of the preceding element," not concatenation. Thus, `Bash+Edit+NotebookEdit` would be treated as a regex requiring one or more "h" after "Bas", etc., which is unlikely to match the intended tool names. Even if intended as a literal string, the presence of `+` would force regex evaluation, not exact match.

## Question 33

A team is building an automated agent using the Claude Agent SDK that runs unattended in a CI pipeline. It needs to run a fixed set of tools (`Read`, `Grep`, `Bash(npm test)`) without any human available to approve prompts, and any tool call outside that fixed set must be rejected outright rather than hang waiting for approval. Which configuration achieves this?

- **A.** Set `allowed_tools` to the fixed set and `permission_mode` to `dontAsk`; listed tools run, and every other call is denied without invoking `canUseTool`.
- **B.** Set `permission_mode` to `bypassPermissions` and omit `allowed_tools` entirely, since bypass mode already restricts execution to a minimal safe tool set by default.
- **C.** Set `permission_mode` to `plan` and set `allowed_tools` to the fixed set, since plan mode auto-denies any tool call that is not explicitly pre-approved.
- **D.** Set `permission_mode` to `default` and register a `canUseTool` callback that always throws an exception for tools outside the fixed set.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. `dontAsk` converts any permission check that would otherwise prompt into a denial without ever calling `canUseTool`, so pairing it with `allowed_tools` gives a fixed, explicit tool surface: listed tools run, and any other tool call is denied immediately instead of hanging on a human who isn't there.
- B: Incorrect. `bypassPermissions` approves every tool call that reaches it, including tools well beyond a minimal set; it does not restrict scope by default and is the opposite of what's needed here.
- C: Incorrect. plan mode routes file-edit and shell-write tools to canUseTool regardless of allow rules, which would hang without a human approver rather than denying outright.
- D: Incorrect. The SDK documentation defines what dontAsk paired with allowed_tools does, but not what happens when a canUseTool callback throws — relying on an uncaught exception to enforce the fixed tool set is undefined behavior, not a documented rejection path. It also reimplements by hand what dontAsk already provides declaratively.
Domain 8: Tools and MCPs

## Question 34

A fintech startup is building an internal support agent with the Claude Agent SDK. The agent must look up account balances from a proprietary ledger service reachable only through an internal REST gateway with no existing MCP server or public SDK. Which approach best fits this requirement?

- **A.** Define a custom tool that calls the internal REST gateway and register it through an in-process MCP server
- **B.** Rely on the built-in WebFetch tool to query the gateway directly from the agent's prompt
- **C.** Write a Skill that documents the ledger schema and expects Claude to reason about balances from memory
- **D.** Search for a community MCP server that might expose a similar ledger balance capability

**Correct answer:** A

**Explanation:**

- A (correct): Correct: a custom tool wraps the handler logic for calling the proprietary gateway and is registered via create_sdk_mcp_server/createSdkMcpServer, giving Claude a purpose-built function for this internal system.
- B: WebFetch is a general-purpose built-in tool for parsing public web pages; it is not designed for authenticated internal gateway calls with structured request/response handling.
- C: A Skill supplies knowledge or workflow instructions, not a live connection to an external system, so Claude would have no way to actually retrieve real balance data.
- D: No public integration exists for this proprietary internal service, so a community MCP server would not have the credentials or schema to reach it.

## Question 35

A small internal tool needs to read files, run shell commands, and search a codebase for a one-off refactor task using the Claude Agent SDK. No external systems or custom domain logic are involved. What is the most appropriate starting point?

- **A.** Use the SDK's built-in tools such as Read, Edit, Bash, Glob, and Grep without building any custom tools or MCP servers
- **B.** Build a custom tool for reading files and another for running shell commands before writing any code
- **C.** Connect an external MCP server that reimplements filesystem and shell access over a network protocol
- **D.** Write a Skill containing instructions for how to read files and run commands in place of built-in tools

**Correct answer:** A

**Explanation:**

- A (correct): Correct: the Agent SDK includes built-in tools for reading files, running commands, and searching code out of the box, covering this task without any custom implementation.
- B: Building custom tools for file reading and command execution duplicates capabilities the built-in tools already provide, adding unnecessary implementation work for a one-off task.
- C: An external MCP server built to reimplement filesystem and shell access over the network adds infrastructure and latency for functionality already available locally as built-in tools.
- D: A Skill provides knowledge or workflow instructions; it cannot substitute for the actual tool execution that Read, Edit, and Bash already perform natively.
Want the full experience?
These are just samples. Practice the full Anthropic Claude Certified Developer – Foundations (CCDV-F) question bank in quiz mode — free, no signup, with domain practice and exam simulation.
Practice all 524 questions in quiz mode
Related certifications
Anthropic Claude Certified Associate – Foundations (CCAO-F)
Anthropic Claude Certified Architect – Foundations (CCAR-F)
Anthropic Claude Certified Architect – Professional (CCAR-P)
About
Announcements
Feedback
Legal
Privacy
Disclaimer
Support us
Donate Share CertSafari on LinkedIn Follow Maarten on LinkedIn
Built and maintained by Maarten van Hooft .
© 2026 CertSafari. All rights reserved.
