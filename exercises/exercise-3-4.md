# Exercise 3.4 — Practice Plan Mode vs Direct Execution Decision-Making

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/3-claude-code-config/3-4-plan-mode-execution#build-exercise

#### Practice Plan Mode vs Direct Execution Decision-Making  ·  45 minutes
1. Identify a complex multi-file task in a codebase (refactoring, migration, or restructuring) and use plan mode to explore dependencies and design an approach
   *Why:* Plan mode is for tasks with multiple valid approaches, architectural decisions, or multi-file modifications. The exam tests whether you choose plan mode upfront when complexity is stated in the requirements rather than waiting for surprises.
   **You should see:** Claude Code explores the codebase without modifying any files. The output includes: identified dependencies between modules, multiple possible approaches with tradeoffs, and a recommended implementation strategy. No files are changed during the planning phase.
2. Identify a simple single-file bug and use direct execution to fix it — observe the efficiency gain over planning
   *Why:* Direct execution is correct when the problem, location, and solution are all clear. The exam tests that you do not over-plan well-understood changes. The decision is about ambiguity, not difficulty.
   **You should see:** Claude Code makes the fix immediately without a planning phase. The change is confined to a single file or function. The total time from prompt to fix is noticeably shorter than the plan mode task above.
3. Use the hybrid approach: plan mode to design a migration strategy for a library change across multiple files, then switch to direct execution to implement the plan
   *Why:* The plan-then-execute hybrid is a specific pattern tested on the exam. Plan mode designs the strategy; direct execution applies it consistently. This is the correct approach for tasks like library migrations affecting many files.
   **You should see:** Phase 1 (plan): Claude identifies all files importing the old library, maps API differences, and produces a migration pattern. Phase 2 (execute): Claude applies the migration pattern file by file using the planned approach. The implementation is consistent across all files.
4. Use the Explore subagent for a verbose codebase discovery task and observe how it keeps the main conversation context clean
   *Why:* The Explore subagent isolates verbose discovery output so the main conversation context stays focused. Without isolation, extensive file listings and analysis fill the context window and degrade subsequent responses.
   **You should see:** The Explore subagent runs the discovery task and returns a concise summary to the main conversation. The full verbose output (file listings, dependency graphs, code excerpts) is not visible in the main conversation. Subsequent responses in the main conversation remain high quality.
5. Create a written decision framework: list your criteria for choosing plan mode vs direct execution, with examples for each
   *Why:* Internalising the decision criteria is essential for the exam. The framework should cover the key distinction: ambiguity determines the mode, not difficulty. A difficult but well-defined fix is direct execution; a simple-sounding feature with multiple approaches is plan mode.
   **You should see:** A clear decision framework with at least four criteria for plan mode and three for direct execution. Each criterion has a concrete example. The framework explicitly addresses the ambiguity-vs-difficulty distinction.
