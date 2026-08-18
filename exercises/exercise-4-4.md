# Exercise 4.4 — Build a Validation-Retry Loop for Document Extraction

**Difficulty:** Advanced · **Estimate:** 60 minutes
**Source:** https://claudecertificationguide.com/learn/4-prompt-engineering/4-4-validation-retry-loops#build-exercise

#### Build a Validation-Retry Loop for Document Extraction  ·  60 minutes
1. Define an extraction tool with calculated_total and stated_total fields, a conflict_detected boolean, and detected_pattern fields for tracking which constructs trigger findings
   *Why:* Self-correction fields like calculated_total vs stated_total enable automatic discrepancy detection without external logic. conflict_detected booleans and detected_pattern fields create the data foundation for systematic prompt improvement.
   **You should see:** A JSON schema with separate calculated_total and stated_total number fields, a total_discrepancy boolean, a conflict_detected boolean, and a detected_pattern string field on each finding in the line_items array.
2. Implement validation logic that checks: field completeness, numerical consistency (calculated sum matches stated total), enum validity, and date ordering
   *Why:* Semantic validation catches errors that tool_use cannot. The exam distinguishes schema syntax errors (eliminated by tool_use) from semantic errors (wrong sums, misplaced values) that require validation logic and retry loops.
   **You should see:** A validation function that returns an array of specific, actionable error messages. Each error should state what was expected versus what was found, not just that validation failed.
3. Build the retry loop: on validation failure, construct a follow-up message containing the original document, the failed extraction, and the specific validation error
   *Why:* Retry-with-error-feedback is dramatically more effective than naive retries. Without the specific error, the model has no guidance and typically reproduces the same mistake. With the error, the model can target its self-correction.
   **You should see:** A retry message that includes all three elements: the original document text, the JSON of the failed extraction, and the specific validation error string. The model should produce a corrected extraction on retry.
4. Test with 5 documents: 2 with fixable errors (misplaced values, wrong totals) and 3 with unfixable errors (absent information) — verify the loop retries only fixable cases
   *Why:* The retry effectiveness boundary is the most aggressively tested concept in this task statement. Retries fix format mismatches and structural errors but cannot create information absent from the source. The exam presents both scenarios and expects you to identify which is fixable.
   **You should see:** The 2 fixable documents succeed after 1-2 retries with corrected totals or field placements. The 3 unfixable documents are correctly identified as having absent information and flagged for human review rather than retried.
5. Log detected_pattern data for each finding and analyse which patterns are most frequently dismissed to identify prompt refinement priorities
   *Why:* detected_pattern fields create a systematic improvement loop. When developers consistently dismiss findings triggered by a specific pattern, that pattern likely needs prompt refinement. This turns dismissal data into actionable prompt improvement priorities.
   **You should see:** A log or table showing each detected_pattern, its frequency, its dismissal rate, and a prioritised list of patterns needing prompt refinement. Patterns with high dismissal rates should be at the top.
