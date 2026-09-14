# Exercise 1.4 — Build a Prerequisite Gate for Financial Operations

**Difficulty:** Advanced · **Estimate:** 60 minutes
**Source:** https://claudecertificationguide.com/learn/1-agentic-architecture/1-4-workflow-enforcement-handoff#build-exercise

#### Build a Prerequisite Gate for Financial Operations  ·  60 minutes
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
