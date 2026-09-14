# Anthropic Claude Certified Architect – Foundations (CCAR-F)

Source: https://www.certsafari.com/anthropic/claude-certified-architect-foundations/practice-questions

Free sample: 35 questions with answers and explanations. The full bank is 480 questions and is gated by the site quiz mode (Cloudflare Turnstile).

## Question 1

An architect reviews a multi-agent research assistant and finds that each subagent independently implements its own retry logic, logging format, and rate-limit backoff, leading to inconsistent behavior across the system. Which change best aligns this design with the hub-and-spoke coordinator pattern's intended benefits?

- **A.** Standardize the retry logic across subagents by copying the identical code into each subagent's own system prompt
- **B.** Remove logging and retry logic from subagents entirely, since coordinator-based systems should never retry failed subtasks
- **C.** Assign one subagent the role of monitoring the others' retries and logs so the coordinator need not track failures
- **D.** Centralize error handling, logging, and retry policy in the coordinator so all subagent communication stays consistent

**Correct answer:** D

**Explanation:**

- A: Duplicating the same retry code into every subagent's prompt still leaves the logic scattered across subagents rather than centralized, and prompts are an unreliable place to enforce consistent behavior.
- B: Retries are still a valid and often necessary response to transient failures; the issue is inconsistency across subagents, not that retrying should never happen.
- C: Delegating monitoring to another subagent adds an extra hop and still requires the coordinator to route information, rather than handling error management where communication naturally converges.
- D (correct): Correct. The coordinator manages all inter-subagent communication and error handling in the hub-and-spoke pattern, so centralizing retry, logging, and backoff policy there produces consistent, observable behavior across the system.

## Question 2

An architect is building a client-side agent loop against the Messages API for a data-cleanup task. The first response has stop_reason set to "tool_use" and contains a tool_use block requesting a file-listing tool. What should the loop do next to correctly continue the agentic execution?

- **A.** Execute the requested tool, append a tool_result block tagged with the tool_use_id, and send the full updated conversation back to Claude
- **B.** Append only the tool_use block to history and send a new request with just the original prompt, dropping the tool result needed to interpret it
- **C.** Hold off on running the requested tool until Claude produces assistant text describing exactly what output it expects the tool call to return
- **D.** Run the tool locally, write its output only to an application log file, and resend the prior conversation exactly as it stood before

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The client executes the tool and returns a tool_result block tied to the tool_use_id in the next request; this is how the agentic loop lifecycle continues.
- B: Incorrect. Dropping later context and resending only the original prompt discards the pending tool call and any prior reasoning, breaking the model's view of what it already asked for.
- C: Incorrect. stop_reason "tool_use" is itself the signal to execute immediately; Claude does not need to narrate expected output before the tool runs.
- D: Incorrect. If the tool output never reaches the conversation as a tool_result, Claude has no way to see it and cannot reason about the next action.

## Question 3

An agent loop generating a long report hits a response where stop_reason comes back as "max_tokens" rather than "tool_use" or "end_turn", because the output was truncated before Claude could finish. The loop's control flow only branches on those two familiar values and falls through to the "end_turn" branch by default. What is the risk of that fallback behavior?

- **A.** The loop treats a truncated, incomplete response as if the task were finished, so it stops the agent before Claude has actually completed the work
- **B.** The loop crashes immediately with an unhandled exception, since "max_tokens" is not a value the Messages API is permitted to return
- **C.** The loop automatically increases the max_tokens parameter on the very next outgoing request without any code change, resolving the truncation entirely
- **D.** The loop discards the truncated response entirely and silently resends the very first request in the conversation from scratch

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Falling through to the "end_turn" branch conflates truncation with genuine completion, so the loop ends the task while Claude's response was actually cut off mid-generation.
- B: Incorrect. "max_tokens" is a valid, documented stop_reason value; encountering it does not itself cause an exception unless the loop's own code is broken.
- C: Incorrect. Nothing in the API automatically adjusts max_tokens on a later request; any such adjustment would have to be implemented explicitly by the developer.
- D: Incorrect. The described fallback treats the response as complete rather than discarding it and restarting; resending the original request from scratch is not what a same-value fallback to "end_turn" does.

## Question 4

A coordinator runs a "web-researcher" subagent that gathers ten sources on a topic, then spawns a "synthesis" subagent to write the final report. The synthesis subagent's output ignores nearly all of the researcher's findings and instead re-derives generic conclusions from scratch. The coordinator's prompt to synthesis only said "Write a report based on the research that was just completed." What change fixes this?

- **A.** Include the complete findings from web-researcher directly in synthesis's prompt, since subagents never automatically inherit parent or sibling context
- **B.** Increase the synthesis subagent's maxTurns so it has enough turns to independently rediscover the same ten sources the researcher already found
- **C.** Switch the synthesis subagent's model to a larger model so it infers the missing research context from the phrase "just completed" more reliably
- **D.** Grant synthesis the same search tools as web-researcher so it can re-run the original queries itself before drafting the final written report

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Each subagent starts with a fresh context window; the only channel from parent to subagent is the prompt string, so any prior findings the subagent needs must be written into that prompt explicitly.
- B: Incorrect. More turns does not give the subagent access to data it was never given; it would just spend more turns without the source material.
- C: Incorrect. A larger model cannot infer specific research findings it was never shown; model choice does not substitute for missing context in the prompt.
- D: Incorrect. Re-running the same searches is wasteful and non-deterministic; it does not guarantee the same findings and defeats the purpose of reusing completed work.

## Question 5

A coordinator prompt for a "research-assistant" subagent currently reads: "Step 1: search for the top 5 articles. Step 2: open each one. Step 3: extract the publish date. Step 4: return a table." Reviewers find the subagent produces a table even when the most useful sources have no clear publish date, or when six sources would answer the question better than five. What change to the coordinator prompt would improve outcomes here?

- **A.** Rewrite the prompt around the research goal and quality bar, such as finding credible, relevant sources and reporting what is verifiable, rather than a fixed step sequence
- **B.** Keep the same four numbered steps but increase the required article count from five to six so the subagent always gathers slightly more source material overall
- **C.** Keep the same four numbered steps but add a fifth step instructing the subagent to double-check the publish date it already extracted back in step three
- **D.** Replace the step list with an even more granular ten-step sequence covering search syntax, click order, and field extraction to remove ambiguity entirely

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Framing the coordinator's prompt around goals and quality criteria rather than a rigid procedure lets the subagent adapt, such as gathering more or fewer sources or handling missing fields sensibly, instead of following steps that don't fit every case.
- B: Incorrect. Hard-coding a different fixed count still leaves the subagent locked into procedural steps and does not address sources with no clear publish date or cases needing a different number of sources.
- C: Incorrect. Adding a verification step keeps the same rigid structure and does not help when a source simply has no publish date to extract.
- D: Incorrect. Making the procedure even more granular increases rigidity rather than adaptability, making it harder, not easier, for the subagent to handle sources that don't fit the assumed shape.

## Question 6

A refund workflow requires that process_refund always be called with the exact customer_id captured by an earlier verified get_customer call, never a value the model retypes from the conversation. A PreToolUse hook already blocks the call when no verified ID exists in session state. What should the hook do once a verified ID is present, to prevent the model from substituting a different ID string?

- **A.** Return an empty object so the call proceeds unchanged, since the presence of a verified ID in session state is enough evidence that the model used it
- **B.** Return permissionDecision "allow" together with updatedInput that overwrites the tool's customer_id argument with the verified ID stored in session state
- **C.** Return permissionDecision "ask" so a human reviewer retypes the same ID manually before every refund, even when verification already succeeded
- **D.** Return permissionDecision "defer" so the query pauses indefinitely until an operator resumes it with the corrected customer_id argument

**Correct answer:** B

**Explanation:**

- A: Incorrect. An empty object allows the call with whatever customer_id the model supplied, which is exactly the untrusted value the workflow needs to prevent from reaching the tool.
- B (correct): Correct. Combining "allow" with updatedInput lets the hook substitute the trusted, verified value for whatever the model passed, closing the gap between what was verified and what actually reaches the tool.
- C: Incorrect. Escalating every already-verified refund to manual retyping adds friction without fixing the substitution risk, and does not correct the argument itself.
- D: Incorrect. Defer ends the query for later resumption; it does not correct the argument and is unnecessary once the ID is already verified in session state.

## Question 7

An architect is drafting the handoff protocol for cases where an agent must escalate mid-process to a human supervisor who cannot see the conversation. The draft template currently has one field: a free-text "notes" box the agent fills in however it sees fit. What is the strongest improvement to make the handoffs reliably useful?

- **A.** Remove the notes field entirely and have the human supervisor call the customer back so they can re-explain the entire situation again from the beginning
- **B.** Keep the single free-text field but increase its maximum character limit so the agent has more room available to describe everything it happened to observe
- **C.** Replace the free-text field with required structured fields for customer details, root cause analysis, and a recommended action, so every handoff contains the same essentials
- **D.** Keep the single free-text field but instruct the agent, via the system prompt, to always remember to mention the customer's name somewhere within its written notes

**Correct answer:** C

**Explanation:**

- A: Incorrect. Requiring the customer to re-explain everything defeats the purpose of an agent-compiled handoff and creates a worse customer experience than a good summary would.
- B: Incorrect. A larger character limit does not add structure; the agent could still omit the root cause or the recommended action entirely within a longer unstructured note.
- C (correct): Correct. A structured handoff with defined fields for customer details, root cause, and recommended action guarantees the human agent gets consistent, complete information every time, rather than depending on what an unstructured note happens to include.
- D: Incorrect. This is still a prompt-based nudge on an unstructured field; it does not guarantee root cause analysis or a recommended action are included, only that a name might appear somewhere.

## Question 8

An architect resumed a session and asked the agent to revert a file to a state from earlier in that same conversation, expecting the session itself to have preserved the file's old contents. The agent instead reports it can only see the file's current, edited contents on disk. What explains this behavior?

- **A.** Sessions persist the conversation history, not a snapshot of the filesystem, so file reverts require a separate checkpointing mechanism
- **B.** The resume call must have used the wrong session ID, since a correct resume would restore the earlier file contents automatically
- **C.** fork_session was required to preserve the file's earlier state, and it was omitted from this particular resume call
- **D.** The agent's read tool caches results only for the current turn, so earlier reads are always inaccessible after resuming

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Sessions save conversation history, tool calls, and results, but not a filesystem snapshot; reverting actual file contents to an earlier point requires the separate file-checkpointing feature, not session resume alone.
- B: Incorrect: resuming the correct session ID restores the conversation's history and reasoning, but conversation history was never a mechanism for restoring file contents, regardless of which session ID was used.
- C: Incorrect: fork_session controls whether resuming creates a branch versus continuing in place; it has no effect on whether filesystem contents are snapshotted or restorable.
- D: Incorrect: earlier tool results remain visible in the resumed conversation history; the issue is that history doesn't restore the file's actual on-disk bytes, not that earlier reads vanish from context.

## Question 9

A reviewer is designing an agentic code review for a pull request that touches 40 files across a monorepo. Reviewers have noticed that when a single pass tries to hold all 40 files in context at once, subtle cross-file issues are missed and comments become generic. What restructuring addresses this attention dilution problem?

- **A.** Run a per-file local analysis pass on each file independently, then run a separate cross-file integration pass over the per-file findings
- **B.** Raise the review prompt's sampling temperature so the single combined pass considers a wider range of possible issues across all the files
- **C.** Keep the single combined pass but instruct the model to prioritize whichever files appear first in the diff ordering
- **D.** Randomize the file order within the single combined pass before each run so different files receive more attention each time

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Splitting the review into focused per-file passes avoids attention dilution, and a dedicated cross-file pass afterward catches integration issues that per-file review alone would miss, matching the recommended pattern for large reviews.
- B: Adjusting sampling temperature does not address the underlying problem of too much context competing for attention in a single pass; it changes output variability, not scope management.
- C: Prioritizing by diff order in a single combined pass still holds all 40 files in context at once and does not solve the dilution problem, it only biases which files get more attention.
- D: Randomizing file order across runs does not reduce the total context held in any single pass and produces inconsistent coverage rather than systematically avoiding dilution.

## Question 10

An architect is building a custom session picker for an internal tool and needs a way to enumerate every session on disk for a repository along with reading a particular session's full message history, without shelling out to the interactive CLI picker. Which SDK-exposed functions fit this need?

- **A.** listSessions() to enumerate sessions and getSessionMessages() to read a session's messages
- **B.** renameSession() to enumerate sessions and tagSession() to read a session's messages
- **C.** getSessionInfo() to enumerate all sessions and resume() to read a session's messages
- **D.** fork_session() to enumerate sessions and continue() to read a session's messages

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Anthropic's Agent SDK (both Python and TypeScript) provides `listSessions()` (or `list_sessions()` in Python) to return a list of all sessions on disk sorted by last-modified time, and `getSessionMessages()` (or `get_session_messages()`) to retrieve the full message history for a given session. These functions are the recommended approach for building custom session pickers or transcript viewers per official documentation.
- B: Incorrect. `renameSession()` is used to rename a session's file, not to enumerate sessions. There is no `tagSession()` function in the SDK. The correct functions are `listSessions()` for enumeration and `getSessionMessages()` for reading messages.
- C: Incorrect. `getSessionInfo()` is not documented as a function to enumerate all sessions; rather, information about a specific session can be obtained from the data returned by `listSessions()`. `resume()` is used to continue an existing session, not to read its message history. Use `getSessionMessages()` to access historical messages.
- D: Incorrect. `fork_session()` is a function to create a new session based on an existing one, not to enumerate sessions. `continue()` is not the standard way to read message history; the SDK provides `getSessionMessages()` for that purpose. For enumeration, use `listSessions()`.
Domain 2: Tool Design & MCP Integration

## Question 11

A single tool, `analyze_document`, extracts data points, produces summaries, and verifies claims against a source. Users report it inconsistently performs only one of these behaviors for ambiguous requests. Which redesign best addresses this?

- **A.** Keep the single tool but instruct the model, in the system prompt, to always call it three separate times per request.
- **B.** Merge the tool with unrelated tools into one larger tool so the model faces fewer total choices overall.
- **C.** Split the tool into `extract_data_points`, `summarize_content`, and `verify_claim_against_source`, each with a narrow contract.
- **D.** Add a required `mode` enum parameter to the existing tool, but leave its single overarching description unchanged.

**Correct answer:** C

**Explanation:**

- A: Incorrect. Forcing three calls per request wastes invocations on tasks that need only one behavior and does not resolve the ambiguity about which behavior was intended.
- B: Incorrect. Merging with unrelated tools increases the surface area of a single tool's responsibilities, worsening overlapping-purpose confusion rather than resolving it.
- C (correct): Correct. Splitting a generic multi-purpose tool into purpose-specific tools with defined input/output contracts removes the ambiguity about which behavior a call should trigger.
- D: Incorrect. Adding a mode parameter without updating the description still leaves the model guessing at the tool's overall purpose and when each mode applies.

## Question 12

An architect is rolling out a GitHub MCP server for the whole engineering team. Every teammate has their own GitHub personal access token, and the config must be checked into the repo without ever committing a real secret. How should the architect configure this?

- **A.** Add the server with project scope in .mcp.json, and set the header to `Authorization: Bearer ${GITHUB_TOKEN}` so each teammate's environment supplies the value at connection
- **B.** Add the server with user scope in ~/.claude.json, and paste each teammate's literal token value into the shared header field before committing that file to the repo
- **C.** Add the server with local scope, then have every teammate individually edit their own copy of .mcp.json to insert their personal token in place of a placeholder
- **D.** Add the server with project scope, then add .mcp.json to .gitignore so the checked-in repository never actually contains the shared server configuration file

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Project scope stores the server in .mcp.json for team-wide sharing via version control, and ${GITHUB_TOKEN} expansion pulls the value from each user's own environment at connection time, so no secret is ever committed.
- B: User scope stores the entry in ~/.claude.json, which is private to one machine and not shared with the team, and pasting literal tokens defeats the goal of never committing secrets.
- C: Local scope is private to the current project on one machine and is not checked into version control at all, so it cannot serve as the shared team configuration the scenario requires.
- D: Ignoring .mcp.json removes the shared configuration entirely, meaning no teammate gets the server automatically and the stated goal of a checked-in, team-wide config is not met.

## Question 13

An architect asks Claude Code to identify every React test file in a codebase where naming mixes `.test.tsx`, `.spec.tsx`, and older files simply ending in `Test.tsx`, spread across many nested feature directories. Only a list of matching file paths is needed, with no content inspection. Which tool is the most direct fit?

- **A.** Bash, using a recursive directory listing command and then manually reading every returned file to check its extension
- **B.** Grep, using output mode files_with_matches and a regex that matches the word test anywhere inside a file's contents
- **C.** Glob, using patterns such as **/*.test.tsx, **/*.spec.tsx, and **/*Test.tsx to match the naming conventions directly
- **D.** Read, pointed at the project root directory so it returns a recursive listing of every file that exists below it

**Correct answer:** C

**Explanation:**

- A: Incorrect. A recursive Bash listing followed by manually reading every file to check its name is far less direct than a purpose-built path-pattern match, and unnecessarily consumes context reading files that were never needed.
- B: Incorrect. Grep searches file contents, not file names; searching for the word test inside file bodies would return unrelated files that mention testing and could miss test files that never use that literal word.
- C (correct): Correct. Glob matches file paths by name pattern, including recursive ** matching, so running it with the three naming conventions directly returns exactly the matching file paths without needing to inspect any file contents.
- D: Incorrect. Read loads the contents of a single file at a given path and does not list directories at all, so pointing it at the project root would not produce a recursive file listing.

## Question 14

A coordinator dispatches the same document-indexing task to three subagents in parallel, each covering a different folder. Subagent 1 finishes cleanly. Subagent 2 hits a permission error on one file it cannot resolve locally and reports partial results plus that failure. Subagent 3's process crashes with no output at all. How should the coordinator's downstream handling differ between subagent 2 and subagent 3?

- **A.** For subagent 2, the coordinator can use the partial results and address the specific reported permission gap; for subagent 3, lacking completed work or diagnostic detail, it must treat the entire folder as unprocessed.
- **B.** The coordinator should treat both subagent 2 and subagent 3 identically by discarding any partial results from subagent 2 and marking both folders for indexing as unprocessed, since neither subagent fully completed its assigned indexing task successfully.
- **C.** The coordinator should treat both subagent 2 and subagent 3 identically by retrying files with permission errors, assuming subagent 3's crash was also due to a permission issue on some file, since that is the most common cause of non-completion in such tasks.
- **D.** For subagent 2, the coordinator should ignore the reported permission error and mark the folder complete, since most files were indexed successfully, and for subagent 3, the coordinator should also mark its folder complete because no error was reported.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Subagent 2 returns partial results and a specific permission error, allowing the coordinator to integrate successes and precisely address the failure. Subagent 3 provides no output, leaving no basis for targeted recovery, so the entire folder must be considered unprocessed.
- B: Incorrect. Discarding subagent 2's partial results wastes completed indexing work and ignores diagnostic detail that could guide precise recovery. Treating a structured partial failure the same as a total, silent crash is wasteful and overlooks actionable information.
- C: Incorrect. Assuming a crash with no output was caused by a permission error is speculative and unfounded; crashes can stem from many root causes. Guessing without evidence risks misdirecting recovery efforts and may not resolve the actual issue.
- D: Incorrect. Ignoring a reported permission gap and marking the folder complete hides a real indexing deficiency from downstream consumers. Additionally, treating subagent 3's folder as complete when no output was received masks a total processing failure.

## Question 15

A tool description reads "Updates a customer record with given fields." In practice, the model frequently passes fields that don't exist on the schema, and it's unclear whether partial updates are supported. What documentation gap explains this failure mode?

- **A.** The tool's JSON schema uses camelCase field names, which conflicts with the model's snake_case training, causing invalid field passing.
- **B.** The customer record tool was declared after read-only tools, causing the model to deprioritize it and pass fields not defined in the schema.
- **C.** The description omits the expected input format and boundary behavior, such as which fields are valid and whether partial updates work.
- **D.** The model cannot reliably handle optional parameters, so the documentation must require every field to be marked required, such as all fields being mandatory.

**Correct answer:** C

**Explanation:**

- A: Incorrect. Anthropic models are trained on diverse text and can handle camelCase field names without issue. There is no documented conflict with snake_case that would cause the model to pass invalid fields. The failure stems from unclear tool specification, not casing conventions.
- B: Incorrect. Tool declaration order does not influence tool prioritization or cause the model to pass invalid fields. The model selects tools based on user intent and tool descriptions, not declaration order. No evidence suggests order impacts field validity.
- C (correct): Correct. Anthropic's best practices stress that tool descriptions must specify valid fields, expected formats, and boundary conditions (like partial update support) to prevent model hallucination. Without these details, the model cannot reliably infer correct inputs, leading to the observed failures. Official documentation emphasizes clear input schemas to avoid such ambiguity.
- D: Incorrect. Claude can handle optional parameters if they are properly defined in the tool's schema. Requiring all fields as mandatory is not a documentation gap but an overly restrictive design choice that deviates from standard API practices and limits flexibility. The core issue is insufficient description, not optional parameter support.

## Question 16

An onboarding agent walks a new user through account setup and needs to call create_profile immediately as the very first action of the conversation, before considering any other tool such as send_welcome_email or assign_default_settings. After that first call, the agent must be free either to call one of the remaining tools or to reply to the user in plain text, depending on what the user says. What is the best way to configure this?

- **A.** Use tool_choice: {"type": "tool", "name": "create_profile"} for the first turn only, then switch to tool_choice: {"type": "auto"} for subsequent turns
- **B.** Use tool_choice: {"type": "any"} for the entire conversation so the model is always forced to pick from create_profile, send_welcome_email, and assign_default_settings
- **C.** Order create_profile first in the tools array and leave tool_choice at {"type": "auto"} for the whole conversation
- **D.** Use tool_choice: {"type": "none"} for the first turn so the model cannot call any tool, then switch to {"type": "auto"} afterward

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Naming the tool in tool_choice forces that specific tool, so create_profile is guaranteed to run as the opening action. Switching to auto afterward is what the later turns need: auto lets Claude decide whether to call any provided tool or not, so the agent can invoke a remaining tool when the user's reply calls for one and answer in plain text when it does not.
- B: Incorrect. The any setting requires the model to use one of the provided tools without forcing a particular one, so it never guarantees that create_profile runs first. It also prefills a tool call on every turn, so the agent could never respond to the user in plain text.
- C: Incorrect. Position in the tools array is not a documented mechanism for controlling which tool is called first. Under auto the model decides whether to call a tool at all and which one, so create_profile is not guaranteed to be the opening action.
- D: Incorrect. The none setting prevents Claude from using any tools, so blocking tool calls on the first turn also blocks create_profile, the very action that is required to happen first.

## Question 17

A coordinator agent delegates a three-step data migration to a subagent: extract, transform, and load, but the load step fails twice on a database connection reset, a known transient condition, before finally succeeding on the third attempt inside the subagent's own execution. What should the subagent report back to the coordinator?

- **A.** A success result summarizing the completed migration, since the transient failures were resolved locally and never needed to surface above the subagent
- **B.** An `isError: true` result describing both connection resets in detail, so the coordinator can decide independently whether the migration should be retried
- **C.** A partial-results payload listing only the extract and transform steps as done, omitting the load step entirely since it initially failed twice
- **D.** An escalation asking the coordinator to obtain new database credentials, since two consecutive connection resets indicate the credentials have expired

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The Claude Agent SDK's subagent design keeps intermediate tool calls and results inside the subagent's own execution: only the subagent's final message returns to the parent, so a subagent can work through a transient failure without that internal detail flowing up to the coordinator's context. Because the load step ultimately succeeded, reporting a success result reflects the actual final state accurately. Flagging the tool result as failed here would misrepresent a step that succeeded, since MCP's isError flag is defined for reporting an execution that still needs correction, not one that already recovered before returning.
- B: Incorrect. The MCP specification defines isError: true for reporting a tool execution that failed, giving actionable feedback the model can use to self-correct and retry — an outcome that still needs to be acted on. By the time the subagent reports back, the load step has already succeeded, so marking the result as an error would misrepresent the actual, successful outcome. The Agent SDK's subagent design also keeps intermediate tool calls and results inside the subagent's own context; only its final message returns to the parent, so surfacing every internal retry to the coordinator defeats the purpose of delegating the step in the first place.
- C: Incorrect. The load step finished successfully on the third attempt, so a report that omits it entirely would understate what was actually accomplished and could cause the coordinator to unnecessarily re-run a step that already completed.
- D: Incorrect. A connection reset is a transient network-level failure, not an authentication failure; expired credentials would produce a consistent authentication error on every attempt rather than a reset that clears on retry. Escalating for new credentials here targets the wrong cause and would delay a migration that had already completed.
Domain 3: Claude Code Configuration & Workflows

## Question 18

A team is choosing between two integration approaches for a new payment provider: one requires a new message queue and asynchronous worker fleet, the other requires synchronous calls from existing services with added retry logic. Each has different infrastructure and operational tradeoffs, and the team has not yet decided which to pursue. What is the most appropriate way to proceed with Claude Code?

- **A.** Have Claude implement the asynchronous queue approach directly and immediately, since new infrastructure work always outranks synchronous changes
- **B.** Use plan mode to have Claude explore both approaches and surface the infrastructure tradeoffs before any implementation starts
- **C.** Have Claude implement both approaches in parallel branches with direct execution and compare the resulting pull requests once both are finished
- **D.** Skip codebase exploration entirely and let Claude choose an approach based solely on which one requires fewer new files to be created

**Correct answer:** B

**Explanation:**

- A: Committing to the asynchronous approach without evaluating the tradeoffs skips the architectural decision the team explicitly has not made yet, and could commit them to unwanted new infrastructure.
- B (correct): Correct. Choosing between integration approaches with different infrastructure requirements is an architectural decision, and plan mode lets Claude investigate and propose a design safely before either approach is committed to code.
- C: Building out two full infrastructure approaches directly is far more costly than evaluating tradeoffs first in plan mode, and defeats the purpose of preventing costly rework.
- D: File count is not a meaningful proxy for infrastructure or operational tradeoffs, and this ignores the exploration step needed to compare the approaches properly.

## Question 19

A CI pipeline needs to parse Claude's response programmatically to decide whether a build step should fail. The team wants the reply to always match a specific JSON shape, for example an object with a boolean `passed` field and an array of `issues` strings, regardless of how Claude phrases its reasoning. Which invocation achieves this?

- **A.** claude -p "review this diff" --output-format json --json-schema '{"type":"object","properties":{"passed":{"type":"boolean"},"issues":{"type":"array","items":{"type":"string"}}},"required":["passed","issues"]}'
- **B.** claude -p "review this diff and reply only with passed:true/false and a list of issues" --output-format text
- **C.** claude -p "review this diff" --output-format stream-json --verbose --include-partial-messages
- **D.** claude -p "review this diff" --append-system-prompt "Always respond with valid JSON matching {passed, issues}"

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Combining --output-format json with --json-schema validates the model's structured output against the supplied schema and returns it in the structured_output field, giving a guaranteed machine-parseable shape.
- B: Asking nicely in the prompt with plain text output gives no schema enforcement; Claude can vary phrasing or omit fields, and the CI script would need fragile text parsing.
- C: stream-json streams turn-by-turn events for real-time display, it does not validate or constrain the final answer to a specific object schema.
- D: Appending schema instructions to the system prompt is a soft hint with no validation; the model can still drift from the exact shape, unlike an enforced --json-schema.

## Question 20

A release pipeline calls `claude -p --output-format json "summarize the changes in this release"` and pipes the result to a script that reads `.result`. Finance now also wants each invocation's per-model API spend recorded for cost tracking, without adding any new flags. Where does that information already appear?

- **A.** The JSON response body already includes total_cost_usd along with a per-model cost breakdown alongside the result field
- **B.** The cost data is only available by separately querying the Claude usage dashboard after the run completes
- **C.** Cost data only appears when --output-format stream-json and --verbose are both set, so the job must switch formats
- **D.** Per-invocation cost is written to a local .claude/usage.log file that the script must additionally parse

**Correct answer:** A

**Explanation:**

- A (correct): Correct. With --output-format json, the response payload includes total_cost_usd and a per-model cost breakdown, so scripted callers can track spend per invocation directly from the existing JSON output.
- B: The usage dashboard is a separate aggregate view; per-invocation cost is already returned inline in the JSON response, so a dashboard lookup isn't required for this use case.
- C: Cost fields are part of the standard --output-format json response; switching to stream-json is unnecessary and changes the output shape the script already depends on.
- D: Claude Code does not write per-invocation cost to a local usage.log file; the cost fields are part of the JSON response returned directly by the CLI.

## Question 21

A developer configured `allowed-tools: Write Edit` on a skill, expecting this to prevent Claude from ever calling Bash while the skill runs. During a session, Claude still calls Bash after asking for the user's approval. Why did this happen, and what should the developer configure instead to fully remove Bash from the available pool while the skill is active?

- **A.** `allowed-tools` is evaluated only after the skill finishes running, so Bash calls made during the skill are unaffected by its configuration. To remove Bash, set `context: fork` on the skill to sandbox execution and block unlisted tools.
- **B.** `allowed-tools` requires trailing wildcards, such as `Write*` and `Edit*`, to restrict tools; without them, all tools including Bash are implicitly allowed. To block Bash, append `*` to each allowed tool so only those tools can be called.
- **C.** `allowed-tools` only constrains tools invoked directly by the user, and does not limit tools that Claude chooses during skill execution. To remove Bash, set `model: inherit` on the skill to override Claude's autonomous tool selection.
- **D.** `allowed-tools` only pre-approves the listed tools without prompting; it does not remove other tools from availability. Adding `disallowed-tools: Bash` removes Bash from Claude's pool while the skill is active.

**Correct answer:** D

**Explanation:**

- A: Incorrect. `allowed-tools` constrains the tool pool for the entire duration the skill is active, not just after it finishes. `context: fork` changes where the skill executes but does not block tools; it's not a sandbox that automatically blocks unlisted tools. To fully remove Bash, `disallowed-tools` should be used.
- B: Incorrect. `allowed-tools` does not require trailing wildcards to restrict tools; it already restricts Claude to only those specifically listed tools. Wildcards are used to match tool names by pattern, but omitting wildcards does not implicitly allow all tools. To block Bash, `disallowed-tools: Bash` must be explicitly set.
- C: Incorrect. `allowed-tools` restricts all tools that Claude can call during skill execution, not just those invoked directly by the user. `model: inherit` only determines which model handles the request and has no impact on tool availability. To remove Bash, you need `disallowed-tools` in the skill configuration.
- D (correct): Correct. `allowed-tools` pre-approves the listed tools so they run without prompting, but it does not remove unlisted tools; they remain callable subject to normal permission settings. To actually remove Bash from Claude's available tools during skill execution, `disallowed-tools: Bash` must be configured. This is why Bash was still callable with approval.

## Question 22

A developer wants Claude Code to implement a rate limiter for an internal API and wants to reduce the number of correction cycles needed afterward. Which opening approach best follows a test-driven iteration pattern?

- **A.** Ask Claude to write a test suite covering the expected throttling behavior, burst limits, and reset timing first, then implement the rate limiter, iterating by sharing test failures.
- **B.** Ask Claude to implement the rate limiter first, then write a matching test suite afterward that validates throttle responses, burst handling, and window resets to document the built behavior.
- **C.** Ask Claude to implement the rate limiter and manually verify it by running sample requests such as bursts, retries, and checking rate limit headers in the terminal, without automated tests.
- **D.** Ask Claude to describe the rate limiting algorithm in a design document covering throttle rules, burst limits, and reset windows, then implement it from that document without writing tests.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Writing the test suite first specifying throttling behavior, burst limits, and reset timing establishes concrete expected behaviors. Iterating by sharing test failures then provides a focused signal that drives progressive refinement toward a correct implementation.
- B: Incorrect. Writing tests after implementation only documents the behavior that was built, so it cannot catch misunderstandings of intended throttling or reset rules. This approach does not guide implementation and misses the opportunity to iterate based on test failures.
- C: Incorrect. Manual checks via terminal sampling of bursts, retries, and headers do not create a repeatable, shareable failure signal. Without automated tests, there is no structured basis for iterative refinement and verifying correctness after changes.
- D: Incorrect. A design document describing throttle rules, burst limits, and reset windows is only a prose specification; it does not provide executable checks. Without tests, Claude cannot verify its own implementation nor iteratively refine based on failures.

## Question 23

A new engineer joins a team that has used Claude Code for six months. All other teammates report that Claude consistently follows the project's commit message format and test-running conventions, but for the new engineer Claude ignores these conventions entirely, even though they cloned the repository fresh and confirmed that a CLAUDE.md file is present in the repo on GitHub. Upon inspection, however, the file is empty and contains none of the expected conventions. What is the most likely root cause?

- **A.** The conventions are stored in the existing team members' personal CLAUDE.md files (e.g., ~/.claude/CLAUDE.md), not in the project's committed CLAUDE.md, so the new engineer never loads them.
- **B.** The new engineer's local git client is silently skipping markdown files during checkout, so CLAUDE.md never lands on disk at all.
- **C.** Claude Code caches CLAUDE.md content per machine on first run, so the new engineer must trigger a manual cache rebuild locally.
- **D.** The repository's CLAUDE.md exceeds the token limit for brand-new sessions, so it is dropped only for engineers with no prior history.

**Correct answer:** A

**Explanation:**

- A (correct): This is the most likely cause. Per Anthropic's documentation, team-wide conventions must be placed in a project-level `CLAUDE.md` file (e.g., `./CLAUDE.md` or `./.claude/CLAUDE.md`) that is committed to the repository. This ensures every developer, including new hires, automatically receives and loads these instructions. User-level `~/.claude/CLAUDE.md` files are for personal preferences only and are not shared via Git, so conventions stored there remain invisible to others. Since the committed project file was empty, the new engineer's Claude Code session had no team conventions to follow.
- B: This scenario is implausible. Git does not silently skip markdown files by default, and the engineer confirmed the file was present in the repository. No known Git configuration or behavior would cause selective omission of `.md` files during clone or checkout. The issue is clearly with the content of the file, not its absence.
- C: Claude Code does not cache `CLAUDE.md` file contents in a way that would cause a new user to ignore conventions. The loading of `CLAUDE.md` files happens dynamically at the start of each session, reading the current file system state. There is no persistent cache that would require a manual rebuild. Official documentation describes the loading as automatic and hierarchical, not dependent on prior runs.
- D: This does not align with documented behavior. While `CLAUDE.md` files are recommended to be concise (ideally under 200 lines) to preserve context window space, exceeding a token limit would not cause the file to be silently dropped only for new engineers. If the file is present and non-empty, it is loaded for every session regardless of user history. The scenario explicitly states the file was empty, so token limits are irrelevant.

## Question 24

A product architect wants Claude Code to build a real-time collaborative document editor, a domain the architect has not built in before. Before any implementation starts, the architect wants to surface cache invalidation strategy, conflict resolution approach, and failure handling considerations that might not be obvious up front. What technique should the architect use?

- **A.** Give Claude a brief description of the feature and ask it to interview the architect using the AskUserQuestion tool, exploring technical implementation, edge cases, and tradeoffs before writing a spec.
- **B.** Write a complete technical specification personally covering every design decision, including cache invalidation, conflict resolution, and failure handling, then hand it to Claude as a fixed set of implementation instructions.
- **C.** Ask Claude to implement a minimal collaborative editor, then use every bug and edge case found through manual testing as the primary source to surface cache invalidation, conflict resolution, and failure handling design considerations.
- **D.** Search for an open-source collaborative editor, instruct Claude to replicate its architecture, and assume that following its design patterns will automatically surface appropriate cache invalidation and conflict resolution strategies.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. This leverages an interactive requirements-gathering interview before any implementation starts, which is the recommended way to surface non-obvious design considerations such as cache invalidation, conflict resolution, and failure handling. The provided research does not independently verify the `AskUserQuestion` tool name, but it does confirm that thoroughly exploring technical implementation, edge cases, and tradeoffs with an architect before writing a specification is a fundamental recommended practice.
- B: Incorrect. Writing a complete fixed specification up front often misses considerations that are not obvious to the architect, especially in an unfamiliar domain. The recommended practice is to clarify constraints, gather feedback, and explore tradeoffs collaboratively before finalizing the spec, not to lock all decisions in beforehand.
- C: Incorrect. This approach starts implementation before surfacing design considerations, which defeats the "before any implementation starts" requirement. Iterative testing and bug review are valuable later, but they are not a substitute for upfront architectural exploration of cache invalidation, conflict resolution, and failure handling.
- D: Incorrect. Copying an open-source architecture does not automatically surface the right design considerations for a different product context; those patterns may hide assumptions or fail under different requirements. The recommended approach is to elicit and examine tradeoffs with the architect before implementation, not to rely on a copied architecture's implicit choices.
Domain 4: Prompt Engineering & Structured Output

## Question 25

Per-file passes on two interdependent files each recommend a different fix for what turns out to be the same underlying data-flow issue, and the two recommendations conflict. What architectural step should resolve this rather than picking one per-file recommendation at random?

- **A.** A separate cross-file integration pass that examines both files together and produces one recommendation based on the actual data flow
- **B.** Re-running each per-file pass a second time and keeping whichever recommendation is worded with higher confidence language
- **C.** Merging the two files into one before review so a single per-file pass can cover both without needing an integration step
- **D.** Asking the original generator to arbitrate between the two recommendations, since it has full context on why it wrote the code that way

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A cross-file integration pass is designed to resolve exactly this kind of conflict by examining how data flows between the interdependent files together, rather than in separate isolated passes.
- B: Incorrect. Confidence-sounding wording doesn't reflect which recommendation actually accounts for the real cross-file data flow.
- C: Incorrect. Merging files together is not the designed mechanism and doesn't generalize; the intended fix is a dedicated integration pass, not restructuring the files under review.
- D: Incorrect. Letting the original generator arbitrate reintroduces the same retained-reasoning bias that independent review is meant to avoid.

## Question 26

A team's automated PR-review prompt currently instructs Claude to "check that comments are accurate." The category produces a high volume of false positives on trivial phrasing nitpicks, and developers have started ignoring its output. An architect is rewriting the instruction to raise precision. Which replacement instruction best applies the principle of explicit criteria over vague instructions?

- **A.** Ask Claude to only flag a comment when it is highly confident the comment makes a factual error about the code, such as claiming a method does not exist when it is clearly present in the codebase, and to ignore borderline cases.
- **B.** Tell Claude to flag any comment that could plausibly be improved in clarity, completeness, or consistency with the team's style guide, such as an ambiguous phrase that might confuse a reader, and to suggest a clearer version.
- **C.** Instruct Claude to evaluate each comment and flag only those that it deems significant enough to warrant developer attention, such as a comment that could cause a bug if misunderstood, and to ignore trivial wording differences.
- **D.** Flag a comment only when it makes a specific claim about behavior that is contradicted by what the code actually does, such as a docstring stating a function returns None when it always returns a value.

**Correct answer:** D

**Explanation:**

- A: Incorrect. Asking Claude to be 'highly confident' relies on the model's internal certainty rather than providing a concrete, verifiable rule. This confidence-based filter does not define explicit criteria for what constitutes a factual error, so it fails to reliably improve precision.
- B: Incorrect. This instruction is broader and vaguer than the original, explicitly inviting style and clarity nitpicks rather than narrowing scope to factual contradictions. It would increase false positives, not reduce them.
- C: Incorrect. This instruction delegates the decision to the model's subjective judgment of 'significance' rather than providing explicit criteria. It relies on the model to determine what warrants attention, which is the same failure mode as the original vague instruction, and does not improve precision.
- D (correct): Correct. This defines a concrete, checkable criterion (a factual contradiction between a stated claim and observed code behavior) with a worked example, which is exactly the kind of explicit categorical rule that reduces false positives compared to a vague instruction like 'check that comments are accurate.'

## Question 27

An automated code reviewer flags many instances of a pattern (a broad except clause) as issues, but a large fraction of those flags are on lines where the pattern is intentional and acceptable, such as top-level error boundaries that log and re-raise. Reviewers are starting to ignore the tool's output because of the false-positive rate. What change would most directly reduce false positives while still catching genuine issues?

- **A.** Add paired examples of a genuinely problematic instance and an acceptable instance, each with the correct verdict
- **B.** Remove the broad except clause check from the rule set entirely, since it currently produces too many false positives
- **C.** Instruct the model to only flag the pattern when it appears more than three times in the same file
- **D.** Lower the confidence threshold so only the single highest-confidence finding per file is reported

**Correct answer:** A

**Explanation:**

- A (correct): Using paired examples with correct verdicts helps the automated reviewer learn the boundary between intentional acceptable uses and genuine violations. Anthropic's guidance for reducing false positives in safety classifiers emphasizes showing both problematic and acceptable instances with labeled verdicts, rather than simply removing or thresholding checks. This approach directly addresses context-based misclassification and preserves detection of real issues.
- B: Removing the check eliminates false positives but also eliminates all genuine detections, creating false negatives. Official safety guidance warns against overly broad removal and emphasizes balancing helpfulness with appropriate limitations. The better approach is to refine the check with labeled examples or adjust its scope, not to remove it wholesale.
- C: A frequency-based threshold is arbitrary and would miss single genuine issues. False positives arise from misclassifying context, not from how many times a pattern appears. This change would reduce true positives without teaching the model the acceptable boundary between intentional top-level error handling and problematic bare except clauses.
- D: Lowering the confidence threshold typically increases false positives, not reduces them, and reporting only one finding per file suppresses other genuine issues. The goal is better boundary discrimination through targeted examples or scope refinement, not artificially limiting output volume.

## Question 28

An invoice-extraction pipeline returns structured JSON that is missing the required `invoice_number` field, even though the number is clearly printed on the source PDF. The team wants to retry the extraction with targeted feedback so the model can correct the omission. Which retry design is most likely to succeed?

- **A.** Resend the original PDF plus the prior failed JSON, and state that `invoice_number` is required but was omitted from that attempt
- **B.** Send only the validation error text by itself, without re-attaching the source PDF or the earlier failed output from the first pass
- **C.** Discard the whole conversation and resend the unchanged original prompt, hoping sampling variance yields a different result this time
- **D.** Rewrite the system prompt with new wording and resend it with the PDF, without naming the missing field or the earlier attempt

**Correct answer:** A

**Explanation:**

- A (correct): Research-supported validation feedback loops recommend providing the original document plus the identified extraction errors as context when asking the model to re-extract problematic fields. Including the prior failed JSON and explicitly naming `invoice_number` gives the model both the source data and the specific omission to fix, making this the strongest retry design among the options. For a more prevent-first approach, Anthropic's Structured Outputs feature can enforce required JSON fields from the start.
- B: Incorrect. Without the source PDF, the model has no document context from which to extract the missing `invoice_number`. Omitting the earlier failed JSON also removes useful context about what the first pass returned, making it harder for the model to identify and correct the specific omission.
- C: Incorrect. Resending the same original prompt without any feedback does not address the omission, and relying on sampling variance is not a reliable correction strategy. The model may repeat the same error, especially since it received no new signal that `invoice_number` is required.
- D: Incorrect. Changing the system prompt wording without explicitly identifying the missing `invoice_number` field or referencing the earlier failed attempt provides only vague guidance. The model is less likely to correct the omission if the specific validation failure is not communicated.

## Question 29

A team building a resume-parsing tool wants to guarantee that structured candidate data is extracted via a `parse_resume` tool on the current turn. They also want to know whether Claude can include natural-language reasoning about ambiguous resume sections before that tool call. Which `tool_choice` configuration should be used to guarantee the `parse_resume` call, and what does Anthropic documentation state about natural-language commentary before a forced tool call?

- **A.** `tool_choice: {"type": "auto"}`, combined with an explicit user-message instruction to use the `parse_resume` tool and share any relevant reasoning as text
- **B.** `tool_choice: {"type": "any"}`, because `any` allows Claude to freely mix natural-language commentary with the forced tool call in the same response
- **C.** `tool_choice: {"type": "tool", "name": "parse_resume"}`, because this is the documented way to force the specific tool; the trade-off is that forced tool use suppresses natural-language text before the tool call
- **D.** `tool_choice: {"type": "none"}`, so Claude can freely decide in text whether to also produce a `parse_resume` tool call afterward

**Correct answer:** C

**Explanation:**

- A: Incorrect. `auto` is the default behavior; Claude decides whether to call any provided tool based on the request and tool descriptions. An explicit instruction may influence the model, but it does not guarantee the `parse_resume` tool will be called. Natural-language reasoning may occur if Claude chooses to respond in text instead of using a tool, which fails the requirement for guaranteed structured extraction.
- B: Incorrect. `any` forces Claude to use one of the provided tools, but does not force the specific `parse_resume` tool; Claude may choose a different tool if multiple are available. Moreover, forced tool use (including `any`) prefills the assistant message to force a tool call, which suppresses any natural-language commentary or explanation before the `tool_use` content block, contradicting the claim that commentary can be freely mixed.
- C (correct): Correct. According to Anthropic documentation, setting `tool_choice` to `{"type": "tool", "name": "parse_resume"}` explicitly forces Claude to invoke the named tool. The documentation states that when `tool_choice` is `tool` or `any`, the API prefills the assistant message to force a tool use, meaning the model will not emit a natural language response or explanation before the `tool_use` content block, even if explicitly asked. This satisfies the guarantee of the `parse_resume` call but confirms the limitation that no natural-language reasoning can appear before the forced tool call.
- D: Incorrect. `tool_choice: {"type": "none"}` explicitly prevents Claude from using any tools, so a `parse_resume` tool call will not be made at all. This is the opposite of the requirement to guarantee structured candidate data extraction via the tool. Natural-language text may be produced, but no tool call will follow.
Domain 5: Context Management & Reliability

## Question 30

A utility company customer needs a multi-step billing correction involving a meter re-read, a prorated credit, and a plan adjustment. Every step is explicitly detailed in the documented billing policy, and the agent has tools to execute each step. Should the agent escalate this case simply because it involves several steps?

- **A.** No, the case should be resolved directly; step count alone is not an escalation trigger when policy fully covers it
- **B.** Yes, any case requiring more than one corrective action should be escalated regardless of policy coverage
- **C.** Yes, multi-step cases are inherently too complex for an agent to execute reliably without human oversight
- **D.** No, but only because billing corrections are categorically exempt from any complexity-based escalation rule entirely

**Correct answer:** A

**Explanation:**

- A (correct): Correct - the number of steps alone doesn't determine whether a case should be escalated; since policy fully covers each step, the agent can resolve it directly.
- B: Incorrect - escalation should be driven by actual triggers like policy gaps or customer requests, not simply by how many steps a resolution requires.
- C: Incorrect - a case being multi-step does not make it inherently unresolvable by the agent when each step is clearly defined by policy.
- D: Incorrect - the reasoning is wrong; there's no special exemption for billing corrections, the actual principle is that step count alone isn't a valid escalation trigger.

## Question 31

A logistics company's bill-of-lading extraction pipeline shows 94% field accuracy in aggregate. A new architect discovers that the 'weight' field is correct only 70% of the time specifically when the source document's units are ambiguous (for example, a number with no unit label present). All other conditions for the weight field exceed 95%. What review policy should be applied to the weight field going forward?

- **A.** Route the weight field to human review whenever the source document does not clearly specify units, while allowing high-confidence, unambiguous cases to bypass review.
- **B.** Leave the weight field's review policy unchanged for all documents, since the field's blended 94% aggregate accuracy across the pipeline already meets the general accuracy bar.
- **C.** Remove the weight field from automated extraction entirely and require full manual entry for every bill of lading, regardless of whether units are specified.
- **D.** Increase the model's temperature setting when extracting the weight field so it generates a wider range of candidate values for reviewers to choose from.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The failure is specifically tied to source ambiguity (missing units), so the appropriate policy routes exactly those ambiguous cases to human review while letting unambiguous, well-performing cases continue with reduced review, matching review effort to the identified risk.
- B: Incorrect. Citing the blended aggregate ignores the documented sub-condition where accuracy drops to 70%, which is well below an acceptable bar for unreviewed automation; leaving the policy unchanged would let that specific failure mode continue unflagged.
- C: Incorrect. Removing the field from automation entirely discards the fact that unambiguous cases already exceed 95% accuracy, which is an overcorrection that wastes reviewer capacity on cases that don't need it.
- D: Incorrect. Raising temperature increases output variability rather than addressing the root cause, which is that the source document itself lacks the information needed to resolve the unit ambiguity; this would not improve accuracy or reviewer usefulness.

## Question 32

A legal-document review pipeline processes contracts where, in some cases, two clauses on different pages state contradictory terms for the same provision (for example, differing renewal notice periods). The model extracts a single value for the field without flagging the contradiction. What review-routing behavior should the team implement for this scenario?

- **A.** Have the model detect when source values conflict across the document and route those specific extractions to human review, even if its confidence in the single value it chose is high.
- **B.** Trust the model's single extracted value whenever its reported confidence score is above the routing threshold, since the score already accounts for any conflicting source text.
- **C.** Average the two conflicting values from the document to produce a single extracted number that falls between them, then route that averaged value through normal processing.
- **D.** Extract only the value from whichever page appears first in the document, since earlier clauses are conventionally assumed to take precedence in contract structure.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Ambiguous or contradictory source documents are a distinct risk signal from low model confidence, and extractions from such documents should be routed to human review regardless of the model's stated confidence in the single value it produced, since a confident-sounding answer can still be based on an unresolved conflict in the source.
- B: Incorrect. A model's confidence score reflects its certainty in the value it output, not necessarily an accurate signal that the source document itself was unambiguous; a model can be confident while silently picking one of two conflicting values.
- C: Incorrect. Averaging two conflicting contractual terms, such as notice periods, produces a legally meaningless number that matches neither clause and does not resolve which term is actually binding; this masks the conflict instead of surfacing it for human resolution.
- D: Incorrect. There is no general convention that an earlier clause automatically overrides a later one in contract interpretation; resolving a genuine contradiction between clauses requires human legal judgment, not a positional heuristic.

## Question 33

An architect is choosing between Claude's citations feature and having subagents manually append plain-text bibliographies to their outputs, for a multi-source synthesis pipeline that must let end users click through to the exact passage supporting each generated statement. Which factor most favors using the citations feature?

- **A.** Citations ground each statement in exact source passages, producing verifiable per-statement references rather than a general list of sources
- **B.** Citations remove the need for subagents to read source documents at all, since the feature retrieves relevant passages automatically
- **C.** Citations guarantee that conflicting statistics from different sources will be automatically reconciled into a single agreed value
- **D.** Citations eliminate the need to track publication dates because the feature timestamps every generated statement automatically

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The citations feature ties each generated statement to the specific passages that support it, giving finer-grained, verifiable provenance than a document-level bibliography can provide.
- B: Subagents still need to read and process source documents; citations ground statements in passages already provided, they do not replace document analysis.
- C: Citations attribute statements to source passages; they do not perform any automatic reconciliation of conflicting statistics between sources.
- D: Citations attribute text to source passages but do not automatically timestamp statements with publication or collection dates, which must still be captured separately.

## Question 34

A coordinator dispatches a pricing-lookup subagent against an internal catalog API. The subagent's HTTP call hangs and exceeds its timeout budget before any response arrives. A separate subagent queries the same catalog for a discontinued SKU and receives a 200 response with zero matching rows. How should the two outcomes be reported to the coordinator?

- **A.** Report the timeout as an access failure eligible for retry, and the zero-row response as a valid empty result needing no retry
- **B.** Report both outcomes as empty results, since neither subagent returned any usable pricing data for the coordinator to act upon
- **C.** Report both outcomes as access failures so the coordinator retries each lookup the same fixed number of times
- **D.** Report the timeout as a valid empty result and the zero-row response as an access failure that needs a retry

**Correct answer:** A

**Explanation:**

- A (correct): Timeout errors are transient failures that should be retried with exponential backoff, as recommended by Anthropic's official documentation. A 200 response with zero matching rows for a discontinued SKU is an expected, valid empty result and does not warrant a retry. The application should handle the empty state gracefully.
- B: A timeout is not an empty result; it is a failure indicating the request did not complete, which is distinct from a successful response with no data. Treating it as empty would miss the opportunity to retry and potentially recover.
- C: Classifying a valid zero-row response as an access failure leads to unnecessary retries that waste resources. Retries are appropriate only for transient errors like timeouts, not for successful but empty responses.
- D: This reverses the correct classification. A timeout should be treated as a failure eligible for retry, while a 200 OK with zero rows is a successful empty response that should not trigger retries.

## Question 35

A brokerage's support workflow includes a configured escalation rule: honor a customer's explicit request for a human agent immediately, without attempting to resolve the underlying issue first. A customer messages support: 'I want a real person, not a bot,' regarding a routine request to reset their account password. The agent has not yet attempted any troubleshooting. Per the configured escalation rule, what is the appropriate response?

- **A.** Escalate to a human agent right away, honoring the request without first attempting to resolve it
- **B.** Walk the customer through the password reset steps first, since the process is quick and routine
- **C.** Ask the customer to explain why a human agent is preferred before deciding how to proceed
- **D.** Offer to reset the password immediately and escalate only if the customer repeats the request afterward

**Correct answer:** A

**Explanation:**

- A (correct): Correct - the configured escalation rule requires honoring an explicit request for a human agent immediately, regardless of how routine the underlying issue is.
- B: Incorrect - resolving the issue first violates the configured rule, which makes no exception for issues that are quick or routine.
- C: Incorrect - asking the customer to justify the request before proceeding delays applying a rule that already specifies an immediate response to an explicit request.
- D: Incorrect - the 'offer first, escalate only if repeated' pattern does not match a rule that triggers on the customer's first explicit request, not on repetition.
Want the full experience?
These are just samples. Practice the full Anthropic Claude Certified Architect – Foundations (CCAR-F) question bank in quiz mode — free, no signup, with domain practice and exam simulation.
Practice all 480 questions in quiz mode
Related certifications
Anthropic Claude Certified Associate – Foundations (CCAO-F)
Anthropic Claude Certified Developer – Foundations (CCDV-F)
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
