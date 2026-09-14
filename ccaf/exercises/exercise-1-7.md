# Exercise 1.7 — Implement Session Management Strategies

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/1-agentic-architecture/1-7-session-state-resumption#build-exercise

#### Implement Session Management Strategies  ·  45 minutes
1. Create a Claude Code session that analyses a 10-file codebase and name it with --name for later resumption
   *Why:* Named sessions resumed with --resume enable continuation of work across breaks. The exam tests when resume is appropriate (no files changed) versus when it creates the stale context problem (files have been modified since the last session).
   **You should see:** A named Claude Code session that reads and analyses 10 source files. The session name should be memorable for later resumption. The agent should produce findings about each file.
2. Record the key findings from the initial analysis as a structured summary (file names, issues found, recommendations)
   *Why:* This structured summary is the knowledge you will inject into the fresh session later. The exam tests whether you preserve prior findings without carrying stale tool results. A good summary captures conclusions without raw tool output.
   **You should see:** A structured document listing each file name, the issues found in it, severity ratings, and specific recommendations. This should be concise enough to inject into a prompt but complete enough to preserve all key findings.
3. Modify 3 files in the codebase to fix some of the identified issues
   *Why:* Modifying files after a session creates the conditions for stale context. The old file contents remain as tool results in the session history while the actual files now contain different code. This is the exact scenario that triggers the contradictory advice bug.
   **You should see:** Three files modified with fixes for the issues identified in the initial analysis. The changes should be substantive enough that the old and new versions would produce different analysis results.
4. Attempt to resume the session with --resume and observe any stale context issues (contradictory advice, references to old code)
   *Why:* This demonstrates the stale context problem. The resumed session contains old tool results showing the unfixed code. The agent may recommend fixing issues that are already fixed, or give contradictory advice by referencing both old and new file contents.
   **You should see:** The agent giving contradictory advice: recommending fixes for issues already resolved, referencing code that no longer exists, or providing inconsistent guidance about the modified files. These are the hallmarks of stale context.
5. Start a fresh session with the structured summary injected into the initial prompt, specifying the 3 changed files for targeted re-analysis
   *Why:* Fresh start with summary injection is the correct approach when files have changed. The exam specifically tests this: no stale tool results, preserved knowledge from the prior session, and targeted re-analysis of only the changed files instead of wasteful full re-exploration.
   **You should see:** A clean session that knows about the prior findings (from the injected summary), targets only the 3 changed files for re-analysis, and produces consistent advice without contradictions.
6. Compare the quality and consistency of advice between the stale resume and the fresh start with targeted re-analysis
   *Why:* This comparison demonstrates why the exam favours fresh start with summary injection over naive resume after file changes. The fresh start produces consistent, accurate advice while the resume produces contradictions from stale context.
   **You should see:** A clear quality difference: the resume session gives contradictory or outdated advice about the modified files, while the fresh session gives accurate, consistent analysis based on the current file contents.
