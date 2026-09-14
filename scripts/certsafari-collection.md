# Collect CertSafari practice questions

The collector uses Codex's in-app browser to work through ordinary Review quizzes,
reveal every option explanation, and save the site's marked correct answers.
It supports single-choice and multiple-response questions. Collection creates
practice attempts in that browser's anonymous CertSafari profile; those scores
are not a measure of the user's exam performance.

Start the local receiver from the repository root:

```sh
python3 scripts/certsafari_receiver.py
```

Initialize the bundled browser through `cua_repl`, then open the three exam pages:

- https://www.certsafari.com/anthropic/claude-certified-architect-foundations
- https://www.certsafari.com/anthropic/claude-architect-professional
- https://www.certsafari.com/anthropic/claude-developer-foundations

Start a Review quiz with 60 questions on each page. Open a fourth tab at
http://127.0.0.1:8768/ as the local save form. Read the current browser tool
documentation and page state before interacting. Load the contents of
`certsafari-browser.js` into the persistent `cua_repl` context, then create:

```js
let collector = createCertSafariCollector([
  { tab: foundationsTab, exam: 'CCAR-F', end: false },
  { tab: professionalTab, exam: 'CCAR-P', end: false },
  { tab: developerTab, exam: 'CCDV-F', end: false },
], saveTab);
await collector.loadKnown();
nodeRepl.write(await collector.run(15));
```

Repeat bounded batches, inspecting results after every call. Between sessions,
call `await collector.restart()`. Loading known records avoids re-exporting
duplicates and uses the site's previously recorded answer on repeat questions.
Matching uses normalized question and option text because the rendered page
does not expose a stable server question ID. Answer letters can shuffle.

On a failed call, inspect the affected tab before retrying. A new quiz can take
longer to appear than the browser's selector deadline. Leave that lane pending
and continue other lanes. If the page requests verification, pause the lane
with `lane.paused = true`; do not bypass the verification or a rate limit.
Once a normal quiz is visibly ready, set `paused` and `end` to `false`.
If CertSafari displays "Whoa there!" and "come back tomorrow", stop requests
for the day. The collector pauses all lanes on that response. Resume only after
the site's limit resets; do not switch anonymous identities to evade the limit.
Use the existing quiz history to resume incomplete quizzes before creating new
ones. Completed questions have already been checkpointed.
If `collector.save()` fails, fix the receiver and retry saving the retained
batch before collecting more. `loadKnown()` restores only records already saved.

Output is checkpointed under `.corpus/certsafari/`. The requested CertSafari
snapshot is tracked explicitly; other `.corpus` material remains ignored. The
CCAR-P and CCDV-F exports are the source of the two practice-exam banks:
`utils/import_certsafari.py` folds them into `ccap/data/questions.json` and
`ccdf/data/questions.json`, keying each item to a blueprint objective through the
`Subdomain X.Y` label CertSafari puts on the question, which the collector keeps
in each record's `snapshot`. Re-run that importer after refreshing a snapshot.
When committing a refreshed snapshot, stage only the three exam directories,
the six combined JSON/Markdown exports, `README.md`, and `status.json`.
Do not include `resume.json`, `duplicates/`, or generated ZIP archives.
New checkpoint files under the ignored parent need a targeted `git add -f`.
`status.json` reports unique counts against the published totals observed on
September 14, 2026: 480 CCAR-F, 456 CCAR-P, and 524 CCDV-F. Check the live totals
when resuming another day. Random selection means a fixed number of quizzes
does not guarantee coverage. Check each live Coverage count before claiming
the whole bank is collected.

Generate or refresh the combined JSON and Markdown exports:

```sh
python3 scripts/certsafari_receiver.py --export
```

The local receiver accepts only its loopback form's origin. It stores source
text, not account identifiers, cookies, or verification tokens. The study
material is preserved as supplied by CertSafari; no claim is made that its
answers or explanations are factually correct. No content is published by
these scripts.
