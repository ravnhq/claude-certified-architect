# Exercise 4.2 — Build a Few-Shot Enhanced Extraction Prompt

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/4-prompt-engineering/4-2-few-shot-prompting#build-exercise

#### Build a Few-Shot Enhanced Extraction Prompt  ·  45 minutes
1. Create a base extraction prompt with detailed instructions but no examples and test it against 10 documents with varied structures: tables, narrative paragraphs, mixed formats
   *Why:* Establishing a baseline without examples demonstrates the consistency problem the exam tests. Detailed instructions alone produce inconsistent output across varied document structures, which is the exact trigger for deploying few-shot examples.
   **You should see:** Inconsistent extraction results across the 10 documents: fields extracted correctly from tables but empty or wrong from narrative paragraphs, different output formats across runs, and inconsistent handling of edge cases.
2. Record which fields are consistently empty or inconsistent across document structures
   *Why:* Identifying the specific failure patterns tells you exactly what your few-shot examples need to demonstrate. The exam tests whether you can diagnose the problem before prescribing the solution.
   **You should see:** A table or log showing which fields fail on which document types. Typical pattern: dates extracted correctly from tables but missed in narrative text, amounts inconsistent when written in words rather than digits, line items empty when embedded in paragraphs.
3. Create 3 few-shot examples targeting the failing patterns — each must include reasoning explaining why the extraction was done that way
   *Why:* Examples with reasoning teach the model to generalise to novel patterns, not just match specific cases. Without reasoning, the model learns only surface-level pattern matching. The exam specifically tests that reasoning-included examples outperform input-output pairs.
   **You should see:** Three examples, each showing a different document structure (table, narrative, mixed), with the correct extraction AND a reasoning section explaining how the data was located and why the extraction decisions were made.
4. Re-run the same 10 documents with the few-shot enhanced prompt and compare: empty field rate, format consistency, and extraction accuracy
   *Why:* Quantifying the improvement demonstrates the effectiveness of few-shot examples as the first-choice technique for consistency problems. The exam expects you to know that few-shot examples outperform additional instructions for this class of problem.
   **You should see:** A measurable reduction in empty fields (especially on narrative documents), improved format consistency across document types, and higher overall extraction accuracy. The improvement should be most dramatic on the document types that previously failed.
5. Document which structural patterns benefit most from few-shot examples and which require different techniques like schema changes
   *Why:* The exam tests whether you can match the right technique to the right problem. Few-shot examples fix consistency and structural variety issues, but malformed JSON needs tool_use, fabricated values need nullable schemas, and sum discrepancies need validation loops.
   **You should see:** A decision matrix showing which problem types improved with few-shot examples and which still need other interventions. Narrative extraction and format consistency should improve. Fabrication of missing data should not improve and needs schema changes instead.
