# Chapter 4: Domain 3 — Claude Code Configuration & Workflows (20%)

*6 task statements. At 20%, roughly 12 of 60 items (derived from the weight).*

## Core Idea
Configuration questions are **scope questions**: project vs user, always-loaded vs on-demand, path-conditional vs directory-bound. Pick the mechanism whose loading behavior matches the requirement — "shared with the team", "automatic", "only for matching files" each select a different file location.

## Task Statements

### 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization
**Knowledge of:** the hierarchy — **user-level** (`~/.claude/CLAUDE.md`), **project-level** (`.claude/CLAUDE.md` or root `CLAUDE.md`), **directory-level** (subdirectory `CLAUDE.md`); that user-level settings apply only to that user and are **not shared with teammates via version control**; the **`@import` syntax** for referencing external files to keep CLAUDE.md modular; the **`.claude/rules/`** directory for topic-specific rule files as an alternative to a monolithic CLAUDE.md.
**Skills in:** diagnosing hierarchy issues (a new teammate not receiving instructions because they live in user-level config); using `@import` to include only the standards files relevant to each package; splitting a large CLAUDE.md into focused files in `.claude/rules/` (`testing.md`, `api-conventions.md`, `deployment.md`); using the **`/memory`** command to verify which memory files are loaded and diagnose inconsistent behavior across sessions.

### 3.2 Create and configure custom slash commands and skills
**Knowledge of:** project-scoped commands in **`.claude/commands/`** (shared via version control) vs user-scoped in **`~/.claude/commands/`** (personal); skills in **`.claude/skills/`** with `SKILL.md` frontmatter supporting **`context: fork`**, **`allowed-tools`**, and **`argument-hint`**; `context: fork` for running a skill in an isolated sub-agent context so its output does not pollute the main conversation; personal skill customization via differently named variants in `~/.claude/skills/`.
**Skills in:** creating project-scoped commands in `.claude/commands/` for team-wide availability; using `context: fork` to isolate verbose output (codebase analysis) or exploratory context (brainstorming alternatives); configuring `allowed-tools` to restrict tool access during skill execution (limiting file write operations to prevent destructive actions); using `argument-hint` to prompt for required parameters when the skill is invoked bare; choosing **skills** (on-demand, task-specific) vs **CLAUDE.md** (always-loaded universal standards).

### 3.3 Apply path-specific rules for conditional convention loading
**Knowledge of:** `.claude/rules/` files with **YAML frontmatter `paths` fields containing glob patterns** for conditional activation; that path-scoped rules load only when editing matching files, cutting irrelevant context and token usage; the advantage of glob-pattern rules over directory-level CLAUDE.md for conventions spanning multiple directories (test files spread throughout a codebase).
**Skills in:** creating rule files with path scoping (`paths: ["terraform/**/*"]`); using globs to apply conventions by file type regardless of location (`**/*.test.tsx`); choosing path-specific rules over subdirectory CLAUDE.md when conventions must apply to files spread across the codebase.

### 3.4 Determine when to use plan mode vs direct execution
**Knowledge of:** **plan mode** is designed for complex tasks — large-scale changes, multiple valid approaches, architectural decisions, multi-file modifications; **direct execution** suits simple, well-scoped changes (adding one validation check to one function); plan mode enables safe exploration and design before committing to changes, preventing costly rework; the **Explore subagent** for isolating verbose discovery output and returning summaries to preserve main-conversation context.
**Skills in:** selecting plan mode for architectural implications (microservice restructuring, library migrations affecting 45+ files, choosing between integration approaches with different infrastructure requirements); selecting direct execution for well-understood scope (a single-file bug fix with a clear stack trace, adding a date validation conditional); using the Explore subagent for verbose discovery to prevent context exhaustion in multi-phase tasks; **combining** plan mode for investigation with direct execution for implementation.

### 3.5 Apply iterative refinement techniques for progressive improvement
**Knowledge of:** concrete **input/output examples** as the most effective way to communicate expected transformations when prose is interpreted inconsistently; **test-driven iteration** — write the test suite first, then iterate by sharing failures; the **interview pattern** — have Claude ask questions to surface considerations the developer had not anticipated before implementing; when to provide all issues in a single message (interacting problems) versus fixing sequentially (independent problems).
**Skills in:** providing **2–3 concrete input/output examples** when natural-language descriptions produce inconsistent results; writing test suites covering expected behavior, edge cases, and performance requirements before implementation, then iterating on failures; using the interview pattern to surface design considerations (cache invalidation strategies, failure modes) in unfamiliar domains; providing specific test cases with example input and expected output to fix edge cases (null values in migration scripts); batching interacting fixes into one detailed message, sequencing independent ones.

### 3.6 Integrate Claude Code into CI/CD pipelines
**Knowledge of:** the **`-p` / `--print` flag** for non-interactive mode in automated pipelines; **`--output-format json`** and **`--json-schema`** CLI flags for enforcing structured output in CI; CLAUDE.md as the mechanism for supplying project context (testing standards, fixture conventions, review criteria) to CI-invoked Claude Code; **session context isolation** — the same session that generated code is less effective at reviewing its own changes than an independent review instance.
**Skills in:** running with `-p` to prevent interactive input hangs; `--output-format json` with `--json-schema` to produce machine-parseable findings for automated inline PR comments; including prior review findings when re-running after new commits, instructing Claude to report only new or still-unaddressed issues to avoid duplicate comments; providing existing test files in context so generation avoids duplicate scenarios; documenting testing standards, valuable-test criteria, and available fixtures in CLAUDE.md to raise test quality and cut low-value output.

## Reference Tables

### Where configuration lives
| Mechanism | Path | Scope | Loading |
|---|---|---|---|
| User memory | `~/.claude/CLAUDE.md` | this user only, **not** version-controlled | always |
| Project memory | `.claude/CLAUDE.md` or root `CLAUDE.md` | whole team via VCS | always |
| Directory memory | subdirectory `CLAUDE.md` | that directory tree | when working there |
| Path rules | `.claude/rules/*.md` with `paths:` globs | whole team via VCS | only when editing matching files |
| Slash command (shared) | `.claude/commands/` | whole team via VCS | on invocation |
| Slash command (personal) | `~/.claude/commands/` | this user only | on invocation |
| Skill (shared) | `.claude/skills/<name>/SKILL.md` | whole team via VCS | on demand |
| Skill (personal) | `~/.claude/skills/` | this user only | on demand |
| MCP server (shared) | `.mcp.json` | whole team via VCS | at connection |
| MCP server (personal) | `~/.claude.json` | this user only | at connection |

### SKILL.md frontmatter options tested
| Option | Effect |
|---|---|
| `context: fork` | runs the skill in an isolated sub-agent context; output does not pollute the main conversation |
| `allowed-tools` | restricts tool access during skill execution |
| `argument-hint` | prompts the developer for required parameters on bare invocation |

### Plan mode vs direct execution
| Signal | Choose |
|---|---|
| Multi-file, architectural, multiple valid approaches | plan mode |
| Library migration affecting 45+ files | plan mode |
| Single-file fix with a clear stack trace | direct execution |
| Adding one validation conditional | direct execution |
| Investigation then implementation | plan mode → direct execution |

## Anti-patterns
- **Team instructions placed in `~/.claude/CLAUDE.md`** — never reaches teammates through version control. The classic diagnosis item.
- **A monolithic root CLAUDE.md with per-area headers**, relying on Claude to infer the right section — inference instead of explicit matching is unreliable.
- **Subdirectory CLAUDE.md for conventions spanning directories** — CLAUDE.md is directory-bound; test files scattered beside their sources need glob rules.
- **Skills for conventions that must apply automatically** — skills require invocation or a decision to load; they cannot guarantee automatic path-based application.
- **Running bare `claude "..."` in CI** — hangs waiting for interactive input; use `-p`.
- **Inventing CLI surface** — `CLAUDE_HEADLESS=true`, `--batch`, and `.claude/config.json` with a commands array do not exist.
- **Reviewing generated code in the generating session** — it retains the generation reasoning; use an independent instance.
- **Deferring plan mode until complexity "emerges"** when the requirements already state the complexity.
- **Re-running CI reviews without prior findings** — produces duplicate comments.

## Worked Example
**Sample Question 6 (Scenario 2)** — the decisive Domain 3 item. A codebase has area-specific conventions (React hooks, async/await API handlers, repository-pattern models), and test files sit beside the code they test (`Button.test.tsx` next to `Button.tsx`). All tests must follow the same conventions **regardless of location**, applied **automatically**.

| Option | Verdict | Reasoning |
|---|---|---|
| A. `.claude/rules/` with YAML frontmatter glob patterns | **Correct** | Globs like `**/*.test.tsx` apply by path regardless of directory — essential for scattered test files |
| B. Consolidate into root CLAUDE.md under headers | Wrong | Relies on inference rather than explicit matching |
| C. Skills in `.claude/skills/` per code type | Wrong | Needs manual invocation or Claude choosing to load — contradicts "automatic" |
| D. A CLAUDE.md per subdirectory | Wrong | CLAUDE.md is directory-bound; cannot cover files spread across many directories |

Two keywords decided it: **"automatically"** eliminates skills, **"regardless of location"** eliminates directory-bound CLAUDE.md.

Also in this domain: **Question 4** — a `/review` command for everyone on clone/pull goes in `.claude/commands/` (project, version-controlled), not `~/.claude/commands/`, not CLAUDE.md, and not a non-existent `.claude/config.json`. **Question 5** — monolith-to-microservices across dozens of files with service-boundary decisions is plan mode, and the complexity is already stated in the requirements rather than something that might emerge. **Question 10** — a hanging CI job needs `-p`, not an invented env var or flag, and not a stdin redirect workaround.

**Preparation Exercise 2** exercises the whole domain: a project-level CLAUDE.md, `.claude/rules/` with glob frontmatter (`paths: ["src/api/**/*"]`, `paths: ["**/*.test.*"]`) verified to load only on matching files, a project skill with `context: fork` and `allowed-tools` verified to run in isolation, `.mcp.json` with env var expansion plus a personal server in `~/.claude.json` available simultaneously, and plan mode vs direct execution compared across a single-file fix, a multi-file migration, and an open-ended feature.

## Key Takeaways
1. "Shared with the team" always means the project path under version control.
2. `.claude/rules/` with `paths:` globs is the only mechanism that applies conventions automatically to files scattered across directories.
3. `context: fork` isolates verbose or exploratory skill output from the main conversation.
4. Skills are on-demand and task-specific; CLAUDE.md is always-loaded and universal.
5. `/memory` diagnoses which memory files are actually loaded.
6. CI needs `-p`; structured CI findings need `--output-format json` with `--json-schema`.
7. An independent review instance beats self-review in the generating session.
8. 2–3 concrete input/output examples outperform more prose.
9. Batch interacting fixes in one message; sequence independent ones.

## Prep-course supplement — Claude Code mechanics

*Source: Anthropic Partner Academy prep courses (Claude Code in Action; Developer Foundations M3). Supplements the Exam Guide — where the two differ, answer from the guide. Items marked (preview) are post-guide product surface; verify against current docs before relying on exact behavior.*

### Permission modes
| Mode | Auto-approves | Still gates / notes |
|---|---|---|
| default | reads only | prompts for every edit and command — baseline for unfamiliar codebases |
| acceptEdits | reads, file edits, common filesystem commands (`mkdir`, `mv`, `cp`, `rm`, `sed`) **inside the working directory** | other shell commands, writes outside the working dir, protected paths. Trap: it auto-approves `rm` on in-tree paths — only default prompts for those |
| plan | reads only — research and propose | every edit and command until a plan is approved |
| auto (preview) | everything, with a separate **classifier model** reviewing each action first | classifier blocks intent escalation (production deploys, migrations, force-push, credential exfiltration, mass deletes) but **never judges correctness** — broken code sails through; pair with a Stop hook that runs tests |
| dontAsk | only pre-approved allow-rule tools plus read-only commands | everything else **auto-denied with no prompt** — for CI and unattended pipelines that must not hang on an approval no one will give |
| bypassPermissions | everything, no checks | skips even the protected-path guard; only inside a disposable container or VM |

Shift+Tab cycles default → acceptEdits → plan → auto. Match the mode to the job; unattended-at-work runs get **auto, not bypass** — the classifier still checks intent.

**Settings levels**: user `~/.claude/settings.json` → project `.claude/settings.json` (version-controlled) → local `.claude/settings.local.json` (personal, git-ignored) → enterprise `managed-settings.json` (admin-set, cannot be overridden). **Deny beats allow at every level** (precedence deny > ask > allow); an enterprise deny rule is the one control that survives even bypass mode. Permission rules can name a single MCP tool — `mcp__server__tool` — so a broad server connects while the agent keeps a narrow slice.

### Hook events and exit codes
| Event | Fires | Use |
|---|---|---|
| PreToolUse | before a tool call | the only point that can **block**. JSON `permissionDecision`: allow / deny / ask (a fourth value, defer, applies only to non-interactive `-p` runs). `updatedInput` rewrites the call without blocking (redact a secret from a bash command) — it replaces the **whole input object**, so echo back unchanged fields |
| PostToolUse | after a successful call | too late to block — format, lint, audit, normalize; can still feed text back to Claude |
| Stop / SubagentStop | the model wants to end its turn | exit 2 refuses "done" — gate the turn on tests actually passing |
| UserPromptSubmit | on prompt submit | validate or inject context before work starts; stdout joins context |
| SessionStart | session starts or resumes | `startup` matcher for fresh starts; **`compact` matcher re-injects state right after compaction** (use this, not PostCompact); stdout joins context |
| PreCompact/PostCompact, SessionEnd, Notification | lifecycle bookkeeping | some events (Notification, SessionStart) ignore blocking entirely |

Exit codes: **0** = success (stdout JSON is parsed; plain text enters context only on SessionStart / UserPromptSubmit-type events). **2** = blocking error — stderr is fed back to Claude, which reads the failure and fixes it. **1 does not block** — the call runs anyway; the classic trap. Anything else is non-blocking and logged.

### Where a rule lives — the three instruction surfaces
- Conventions that always apply → **CLAUDE.md**. Procedures and reference tied to a kind of task → **a skill**. A rule Claude must not be able to skip → **a hook** — CLAUDE.md and skills are instructions the model follows; hooks are code that runs. "Never push to main" belongs in a PreToolUse hook, not a memory file.
- CLAUDE.md is not enforced configuration: the longer it grows, the more it competes with itself — a single buried rule stops landing in an 800-line file. Treat it like production code: delete lines you cannot justify.
- The memory stack has four layers: **managed policy → user → project → local** (personal per-project notes, not shared). All load together; org policy is always in play.
- `@import` expands referenced files inline at launch — it organizes a large file but does **not** reduce context.
- Phrasing rules: be specific and checkable ("use named exports, not default exports") instead of vague ("follow best practices"); **name the replacement**, not just the ban; emphasis ("IMPORTANT", "you must") is a **budget** — it raises priority only relative to everything quieter, so spend it on the two or three rules that hurt when broken.
- Treat wrong behavior as a bug report against CLAUDE.md: tell Claude "add that to CLAUDE.md" and it writes the rule.
- `/init` scans the codebase and generates a starter CLAUDE.md (accepts focus instructions; validate before trusting); `#` appends a quick note into project, user, or local memory.
- A `.claude/rules/` file **without** a `paths:` frontmatter loads unconditionally, exactly like CLAUDE.md — scoping comes from the frontmatter, never from where the file sits inside `.claude/rules/`.

### Skills and subagents — loading nuances
- Only skill **descriptions** load until a skill triggers; the description is the matching criterion. A skill folder can carry side files — a `reference.md` Claude reads only when it needs depth, and scripts it executes without loading — so SKILL.md itself stays lean.
- First skill worth building: a **verification skill** — run the suite, read the diff, check no test was weakened to pass, report pass/fail with evidence attached.
- The built-in **Explore and Plan subagents skip CLAUDE.md** (fast, cheap research); the general-purpose subagent loads it. When project constraints must be respected, delegate to general-purpose or a custom subagent.
- Subagents do **not** inherit skills: a custom subagent must list needed skills explicitly in its frontmatter.
- Portability: no absolute paths or machine-local assumptions in skill bodies — use `$CLAUDE_PROJECT_DIR` (project scripts) and `${CLAUDE_PLUGIN_ROOT}` (plugin-bundled scripts); document every required env var.

### Plugins — packaging a team setup
- A plugin is **one versioned installable unit** bundling skills, subagents, hooks, commands, and MCP server configs. Manifest: `.claude-plugin/plugin.json`; only `name` is required, and it namespaces every component (`/payments:run-tests`). Without a manifest, components are discovered by directory convention.
- Teams distribute through a **marketplace** (`/plugin marketplace add owner/repo`); enterprise managed settings can allowlist marketplace sources and push plugins org-wide (managed scope overrides user and project).
- Security model: a plugin runs code with your privileges, and its hooks fire on every matching tool call — a community plugin can ship a Stop hook that calls a network endpoint with no warning. Plugin hooks **stack** with yours; skills, agents, and commands are namespaced so they never clash. Read every hook, agent, and MCP server before installing; reviewed is not trusted.
- Distribution failure mode: absolute paths and undeclared env vars install cleanly, then fail on every machine but the author's. Bundle assets, validate env vars at install, test on a clean machine.

### Headless, routines, CI (preview surface)
- `-p` / `--print`: one-shot non-interactive run — reads stdin, writes stdout, pipes like any shell tool. A bare variant skips auto-discovery of hooks, skills, plugins, MCP servers, and CLAUDE.md: Claude plus explicitly allowed tools only — reproducible CI runs, faster startup.
- `--output-format json` with `--json-schema`: the schema-conforming object lands in a `structured_output` field of the JSON response (pipe through `jq`). Capture the session id from JSON output and `--resume` it later for multi-step automation.
- **Routine** (preview): a saved prompt + repository + connectors that runs on Anthropic-managed infrastructure on a trigger — cron (at most hourly), an HTTP POST endpoint, or a GitHub event. Each run starts from a **fresh clone of the default branch** and can push only to `claude/`-prefixed branches unless loosened per repo. Selection rule: routine for repeat work with nothing to host → headless `-p` when the job needs your pipeline or environment → Agent SDK (a `query` function taking prompt + options: allowed tools, system prompt, permission mode) when the work belongs inside your own product.
- GitHub, two paths: managed **Code Review** (preview) reviews the diff against the full codebase, posts deduplicated, severity-tagged inline findings — it **never approves or blocks** the PR (judgment stays human) and has no managed autofix (apply findings locally with `/code-review --fix`). The **Claude Code GitHub Action** covers everything beyond review: `@claude` comment triggers, cron rollups, workflow_dispatch; tune via `claude_args` — cap `max-turns`, set `dontAsk` permission mode, scope `allowedTools` to exactly what the job needs (read-only for a report).

### Verifying unsupervised runs
Verify **in proportion to how unsupervised the run was**: a watched session needs a glance; an unattended or CI run needs a real check, because nobody saw it happen.
1. Read the **diff itself**, not Claude's summary of it — a tidy summary can read fine while the diff touched a file you did not expect.
2. Wire the tests as a **Stop hook** so the gate fires whether or not you remember to ask; exit 2 feeds the failure back and Claude fixes it unprompted. "Claude ran the tests" must be enforced, not claimed.
3. Verify headless runs by their **JSON result and exit code**.
4. Get a **cold second opinion**: hand the diff to a reviewer that never saw the build — a separate session or subagent, carrying none of the original run's context. Independence is the mechanism: a reviewer holding the reasoning that produced the code inherits its blind spots. (The guide's independent-review rule, 3.6/4.6, applied to unsupervised runs.)

### Steering long sessions
- Scope before running: plan mode, then actually read the plan and iterate on it — revising a plan is cheaper than repairing an execution.
- `/compact` accepts instructions — "keep the API changes, drop the debugging" — directing what the summary preserves; undirected compaction is where details vanish and drift begins.
- Double-tap Escape opens the **rewind** menu: every user prompt is a checkpoint; restore code, conversation, or both; summarize everything after a checkpoint (discard a side quest) or up to it (compress a long setup phase).
- Parallel agents on one repo → **git worktrees**: independent file trees prevent sessions fighting over files; a `.worktreeinclude` file at the repo root lists git-ignored files (`.env`, local config) to copy into each; clean worktrees auto-remove on exit.

## Connects To
- **ch02 (Domain 1)**: `--resume` and `fork_session` session management (1.7) are the companion Claude Code surface.
- **ch05 (Domain 4)**: CI review prompts need explicit criteria (4.1) and multi-pass architecture (4.6).
- **ch06 (Domain 5)**: the Explore subagent and `/compact` for context management in long sessions (5.4).
- **ch08**: Sample Questions 4, 5, 6, 10.
