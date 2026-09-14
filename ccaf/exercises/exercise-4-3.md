# Exercise 4.3 — Build a Structured Extraction Tool with JSON Schema

**Difficulty:** Intermediate · **Estimate:** 45 minutes
**Source:** https://claudecertificationguide.com/learn/4-prompt-engineering/4-3-structured-output#build-exercise

#### Build a Structured Extraction Tool with JSON Schema  ·  45 minutes
1. Define an extraction tool with a JSON schema: 3 required fields, 3 optional/nullable fields, an enum with unclear and other options, and a detail string field for the other category
   *Why:* Schema design directly prevents fabrication. Required fields pressure the model to invent values when information is absent. Optional/nullable fields allow honest null responses. This is the root cause fix for hallucinated extraction data.
   **You should see:** A valid JSON schema with required array containing only the 3 always-present fields, nullable type definitions for optional fields, and an enum array including unclear and other alongside the standard categories.
2. Test with tool_choice auto and observe cases where the model returns text instead of calling the tool
   *Why:* The exam tests the distinction between auto, any, and forced tool_choice. Auto allows the model to respond conversationally instead of calling a tool, which means no guaranteed structured output. You need to see this failure mode firsthand.
   **You should see:** At least one response where the model returns a text message describing the document contents instead of calling the extraction tool. This demonstrates why auto is unsuitable when you need guaranteed structured output.
3. Switch to tool_choice any and verify the model always returns structured output via a tool call
   *Why:* tool_choice any guarantees a tool call while letting the model choose which tool. This is the correct setting for guaranteed structured output when the document type is unknown, a key exam distinction from auto.
   **You should see:** Every response has stop_reason of tool_use and contains a valid tool call with structured output conforming to your schema. No text-only responses.
4. Force a specific tool with tool_choice {type: tool, name: extract_metadata} and verify the mandatory extraction step runs
   *Why:* Forced tool selection ensures a mandatory first step executes regardless of the model decision. The exam tests this for scenarios like metadata extraction that must run before enrichment steps.
   **You should see:** The response always calls the exact tool you specified, even when the document content might suggest a different tool would be more appropriate. The model has no flexibility in tool selection.
5. Process 5 documents — 3 with complete data and 2 with missing fields — and verify nullable fields return null rather than fabricated values
   *Why:* This validates the most important schema design principle: optional/nullable fields prevent fabrication. The exam specifically tests the scenario where required fields pressure the model to invent plausible-looking data for absent information.
   **You should see:** For the 3 complete documents, all fields populated with correct values. For the 2 documents missing information, the nullable fields return null instead of fabricated values. No invented dates, amounts, or identifiers.
