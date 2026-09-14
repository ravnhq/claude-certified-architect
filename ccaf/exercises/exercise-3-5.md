# Exercise 3.5 — Practice Iterative Refinement Techniques

**Difficulty:** Beginner · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/3-claude-code-config/3-5-iterative-refinement#build-exercise

#### Practice Iterative Refinement Techniques  ·  30 minutes
1. Describe a code transformation in prose and run it three times, noting how interpretation varies across runs
   *Why:* This demonstrates the core problem that concrete examples solve. Prose descriptions rely on interpretation, and interpretation varies across runs. Observing this inconsistency firsthand makes the case for switching to examples.
   **You should see:** Three different outputs from the same prose description. The variations may be subtle (different naming choices, different edge case handling) or significant (different structural approaches). This proves that prose alone produces inconsistent results.
2. Provide 2-3 concrete input/output examples of the same transformation and run it three times — compare the consistency
   *Why:* Concrete examples are the documented first-line technique for inconsistent interpretation. The model generalises from examples more reliably than from prose. This step proves the effectiveness difference experimentally.
   **You should see:** Three outputs that are consistent with each other and match the pattern established by the examples. The variation observed in the prose-only step is eliminated or drastically reduced.
3. Write a test suite for a function with happy path, edge cases, and error cases, then iterate by sharing test failures with Claude Code
   *Why:* Test-driven iteration is the most effective technique for complex transformations. Test failures provide unambiguous feedback — "Expected X, got Y" leaves no room for interpretation. This technique complements examples for more complex scenarios.
   **You should see:** After sharing test failures, Claude Code makes targeted fixes that address the specific failing assertions. Each iteration reduces the number of failing tests. The feedback loop is faster and more precise than prose-based corrections.
4. Use the interview pattern for a task outside your expertise — ask Claude to pose questions before implementing and note what considerations surface
   *Why:* The interview pattern is for unfamiliar domains where you might miss important requirements. It surfaces considerations an expert would know to address. The exam tests whether you can distinguish this from the examples technique — they solve different problems.
   **You should see:** Claude asks 5-10 targeted questions about requirements, edge cases, and constraints you had not considered. The questions reveal considerations like cache invalidation strategies, consistency requirements, failure modes, or security implications that would have been missed.
5. Practice batching: give Claude three interdependent issues in one message and observe whether the fix is coherent across all three
   *Why:* When issues interact, batching them in one message lets the model see all constraints simultaneously. Sequential fixing of interdependent issues causes the model to fix one issue in a way that conflicts with the others. The exam tests this distinction.
   **You should see:** A single coherent fix that addresses all three interdependent issues consistently. The error response shape, the logging format, and the type definitions all align with each other. Compare this to fixing them sequentially, where each fix might conflict with the next.
