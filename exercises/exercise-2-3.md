# Exercise 2.3 — Configure Tool Distribution Across a Multi-Agent System

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/2-tool-design-mcp/2-3-tool-distribution-choice#build-exercise

#### Configure Tool Distribution Across a Multi-Agent System  ·  45 minutes
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
