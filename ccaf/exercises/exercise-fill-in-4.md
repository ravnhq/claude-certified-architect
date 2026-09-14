# Fill-in Exercise 4 — Use /compact and /memory Without Losing Critical Facts

**Difficulty:** Beginner · **Estimate:** 30 minutes
**Source:** Ravn Study Guide §5.7–5.8, Domain 5.1 / 5.4 — https://ravnhq.github.io/claude-certified-architect/guides/en.html

1. Run a long investigation session (10+ turns of file reads and searches) until the context window is heavily used, with specific facts discovered along the way: exact line numbers, amounts, dates, identifiers.
   *Why:* You need real context pressure to see what /compact actually does. The exam tests the risk, not just the command: summarisation compresses prior history, and exact numeric values, dates, and specific details can be lost in the process.
   **You should see:** A session with concrete discovered facts recorded somewhere you can check later — for example "refund amount $247.83, order #8891, March 3rd, bug at auth.ts:42". Several of these facts should live only in the conversation so far.
2. Before compacting, extract the critical facts into a persistent location: a case-facts block in your prompt, a scratchpad file, or CLAUDE.md via /memory.
   *Why:* This is the exam's required pairing: /compact frees the context window, but you must first protect transactional facts outside the summarised history. Compacting without extraction is the progressive-summarisation trap; compacting after extraction is the intended workflow.
   **You should see:** The key facts now exist outside raw conversation history — in a delimited facts block, a scratchpad file, or a CLAUDE.md entry. Each fact is specific (exact values), not a summary ("a refund of some amount").
3. Run /compact, then ask the agent questions that require the protected facts.
   *Why:* This is the verification that the pattern works. After summarisation, the conversation history no longer contains the original turns verbatim — only the facts you protected survive intact. The exam tests that lossy summarisation is acceptable *because* critical facts were extracted first.
   **You should see:** Correct, specific answers post-compact: the exact amount, order number, date, and line number come back. Try the same questions on a control run where you compacted *without* step 2 and observe degraded answers ("around $250", "early March").
4. Use /memory to persist a project convention or preference you want available next session, then confirm it loads in a fresh session.
   *Why:* /memory is the guide's designated command for cross-session persistence: it opens the CLAUDE.md file for editing, and the saved information loads automatically on startup. The exam contrasts this with re-explaining the same instructions every session.
   **You should see:** An entry added to CLAUDE.md through /memory (for example a testing convention or a frequently used command). A new session in the same project has that entry in its loaded configuration under /context, with zero re-explanation.
5. Write a two-line rule for your team: when to /compact, and what must be true before you do it.
   *Why:* The exam rewards knowing the conditions, not the keystroke. The rule should bind the two commands together: /compact is for long sessions filling with verbose tool output; before running it, critical facts must live in a persistent block, scratchpad, or memory.
   **You should see:** A written rule a teammate could apply without asking you. Example: "Long investigation filling context? Extract facts to scratchpad or /memory first, then /compact. Never compact with unprotected specifics in history."
