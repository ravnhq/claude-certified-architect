# Exercise 5.1 — Build a Persistent Case Facts Context Manager

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/5-context-management/5-1-context-window-management#build-exercise

#### Build a Persistent Case Facts Context Manager  ·  45 minutes
1. Create a case facts extractor that identifies transactional data (amounts, dates, order numbers, statuses) from tool results
   *Why:* The persistent case facts block is the single most important pattern in context window management. Extracting transactional facts into a structured block that is never summarised prevents the progressive summarisation trap from destroying critical numerical values and identifiers.
   **You should see:** A function that takes raw tool output and returns a structured object containing only the transactional facts: customer ID, order numbers, amounts, dates, and statuses. Non-transactional narrative content should be excluded.
2. Implement a persistent case facts block that is prepended to every prompt, outside summarised history
   *Why:* The case facts block must persist across every turn regardless of what happens to the conversation history. It sits outside the summarised portion of the context, ensuring amounts, dates, and order numbers survive even when earlier conversation turns are compressed.
   **You should see:** A prompt construction function that always includes the case facts block at the top of every message, followed by any summarised history, followed by the current turn. The case facts block should be clearly delimited with a section header.
3. Build a tool result trimmer that filters order lookup responses from 40+ fields to only the 5 relevant return-related fields
   *Why:* Untrimmed tool results are a silent context budget killer. An order lookup returning 40+ fields consumes tokens in every subsequent turn as conversation history grows. Trimming to relevant fields before results enter context is essential, not optional.
   **You should see:** A trimming function that takes a raw tool result object and returns only the fields needed for the current task. The trimmed result should be 80-90% smaller than the original.
4. Test with a multi-turn conversation where summarisation occurs and verify that transactional facts survive intact across all turns
   *Why:* This validates that the persistent case facts pattern actually works. The exam tests whether you understand that progressive summarisation destroys specific amounts and dates, and the case facts block is the fix. You need to verify this empirically.
   **You should see:** A 6-8 turn conversation where summarisation occurs after turn 4. After summarisation, the agent should still reference the exact refund amount ($247.83), order number (#8891), and date (March 3rd) from the case facts block. Without the block, these values would be lost to summarisation.
5. Add key findings placement logic that positions summaries at the beginning of aggregated inputs to mitigate the lost-in-the-middle effect
   *Why:* Models process information at the beginning and end of long inputs reliably, but findings buried in the middle may be missed. Placing key findings summaries at the start of aggregated inputs is a structural fix for this well-documented phenomenon.
   **You should see:** An aggregation function that places a Key Findings Summary section at the top of combined inputs, followed by detailed results with explicit section headers. The key findings should be concise bullet points drawn from the detailed content.
