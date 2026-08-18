# Exercise 4.5 — Design a Batch Processing Strategy

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/4-prompt-engineering/4-5-batch-processing#build-exercise

#### Design a Batch Processing Strategy  ·  45 minutes
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
