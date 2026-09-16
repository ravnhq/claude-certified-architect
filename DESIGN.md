---
version: alpha
name: Ravn Certification Study
description: Current Ravn web identity adapted for certification study.
colors:
  background: "#0E0E0E"
  surface: "#141414"
  surface-elevated: "#1C1C1C"
  foreground: "#FFFFFF"
  secondary: "#A3A3A3"
  muted: "#949494"
  border: "#292929"
  border-strong: "#333333"
  primary: "#FFFFFF"
  on-primary: "#0E0E0E"
  accent: "#F8E3A0"
  success: "#6FA97C"
  error: "#C16B57"
typography:
  display:
    fontFamily: Inter
    fontSize: 52px
    fontWeight: 600
    lineHeight: 1.16
    letterSpacing: -0.025em
  heading:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.025em
  body:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0.06em
rounded:
  sm: 4px
  md: 8px
  surface: 18px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  section: 64px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 12px
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.border}"
    rounded: "{rounded.surface}"
    padding: 24px
---

## Overview

Ravn's current website uses a dark, restrained technical identity: Inter headlines,
JetBrains Mono labels, neutral surfaces, white calls to action, and pale gold used
sparingly for highlights. Preserve the official wordmark and clear type hierarchy.
This study site adapts that identity for sustained reading and interactive quizzes.

### Sources and extraction

Captured on 2026-09-15 from [ravn.com](https://www.ravn.com/). Firecrawl's successful
homepage scrape is saved locally in `.firecrawl/ravn-content.md` (scrape ID
`01a0a566-bb9c-75ee-a6d3-e52eb710f180`). It confirms the current homepage and content.
The successful Firecrawl branding extraction is `.firecrawl/ravn-branding.json`
(scrape ID `01a0a567-a3bd-70e9-b47a-8c204ce705d8`). It identifies Inter,
JetBrains Mono, the dark background, 52px/40px headings, and 8px white/gray buttons.

Color roles were cross-checked against rendered browser styles and the site's
[font stylesheet](https://www.ravn.com/_next/static/chunks/3x_31klo9518j.css) and
[theme stylesheet](https://www.ravn.com/_next/static/chunks/1fhch-tvh1n2m.css), saved
in `.firecrawl/`. Firecrawl classified red/teal comparison accents as primary colors
and reported dark primary text; those classifications do not describe the overall
page hierarchy. The tokens here follow the actual root CSS and rendered components.

This document follows the [Google Labs DESIGN.md draft specification](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md),
version `alpha`: optional YAML token frontmatter followed by the recommended prose
sections. This is a draft interchange format, not a claim of an industry-wide standard.

## Colors

The source's background is `hsl(0 0% 5.5%)`, card surface `hsl(0 0% 8%)`, elevated
surface `hsl(0 0% 11%)`, borders `hsl(0 0% 16%)` and `hsl(0 0% 20%)`, and gold
`hsl(47 88% 76%)`. Tokens above use rounded sRGB hex equivalents. The source uses
white headlines and 60%-white secondary text. This site uses opaque gray equivalents
so text remains predictable over different surfaces.

White fills identify primary actions. Pale gold identifies selected controls,
question references, and study emphasis. Red and green retain their existing quiz
feedback meanings; they are functional study-site adaptations, not brand accents.

The guide's optional light reading mode is a local adaptation: white background,
near-black text, gray borders, and dark gold `#725B1A` for legible links. Exams and
cheatsheets retain the dark identity. Do not infer a public Ravn light theme.

## Typography

Use Inter for headings and prose, with 600-weight display headings rather than the
previous 800-weight Work Sans. Use JetBrains Mono for code, question IDs, and
technical labels. Source homepage samples at desktop: H1 52px/600, H2 40px/600,
lead 24px/500, body 18px/400, and mono labels 14px/500.

Study adaptations use 16px body text, a 32–52px responsive landing heading, smaller
question headings, and 12px utility labels. Keep paragraphs at approximately
65–70 characters and line height around 1.6. Balance headings and wrap long paths,
URLs, and identifiers without widening mobile pages.

`docs/assets/fonts.css` embeds the source website's Latin variable-font subsets,
including Spanish and Portuguese characters. The site links this local stylesheet;
standalone exam and cheatsheet generators inline it so downloaded pages retain
their typography. Font licenses accompany it in `docs/assets/`.

## Layout

Keep the existing three-track chooser and navigation. Use a 980px study content
container, a 70ch prose measure, generous section spacing, and compact quiz controls.
On phones, stack navigation as needed and allow prose containers to shrink. Preserve
the incoming mobile fixes: wrapping fenced code and URLs, zero-minimum grid tracks,
and a wrapping Previous / Next / Finish row.

## Elevation & Depth

Separate surfaces with subtle tonal steps and thin borders. A faint cool radial
wash may sit behind the landing introduction, echoing the public site's atmospheric
hero. Keep reading and answer surfaces quiet. Avoid conspicuous shadows and the old
gold dot-matrix decoration. Content must be visible immediately without scroll reveals.

## Shapes

Use 8px control corners, 4px small tags, and 18px site cards, reflecting the source's
control and surface radii. Dense quiz answer options retain their compact 8px shape.
Do not apply pill geometry to every control.

## Components

- **Header:** white Ravn wordmark, restrained site label, simple search/theme controls.
- **Primary action:** white background, dark label, 8px radius, visible focus state.
- **Secondary action:** transparent or subtly elevated surface with a neutral border.
- **Track chooser:** all three exams as equal-width peers in one grid, each card
  carrying the exam name, who it is for, exam code / item count / languages, and a
  single primary action. The per-language resource matrix sits behind a collapsed
  disclosure so tracks with four materials and six materials keep the same height;
  registration is a quiet tertiary link, below the free material this site ships.
- **Question bank:** stable question numbers, readable stems, compact metadata,
  expandable answers, and text search. Preserve exact-number search such as `#42`.
- **Quiz:** selection and correctness remain visually distinct; feedback includes text.
- **Guide:** readable prose, a responsive contents panel, wrapping code, and localized navigation.

## Do's and Don'ts

- Use the current Inter/JetBrains pairing and measured neutral palette.
- Keep all three exam blueprints, language variants, scoring, and saved progress intact.
- Keep ordinary scrolling and visible keyboard focus; honor reduced-motion preferences.
- Use accent color sparingly. Do not recolor the whole headline gold.
- Do not restore Work Sans, Source Code Pro, or the old champagne-gold dot motif.
- Do not copy marketing animations into the study flow or hide content until scrolling.
- Regenerate all exam, bank, and cheatsheet HTML after changing their source styles.
