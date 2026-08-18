# Exercise 2.5 — Trace and Refactor a Deprecated Function Using Built-in Tools

**Difficulty:** Intermediate · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/2-tool-design-mcp/2-5-built-in-tools#build-exercise

#### Trace and Refactor a Deprecated Function Using Built-in Tools  ·  30 minutes
1. Use Grep to search for all callers of a target function (e.g. processLegacyOrder) across the codebase
   *Why:* Grep searches file contents — it is the correct tool for finding function callers. Using Glob here would fail because Glob matches file paths, not contents. The exam tests this distinction directly and penalises candidates who confuse the two.
   **You should see:** A list of file paths containing calls to processLegacyOrder, with line numbers and matching lines showing the exact call sites. For example: src/OrderProcessor.ts:42: await processLegacyOrder(orderId).
2. Use Glob to find test files matching the caller filenames (e.g. `**/*.test.tsx`)
   *Why:* Glob matches file paths by naming pattern — it is the correct tool for finding test files by extension or naming convention. This completes the Grep-then-Glob pattern: content search to find callers, then path matching to find their tests.
   **You should see:** A list of test file paths matching the pattern, such as src/OrderProcessor.test.tsx and src/RefundHandler.test.tsx. These correspond to the caller files found by Grep in the previous step.
3. Use Read to examine each caller file and understand the usage pattern and context
   *Why:* Reading files incrementally — only after Grep identifies which files matter — is the correct approach. Reading all source files upfront is a context-budget killer that the exam explicitly penalises. Each Read should be justified by what you discovered in the previous step.
   **You should see:** The full contents of each caller file, showing how processLegacyOrder is called, what parameters are passed, how the return value is used, and whether the function is imported directly or through a wrapper module.
4. Use Edit to replace the deprecated function call with the new API in each caller file
   *Why:* Edit is the preferred modification tool because it targets specific text and uses less context than Read + Write. The exam penalises defaulting to Read + Write for every modification. Always try Edit first — it is faster and more precise.
   **You should see:** Each caller file updated with the new API call replacing the deprecated one. For example, processLegacyOrder(orderId) replaced with processOrder(orderId, { validate: true }). The Edit tool confirms the replacement was made successfully.
5. When Edit fails with a non-unique match, widen old_string with more surrounding lines until it pins down one location (or set replace_all: true if you actually want every occurrence updated). Only fall back to Read + Write if neither option can disambiguate the target
   *Why:* Edit fails when the target text appears multiple times in the file — this is a safety mechanism, not a bug. Per the Edit tool documentation, the documented recovery is to expand the anchor with more surrounding context until it matches one place, or to use replace_all for global replacements. Both keep you on Edit and cost almost nothing in context. Read + Write loads the entire file for what is usually a single-line change — keep it as a last resort.
   **You should see:** On the first try, Edit fails with an error like: old_string matches 3 locations. On the retry with a wider old_string that includes the surrounding function name or unique adjacent line, Edit succeeds and changes exactly one occurrence. If replace_all: true was the right call, every occurrence is updated atomically.
