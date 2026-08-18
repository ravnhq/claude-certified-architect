# Exercise 3.6 — Set Up a CI/CD Pipeline with Claude Code

**Difficulty:** Advanced · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/3-claude-code-config/3-6-cicd-integration#build-exercise

#### Set Up a CI/CD Pipeline with Claude Code  ·  45 minutes
1. Write a CI script that runs Claude Code with the -p flag for non-interactive PR analysis
   *Why:* The -p flag is the single most directly testable fact in Domain 3. Without it, the CI job hangs indefinitely waiting for interactive input. This is Question 10 in the official sample questions.
   **You should see:** A CI script (GitHub Actions YAML, GitLab CI, or similar) that invokes claude -p with a review prompt. The job completes successfully without hanging. The output is printed to stdout and captured by the CI system.
2. Add --output-format json and --json-schema to produce structured findings with file, line, severity, and message fields
   *Why:* CI output must be machine-parseable. Automated systems need structured JSON to post inline PR comments, filter by severity, and track findings across runs. Human-readable text output cannot be reliably parsed by downstream tools.
   **You should see:** The Claude Code output is a JSON envelope whose structured_output field conforms to the specified schema. Each finding has file, line, severity, and message fields. Piping the output to jq .structured_output extracts the validated data without errors.
3. Configure the pipeline to parse the JSON output and post findings as inline PR comments
   *Why:* Inline PR comments at exact file and line numbers provide actionable feedback. Generic PR-level comments are ignored. Structured JSON output makes precise inline commenting possible.
   **You should see:** Each finding from the JSON output appears as an inline comment on the PR at the exact file and line number. Severity levels are visible. Developers can see the finding in context alongside the code it references.
4. Add a section to CLAUDE.md documenting testing standards, available fixtures, and review criteria for CI-invoked Claude Code
   *Why:* Claude Code reads CLAUDE.md in CI just as in interactive mode. Without project context, CI-invoked test generation produces low-value boilerplate. With testing standards and fixture documentation, generated tests follow team patterns.
   **You should see:** The CLAUDE.md file contains a clearly marked CI-relevant section with testing standards, available fixture paths, and review severity criteria. CI-invoked Claude Code produces tests using the documented factories and fixtures rather than generic boilerplate.
5. Set up two separate Claude Code invocations: one for code generation and an independent one for review (no shared session context)
   *Why:* The same session that generated code is less effective at reviewing it because it retains reasoning context that biases it toward its own decisions. Independent review instances evaluate code on its own merits without prior justification bias.
   **You should see:** Two distinct claude -p invocations in the CI script: one for generation and one for review. They share no session context. The review invocation analyses the generated code independently. The review findings are more thorough than self-review in the same session.
6. Implement incremental review: store previous findings, include them in the next review run, and instruct Claude to report only new or still-unaddressed issues
   *Why:* Without incremental context, each review run analyses the entire PR from scratch and produces duplicate comments. Duplicate comments erode developer trust — when the same five issues appear on every push regardless of fixes, developers stop reading them.
   **You should see:** The first review run produces findings and stores them (as a JSON artifact or file). Subsequent runs include the previous findings in context. The output contains only new issues or issues that remain unaddressed. Previously fixed issues do not reappear as comments.
