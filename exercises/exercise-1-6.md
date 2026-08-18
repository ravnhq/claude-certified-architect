# Exercise 1.6 — Build a Multi-Pass Code Review Pipeline

**Difficulty:** Advanced · **Estimate:** 60 minutes
**Source:** https://claudecertificationguide.com/learn/1-agentic-architecture/1-6-task-decomposition#build-exercise

#### Build a Multi-Pass Code Review Pipeline  ·  60 minutes
1. Create a code review agent that accepts a directory path containing at least 10 source files
   *Why:* The 10+ file threshold is where attention dilution becomes observable. The exam uses a 14-file example where detailed feedback for early files degrades to superficial analysis for later files. Your setup must replicate this scale.
   **You should see:** A code review function that reads all files in a directory and prepares them for analysis. It should handle at least 10 TypeScript or JavaScript source files.
2. Implement a single-pass review that processes all files at once and record the results
   *Why:* The single-pass approach is the baseline that demonstrates attention dilution. The exam expects you to recognise the symptoms: thorough analysis for early files, shallow analysis for later files, and contradictory pattern evaluation.
   **You should see:** A review result where early files receive detailed feedback with specific line references and bug identification, while later files receive increasingly brief or missing feedback. This is the attention dilution pattern.
3. Implement per-file local analysis passes that produce structured feedback for each file individually (bug count, severity, specific line references)
   *Why:* Per-file passes give each file the full attention budget. This is the first layer of multi-pass architecture. The exam contrasts this with single-pass to show that structural decomposition solves attention dilution, not better prompts or larger context windows.
   **You should see:** Consistent analysis depth across all files. The last file receives the same level of detail as the first. Each review includes bug count, severity ratings, and specific line references in a structured format.
4. Implement a cross-file integration pass that checks for data flow issues, API consistency, and pattern usage consistency across all files
   *Why:* Per-file passes catch local issues but miss cross-cutting concerns. The exam tests whether you include a cross-file integration pass — batching without it still misses data flow issues and pattern inconsistencies across files.
   **You should see:** A separate analysis that takes the per-file summaries and checks for cross-file issues: inconsistent API usage, data flow problems between modules, and patterns used differently across files.
5. Compare results: document which issues the single-pass review caught versus the multi-pass approach, paying special attention to consistency of analysis depth across all files
   *Why:* This comparison demonstrates the exam argument quantitatively. Attention dilution is not a model capability problem — it is an architectural problem. The same model produces better results with multi-pass architecture, proving the fix is structural.
   **You should see:** A comparison table showing: more total issues found by multi-pass, consistent issue counts across files (no drop-off for later files), and cross-file issues caught only by the integration pass.
6. Record any cases where the single-pass review flagged a pattern in one file but approved identical code in another — these are attention dilution artefacts
   *Why:* Contradictory pattern evaluation is the clearest symptom of attention dilution. The exam uses the forEach example: flagged as inefficient in File 3, approved without comment in File 11. Documenting these artefacts proves the structural nature of the problem.
   **You should see:** At least one case where the single-pass review treated identical code patterns differently across files. The multi-pass review should treat the same pattern consistently.
