# Anthropic Claude Architect Professional

Source: https://www.certsafari.com/anthropic/claude-architect-professional/practice-questions

Free sample: 35 questions with answers and explanations. The full bank is 456 questions and is gated by the site quiz mode (Cloudflare Turnstile).

## Question 1

A software vendor wants to build a RAG assistant over its own internal support-ticket archive (not the public web) and needs the same quality of source attribution that citation-grounded answers provide, without sending queries to an external search index. Which feature fits this requirement?

- **A.** Web search tool, because it augments Claude's knowledge with current information regardless of where the documents are hosted.
- **B.** Web fetch, because retrieving full page content from specified URLs works equally well for private ticket archives.
- **C.** Search results, because it provides citation-quality source attribution for custom knowledge bases outside the public web.
- **D.** Code execution, because running retrieval scripts in a sandbox lets the model fetch and cite ticket content directly.

**Correct answer:** C

**Explanation:**

- A: Incorrect. The web search tool augments Claude with public web content and is not the mechanism for attributing answers to a private, internal ticket archive.
- B: Incorrect. Web fetch retrieves content from specified URLs on the web; it is not designed to provide citation attribution over an internal, non-web knowledge base.
- C (correct): Correct. Search results is built to enable natural citations for RAG applications, achieving web-search-quality citations for custom knowledge bases and internal tools.
- D: Incorrect. Code execution runs sandboxed code for analysis and file processing; it is not a citation or source-attribution feature for retrieval-augmented answers.

## Question 2

A long-running autonomous coding agent needs two things in its architecture: automatically clearing stale tool results from context as a session approaches the token limit, and retaining key project facts across separate sessions run days apart. Select all components that correctly satisfy these two needs. (Select 2 )

- **A.** Context editing, which supports clearing tool results automatically as a conversation approaches the token limit
- **B.** The memory tool, which lets Claude store and retrieve information across separate conversations over time
- **C.** Fine-grained tool streaming, which reduces latency by streaming tool parameters without JSON buffering
- **D.** Compaction, positioned as the sole mechanism that fully replaces context editing for long-running sessions
- **E.** Code execution, which runs code in a sandboxed container for data analysis and file processing tasks F . The Files API, which lets uploaded documents be referenced repeatedly without re-uploading their content

**Correct answer:** 

**Explanation:**


## Question 3

A team is choosing between orchestrator-workers and parallelization by sectioning for a document-analysis pipeline. Which statements correctly distinguish orchestrator-workers from parallelization by sectioning? (Select 2 )

- **A.** In orchestrator-workers, a central LLM determines subtasks at runtime, whereas sectioning requires subtasks predefined before execution
- **B.** In orchestrator-workers, worker LLMs run in a fixed, predetermined order, whereas sectioning always runs its subtasks simultaneously
- **C.** Orchestrator-workers suits subtasks that vary unpredictably case to case, while sectioning suits tasks that split cleanly into known subtasks
- **D.** Parallelization by sectioning always requires a second LLM to evaluate the sectioned outputs before combining them into a final result
- **E.** Orchestrator-workers and parallelization by sectioning both aggregate multiple independent votes on one input to reach a majority-based answer

**Correct answer:** 

**Explanation:**


## Question 4

A team is building an agent that must audit a large codebase across three distinct dimensions: security vulnerabilities, code quality, and test coverage. Each dimension requires a different set of tools and a different area of focus. Which approach best decomposes this problem using the Agent SDK?

- **A.** Define an orchestrator agent that invokes specialized subagents through the Agent tool, each configured with a scoped tool set and description matching its subtask domain
- **B.** Send one prompt to the main agent instructing it to sequentially perform code quality checks, then security scanning, then test coverage analysis without additional configuration
- **C.** Configure a single MCP server that exposes security, quality, and coverage checks as three separate tools, and let the primary agent call each tool directly instead of delegating
- **D.** Increase the primary agent's context window and rely on extended thinking so it can reason through all three review dimensions within one continuous session

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The Agent SDK's subagent capability lets an orchestrator delegate focused subtasks to specialized agents, each with its own scoped tools and description, then aggregate their results — the intended decomposition pattern for multi-dimensional review work.
- B: Incorrect. A single undifferentiated prompt forces one agent to hold all three review contexts and tool needs at once, losing the isolation and specialization benefits of decomposition.
- C: Incorrect. Exposing checks as tools on one MCP server still leaves a single agent responsible for orchestrating and interpreting all three domains itself, rather than delegating focused reasoning to specialized subagents.
- D: Incorrect. A larger context window and extended thinking add reasoning depth but do not decompose the task into independently scoped, delegatable units of work.

## Question 5

An enterprise customer's support desk has committed to a contractual 99.9% uptime and sub-2-second p95 response SLA for its Claude-powered ticket triage assistant. During architecture review, the team must select which platform capabilities to prioritize primarily to protect this SLA commitment. Which two capabilities are the most directly relevant to protecting a latency and availability SLA? (Select 2) (Select 2 )

- **A.** Server-side fallback, which retries a refused request against a backup model within the same API call for a timely response
- **B.** Choosing a model with faster comparative latency, such as Claude Haiku 4.5, for the latency-sensitive triage path
- **C.** Batch processing, which processes large volumes of requests asynchronously at a discounted rate over an extended completion window
- **D.** Agent Skills, which extend Claude's capabilities with pre-built instructions and scripts for document-format tasks
- **E.** The Files API, which lets documents be uploaded once and referenced across multiple requests without re-uploading content

**Correct answer:** 

**Explanation:**


## Question 6

A manufacturing client wants a Claude-based quality-inspection assistant that repeatedly analyzes the same reference specification documents alongside new inspection reports throughout the day. The client's stated goal is to reduce redundant token spend on the unchanging reference material while keeping individual inspection turnaround fast. Which architectural choice best serves this efficiency and cost goal?

- **A.** Use prompt caching so the unchanging reference specification is cached and reused across requests, cutting cost and latency
- **B.** Move the entire workload to the Message Batches API so all inspection reports are processed together once per day
- **C.** Increase the effort parameter to xhigh on every inspection request so Claude reasons more thoroughly each time
- **D.** Re-upload the full reference specification as plain text in every single request to guarantee the model always has the latest version

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Prompt caching is designed exactly for this pattern: providing Claude with recurring background context, such as an unchanging reference document, so subsequent requests reduce both cost and latency instead of reprocessing the same content each time.
- B: Batch processing trades same-day turnaround for cost savings on non-urgent work, which conflicts with the client's requirement to keep individual inspection turnaround fast throughout the day.
- C: Raising the effort parameter increases reasoning depth and token usage per request, which adds cost rather than reducing the redundant token spend the client wants to cut.
- D: Re-uploading the full reference document in every request is the exact redundant-token pattern the client wants eliminated, and it neither reduces cost nor improves turnaround.

## Question 7

A coding assistant must modify an unknown number of files across a repository to implement a feature, where the exact files and scope of changes can only be determined once the assistant inspects the codebase. Which pattern is most appropriate?

- **A.** Orchestrator-workers, where a central LLM inspects the repository and dynamically delegates each file edit to a worker LLM
- **B.** Prompt chaining, where the assistant edits files in a fixed sequence determined before inspecting the repository
- **C.** Parallelization by sectioning, where the assistant edits every file in the repository simultaneously using a predetermined split
- **D.** Routing, where the assistant classifies the feature request and sends it to one of several fixed file-editing prompts

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Anthropic describes the orchestrator-workers pattern as having a central LLM dynamically break down tasks, delegate them to worker LLMs, and synthesize results. Official guidance states this pattern is "well-suited for complex tasks where you can't predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task)." This matches the scenario of an unpredictable set of repository edits. Anthropic does note that real-time coordination among coding agents is still challenging, but among the available workflow patterns this is the documented fit.
- B: Incorrect. Prompt chaining uses a predefined sequence in which the output of one step feeds the next. In this scenario, the files and scope of changes cannot be known until the repository is inspected, so a fixed sequence determined before inspection would likely miss the correct edits or require rework. A dynamic delegation pattern such as orchestrator-workers is more appropriate.
- C: Incorrect. Parallelization by sectioning works when the task can be divided into independent, predictable sections before execution. Here the exact files are unknown and cannot be predetermined before inspecting the codebase. Editing every file simultaneously using a fixed split would be inefficient and could introduce incorrect changes; orchestrator-workers handles dynamic delegation instead.
- D: Incorrect. Routing classifies an input and sends it to a specialized fixed prompt or workflow, but it does not inspect the repository and dynamically delegate individual file edits as subtasks emerge. The described task requires dynamic planning and delegation, which is characteristic of the orchestrator-workers pattern.
Domain 2: Claude Models, Prompting & Context Engineering

## Question 8

A developer is building an email-triage agent that reads inbound email bodies via a tool and drafts replies. To harden it against embedded instructions in email bodies, which combination of design choices should the developer apply? (Select all that apply) (Select 3 )

- **A.** State a system prompt policy that content returned by tools is untrusted data and must never override the system prompt or the user's original request
- **B.** JSON-encode the email body when passing it as a tool result so quotes or tags in the content cannot break out of the surrounding structure
- **C.** Screen tool outputs with a lightweight classifier model before passing them to the main agent, and strip or flag content if an injection is suspected
- **D.** Place the developer's own operating instructions inside the same tool_result block as the email body so both travel together in one message
- **E.** Grant the agent broad, unscoped access to the user's full mailbox and account settings so it never needs to ask for additional permissions mid-task

**Correct answer:** 

**Explanation:**


## Question 9

A team is building an English-to-Spanish translation feature that will be called repeatedly with different user-submitted text. They want to keep the instructional wording consistent across calls while making it easy to swap in new text and track changes to the instructions separately from the text being translated. Which approach best fits this goal?

- **A.** Define a prompt template with the fixed instruction text and a placeholder such as {{text}}, substituting only the variable content on each call while the surrounding instructions stay constant.
- **B.** Regenerate the complete translation prompt on every call by constructing the instruction string dynamically with the user's text, ensuring that each request carries an up-to-date version of the wording.
- **C.** Store the entire prompt containing the fixed instructions and the user's text as one static string, editing the string by hand for each new translation request so the prompt is always up to date.
- **D.** Send the fixed instruction text and the user's text to the model in two separate API calls, then concatenate the responses, placing the translation after the instruction output to form the final result.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A prompt template separates fixed instructions from variable placeholders like {{text}}. This keeps the instructional wording consistent across calls, lets the variable content change per request, and makes it straightforward to version and track the fixed portion independently of what's being translated.
- B: Incorrect. Regenerating the complete prompt including instructions on every call defeats the goal of keeping instructional wording consistent, because the surrounding text may drift. It also makes it harder to track changes to the instructions independently from the user's text.
- C: Incorrect. Storing the entire prompt as one static string and editing it by hand conflates fixed instructions with variable content, making it error-prone and hard to test edge cases. This approach does not allow tracking instruction changes separately from the translated text.
- D: Incorrect. Splitting into two API calls and concatenating responses adds unnecessary complexity and cost without providing reusable instruction wording. It does not achieve the goal of maintaining consistent, separately trackable instructions.

## Question 10

An agent runs long tool-use loops involving dozens of file reads per session. The team wants old tool results automatically cleared once input tokens exceed 30,000, while always preserving the 3 most recent tool exchanges and never clearing results from the web_search tool. Which context_management configuration achieves this?

- **A.** Configure a clear_tool_uses_20250919 edit with trigger set to 30000 input tokens, keep 3 tool uses, exclude_tools set to web_search.
- **B.** A clear_thinking_20251015 edit with trigger set to 30000 input tokens, keep set to 3 thinking turns, and exclude_tools set to web_search should be used.
- **C.** A clear_tool_uses_20250919 edit with trigger set to tool_uses 30000, with no keep value explicitly set, and with no exclude_tools value explicitly set.
- **D.** A clear_tool_uses_20250919 edit with trigger set to 30000 input tokens, keep set to 3 tool uses, and exclude_tools set to file_read should be used.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. clear_tool_uses_20250919 is the appropriate edit for clearing old tool results. Setting the trigger to 30,000 input tokens, keeping the 3 most recent tool uses, and excluding web_search meets all specified requirements: auto-clears at the token threshold, preserves the last 3 exchanges, and never clears web_search results.
- B: Incorrect. The clear_thinking_20251015 edit is designed to manage extended thinking blocks, not tool results. Using it would fail to clear old file-read outputs, regardless of trigger or exclusion settings.
- C: Incorrect. This configuration triggers on a tool_uses count of 30,000 instead of the required input token threshold. Additionally, without setting keep or exclude_tools, recent tool exchanges are not preserved, and web_search results are not protected from clearing.
- D: Incorrect. Excluding file_read instead of web_search results in file_read results being never cleared, while web_search results remain subject to automatic clearing—the opposite of the requirement.

## Question 11

A code-review prompt needs Claude to generate a fix, verify the fix against a set of criteria, and then refine the fix if criteria are not met. The team wants to inspect the intermediate review step and log it separately before the final refinement is produced. Which approach best fits this requirement?

- **A.** Ask Claude to generate, verify, and refine the fix in one response using extended reasoning, but this keeps the review internal and unloggable.
- **B.** Break the task into separate API calls: generate a fix, review it against the criteria, then refine the fix, so each step can be logged independently.
- **C.** Add <thinking> tags around the review step so Claude places the review inside and the fix outside, and the review can be extracted and logged apart.
- **D.** Provide five few-shot examples of correct fixes for Claude to mimic, bypassing the review step, removing the intermediate step and preventing logging.

**Correct answer:** B

**Explanation:**

- A: Incorrect. Asking Claude to handle everything in one response with extended reasoning keeps the review internal to the model's generation process. The intermediate verification step cannot be extracted or logged separately, which fails to meet the team's logging requirement.
- B (correct): Correct. Breaking the task into separate API calls implements a self-correction chaining pattern where each phase—generation, review against criteria, and refinement—is isolated. Each step can be independently inspected, logged, or branched on, exactly matching the need for separate logging.
- C: Incorrect. While adding <thinking> tags might seem to separate the review visually, the entire generation, review, and refinement still occur in a single API response. This makes it impractical to reliably extract and log a clean intermediate review step without mixing it with the draft or refinement content.
- D: Incorrect. Providing few-shot examples for Claude to mimic bypasses the explicit review-against-criteria step entirely. Without performing a distinct review and refinement cycle, there is no intermediate step to log, so this approach fails to satisfy the requirement.
Domain 3: Integration

## Question 12

A platform wants Claude to discover tools using an existing embeddings index rather than the built-in regex or BM25 matching, because tool descriptions are sparse but semantically related through the embedding space. Which implementation matches this requirement?

- **A.** Build a custom tool that runs the embeddings search and returns tool_reference blocks in its tool_result for Claude to expand.
- **B.** Enable the built-in BM25 tool search variant, since BM25 ranking approximates embedding-based semantic similarity closely enough.
- **C.** Enable the built-in regex tool search variant and rely on broad wildcard patterns to approximate semantic matching.
- **D.** Disable tool search and load every tool definition up front so the embeddings index becomes unnecessary.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A custom client-side tool search implementation can run any retrieval method, including embeddings, and return standard tool_result content with tool_reference blocks, which the API expands into full tool definitions.
- B: BM25 is a term-frequency-based lexical ranking method, not a true semantic embedding similarity search, so it would not reproduce the intended embeddings-based matching.
- C: Regex matching operates on literal patterns against names and descriptions and cannot capture semantic relationships between sparse, differently worded tool descriptions.
- D: Loading every definition up front abandons retrieval entirely and reintroduces the context bloat problem that made an embeddings-based discovery approach necessary.

## Question 13

A support-ticket assistant retrieves passages from a 500-document internal knowledge base for each incoming ticket and must cite the exact source passage in every reply, without re-sending the entire corpus on each request. Which approach best matches this data shape and query pattern?

- **A.** Return the retrieved passages as search result content blocks from a retrieval tool, each carrying source and title metadata, so Claude generates natural citations per ticket.
- **B.** Upload all 500 documents as citable text documents in the system prompt so that Claude can reference any passage directly, and then instruct it to cite the source document and section for every reply.
- **C.** Concatenate the full corpus into a single long-context user message with all 500 documents separated by titles, then prompt Claude to extract the relevant passage and cite its source.
- **D.** Store the corpus in the memory tool by saving each document as a separate entry, configure assistant to load all entries before answering, and prompt it to cite source document for any retrieved passage.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. This approach uses a retrieval tool to dynamically fetch only relevant passages per query, with each result block including source and title metadata. This enables Claude to generate natural citations without resending the entire corpus, which is efficient and aligns with the need for exact source passage citations.
- B: Incorrect. Uploading all 500 documents in the system prompt sends the full corpus with every request, defeating the purpose of avoiding corpus resending. It also wastes context on irrelevant passages, making it inefficient for a repeated ticket-answering workflow.
- C: Incorrect. Concatenating the full corpus into a long user message per request is costly in terms of tokens and degrades accuracy as context grows. It skips the targeted retrieval step that efficiently supplies only relevant passages, which is what this query pattern requires.
- D: Incorrect. The memory tool is intended for Claude to persist notes across conversation turns, not as a document retrieval index. Storing each document as a memory entry and loading all entries for each query is inefficient and does not support targeted retrieval with source metadata for citations.

## Question 14

A team originally split their onboarding manual into fixed 500-character chunks with no overlap. They now find that many chunks begin or end mid-sentence, and answers near a chunk boundary are frequently missed because the relevant sentence is split across two separate embeddings. Which chunking adjustment most directly addresses this specific failure?

- **A.** Split chunks along natural boundaries such as paragraphs or sections, and add a small overlap between adjacent chunks so boundary sentences appear intact in at least one chunk.
- **B.** Reduce the chunk size so each chunk contains exactly one sentence, splitting on punctuation such as periods or exclamation points, and drop the fixed character limit to prevent mid-sentence breaks.
- **C.** Remove overlap and set a smaller fixed chunk size, such as 250 characters, to lower the vector index count and accelerate semantic search without changing how sentences are split.
- **D.** Keep the fixed 500-character boundaries and increase the embedding model's context window so that each vector encodes more surrounding text, reducing missed answers near splits.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Chunking on natural document boundaries such as paragraphs or sections, combined with a small overlap, ensures that sentences near chunk edges appear intact in at least one chunk. This directly addresses the problem of split-sentence retrieval failures.
- B: Incorrect. Reducing chunks to single sentences by splitting on punctuation eliminates mid-sentence breaks, but loses the surrounding context necessary for accurate retrieval. Additionally, multi-sentence ideas are still separated across chunks, which can degrade answer completeness.
- C: Incorrect. Removing overlap and using smaller fixed-size chunks increases the likelihood that a relevant sentence will be split across a chunk boundary. This strategy worsens the original problem rather than resolving it.
- D: Incorrect. Increasing the embedding model's context window does not change where the pipeline cuts text; with fixed 500-character boundaries, sentences near the cuts remain split. The retrieval misses at boundaries persist regardless of the model's capacity.

## Question 15

An agent's project has accumulated a dozen skills, several of which perform side-effecting actions such as sending Slack messages or deleting stale branches. Reviewers notice Claude occasionally auto-triggers these side-effecting skills based on vague description matches, and want to reduce the agent's effective capability surface so these skills only run when a person explicitly invokes them. What is the most direct fix?

- **A.** Set disable-model-invocation: true in the frontmatter of each side-effecting skill so Claude cannot select them automatically and only the user can invoke them with /name.
- **B.** Delete the skill descriptions from the frontmatter of each side-effecting skill so Claude has no basis for automatic matching and only the user can invoke those skills by name.
- **C.** Move the side-effecting skills into CLAUDE.md so they load as always-on context, which ensures Claude only uses them when the user explicitly invokes them by name in a request.
- **D.** Rewrite the instructions of each side-effecting skill to instruct Claude to ask for confirmation before performing the side effect, without modifying frontmatter fields.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Setting `disable-model-invocation: true` in the frontmatter hides the skill from Claude's automatic selection, so it cannot be triggered by vague description matches. The skill becomes accessible only when a user explicitly invokes it with `/name`, thus reducing the effective capability surface as intended.
- B: Incorrect. Deleting skill descriptions may prevent automatic matching, but skills also rely on descriptions for proper discovery and correct invocation by users. This approach is not the documented method for controlling automatic model invocation and could lead to confusion or broken workflows.
- C: Incorrect. Moving skills into `CLAUDE.md` would load them as always-on context in every session, meaning Claude could still act on them without an explicit user request, potentially increasing the effective capability surface rather than reducing it.
- D: Incorrect. Adding instructions to ask for confirmation does not prevent Claude from auto-triggering the skill based on description matches; the skill may still be activated automatically, only then prompting for confirmation. This does not restrict invocation to explicit user commands.
Domain 4: Evaluation, Testing & Optimization

## Question 16

A team is defining the success criteria for a new claims-summarization feature before building the evaluation dataset. The current draft criterion reads: "the summaries should be concise and helpful." Which revised criterion best follows the SMART framework for evaluation design?

- **A.** Require summaries to average at least 4 out of 5 on a completeness rubric across a 500-claim sample
- **B.** Require summaries to earn a perfect 5 out of 5 completeness score from every adjuster in the sample
- **C.** Require summaries to sound less robotic and read more naturally to the adjusters who review them
- **D.** Require every summary to be signed off by a senior adjuster before it counts as acceptable

**Correct answer:** A

**Explanation:**

- A (correct): Correct. This criterion is specific (completeness rubric), measurable (numeric threshold), achievable (a 4/5 average rather than perfection), and relevant (tied directly to summary quality), and it defines a concrete sample size for measurement.
- B: Incorrect. Requiring a perfect score from every adjuster is not achievable in practice; SMART criteria should be realistic targets grounded in frontier model capability, not unattainable perfection.
- C: Incorrect. "Sound less robotic" and "read more naturally" are not measurable without a defined metric or scale, so this fails the Measurable requirement of SMART criteria.
- D: Incorrect. This describes a manual sign-off process, not a measurable success criterion for the model's output quality, so it does not give the evaluation team a quantifiable target.

## Question 17

A platform engineer sets CLAUDE_CODE_ENABLE_TELEMETRY=1 on every CI runner but the team's OTLP collector never receives any spans, metrics, or logs from Claude Code jobs. No other telemetry variables were configured. What is the most likely cause of the missing data?

- **A.** The collector rejects every signal until CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1 is also set, regardless of which exporters are chosen
- **B.** Telemetry is enabled but no exporter was selected, so OTEL_METRICS_EXPORTER and OTEL_LOGS_EXPORTER default to producing no export at all
- **C.** The CLI only emits telemetry once the console exporter has been configured first as a required local fallback
- **D.** The organization's Admin API key must be exported through OTEL_EXPORTER_OTLP_HEADERS before the CLI will emit any signal

**Correct answer:** B

**Explanation:**

- A: Incorrect. The enhanced telemetry beta flag is only required to unlock distributed tracing spans; metrics and log events do not depend on it, and it has no bearing on whether an exporter is configured.
- B (correct): Correct. Enabling telemetry alone does not choose a destination. Each signal has its own exporter switch (OTEL_METRICS_EXPORTER, OTEL_LOGS_EXPORTER, OTEL_TRACES_EXPORTER), and leaving them unset means nothing is exported even though telemetry generation is on.
- C: Incorrect. The console exporter is one optional choice among several (otlp, prometheus, console, none); it is not a prerequisite the CLI requires before other exporters will function.
- D: Incorrect. OTEL_EXPORTER_OTLP_HEADERS carries authentication for the collector endpoint, not an Anthropic Admin API key, and its absence would cause auth failures at the collector, not a total absence of any emitted telemetry.

## Question 18

An agentic coding assistant runs long sessions that accumulate hundreds of tool calls, and the conversation regularly approaches the model's context window limit before the task is finished. Engineers want strategies that let the session continue productively without losing critical state. Which approaches address this goal? (Select 3 )

- **A.** Enable server-side compaction so earlier turns are automatically summarized once the conversation nears the context window limit
- **B.** Configure context editing to clear old tool results once a token threshold is reached, keeping only recent tool use/result pairs
- **C.** Use the memory tool to persist critical state to durable storage before old context is cleared, so a session recovers quickly
- **D.** Lower the effort parameter to low so Claude generates shorter replies, preventing the context window from ever filling up
- **E.** Switch the session to the Message Batches API so each turn runs as an independent asynchronous request with fresh context F . Increase the effort parameter to max so Claude reasons more thoroughly and needs fewer total turns to finish the task

**Correct answer:** 

**Explanation:**


## Question 19

A team wants to lower per-request cost and latency for a chat feature without switching models or losing response quality on genuinely hard questions. They want the model itself to spend fewer tokens on easy turns while still reasoning thoroughly on complex ones. Which lever should they reach for first?

- **A.** Lower the effort parameter for routine turns, since it reduces token spend while letting Claude think harder when warranted
- **B.** Disable prompt caching entirely, since removing all cached writes always guarantees the very lowest possible token count of all
- **C.** Force every request through the Message Batches API, since batch requests are billed at a flat discounted rate
- **D.** Set max_tokens to a small fixed value on all requests so Claude cannot generate long responses on hard questions

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The effort parameter is described as a behavioral signal that trades thoroughness for token efficiency across text, tool calls, and thinking, within a single model. At lower effort, Claude still thinks on sufficiently difficult problems but spends fewer tokens on simpler ones, which is exactly the described goal.
- B: Cache writes do cost more than base input, but cache reads cost 90% less; disabling caching entirely removes the possibility of cheap cache reads and would generally increase, not decrease, cost for any repeated content.
- C: The Batch API requires asynchronous processing without immediate responses, which is incompatible with an interactive chat feature, and it does not adapt token spend to per-turn difficulty.
- D: A small fixed max_tokens risks truncating responses on genuinely hard questions where more output is needed, directly conflicting with the requirement to preserve quality on complex turns.

## Question 20

Ahead of launch, a product manager sets a success criterion requiring the model to achieve 100% accuracy on an open-ended reasoning task, with zero tolerance for any incorrect or incomplete answer, matching or exceeding what a domain expert could produce. What is the main problem with this success criterion, and how should it be revised?

- **A.** The target is unachievable because it exceeds realistic frontier-model capability. It should instead be grounded in benchmark results, prior experiments, or comparable industry performance.
- **B.** The target is not specific enough because it does not name a single numeric metric, so it should be replaced with a quantifiable percentage like a 95% accuracy score, regardless of feasibility.
- **C.** The target is not relevant because reasoning tasks should never have accuracy targets; instead, the criterion should specify maximum latency and cost, which are the only meaningful production metrics.
- **D.** The target is not measurable because open-ended tasks cannot be scored automatically under any circumstances, so the criterion should rely on subjective human ratings with no automated evaluation.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. The target of 100% accuracy with zero tolerance is unachievable because it exceeds realistic frontier-model capability. It should be grounded in benchmark results, prior experiments, or comparable industry performance to ensure the success criterion is realistic and attainable.
- B: Incorrect. The target is already specific: 100% accuracy is a single numeric metric. The real problem is that it is unachievable, not that it lacks specificity, so replacing it with an arbitrary percentage like 95% without considering feasibility does not address the core issue.
- C: Incorrect. Accuracy targets are relevant and appropriate for reasoning tasks; the problem is the unrealistic threshold, not the use of an accuracy metric. Additionally, latency and cost are not the only meaningful production metrics—accuracy and safety are also critical.
- D: Incorrect. Open-ended reasoning tasks can be scored automatically using methods like LLM-based evaluation or rubric-based grading, so measurability is not the main problem. The core issue is that the 100% zero-tolerance target is unachievable and not grounded in realistic performance.

## Question 21

A team has been iterating on a claims-processing prompt using the same 200-example development set for every round of refinement. They now want to declare a final winning version before shipping. What should they do before making that final decision?

- **A.** Evaluate the leading prompt candidate on a separate held-out test set not used during iteration to confirm that improvements generalize beyond the development set.
- **B.** Run one more round of refinement on the same 200-example development set, perhaps switching to a different model or adding few-shot examples, to maximize the score before finalizing the prompt.
- **C.** Reduce the development set to only the examples that the current prompt candidate already passes, then present the accuracy on that subset as the final metric to make the score appear higher.
- **D.** Ship the candidate that achieves the highest score on the 200-example development set right away, as iteratively refining on that same set already demonstrates its production readiness.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Reusing the same development set throughout iterations risks overfitting, so the candidate may not generalize. Testing on a separate held-out set is essential to confirm that improvements extend beyond the development data.
- B: Incorrect. Another round of refinement on the same set only deepens overfitting to that specific data, making the prompt less reliable on new examples. Maximizing the development score does not guarantee real-world performance.
- C: Incorrect. Discarding failing examples creates an artificially high accuracy that masks the prompt's true weaknesses. This cherry-picking prevents fair assessment and leads to an unreliable final metric.
- D: Incorrect. The highest score on the iteratively used development set likely reflects overfitting to that set's specific patterns. Production readiness requires validation on unseen data to ensure the prompt performs well in practice.

## Question 22

A team currently runs a moderately complex data-extraction workflow on Claude Haiku 4.5. Which of the following observations would be valid evidence that the workflow has a model-capability mismatch and should be evaluated on a more capable model like Claude Opus 4.8? (Select all that apply.) (Select 3 )

- **A.** On a use-case benchmark, accuracy on multi-step reasoning subtasks stays below threshold even after prompt revisions.
- **B.** The workflow needs nuanced understanding across long chains of interdependent steps where partial errors compound.
- **C.** Manual review shows the extraction errors resemble genuine reasoning mistakes rather than missing or truncated input.
- **D.** The team's monthly API spend for the workflow is higher than they originally budgeted for the project.
- **E.** The workflow occasionally times out because of ordinary network latency between the client and the API. F . The workflow's prompt was designed for an older model and has not been adapted to the current model's capabilities.

**Correct answer:** 

**Explanation:**


## Question 23

A compliance analyst asks Claude to review a 40-page vendor contract and flag every clause that conflicts with the company's data-retention policy. In early testing, Claude cites clause numbers and language that do not actually appear in the contract. Which prompting change is most effective at grounding the review in the actual document text for this kind of long-document task?

- **A.** Ask Claude to answer using its general knowledge of standard contract clauses instead of the specific text, since standard clauses are usually representative
- **B.** Instruct Claude to summarize the entire contract into three paragraphs first, then perform the compliance analysis using only that summary as its source
- **C.** Reduce the max_tokens parameter for the response so Claude produces a shorter, more focused answer that is less likely to drift from the source contract
- **D.** Instruct Claude to first extract exact, word-for-word quotes relevant to data retention, and only then analyze compliance by referencing those extracted quotes

**Correct answer:** D

**Explanation:**

- A: Incorrect. Relying on general knowledge instead of the provided document is the hallucination risk being addressed, not a fix for it.
- B: Incorrect. Summarizing first discards detail and can itself introduce the drift and inaccuracy the task is trying to eliminate.
- C: Incorrect. Response length has no bearing on whether cited clauses actually appear in the source document.
- D (correct): Correct. For long documents, having Claude extract word-for-word quotes before analyzing grounds its output in the actual text and reduces hallucinated citations.

## Question 24

A fintech company's Claude-powered agent can initiate wire transfers through a custom MCP tool. Even though the operations team has configured allowedTools to auto-approve most read and reporting tools, they want every wire-transfer tool call to require a human's explicit approval no matter what permission mode the session is later switched to, including bypassPermissions. Which approach best satisfies this requirement?

- **A.** Register a PreToolUse hook scoped to the wire-transfer tool that returns permissionDecision "ask" for every call, since hooks execute before deny rules, ask rules, the permission mode check, and allow rules, and their decision holds even under bypassPermissions.
- **B.** Add a bare allowedTools entry for the wire-transfer tool so it auto-approves, then depend on the canUseTool callback to intercept it, since bare allow rules approve every matching call before canUseTool is ever consulted, so the callback never runs for that tool.
- **C.** Switch the session's permission mode to acceptEdits, expecting the wire-transfer tool to fall outside its file-edit scope and always route to canUseTool, though other tools under acceptEdits still fall through to any allow rules that already approve them.
- **D.** Add the wire-transfer tool to disallowed_tools with a wildcard pattern so it is blocked by default, then have the canUseTool callback lift the deny rule per call, though deny rules are evaluated before canUseTool runs and cannot be reversed from inside that callback.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Hooks run first in the evaluation order and a PreToolUse hook's decision applies regardless of permission mode, including bypassPermissions, guaranteeing the prompt for this tool.
- B: Incorrect mechanism. A bare allow-rule entry auto-approves every matching call and the call never reaches canUseTool, so this design silently removes the intended approval step.
- C: Incorrect. acceptEdits only auto-approves file edits and specific filesystem commands; other tools still fall through to normal permission handling, which could still resolve via an existing allow rule rather than always prompting.
- D: Incorrect. Deny rules are evaluated before canUseTool in the flow, so the callback has no mechanism to reverse a deny decision for a specific call.

## Question 25

A solutions architect is scoping the ethical-risk controls for a Claude-based assistant that will draft internal performance-review summaries from manager notes across a multinational workforce. The compliance team wants a set of concrete measures that address bias, fairness, and transparency before launch. Which of the following measures should be included? (Select 3) (Select 3 )

- **A.** Run paired-scenario evaluations comparing summary tone and detail across employee groups given identical underlying performance notes.
- **B.** Document, in a form reviewers can inspect, which specific decision factors the assistant is instructed to weigh whenever it drafts a summary.
- **C.** Give every employee, regardless of role or seniority, a mechanism to request the specific factors that shaped their own summary.
- **D.** Skip bias testing across the initial launch region and only extend testing later if formal complaints get filed after go-live.
- **E.** Let each manager's personal phrasing preferences silently override the standardized summary template with absolutely no logging kept. F . Restrict summary review access to a single manager with no secondary sign-off, to keep the rollout process deliberately lightweight.

**Correct answer:** 

**Explanation:**


## Question 26

A solutions architect is running the first discovery session with a new prospect before recommending any specific Claude model. According to Anthropic's model-selection guidance, which factors should the architect establish as key criteria during this session? (Select 3 )

- **A.** The specific capabilities the model must have to meet the prospect's needs
- **B.** How quickly the model must respond within the prospect's application
- **C.** The prospect's available budget for development and production usage
- **D.** The exact number of employees currently working in the prospect's IT department
- **E.** Which social media platforms the prospect uses for customer marketing F . The version number of the prospect's internal ticketing software

**Correct answer:** 

**Explanation:**


## Question 27

A financial services customer's compliance team says every AI-generated answer referencing internal policy documents must point to the exact sentence it was drawn from, so auditors can verify the source without re-reading the whole document. Which capability addresses this discovery finding?

- **A.** Citations, which let Claude reference the exact sentences and passages in source documents used to generate a response
- **B.** Search results, which enable natural citations for RAG applications by attaching proper source attribution to search results
- **C.** Token counting, which determines the number of tokens in a message before it is sent to Claude
- **D.** The Files API, which uploads and manages documents so they do not need to be re-sent with every request

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Citations is documented as grounding responses in source documents with references to the exact sentences and passages used, matching the auditability requirement described.
- B: Incorrect. Search results attaches source attribution specifically for RAG applications built around a search tool, which is a narrower fit than directly citing provided internal policy documents.
- C: Incorrect. Token counting measures message size before sending; it has no role in producing verifiable source references for auditors.
- D: Incorrect. The Files API avoids re-uploading documents across requests but does not itself produce sentence-level source references in responses.

## Question 28

A customer support tooling vendor still runs Claude Haiku 3.5 in a legacy component and receives Anthropic's notice that the model is retired outside of Bedrock and Google Cloud. Their engineering stakeholders want to know how this affects their committed timeline. What is the accurate expectation to set?

- **A.** Direct API and other non-Bedrock/Vertex-hosted traffic on Haiku 3.5 must migrate to a supported model before retirement, while deployments specifically on Bedrock or Google Cloud can keep running it under those platforms' own timelines
- **B.** The retirement notice only affects new customers who sign up after the announcement date, so the vendor's existing production traffic is permanently exempt regardless of hosting platform
- **C.** Retirement notices apply uniformly across every hosting platform including Bedrock and Google Cloud, so all deployments of Haiku 3.5 everywhere must migrate by the same date
- **D.** Model retirement only restricts access to the Console UI for prompting Haiku 3.5, while direct Messages API traffic on any platform continues indefinitely unaffected

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Haiku 3.5 is documented as retired except on Bedrock and Google Cloud, meaning direct API usage elsewhere must migrate while those two platforms retain their own continuation timelines.
- B: Incorrect. Retirement affects existing production traffic on the direct API, not just new signups; there is no blanket exemption tied to account age.
- C: Incorrect. This contradicts the documented exception carved out for Bedrock and Google Cloud, which are explicitly excluded from the retirement on the same schedule.
- D: Incorrect. Retirement affects the model's availability for actual inference, not merely a Console UI restriction; direct Messages API traffic on the retired platforms is the traffic that must migrate.

## Question 29

Two months after a customer support assistant goes live, the operations team notices their monthly Claude spend has grown faster than ticket volume and wants to identify which workspace and model combination is driving the increase. Which monitoring approach addresses this?

- **A.** Query the Usage and Cost Admin API grouped by workspace and model to reconcile spend against token consumption
- **B.** Re-run the original evaluation set from the design phase to check whether output quality has regressed
- **C.** Increase the agent's allowed_tools scope so it can investigate its own billing records directly
- **D.** Ask the support team to manually count tickets handled per day and compare that figure to the invoice total

**Correct answer:** A

**Explanation:**

- A (correct): Correct - the Usage and Cost Admin API supports grouping by workspace and model, which directly answers where the added spend is coming from.
- B: Re-running the evaluation set measures output quality, not which workspace or model is responsible for the cost increase.
- C: Expanding the agent's own tool permissions to inspect billing is unnecessary and unrelated to how usage and cost reporting is retrieved.
- D: Manually reconciling ticket counts against invoices is far less precise than the granular, per-workspace and per-model data the API already provides.

## Question 30

A team is documenting the caching architecture for a service where the same large system prompt and tool definitions are sent with nearly every request. The implementation guidance needs to explain how to cut repeated processing cost and latency for that static content. What should the guidance recommend?

- **A.** Mark the reusable system prompt and tool definitions as cached blocks so repeated requests reuse the prefix instead of reprocessing it.
- **B.** Increase the context window to 1M tokens so the large system prompt fits entirely without ever needing to be truncated across requests.
- **C.** Move the system prompt into the Files API so it uploads once and Claude re-reads it fresh from storage on every single request.
- **D.** Enable batch processing so every request carrying the large system prompt is queued and billed at half price automatically.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Prompt caching is designed exactly for this scenario: marking the static system prompt and tool definitions as cached lets repeated requests skip reprocessing that content, reducing both cost and latency.
- B: Incorrect. A larger context window changes how much content fits in a request but does not stop the same static content from being reprocessed on every call.
- C: Incorrect. The Files API avoids re-uploading file content, but re-reading a stored file on every request still requires reprocessing it, so it does not address the repeated-processing cost.
- D: Incorrect. Batch processing is for asynchronous bulk workloads with a discount on the whole request, not a mechanism for avoiding repeated processing of a shared prefix on synchronous calls.

## Question 31

Your coding-agent product is exceeding its latency budget on Claude Opus 4.8. Before proposing a switch to a smaller model, a colleague suggests first tuning the effort parameter. How should you frame this trade-off to the team?

- **A.** Adjusting effort trades intelligence for latency and cost within the same model; lowering it from the default may recover budget without the accuracy loss that comes from switching to a different, less capable model.
- **B.** The effort parameter governs only tool-call count per turn, not the model’s raw inference latency, so the team should focus on switching to a smaller model that fits the latency budget for the coding-agent product.
- **C.** Effort on Claude Opus 4.8 can only be increased, never decreased, which prevents the team from lowering latency through this parameter; therefore, the migration to a model family that offers a tunable effort floor is the correct path to meet the latency budget.
- **D.** Effort tuning is only available via the Claude API, not in Claude Code, so the coding-agent product cannot lower latency this way; the team should switch to a model family with native effort controls in Claude Code.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. Tuning the effort parameter directly trades off intelligence, latency, and cost within the same model; lowering effort from the default can bring latency back within budget while avoiding the accuracy degradation that typically comes from moving to a less capable model. This approach leverages the existing model’s strengths with a controlled trade-off.
- B: Incorrect. The effort parameter actually controls reasoning depth and token usage, which directly influences raw inference latency, not just the number of tool calls. It is a global control over model intelligence, so adjusting it can meaningfully reduce latency without immediately resorting to a model switch.
- C: Incorrect. The effort parameter can be set to levels lower than the default, allowing latency to be reduced on Opus 4.8. There is no restriction preventing decreases; thus, tuning effort is a viable first step before considering model migration.
- D: Incorrect. Effort tuning is available across all surfaces, including Claude Code and the API. The coding-agent product can adjust effort in both environments, so the option’s assertion that it’s API-only is false, making a switch unnecessary on these grounds.
Domain 7: Developer Productivity & Operational Enablement

## Question 32

A solutions architect is designing the initial rollout of Claude Code for a mid-size company with no existing device management. The company has developers on unmanaged laptops, wants centralized visibility into token spend, and needs org-wide policy to reach both local sessions and Claude Code on the web. Which set of decisions correctly matches each requirement to the right mechanism? (Select 3) (Select 3 )

- **A.** Choose Claude for Teams or Enterprise as the API provider so Claude Code and claude.ai share one per-seat subscription with no infrastructure to run
- **B.** Use server-managed settings delivered from the claude.ai admin console, since it reaches both local and web sessions without requiring MDM
- **C.** Use the usage dashboard at claude.ai/analytics/claude-code for centralized spend visibility, available on Claude for Teams and Enterprise plans
- **D.** Deploy a plist-based managed-settings policy through macOS MDM as the primary policy channel, since it is the strongest enforcement mechanism available
- **E.** Rely exclusively on project-level .claude/settings.json files committed to each repository to establish organization-wide policy F . Configure Amazon Bedrock as the API provider so the company can use server-managed settings for centralized policy delivery

**Correct answer:** 

**Explanation:**


## Question 33

A platform team is wiring Claude Code into a locked-down CI pipeline where no human is available to approve prompts, and only a pre-approved set of tools defined in permission rules should ever run. Which permission mode fits this pipeline?

- **A.** dontAsk mode, which auto-denies anything not covered by an explicit allow rule
- **B.** acceptEdits mode, which auto-approves file edits and common filesystem commands
- **C.** plan mode, which restricts Claude to reads and a proposed plan with no execution
- **D.** auto mode, which relies on a classifier to approve most actions in real time

**Correct answer:** A

**Explanation:**

- A (correct): Correct. dontAsk mode only executes actions matching pre-approved allow rules and read-only commands, auto-denying everything else instead of prompting, which makes a session fully non-interactive and safe for a CI pipeline with no human available.
- B: Incorrect. acceptEdits still prompts for Bash commands outside its narrow auto-approved filesystem set, so an unattended CI run could stall waiting on a prompt that no human is present to answer.
- C: Incorrect. plan mode prevents any execution at all, including of pre-approved tools, so it cannot let a pipeline actually apply pre-approved fixes or changes.
- D: Incorrect. auto mode uses a classifier to approve actions dynamically rather than restricting execution to a fixed, pre-approved allow list, which does not match the requirement that only pre-approved tools ever run.

## Question 34

During a long debugging session, Claude Code raises "Autocompact is thrashing: the context refilled to the limit..." immediately after automatic compaction completes, and it stops retrying. The team was asking Claude to read an entire 40,000-line production log file to find the root cause of an outage. What is the most effective way to recover and continue the investigation?

- **A.** Raise CLAUDE_CODE_MAX_RETRIES so Claude Code keeps retrying compaction until the log file finishes loading successfully.
- **B.** Ask Claude to read the log file in smaller chunks, such as a specific line range, or delegate the analysis to a subagent instead.
- **C.** Set DISABLE_AUTO_COMPACT so Claude Code stops summarizing history and keeps the entire log output available for reference.
- **D.** Run /clear to discard the conversation, then paste only the final error line from the log file into a fresh session.

**Correct answer:** B

**Explanation:**

- A: Incorrect. CLAUDE_CODE_MAX_RETRIES governs retries of failed API requests, not the compaction-thrashing loop. Thrashing happens because the file itself refills the context after each compaction, so retrying compaction more times does not solve the underlying problem.
- B (correct): Correct. Auto-compaction succeeded but the oversized file output immediately refilled the context window several times in a row, so Claude Code stopped retrying to avoid wasted API calls. Reading the file in smaller chunks or moving the work to a subagent's separate context window is the documented recovery path.
- C: Incorrect. Disabling auto-compaction removes the safeguard that prevents the context window from overflowing, so it would make the thrashing problem worse, not better, since the full log would still need to fit in context.
- D: Incorrect. This is more drastic than necessary and discards useful investigation context. The documented recovery steps are to chunk the file, use a targeted /compact, or delegate to a subagent, not to abandon the conversation entirely.

## Question 35

A team's project relies on an internal MCP server for ticket lookups. Running /mcp shows the server status as connected, but Claude reports it has no tools available from that server and cannot look up tickets. What is the correct next step to diagnose the failure?

- **A.** Select Reconnect for the server from /mcp, and if the tool count stays at zero, run claude --debug mcp to see the server's stderr output.
- **B.** Edit .mcp.json to change the server's command from a relative path to an absolute path, since a relative path always prevents any tools from loading.
- **C.** Approve the server from /mcp again, since project-scoped MCP servers silently stop returning tools after the one-time approval expires.
- **D.** Restart Claude Code with claude --safe-mode, since a server that reports zero tools while connected is always disabled under safe mode.

**Correct answer:** A

**Explanation:**

- A (correct): Correct. A server that shows connected but lists zero tools has started but isn't returning a tool list. The documented step is to select Reconnect from /mcp, and if the count stays at zero, run claude --debug mcp to inspect the server's stderr output.
- B: Incorrect. A relative path in command or args typically causes the server to fail to start entirely, which shows as failed in /mcp, not connected with zero tools. That is not the situation described here.
- C: Incorrect. Project-scoped approval does not silently expire; once approved, a server stays enabled. This does not explain a connected server returning no tools.
- D: Incorrect. Safe mode disables all MCP servers for the session, so the server would not show as connected at all, let alone connected with zero tools. This is not a diagnostic step for this symptom.
Want the full experience?
These are just samples. Practice the full Anthropic Claude Certified Architect – Professional (CCAR-P) question bank in quiz mode — free, no signup, with domain practice and exam simulation.
Practice all 456 questions in quiz mode
Related certifications
Anthropic Claude Certified Associate – Foundations (CCAO-F)
Anthropic Claude Certified Developer – Foundations (CCDV-F)
Anthropic Claude Certified Architect – Foundations (CCAR-F)
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
