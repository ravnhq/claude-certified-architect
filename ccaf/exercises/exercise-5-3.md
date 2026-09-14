# Exercise 5.3 — Build a Structured Error Propagation System

**Difficulty:** Advanced · **Estimate:** 50 minutes
**Source:** https://claudecertificationguide.com/learn/5-context-management/5-3-error-propagation#build-exercise

#### Build a Structured Error Propagation System  ·  50 minutes
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
