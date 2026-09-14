# Exercise 5.5 — Build a Confidence-Calibrated Review Router

**Difficulty:** Advanced · **Estimate:** 50 minutes
**Source:** https://claudecertificationguide.com/learn/5-context-management/5-5-human-review-calibration#build-exercise

#### Build a Confidence-Calibrated Review Router  ·  50 minutes
1. Create a mock extraction system that outputs field-level confidence scores for different document types (invoices, receipts, scanned PDFs, international documents)
   *Why:* Field-level confidence scores are the foundation of intelligent review routing. The exam tests that raw model confidence is not calibrated and must be validated against ground truth before use. Building the mock system gives you data to calibrate against.
   **You should see:** An extraction function that returns each field with its value and a confidence score between 0.0 and 1.0. The system should process at least 4 document types with noticeably different confidence distributions per type.
2. Implement accuracy tracking broken down by document type and field segment — not just aggregate metrics
   *Why:* The aggregate metrics trap is the most dangerous misconception in production extraction systems. 97% overall accuracy can hide catastrophic failure rates on specific document types because standard invoices dominate the volume. The exam tests that you must validate by document type AND field segment before automating.
   **You should see:** An accuracy table showing each document type and field combination separately. Standard invoices should show 95%+ accuracy while handwritten receipts and international documents show 40-70%. The aggregate should look excellent (90%+) despite the poor per-type numbers.
3. Build a calibration module that takes a labelled validation set (ground truth) and produces calibrated confidence thresholds per field type per document type
   *Why:* Raw model confidence scores are not calibrated. A model reporting 0.90 confidence might actually be correct 94% of the time on date fields but only 82% on amount fields. Calibration using labelled validation sets is required before confidence scores can drive automated routing decisions.
   **You should see:** A calibration curve for each field type per document type, mapping reported confidence ranges to actual accuracy percentages. The curve should reveal that the same confidence score means different things for different field-document combinations.
4. Implement stratified random sampling that selects high-confidence extractions for ongoing verification, sampling proportionally across all document types
   *Why:* High-confidence extractions are automated and not reviewed. If the model develops a novel error pattern affecting high-confidence items, only stratified sampling will catch it. Sampling only low-confidence items leaves you blind to systematic errors in automated extractions.
   **You should see:** A sampling function that selects a representative subset from each stratum (document type and confidence band), including samples from the high-confidence automated extractions. The sample should be proportional to the volume in each stratum.
5. Build a review router that prioritises limited reviewer capacity on the highest-uncertainty items, dynamically reordering the review queue as new extractions arrive
   *Why:* Human reviewers are expensive and limited. Spreading capacity evenly across all extractions wastes time on high-confidence items while leaving insufficient capacity for uncertain items that need human judgement. Dynamic priority ordering ensures the most uncertain items are always reviewed first.
   **You should see:** A priority queue that orders items by uncertainty (lowest confidence first), dynamically reorders as new extractions arrive, and serves the next-highest-uncertainty item to each available reviewer. The queue should never serve items in chronological order.
