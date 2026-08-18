# Exercise 1.1 — Build a Multi-Tool Agent Loop

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/1-agentic-architecture/1-1-agentic-loops#build-exercise

#### Build a Multi-Tool Agent Loop  ·  45 minutes
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
