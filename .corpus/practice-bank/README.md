# Practice-bank question download — partial, resumable

Collected on September 14, 2026 through normal Review quizzes in Codex's in-app browser.

| Exam | Collected | Published bank | Remaining |
|---|---:|---:|---:|
| CCAR-F | 471 | 480 | 9 |
| CCAR-P | 421 | 456 | 35 |
| CCDV-F | 475 | 524 | 49 |
| Total | 1367 | 1460 | 93 |

The practice bank stopped further practice with its daily limit: "come back tomorrow".
This archive is not the complete bank. The active quiz sessions were preserved
for resumption after the site's daily limit resets. No bypass was attempted.

Each exam has JSON and Markdown exports. Every JSON record includes question
text, all choices, correct choices as marked by the site, an explanation for
each option, a rendered snapshot, and the capture timestamp.
All saved records passed structural validation. Single-choice and multi-response
questions are included. Answers are copied from the practice bank, not independently
verified for factual correctness. These are third-party practice questions.

Records are deduplicated by question and choice text, ignoring answer ordering.
Some questions share a stem but have different choices; those are retained.
One early Markdown-formatting duplicate was excluded from the bank.

Per-question files in the working folder are resumable checkpoints. The reusable
browser collector and receiver are described in scripts/practice-bank-collection.md
in the source repository. Refresh these combined exports with:

    python3 scripts/practice_bank_receiver.py --export

This practice-bank snapshot is included in the repository at the user's request.
Other local corpus material, temporary browser state, duplicates, and ZIP
archives are excluded.
