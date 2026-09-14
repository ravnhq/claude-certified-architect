# Exercise 1.2 — Build a Hub-and-Spoke Research Coordinator

**Difficulty:** Intermediate · **Estimate:** 60 minutes
**Source:** https://claudecertificationguide.com/learn/1-agentic-architecture/1-2-orchestration-patterns#build-exercise

#### Build a Hub-and-Spoke Research Coordinator  ·  60 minutes
1. Create a coordinator agent that accepts a broad research topic as input
   *Why:* The coordinator is the central hub in hub-and-spoke architecture. The exam tests whether you understand that the coordinator owns task decomposition, subagent selection, and result aggregation — not the subagents.
   **You should see:** A coordinator function that accepts a topic string and returns a structured research report. It should have a system prompt defining its role as the orchestrating hub.
2. Implement task decomposition logic that breaks the topic into at least 5 distinct subtopics covering the full breadth of the subject
   *Why:* Narrow decomposition is a specific exam failure pattern. The coordinator that only assigns solar and wind for renewable energy misses entire categories. The exam expects you to recognise that incomplete output traces back to the coordinator decomposition.
   **You should see:** A decomposition function that produces 5 or more subtopics for any broad topic. For renewable energy, it should cover solar, wind, geothermal, tidal, biomass, and fusion at minimum.
3. Spawn two subagents (web search and document analysis) with explicit context passing — include all relevant information in each subagent prompt
   *Why:* Subagent isolation means no shared memory and no inherited context. The exam heavily tests this: if a subagent produces poor results, check whether the coordinator gave it sufficient context, not whether the subagent itself is flawed.
   **You should see:** Two subagent invocations where each receives the full assigned subtopic, the research goal, and any relevant context from prior agents — all explicitly included in the prompt.
4. Aggregate results from both subagents and evaluate coverage completeness
   *Why:* The coordinator must evaluate whether the combined results cover the full breadth of the original topic. This is where iterative refinement starts — gaps detected here trigger re-delegation.
   **You should see:** An aggregation function that combines results from both subagents and produces a coverage assessment listing which subtopics are well-covered, partially covered, or missing.
5. Implement an iterative refinement loop: if the coordinator identifies coverage gaps, re-delegate to subagents with targeted queries and re-invoke until coverage is sufficient
   *Why:* Iterative refinement is a core coordinator responsibility the exam tests. A single-shot delegation is not enough — the coordinator must evaluate output and re-delegate for gaps. This distinguishes a coordinator from a simple dispatcher.
   **You should see:** A loop that checks coverage, identifies gaps, sends targeted follow-up queries to subagents for the missing subtopics, and re-evaluates until a coverage threshold is met or a maximum iteration count is reached.
6. Test with the topic renewable energy technologies and verify that the final output covers solar, wind, geothermal, tidal, biomass, and fusion
   *Why:* This specific test case maps to the exam narrow decomposition failure pattern. If your output only covers solar and wind, the root cause is the coordinator decomposition — the exact diagnostic the exam expects you to make.
   **You should see:** A final research report with substantive sections on all six energy types: solar, wind, geothermal, tidal, biomass, and fusion. The coverage evaluation should show 100% completeness.
