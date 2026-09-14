# Exercise 4.1 — Build an Explicit Criteria Code Review Prompt

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/4-prompt-engineering/4-1-system-prompts#build-exercise

#### Build an Explicit Criteria Code Review Prompt  ·  45 minutes
1. Write a system prompt with vague instructions (be conservative, only flag important issues) and test it against 5 code snippets containing known bugs, security issues, and style nitpicks
   *Why:* Establishing a baseline with vague instructions demonstrates the false positive problem the exam tests. You need empirical evidence that phrases like be conservative give the model no actionable decision boundary.
   **You should see:** Inconsistent classification across the 5 snippets: some style nitpicks flagged as critical, some genuine bugs missed or marked minor, and different results if you run the same snippets twice.
2. Rewrite the prompt with explicit categorical criteria: define exactly which issues to report (bugs, security vulnerabilities) and which to skip (style preferences, local patterns)
   *Why:* Explicit categorical criteria are the correct approach tested on the exam. This step demonstrates that concrete categories eliminate the ambiguity that causes false positives.
   **You should see:** The rewritten prompt has clear categories: report bugs and security vulnerabilities, skip style preferences and local patterns, flag comments only when claimed behaviour contradicts actual code behaviour.
3. Add concrete code examples for each severity level — critical, major, minor — showing actual code patterns, not prose descriptions
   *Why:* The exam specifically tests that code examples outperform prose descriptions for severity calibration. Prose like issues that could cause system failures forces the model to interpret, while code examples remove ambiguity entirely.
   **You should see:** Your prompt now contains at least one code snippet per severity level, each showing the actual pattern that defines that severity, not a prose description of what that severity means.
4. Compare false positive rates between the two versions on the same test set and document which approach produces more consistent classification
   *Why:* Quantifying the improvement validates the explicit criteria approach and builds the evaluation skill the exam expects. You should be able to articulate why one approach outperforms the other with data, not intuition.
   **You should see:** A clear reduction in false positives with the explicit criteria version. The vague prompt should produce 30-50% inconsistency while the explicit criteria version should be below 15%. Classification should be stable across repeated runs.
5. Temporarily disable any category with above 25% false positive rate and document the criteria refinements needed before re-enabling
   *Why:* The trust recovery strategy is a key exam concept: high false positive rates in one category destroy developer trust in ALL categories. Disabling problematic categories restores system-wide trust while you iterate on their criteria.
   **You should see:** A document listing which categories exceed the 25% threshold, what specific criteria refinements are needed (e.g., add code examples for edge cases), and a re-enablement plan with target false positive rates.
