# Fill-in Exercise 1 — Compare Approaches in Parallel with fork_session

**Difficulty:** Intermediate · **Estimate:** 40 minutes
**Source:** Ravn Study Guide §5.10, Domain 1.3 / 1.7 — https://ravnhq.github.io/claude-certified-architect/guides/en.html

1. Start a Claude Code session that investigates a shared problem, for example: "This React app re-renders too often. Map the component tree and identify where state lives."
   *Why:* fork_session branches from *shared* context. You need a completed investigation phase first so both forks inherit the same discoveries. Without shared groundwork, you are not forking — you are just starting two independent sessions.
   **You should see:** A session that has mapped the component tree and located the state-holding components, with the findings present in context. No new code written yet.
2. Fork the session twice: fork A gets the prompt "Implement a fix using Redux", fork B gets "Implement a fix using Context API".
   *Why:* Both forks inherit everything up to the branch point and then diverge independently. This is the exact exam use case: comparing viable implementation approaches from a common understanding without re-explaining the investigation to either branch.
   **You should see:** Two independent sessions whose contexts both contain the original investigation. Neither fork sees the other's work. Each pursues only its assigned approach.
3. Let each fork complete a minimal implementation and record the results: lines changed, new dependencies, and any trade-offs each fork surfaced.
   *Why:* The value of forking is a like-for-like comparison. Because both branches started from identical context, differences in the outcome are attributable to the approach, not to uneven information.
   **You should see:** Two implementations you can compare directly: same investigation baseline, different solutions. Each fork's summary lists files touched, new dependencies (Redux adds one; Context API adds none), and discovered trade-offs.
4. Decide which approach to keep and discard the losing branch.
   *Why:* Forking is explicitly for exploring alternatives in parallel — the losing branch costs nothing and leaves no trace in the winning session. The exam contrasts this with the alternative: serially trying approach A, then reverting and trying B, which pollutes one session's context with a dead end.
   **You should see:** One surviving session with the chosen implementation. The abandoned approach's context is gone — no dead-code exploration lingering in the session you continue in.
5. Write down when you would fork versus when you would start a fresh session or use --resume, in three rules.
   *Why:* The exam tests the boundary between the three session strategies. fork_session is for branching alternatives from shared context; --resume is for continuing work when files are unchanged; fresh-start-with-summary is for when prior tool results have gone stale.
   **You should see:** Three written rules. Example: fork when comparing approaches from a shared investigation; resume when continuing unchanged work; fresh-start when files changed since the last session. Each rule names the trap it avoids.
