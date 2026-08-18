# Exercise 1.3 — Implement Context Passing with Structured Metadata

**Difficulty:** Intermediate · **Estimate:** 50 minutes
**Source:** https://claudecertificationguide.com/learn/1-agentic-architecture/1-3-subagent-invocation-context#build-exercise

#### Implement Context Passing with Structured Metadata  ·  50 minutes
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
