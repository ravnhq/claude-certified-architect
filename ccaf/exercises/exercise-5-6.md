# Exercise 5.6 — Build a Provenance-Preserving Synthesis Pipeline

**Difficulty:** Advanced · **Estimate:** 60 minutes
**Source:** https://claudecertificationguide.com/learn/5-context-management/5-6-information-provenance#build-exercise

#### Build a Provenance-Preserving Synthesis Pipeline  ·  60 minutes
1. Define a structured claim-source mapping schema with fields: claim, sourceUrl, documentName, relevantExcerpt, publicationDate
   *Why:* Every finding in a multi-agent research system must carry its provenance. Without structured claim-source mappings, attribution dies during summarisation and the final output becomes untraceable plausible-sounding text with no verifiable sources.
   **You should see:** A TypeScript interface or JSON schema with all five required fields: claim (the assertion), sourceUrl (where found), documentName (title), relevantExcerpt (supporting passage), and publicationDate (when published or data collected). Each field should be required, not optional.
2. Implement two research subagents that output findings using the claim-source mapping schema, including publication dates
   *Why:* Subagents must output in the structured format from the start. If subagents return unstructured prose, attribution is already lost before synthesis begins. Requiring structured output at the subagent level is the foundation of end-to-end provenance.
   **You should see:** Two subagent functions that each return an array of ClaimSourceMapping objects with all fields populated, including publication dates. Each subagent should research a different aspect of the same topic.
3. Build a synthesis agent that merges findings from both subagents while explicitly preserving all claim-source mappings through the merge process
   *Why:* Step 3 (synthesis) is the most common failure point for attribution. The synthesis agent naturally compresses and paraphrases, destroying claim-source mappings unless explicitly instructed to preserve them. The exam tests whether you understand that attribution must be explicitly maintained through every synthesis step.
   **You should see:** A synthesis output where every claim is traceable to its source. The synthesis should combine related findings but maintain inline citations or a reference section linking each claim to its original source URL, document name, and publication date.
4. Handle conflicting sources by annotating both values with full attribution and possible explanations, without arbitrarily selecting one value
   *Why:* When two credible sources report different statistics, arbitrarily selecting one destroys information and presents false certainty. The exam tests that the correct approach is to annotate both values with source attribution and let the consumer decide. Different publication dates often explain different numbers as trends, not contradictions.
   **You should see:** A conflict handling function that detects overlapping claims with different values, preserves both with full attribution, and adds a possible explanation noting temporal or methodological differences. The output should never silently pick one value.
5. Implement content-appropriate rendering in the final output: format financial data as tables, news findings as prose, and technical findings as structured lists
   *Why:* The exam tests that synthesis should not flatten everything into a uniform format. Financial data is most readable as tables, news context reads naturally as prose, and technical findings are clearest as structured lists. Forcing all content into one format degrades readability.
   **You should see:** A rendering function that detects the content type of each section and applies the appropriate format. Financial data should appear in tables with columns for year, value, and source. News should be prose paragraphs. Technical findings should be bulleted lists.
