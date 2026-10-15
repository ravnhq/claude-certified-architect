---
name: verify-study-site
description: "Build, serve, and drive the published study site (docs/) in a real browser and keep evidence. Use to confirm a change to the guides, practice exams, question banks, preflight checklists, score-report reader, or site build works as a user sees it — beyond the stub-DOM checks in utils/test_exam_*.mjs."
---

# Verify the study site

The product is the static GitHub Pages site that `scripts/build-pages.mjs` writes to `docs/`. Verification means building it the way `.github/workflows/pages.yml` does, serving it under its `<base href>`, and driving it in Chrome through `agent-browser`. Every run is **isolated**: it builds a snapshot of the working tree in its own directory, serves on its own port, and uses its own browser session, so it never dirties `<track>/dist/` and never touches another run.

Scripts live in `.claude/skills/verify-study-site/scripts/`; call them from the repo root. `<run-id>` is what `launch.sh` prints.

| Path | Holds | Survives cleanup |
|---|---|---|
| `$TMPDIR/verify-study-site/runs/<run-id>/` | snapshot, built `docs/`, `build.log`, `server.log`, `run.env` | no |
| `$TMPDIR/verify-study-site/evidence/<run-id>/` | proof per feature, fixtures, copies of `run.env` and `build.log` | yes |
| `$TMPDIR/verify-study-site/deps/` | pinned build deps, shared across runs | yes |

## Launch

```bash
RUN_ID=$(.claude/skills/verify-study-site/scripts/launch.sh)
```

- Snapshots tracked and untracked-not-ignored files as they are on disk, so uncommitted edits are what gets built. `.corpus/` is left out; only `import_practice_bank.py` reads it.
- Installs the pinned deps from `pages.yml` into `deps/` on first use (~20 s).
- Builds in CI order: `build_exam_html.py`, `build_professional_exam.py`, `build-pages.mjs`, `minify-docs.mjs`. About 80 s.
- Starts `node scripts/serve-docs.mjs <free-port>` (gzip + base path, as Pages serves).
- **Ready** when the server log says `Serving docs` and `GET index.html` returns 200. Then it prints the run id as its only stdout line. A non-zero exit prints the tail of `build.log` or `server.log`; run cleanup on that id anyway.

The guide PDFs are not built (CI makes them with `md-to-pdf` and Puppeteer), so the download links under `pdf/` return 404 locally.

## Doctor

```bash
.claude/skills/verify-study-site/scripts/doctor.sh "$RUN_ID"
```

Read-only. Passes only when the recorded pid is `serve-docs.mjs` on the recorded port with its cwd in this run's snapshot, `lsof` shows that pid owning the port, the served `index.html` is byte-identical to this run's build, `build.log` ends in `docs/ built`, and the main pages answer 200. It prints `URL`, `SESSION`, and `EVIDENCE`, and records the source commit and uncommitted-file count. Run it before driving, and again whenever a result looks like it came from a different build.

## Drive

Every browser action goes through the wrapper, which pins the run's session and the Chrome engine (the recipes need screenshots and `localStorage` that survives a reload):

```bash
b() { .claude/skills/verify-study-site/scripts/browser.sh "$RUN_ID" "$@"; }
b open practical/en.html          # page path relative to the site root
b snapshot -i -c                  # accessible names and refs
b find role button click --name "FINISH & REVIEW"
b get text '#answeredCount'
```

- Define `b` as a function. In zsh a command held in a variable is not word-split, so `$B open …` fails.
- Read [`features/README.md`](features/README.md) first, then follow the feature file for the behaviour under test. It lists the user entry points, handles, and expected results.
- Prefer accessible names (`find role … --name`) for controls. Element ids (`#qCard`, `#browseCount`, `#report-file`) are fine for reading state.
- Native `confirm()` dialogs block every other command until you run `b dialog accept` or `b dialog dismiss`.
- Changing generator code means relaunching: a run serves the snapshot it was built from.

## Evidence

```bash
b proof <feature> <step-name>     # → evidence/<run-id>/<feature>/<step>.{url.txt,aria.txt,png}
```

- Capture the user action and the state it produced: one `proof` before a change and one after, not only the final screen.
- Persistence claims need a second view: reload, or open the other page that reads the same store, and capture that.
- Read stored state with `b eval 'localStorage["<key>"]'` as a read-only second view. Drive state changes through the UI, never by writing storage, since that skips the code under test.
- Write the verdict in your report with the feature id, entry point, and proof paths. An entry point you could not reach is reported as unreached, with the command tried and the unmet precondition.

## Cleanup

```bash
.claude/skills/verify-study-site/scripts/cleanup.sh "$RUN_ID"
```

Closes the run's browser sessions, stops the server only if the pid is still this run's `serve-docs.mjs` with its cwd in this run's snapshot, and deletes `runs/<run-id>/`. Evidence and `deps/` stay. It is safe to re-run and safe after a failed launch, so clean up failed attempts too. Afterwards, `ls` the evidence directory to confirm the proof survived.

## Helpers

| Script | Invocation | Does |
|---|---|---|
| `launch.sh` | `launch.sh` | snapshot, build, serve; prints `<run-id>` |
| `doctor.sh` | `doctor.sh <run-id>` | read-only identity and health checks |
| `browser.sh` | `browser.sh <run-id> open <page>` / `proof <feature> <name>` / any `agent-browser` command | drives the run's Chrome session |
| `make-score-report.sh` | `make-score-report.sh <run-id> [CCAR-F\|CCAR-P\|CCDV-F] [rows] [--no-code]` | prints a synthetic score-report PDF into `evidence/<run-id>/fixtures/` and prints its path |
| `cleanup.sh` | `cleanup.sh <run-id>` | stops owned processes, removes scratch, keeps evidence |

## Upkeep

When a feature, handle, or build step changes, update the matching feature file and script in the same change. Use the `maintain-verification-skill` skill for that upkeep.
