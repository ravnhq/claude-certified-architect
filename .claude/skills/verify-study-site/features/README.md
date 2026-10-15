# Study site verification map

This directory is the maintained source for verifying what a candidate sees on the study site. Read this index before driving the site, then use the matching feature file as the recipe.

## Baseline preconditions

- A run launched with `scripts/launch.sh`, and `scripts/doctor.sh <run-id>` passing for it.
- `b` defined as the `browser.sh` wrapper for that run (see `SKILL.md`, Drive).
- A fresh run's browser session has empty `localStorage`. Every recipe assumes that unless its preconditions say otherwise.
- Drive only the instance doctor confirmed. Never point a recipe at the published site or another run's port.

## Driving conventions

- Page paths are relative to the site root under `/claude-certified-architect/`: `b open practical/en.html`.
- Prefer roles and accessible names for actions. Button labels render in uppercase (`FINISH & REVIEW`, `RESET CHECKLIST`); `--name` matching follows the rendered text.
- Read state through stable ids and the visible text: `#answeredCount`, `#totalCount`, `#browseCount`, `#search-status`.
- Answer native `confirm()` prompts explicitly with `b dialog accept` or `b dialog dismiss`.
- Local state is per page family. Each feature file names its `localStorage` keys so a second view can read them without writing.

## Proof and skip reporting

- Capture the action and the resulting state with `b proof <feature> <step>`, before and after a change.
- Persistence proof is a second view: a reload or another page reading the same key, captured.
- Report the feature id and the entry point with every artifact.
- Report an unreachable path with the attempted command and the unmet precondition. A behaviour verified through one entry point is not verified through another.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behaviour, then exactly four H2 sections in this order:

1. `Sub-features`: short ids, one line each.
2. `How to get to it (user POV)`: every user entry point.
3. `Driving it with agent-browser`: starts with `Preconditions:`, then labelled bullets pairing each user action with an exact command and its observable result.
4. `Gotchas`: traps that waste or invalidate a run.

Keep implementation detail out of the map. Name user paths, stable handles, required state, commands, and observable proof.

## Features

- [Practice exam](./practice-exam.md): draw, study and exam modes, answering, finishing, scoring, persistence, domain drills, all five exam pages.
- [Score report](./score-report.md): PDF upload, exam detection and choice, personalized plan, targeted practice, saved data and deletion.
- [Question bank](./question-bank.md): browsing a track's whole bank by topic, objective, and search.
- [Preflight checklist](./preflight.md): readiness ticks per track, persistence, reset.
- [Study guides and site chrome](./study-guides.md): guide pages, contents rail, cross-language search, theme toggle, home track chooser.

Unmapped: the cheatsheet pages (`cheatsheet/{en,es,pt}.html`, static) and the guide PDFs (not built locally).
