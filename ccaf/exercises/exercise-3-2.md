# Exercise 3.2 — Create Custom Commands and Skills

**Difficulty:** Intermediate · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/3-claude-code-config/3-2-slash-commands-skills#build-exercise

#### Create Custom Commands and Skills  ·  30 minutes
1. Create a project-scoped /review command in .claude/commands/review.md containing a team code review checklist
   *Why:* Project-scoped commands are shared via git so every developer gets them on clone. The exam tests whether you place team commands in .claude/commands/ (project) vs ~/.claude/commands/ (personal).
   **You should see:** A file at .claude/commands/review.md in the repository. Running /review in Claude Code triggers the code review checklist. The command appears when any developer clones the repository.
2. Create a personal /brainstorm skill in ~/.claude/skills/brainstorm/SKILL.md with context: fork in the frontmatter
   *Why:* The context: fork frontmatter option isolates verbose skill output from the main conversation. Without it, codebase analysis output fills the context window and degrades subsequent responses. The exam directly tests this concept.
   **You should see:** A SKILL.md file at ~/.claude/skills/brainstorm/SKILL.md with YAML frontmatter containing context: fork. The skill is available only in your sessions, not shared with teammates.
3. Add allowed-tools to the brainstorm skill, restricting it to Read, Grep, and Glob (read-only operations)
   *Why:* The exam guide describes allowed-tools as restricting which tools a skill can access, and that is the expected exam answer. In current Claude Code it pre-approves the listed tools so they run without a permission prompt (disallowed-tools is the actual boundary), but the intent is the same: a read-only analysis skill should never be using Write or Bash.
   **You should see:** The SKILL.md frontmatter now includes an allowed-tools list with exactly Read, Grep, and Glob. Under the exam-guide model the skill cannot use Write or Bash; in current Claude Code the list pre-approves those three tools for promptless use.
4. Add argument-hint to the brainstorm skill: "Provide a feature description or codebase area to explore"
   *Why:* The argument-hint prompts developers for required parameters when invoking the skill without arguments. This improves developer experience and is one of the three SKILL.md frontmatter options tested on the exam.
   **You should see:** The SKILL.md frontmatter now includes argument-hint. When a developer invokes /brainstorm without arguments, they see a prompt asking for a feature description or codebase area.
5. Test that /review appears for all project users (shared via git) and /brainstorm only for you
   *Why:* This verifies the scoping boundary that the exam repeatedly tests: .claude/ is project-scoped and shared via git, while ~/.claude/ is user-scoped and personal. Confirming this experimentally solidifies the concept.
   **You should see:** Running /review works in any clone of the repository. Running /brainstorm works only in your session. A colleague or fresh clone without your home directory config does not see /brainstorm as an available command.
6. Invoke the brainstorm skill and verify that its verbose output does not appear in the main conversation context
   *Why:* The context: fork option runs the skill in an isolated sub-agent. The main conversation receives only the summary, not the full verbose output. This is critical for preserving context window tokens during exploratory tasks.
   **You should see:** After invoking /brainstorm with a codebase area, the main conversation shows a concise summary of findings. The verbose file listings, code excerpts, and analysis notes are not visible in the main conversation history. Subsequent responses remain high quality because the context window is not filled with exploration output.
