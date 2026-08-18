# Exercise 2.1 — Design Tool Descriptions That Eliminate Misrouting

**Difficulty:** Beginner · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/2-tool-design-mcp/2-1-tool-schema-design#build-exercise

#### Design Tool Descriptions That Eliminate Misrouting  ·  30 minutes
1. Create two MCP tools with intentionally ambiguous descriptions (e.g. get_customer: Retrieves customer information and lookup_order: Retrieves order details)
   *Why:* Reproducing a misrouting scenario first-hand builds intuition for why minimal descriptions fail. The exam tests your ability to identify ambiguous descriptions as the root cause of tool selection errors.
   **You should see:** Two tool definitions registered with your MCP server, each having a single-sentence description that does not mention input formats, example queries, or boundaries.
2. Test with 10 queries covering different user intents and log which tool the model selects for each
   *Why:* Quantifying selection accuracy before and after description changes gives you concrete evidence of the impact. The exam expects you to know that description quality directly affects selection reliability.
   **You should see:** A log showing at least 2-3 misrouted queries where the model selected get_customer for order-related queries or vice versa, demonstrating the ambiguity problem.
3. Rewrite both descriptions to include: purpose, expected inputs with formats, example queries, edge cases, and explicit boundaries against the other tool
   *Why:* This is the core exam skill — the lowest-effort, highest-leverage fix for misrouting. Production-grade descriptions include all five elements: purpose, inputs, examples, edge cases, and boundaries.
   **You should see:** Each tool description is 3-5 sentences long, explicitly states accepted identifier formats, gives example queries, and includes a boundary statement like "Do NOT use for order-specific queries — use lookup_order for those."
4. Re-run the same 10 queries and compare selection accuracy before and after
   *Why:* Measuring improvement validates that description quality is the root cause. The exam expects you to understand that better descriptions produce measurably better selection without any architectural changes.
   **You should see:** Selection accuracy improves to 9/10 or 10/10 correct, with previously misrouted queries now hitting the correct tool. A clear before/after comparison showing the improvement.
5. Review your system prompt for keyword-sensitive instructions that could override the improved descriptions
   *Why:* System prompt conflicts are a subtle failure mode the exam tests. Keywords like "always check customer details" can create unintended tool associations that override even well-written descriptions.
   **You should see:** A list of any keyword-sensitive phrases in your system prompt that could trigger incorrect tool associations, along with rewritten versions that avoid the conflict.
