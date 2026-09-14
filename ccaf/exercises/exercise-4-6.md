# Exercise 4.6 — Build a Multi-Pass Code Review System

**Difficulty:** Advanced · **Estimate:** 60 minutes
**Source:** https://claudecertificationguide.com/learn/4-prompt-engineering/4-6-multi-pass-review#build-exercise

#### Build a Multi-Pass Code Review System  ·  60 minutes
1. Create a single-pass review prompt and run it against a 10-file mock PR — document instances of inconsistent depth, missed issues, and contradictory findings
   *Why:* Establishing the single-pass baseline demonstrates the three symptoms of attention dilution: inconsistent depth across files, missed bugs in the middle of the review, and contradictory findings flagging the same pattern differently in different files.
   **You should see:** Detailed feedback on some files (typically first and last) but superficial comments on others, at least one obvious bug missed in a middle file, and at least one contradictory finding where the same code pattern is flagged as problematic in one file but approved in another.
2. Implement per-file local analysis: iterate over each file with a focused review prompt that examines only that file for bugs, security issues, and logic errors
   *Why:* Per-file analysis ensures every file receives consistent, focused attention. Each invocation examines only one file, eliminating the attention dilution that causes inconsistent depth and missed bugs in single-pass reviews.
   **You should see:** Consistent review depth across all 10 files. Bugs that were missed in the single-pass review should now be caught, especially those in the middle files. Each review should be focused and thorough.
3. Implement a cross-file integration pass: feed all per-file findings into a separate prompt that checks for data flow inconsistencies, contradictory findings across files, and API contract violations
   *Why:* Per-file analysis catches local issues but misses cross-file concerns: data flow between modules, consistent API usage, and contradictions in per-file findings. The integration pass is a separate invocation that receives all findings and checks for systemic issues.
   **You should see:** A synthesis output identifying cross-file issues that no single-file review could catch: data passed between modules in incompatible formats, contradictory findings from per-file reviews, and API contracts violated across service boundaries.
4. Add confidence scoring to each finding (0.0-1.0) and implement routing: high confidence findings go directly to the developer, low confidence findings go to a human review queue
   *Why:* Confidence-based routing directs limited human reviewer attention to the findings that need it most. The exam distinguishes raw uncalibrated confidence from calibrated thresholds validated against labelled sets.
   **You should see:** Each finding annotated with a confidence score, reasoning for the score, and a routing decision (direct_report or human_review). The routing threshold should separate clear-cut findings from uncertain ones.
5. Use a separate Claude instance (fresh session, no prior context) to review a subset of the generated findings and compare its assessment to the original confidence scores for calibration
   *Why:* Independent review instances approach output fresh without the bias of I chose this because reasoning. This step calibrates confidence thresholds by comparing self-reported confidence against independent assessment, the method the exam identifies as the correct approach.
   **You should see:** A calibration dataset showing the relationship between reported confidence scores and independent verification results. Some high-confidence findings may be overturned, revealing calibration gaps that adjust your routing thresholds.
