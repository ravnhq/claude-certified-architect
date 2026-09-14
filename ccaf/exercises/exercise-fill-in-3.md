# Fill-in Exercise 3 — Modular CLAUDE.md with @path Imports and the Depth-5 Limit

**Difficulty:** Beginner · **Estimate:** 30 minutes
**Source:** Ravn Study Guide §5.2, Domain 3.1 — https://ravnhq.github.io/claude-certified-architect/guides/en.html

1. Split a monolithic CLAUDE.md into topic files and import them with @path: coding standards in @./standards/coding-style.md, test requirements in @./standards/testing-requirements.md, project overview in @README.md.
   *Why:* The @path syntax is what makes CLAUDE.md modular. Each topic lives in one file, edited once, imported wherever relevant — avoiding the duplication-and-drift problem of copying conventions into multiple files. The exam tests the exact syntax: `@` immediately before the path, on its own line, no `@import` keyword.
   **You should see:** A short CLAUDE.md whose imports resolve inline — run /context and confirm the imported file contents appear as part of the loaded configuration. A standards/ directory containing the split-out files.
2. Verify that a relative @path resolves relative to the file containing the import, not the project root.
   *Why:* Resolution-relative-to-importer is the detail that breaks nested configurations. A CLAUDE.md in packages/api/ that writes @standards/api.md resolves against packages/api/, not the repo root. The exam tests whether you place imports correctly in multi-level setups.
   **You should see:** An import inside a directory-level CLAUDE.md that resolves correctly relative to that file's location. Moving the referenced file without updating the path breaks the import, confirming the resolution root.
3. Build an import chain five levels deep: CLAUDE.md imports A.md, A.md imports B.md, and so on to E.md. Confirm the chain loads.
   *Why:* The maximum import nesting depth is 5 — an explicit exam fact. You need a working depth-5 chain as the boundary case before you can demonstrate the failure at depth 6.
   **You should see:** Five levels of nesting resolving: content from E.md (the fifth hop) appears in the loaded configuration when you run /context.
4. Add a sixth level (E.md imports F.md) and observe what happens.
   *Why:* Knowing the limit exists is different from seeing the boundary behaviour. The exam tests the number 5 because it is an easy detail to get wrong — candidates who guess "unlimited" or "3" lose the point.
   **You should see:** The depth-6 import not resolved: F.md content does not appear in the loaded configuration. The chain silently stops at the depth limit rather than recursing further.
5. Refactor the over-deep chain: hoist the deepest shared files so no import chain exceeds the limit, and re-verify all content loads.
   *Why:* The practical skill is designing a modular layout that stays inside the constraint: keep shared standards near the top of the import graph and let leaf files import them, rather than chaining imports through intermediate files.
   **You should see:** A restructured layout where every file's content loads under /context, with the longest chain at 5 levels or fewer. Shared files are imported directly by the files that need them instead of being relayed through multiple hops.
