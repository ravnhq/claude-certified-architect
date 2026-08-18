# Exercise 3.3 — Configure Path-Specific Rules with Glob Patterns

**Difficulty:** Intermediate · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/3-claude-code-config/3-3-path-specific-rules#build-exercise

#### Configure Path-Specific Rules with Glob Patterns  ·  30 minutes
1. Create .claude/rules/testing.md with YAML frontmatter paths: [`"**/*.test.ts"`, `"**/*.test.tsx"`, `"**/*.spec.ts"`] and test conventions (naming, assertions, mocking patterns)
   *Why:* Path-specific rules with glob patterns are the correct solution for conventions that apply to a file type spread across many directories. The exam favourite scenario is test files co-located with source files across 50+ directories.
   **You should see:** A file at .claude/rules/testing.md with YAML frontmatter containing a paths array with glob patterns. The body contains at least three test conventions covering naming, assertions, and mocking.
2. Create .claude/rules/api-conventions.md with paths: [`"src/api/**/*"`, `"**/routes/**/*"`] and API conventions (response shape, validation, error handling)
   *Why:* Separating API conventions into their own path-scoped rule means they only load when editing API files. This avoids consuming tokens with irrelevant context when working on frontend or infrastructure code.
   **You should see:** A file at .claude/rules/api-conventions.md with YAML frontmatter paths targeting API directories. The body contains at least three API conventions.
3. Create .claude/rules/terraform.md with paths: [`"terraform/**/*"`, `"**/*.tf"`] and infrastructure conventions
   *Why:* Infrastructure conventions are completely irrelevant when editing application code. Path-scoped rules ensure Terraform rules never consume tokens during React or API development sessions.
   **You should see:** A file at .claude/rules/terraform.md with YAML frontmatter paths matching Terraform files. The body contains infrastructure-specific conventions.
4. Edit a test file and use /memory to verify that testing rules are loaded but API and Terraform rules are not
   *Why:* This proves the conditional loading mechanism works. The exam tests whether you understand that path-specific rules load only for matching files, and /memory is the diagnostic tool to verify this.
   **You should see:** When editing a .test.ts file, /memory output lists .claude/rules/testing.md as loaded. The .claude/rules/api-conventions.md and .claude/rules/terraform.md files do NOT appear in the /memory output.
5. Edit an API handler and verify that API rules load while testing and Terraform rules do not
   *Why:* This is the complementary verification. Switching contexts should swap which rules are loaded, confirming that the glob patterns correctly scope each rule file.
   **You should see:** When editing a file in src/api/, /memory output lists .claude/rules/api-conventions.md as loaded. The testing and Terraform rule files do NOT appear.
6. Compare the token footprint when all conventions are in root CLAUDE.md versus split into path-specific rules
   *Why:* Token efficiency is a key exam concept. Root CLAUDE.md loads all conventions for every session regardless of relevance. Path-specific rules load only matching conventions, reducing irrelevant context and preserving token budget for actual work.
   **You should see:** With all conventions in root CLAUDE.md, /memory shows the full set of conventions loaded even when editing a simple utility file. With path-specific rules, /memory shows only the relevant subset. The token count for loaded configuration is measurably smaller when using path-specific rules for targeted editing sessions.
