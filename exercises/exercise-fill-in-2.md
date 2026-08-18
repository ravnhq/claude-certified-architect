# Fill-in Exercise 2 — Isolate Verbose Discovery with an Explore Subagent

**Difficulty:** Intermediate · **Estimate:** 40 minutes
**Source:** Ravn Study Guide §5.6, Domain 3.4 / 5.4 — https://ravnhq.github.io/claude-certified-architect/guides/en.html

1. Pick a verbose codebase discovery task, for example: "Trace every import chain that reaches the payments module." Estimate its raw output size before running it.
   *Why:* The Explore subagent exists for one reason: verbose discovery output exhausts the main context window and degrades every later response in the session. You need a task chatty enough that running it inline would visibly pollute context — file listings, import chains, code excerpts across a dozen files.
   **You should see:** A task whose full raw output would span dozens of files and thousands of tokens, and a rough token estimate of that output written down before you run anything.
2. Run the task inline in the main session and note the effect on the conversation.
   *Why:* You need the baseline failure mode firsthand. Inline discovery dumps every intermediate file and search result into the main context, where it stays for the rest of the session. The exam treats "main agent reads 15 files directly" as the anti-pattern this exercise replaces.
   **You should see:** The main conversation context filled with file contents and search results. Ask a follow-up question afterwards and note that the model's answers now compete with a large volume of discovery noise.
3. Repeat the same task delegated to an Explore subagent and compare what enters the main context.
   *Why:* The Explore subagent isolates verbose output and returns only a summary. The main agent keeps one line — "Payments depends on AuthService, OrderModel, and the external PaymentGateway API" — instead of 15 files. The exam names this as the correct defence against context-window exhaustion in multi-phase tasks.
   **You should see:** The main conversation receives a concise structured summary: key findings, file paths, class names. The raw listings and excerpts never appear in the main context. A follow-up question is answered without degradation.
4. Check the context budget difference between the two runs.
   *Why:* Quantifying it proves the mechanism. The exam expects you to know *why* delegation works, not just that it works: subagents operate in their own context budget, and only their return value costs tokens in the coordinator session.
   **You should see:** A measurable difference in context usage between the inline run and the delegated run, roughly matching the size of the raw output you estimated in step 1. The delegated run's main-context cost is the summary only.
5. Add the pattern as a standing rule: in your CLAUDE.md or a skill with context: fork, require verbose discovery to run in an isolated subagent that returns a summary.
   *Why:* One-off discipline does not survive long sessions. The guide's standard mechanism is a skill with `context: fork` frontmatter (exercise 3.2) or an explicit team convention, so every discovery task gets isolation by default rather than by remembering.
   **You should see:** A written rule or skill frontmatter entry that routes verbose exploration through an isolated context. The rule states what the subagent must return: a structured summary, not raw output.
