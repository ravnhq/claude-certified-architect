# Exercise 3.1 — Build a Multi-Level CLAUDE.md Configuration

**Difficulty:** Beginner · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/3-claude-code-config/3-1-claude-md-hierarchy#build-exercise

#### Build a Multi-Level CLAUDE.md Configuration  ·  30 minutes
1. Create a project-level .claude/CLAUDE.md with universal coding standards: naming conventions, error handling patterns, and a code review checklist
   *Why:* Project-level configuration is the foundation of team-wide standards. The exam tests whether you place shared conventions here rather than in user-level config, which is the most common misconfiguration scenario.
   **You should see:** A .claude/CLAUDE.md file at the repository root containing at least three sections: naming conventions, error handling patterns, and a code review checklist. Running /context in the project root lists this file under Memory files.
2. Create a directory-level CLAUDE.md in a /packages/api/ subdirectory with API-specific conventions (REST endpoint naming, request/response schema requirements)
   *Why:* Directory-level configuration scopes conventions to a specific package. The exam tests whether you know that directory-level CLAUDE.md applies only within that directory, not across the entire project.
   **You should see:** A CLAUDE.md file inside /packages/api/ containing REST-specific conventions. When you run /context while working in /packages/api/, both the project-level and directory-level files appear under Memory files.
3. Create .claude/rules/testing.md with test-specific conventions (test naming pattern, assertion style, fixture usage)
   *Why:* The .claude/rules/ directory holds topic-specific rule files that can optionally include YAML frontmatter for path scoping. Understanding this mechanism is tested alongside path-specific rules in Task Statement 3.3.
   **You should see:** A testing.md file inside .claude/rules/ containing at least three test conventions. Running /context lists this rules file under Memory files.
4. Use an @ path import in the project-level CLAUDE.md to reference a shared standards file at ./standards/naming.md
   *Why:* The @ import syntax enables modular organisation of conventions. There is no @import keyword — a path prefixed with @ on its own line is the import. Each package can import only relevant standards, reducing duplication and drift in the source files. The exam tests whether you know the mechanism exists and how the syntax actually looks.
   **You should see:** The project-level .claude/CLAUDE.md contains a line beginning with @ pointing to ./standards/naming.md. A separate file at .claude/standards/naming.md (or standards/naming.md relative to the CLAUDE.md) exists with naming conventions. Running /context confirms the imported content is loaded inline.
5. Run /context in different directories to verify the correct files are loaded in each context
   *Why:* The exam tests that the diagnostic command reveals loaded files but does not trigger loading — configuration loads automatically based on location. The guide names /memory for this; current Claude Code reports the loaded set under /context, so that is what you run here.
   **You should see:** In the project root, /context shows the project-level CLAUDE.md and rules files under Memory files. In /packages/api/, it additionally shows the directory-level CLAUDE.md. The imported standards file content appears as part of the project-level configuration.
6. Move one convention from project-level to user-level (~/.claude/CLAUDE.md) and verify that a different user session does NOT pick it up — confirming the scoping boundary
   *Why:* This is the exam favourite trap scenario. When conventions live in user-level config, new team members who clone the repo do not receive them. Proving this boundary experimentally cements the concept.
   **You should see:** After moving a convention to ~/.claude/CLAUDE.md, your own /context shows it loaded. A simulated second user session (or a fresh clone without your home directory config) does NOT show that convention. This confirms the scoping boundary.
