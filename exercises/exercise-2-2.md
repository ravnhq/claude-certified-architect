# Exercise 2.2 — Build Structured Error Responses for All Four Categories

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/2-tool-design-mcp/2-2-structured-error-responses#build-exercise

#### Build Structured Error Responses for All Four Categories  ·  45 minutes
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
