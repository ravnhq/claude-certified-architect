#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import MiniSearch from 'minisearch';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const DOCS = path.join(ROOT, 'docs');

const LANGS = [
  { code: 'en', label: 'English',    guide: 'guide_en.MD',  test: 'exam_en.html' },
  { code: 'es', label: 'Español',    guide: 'guide_es.md',  test: 'exam_es.html' },
  { code: 'pt', label: 'Português',  guide: 'guide_pt.md',  test: 'exam_pt.html' },
];

const PROFESSIONAL_GUIDES = [
  {
    code: 'en',
    label: 'English',
    title: 'Professional - English',
    guide: 'professional_en.md',
    output: 'professional-en',
    test: 'professional_exam_en.html',
  },
];

const DEVELOPER_GUIDES = [
  {
    code: 'en',
    label: 'English',
    title: 'Developer - English',
    guide: 'developer_en.md',
    output: 'developer-en',
    test: 'developer_exam_en.html',
  },
];

const RAVN_BASE_HREF = process.env.RAVN_BASE_HREF || '/claude-certified-architect/';
const MINISEARCH_BROWSER = path.resolve(
  path.dirname(fileURLToPath(import.meta.resolve('minisearch'))),
  '../umd/index.js',
);

// Official RAVN wordmark — inlined so `fill: currentColor` follows the theme
// (white on the dark canvas, near-black on the light variant).
const RAVN_LOGO = '<svg viewBox="0 0 148 33" role="img" aria-label="Ravn"><path d="M147.001 0.000976562H139.097V21.1196L120.763 0.00198534H112.859V32.9979H120.763V11.8853L139.095 33.001L139.098 32.9979H147.001V0.000976562Z"/><path d="M94.3156 33H85.8811L73.0273 0H81.4608L90.0978 22.1056L98.7348 0H107.169L94.3156 33Z"/><path d="M64.4406 0H56.0061L43.1523 33H51.5868L60.2238 10.8934L68.8598 33H77.2943L64.4406 0Z"/><path d="M28.8517 22.5101C33.8779 21.1825 37.5735 16.7376 37.5735 11.4583C37.5735 5.23989 32.4481 0.178564 26.0589 0.00605301V0H7.64995H0L6.34956 7.63688H7.64995V7.6389H25.7781C27.9333 7.66916 29.671 9.36703 29.671 11.4573C29.671 13.5668 27.902 15.2768 25.7197 15.2768H22.8382H12.7002L27.4355 33H37.5724L28.8517 22.5101Z"/><path d="M8.53644 32.9974C11.4172 32.9974 13.7526 30.7402 13.7526 27.9557C13.7526 25.1713 11.4172 22.9141 8.53644 22.9141C5.65565 22.9141 3.32031 25.1713 3.32031 27.9557C3.32031 30.7402 5.65565 32.9974 8.53644 32.9974Z"/></svg>';

let headingSlug = createSlugger();

marked.use({
  useNewRenderer: true,
  renderer: {
    heading({ tokens, depth }) {
      const raw = tokens.map(t => t.raw ?? t.text ?? '').join('');
      const id = headingSlug(raw);
      const inner = this.parser.parseInline(tokens);
      return `<h${depth} id="${id}">${inner}</h${depth}>\n`;
    },
  },
});

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

async function ensureDir(p) { await fs.mkdir(p, { recursive: true }); }

function pageShell({ title, lang, body, baseHref }) {
  return `<!doctype html>
<html lang="${lang}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<base href="${baseHref}">
<link rel="stylesheet" href="styles.css">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;800&family=Source+Code+Pro:wght@400;600&display=swap">
<script>
  // theme bootstrap (no FOUC) — defaults to dark, matches Ravn's identity
  (() => {
    const t = localStorage.getItem('theme');
    document.documentElement.dataset.theme = t || 'dark';
  })();
</script>
</head>
<body>
${body}
${siteFooter()}
<script src="vendor/minisearch.js" defer></script>
<script src="app.js" defer></script>
</body>
</html>`;
}

function siteFooter() {
  return `<footer class="site-footer">
  <p>© Ravn</p>
  <p><a href="https://www.ravn.co/">ravn.co</a></p>
</footer>`;
}

function header(_currentLang) {
  return `<header class="topbar">
  <a class="brand" href="index.html" aria-label="Ravn — Claude Certified Architect">
    ${RAVN_LOGO}
    <span>Claude Certified Architect</span>
  </a>
  <nav class="topbar-actions" aria-label="Page controls">
    <button type="button" id="search-toggle" class="icon-btn" aria-label="Search">⌕</button>
    <button type="button" id="theme-toggle" class="icon-btn" aria-label="Toggle theme">◐</button>
  </nav>
</header>
<dialog id="search-dialog" aria-labelledby="search-title">
  <h2 id="search-title" class="visually-hidden">Search the study guides</h2>
  <div class="search-filter" role="group" aria-label="Filter by language">
    <button type="button" class="search-lang active" data-lang="all" aria-pressed="true">All</button>
    <button type="button" class="search-lang" data-lang="en" aria-pressed="false">EN</button>
    <button type="button" class="search-lang" data-lang="es" aria-pressed="false">ES</button>
    <button type="button" class="search-lang" data-lang="pt" aria-pressed="false">PT</button>
  </div>
  <label class="visually-hidden" for="search-input">Search terms</label>
  <input id="search-input" type="search" placeholder="Search the guide…" autocomplete="off">
  <p id="search-status" class="search-status" role="status" aria-live="polite"></p>
  <ul id="search-results" aria-label="Search results"></ul>
</dialog>`;
}

function landing() {
  const foundationCards = LANGS.map(l => `
    <article class="card" data-lang="${l.code}">
      <h2>${l.code.toUpperCase()}</h2>
      <div class="lang-name">${l.label}</div>
      <ul>
        <li><a href="guides/${l.code}.html">Read the guide</a></li>
        <li><a href="practical/${l.code}.html">Practice exam</a></li>
        <li><a href="cheatsheet/${l.code}.html">Cheatsheet</a></li>
        <li><a href="pdf/guide_${l.code}.pdf">PDF download</a></li>
      </ul>
    </article>`).join('');
  const professionalCards = PROFESSIONAL_GUIDES.map(l => `
    <article class="card" data-lang="${l.code}">
      <h2>${l.code.toUpperCase()}</h2>
      <div class="lang-name">${l.label}</div>
      <p class="card-summary">Seven-domain guidance for production architecture, integration, evaluation, governance, and lifecycle leadership.</p>
      <ul>
        <li><a href="guides/${l.output}.html">Read the study guide</a></li>
        <li><a href="practical/${l.output}.html">Practice exam (63 questions)</a></li>
        <li><a href="https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification">Official registration</a></li>
      </ul>
    </article>`).join('');
  const developerCards = DEVELOPER_GUIDES.map(l => `
    <article class="card" data-lang="${l.code}">
      <h2>${l.code.toUpperCase()}</h2>
      <div class="lang-name">${l.label}</div>
      <p class="card-summary">Build, integrate, and ship production applications, agents, and workflows on Claude at a foundational level.</p>
      <ul>
        <li><a href="guides/${l.output}.html">Read the study guide</a></li>
        <li><a href="https://anthropic-partners.skilljar.com/claude-certified-developer-foundations-certification">Official registration</a></li>
      </ul>
    </article>`).join('');

  // Track chooser — a one-glance self-selection grid placed above the
  // per-track sections. The two Architect exams are grouped as a progression
  // (Foundations then Professional); Developer is set apart as a separate
  // role. Each card carries the credential, exam code, audience, the hard
  // facts that differentiate the tracks (item count + available languages),
  // what Ravn ships for it, and a single link into that track's section.
  const chooserArchitectCards = `
    <article class="card chooser-card">
      <p class="chooser-code">CCAR-F</p>
      <h2 class="chooser-name">Architect — Foundations</h2>
      <p class="card-summary">For practitioners building with Claude Code, the Agent SDK, the Claude API, and MCP.</p>
      <dl class="chooser-facts">
        <div class="chooser-fact"><dt class="chooser-fact-k">Items</dt><dd class="chooser-fact-v">60</dd></div>
        <div class="chooser-fact"><dt class="chooser-fact-k">Languages</dt><dd class="chooser-fact-v">EN · ES · PT</dd></div>
      </dl>
      <p class="chooser-includes">Study guide, practice exam, and cheatsheet, each in English, Spanish, and Portuguese.</p>
      <a class="chooser-link" href="#track-foundations">Start with Foundations</a>
      <a class="chooser-link" href="preflight/architect-foundations.html">Preflight checklist</a>
    </article>
    <article class="card chooser-card">
      <p class="chooser-code">CCAR-P</p>
      <h2 class="chooser-name">Architect — Professional</h2>
      <p class="card-summary">For architects owning production architecture, evaluation, governance, and lifecycle.</p>
      <dl class="chooser-facts">
        <div class="chooser-fact"><dt class="chooser-fact-k">Items</dt><dd class="chooser-fact-v">63</dd></div>
        <div class="chooser-fact"><dt class="chooser-fact-k">Languages</dt><dd class="chooser-fact-v">EN</dd></div>
      </dl>
      <p class="chooser-includes">Study guide, plus a practice exam drawing 63 questions from a bank of 126.</p>
      <a class="chooser-link" href="#track-professional">Go to Professional</a>
      <a class="chooser-link" href="preflight/architect-professional.html">Preflight checklist</a>
    </article>`;
  const chooserDeveloperCard = `
    <article class="card chooser-card">
      <p class="chooser-code">CCDV-F</p>
      <h2 class="chooser-name">Developer — Foundations</h2>
      <p class="card-summary">For engineers building and shipping production applications, agents, and workflows.</p>
      <dl class="chooser-facts">
        <div class="chooser-fact"><dt class="chooser-fact-k">Items</dt><dd class="chooser-fact-v">53</dd></div>
        <div class="chooser-fact"><dt class="chooser-fact-k">Languages</dt><dd class="chooser-fact-v">EN</dd></div>
      </dl>
      <p class="chooser-includes">Study guide and a practice exam drawing 53 questions from a bank of 106.</p>
      <a class="chooser-link" href="#track-developer">Go to Developer</a>
      <a class="chooser-link" href="preflight/developer-foundations.html">Preflight checklist</a>
    </article>`;

  return `<main class="landing">
  <section class="hero">
    <p class="eyebrow">Ravn study materials</p>
    <h1>Claude Certified Architect <span class="accent">— choose your track.</span></h1>
    <p class="lede">Study guides, practice exams, and cheatsheets for the Claude certification exams — free, open, and in three languages wherever the exam is offered in three languages.</p>
  </section>
  <section class="track-chooser" aria-labelledby="chooser-title">
    <div class="track-heading">
      <p class="track-label">Choose your track</p>
      <h2 id="chooser-title">Three exams, two roles</h2>
      <p>Architect runs Foundations then Professional, so the second builds on the first. Developer Foundations sits alongside them — a different job, not a further level.</p>
    </div>
    <div class="chooser-group">
      <p class="chooser-role">Architect</p>
      <div class="cards chooser-cards">${chooserArchitectCards}</div>
    </div>
    <div class="chooser-group">
      <p class="chooser-role">Developer</p>
      <div class="cards chooser-cards">${chooserDeveloperCard}</div>
    </div>
  </section>
  <section class="track">
    <div class="track-heading">
      <p class="track-label">Before you book</p>
      <h2>Check that you are ready</h2>
      <p>One checklist per exam: ten checks, that exam's blueprint, and the practice material that exists for it — a retake costs the full fee and a 14-day wait.</p>
    </div>
    <div class="cards">
      <article class="card">
        <h2>CCAR-F</h2>
        <div class="lang-name">Preflight</div>
        <p class="card-summary">A saved checklist you work through before you book an Architect &mdash; Foundations slot.</p>
        <ul>
          <li><a href="preflight/architect-foundations.html">Open the checklist</a></li>
        </ul>
      </article>
      <article class="card">
        <h2>CCAR-P</h2>
        <div class="lang-name">Preflight</div>
        <p class="card-summary">A saved checklist you work through before you book an Architect &mdash; Professional slot.</p>
        <ul>
          <li><a href="preflight/architect-professional.html">Open the checklist</a></li>
        </ul>
      </article>
      <article class="card">
        <h2>CCDV-F</h2>
        <div class="lang-name">Preflight</div>
        <p class="card-summary">A saved checklist you work through before you book a Developer &mdash; Foundations slot.</p>
        <ul>
          <li><a href="preflight/developer-foundations.html">Open the checklist</a></li>
        </ul>
      </article>
    </div>
  </section>
  <section class="track" id="track-foundations">
    <div class="track-heading">
      <p class="track-label">Architect — Foundations · CCAR-F</p>
      <h2>Pick your language</h2>
      <p>The five-domain Foundations certification in English, Spanish, or Portuguese — guide, practice exam, and cheatsheet for each.</p>
    </div>
    <div class="cards">${foundationCards}</div>
  </section>
  <section class="track" id="track-professional">
    <div class="track-heading">
      <p class="track-label">Architect — Professional · CCAR-P</p>
      <h2>Own the production architecture</h2>
      <p>Guidance for the seven-domain CCAR-P blueprint, effective July 2026.</p>
    </div>
    <div class="cards cards-single">${professionalCards}</div>
  </section>
  <section class="track" id="track-developer">
    <div class="track-heading">
      <p class="track-label">Developer — Foundations · CCDV-F</p>
      <h2>Build and ship on Claude</h2>
      <p>Guidance for the eight-domain Developer – Foundations blueprint (CCDV-F).</p>
    </div>
    <div class="cards cards-single">${developerCards}</div>
  </section>
</main>`;
}

// ---------- preflight checklist ----------

// One entry per certification track. Each drives a standalone checklist page:
// its own facts, blueprint, items, resources, and localStorage key, rendered
// through the shared preflight() below. `files` lists every filename the page
// is written to — Foundations also answers to the original `en.html`, which
// the README and the landing page have always linked.
const PREFLIGHT_TRACKS = [
  {
    slug: 'architect-foundations',
    files: ['architect-foundations.html', 'en.html'],
    storageKey: 'ccaf-preflight:state',
    title: 'Preflight checklist — Claude Certified Architect – Foundations · Ravn',
    eyebrow: 'Architect &mdash; Foundations &middot; CCAR-F',
    heading: 'Ten checks before <span class="accent">you book the slot.</span>',
    lede: 'Retakes wait 14, then 30, then 90 days &mdash; four attempts maximum per year, $125 each. Tick what is true and see what is left.',
    scope: 'This checklist is for <strong>Architect &mdash; Foundations</strong> only. <a href="preflight/architect-professional.html">Architect &mdash; Professional</a> and <a href="preflight/developer-foundations.html">Developer &mdash; Foundations</a> are separate exams with their own blueprints, so the domains and prep courses below do not carry over.',
    note: 'Multiple-choice <em>and</em> multiple-response. 4 scenarios drawn from a bank of 6. Delivered by Pearson VUE — OnVUE at home or a test centre.',
    facts: [
      { k: 'Code', v: 'CCAR-F' },
      { k: 'Questions', v: '60' },
      { k: 'Time', v: '120 min' },
      { k: 'Pass', v: '720 / 1000' },
      { k: 'Fee', v: '$125' },
      { k: 'Valid', v: '12 months' },
    ],
    domains: [
      { n: '01', name: 'Agentic Architecture &amp; Orchestration', weight: 27 },
      { n: '02', name: 'Tool Design &amp; MCP Integration', weight: 18 },
      { n: '03', name: 'Claude Code Configuration &amp; Workflows', weight: 20 },
      { n: '04', name: 'Prompt Engineering &amp; Structured Output', weight: 20 },
      { n: '05', name: 'Context Management &amp; Reliability', weight: 15 },
    ],
    items: [
      {
        n: '01',
        label: 'Prep courses that carry weight',
        detail: `Seven exist, none required. Highest yield: <strong>Claude Code in Action</strong> (Domain 3), <strong>Intro to MCP</strong> (Domain 2), <strong>Building with the Claude API</strong> (Domains 2 and 4). Skim the rest. ${extLink('https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses', 'Courses')}`,
      },
      {
        n: '02',
        label: 'Bonus courses done',
        detail: `Off the prep page, on the blueprint: ${extLink('https://anthropic-partners.skilljar.com/introduction-to-subagents', 'Introduction to subagents')} (Domain 1) and ${extLink('https://anthropic-partners.skilljar.com/model-context-protocol-advanced-topics', 'MCP: Advanced Topics')} (Domain 2).`,
      },
      {
        n: '03',
        label: 'Read the exam guide end-to-end',
        detail: `v1.0, July 2026. Source of truth. Not skimmed. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification', 'Official guide')} · <a href="guides/en.html">Ravn study guide</a>`,
      },
      {
        n: '04',
        label: 'Can name and explain all 5 domains',
        detail: 'Without notes. Use the blueprint above to self-check.',
      },
      {
        n: '05',
        label: 'Worked the official sample questions',
        detail: `The self-service practice exam is retired. What remains: the guide&rsquo;s samples, plus a graded quiz ending every prep course that reveals its answer key once you pass. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification', 'Get the guide')}`,
      },
      {
        n: '06',
        label: 'Worked through community mocks',
        detail: 'With the official mock gone, these carry more weight. Full list in Resources below.',
      },
      {
        n: '07',
        label: 'Registered and slot booked',
        detail: `Pay in Partner Academy, then schedule in Pearson VUE with the emailed credentials. Reschedule 24h+ ahead or forfeit the fee. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification', 'Register')}`,
      },
      {
        n: '08',
        label: 'OnVUE system test passed',
        detail: `On the actual machine and network you will use. Webcam, mic, and OnVUE domains reachable. ${extLink('https://www.pearsonvue.com/us/en/anthropic.html', 'Pearson VUE')}`,
      },
      {
        n: '09',
        label: 'Workspace ready',
        detail: 'Government photo ID matching your registration name. Quiet room, no second monitor, phone away.',
      },
      {
        n: '10',
        label: 'You would expect to pass right now',
        detail: 'Not hope. Expect.',
      },
    ],
    resources: [
      {
        group: 'Ravn materials',
        items: [
          { name: 'Study guide', href: 'guides/en.html', note: 'The full Foundations guide.', internal: true },
          { name: 'Practice exam', href: 'practical/en.html', note: '60 questions drawn from a bank of 136, scored to 1000.', internal: true },
          { name: 'Cheatsheet', href: 'cheatsheet/en.html', note: 'One-page recap of the five domains.', internal: true },
        ],
      },
      {
        group: 'External practice',
        items: [
          {
            name: 'claudecertificationguide.com — diagnostic',
            href: 'https://claudecertificationguide.com/learn/diagnostic',
            note: 'Short. Use this to gauge readiness before the full mocks.',
          },
          {
            name: 'claudecertificationguide.com — full mock',
            href: 'https://claudecertificationguide.com/mock-exam',
            note: 'Full-length community mock.',
          },
          {
            name: 'certsafari.com',
            href: 'https://www.certsafari.com/anthropic/claude-certified-architect',
            note: '614 questions, aligned to guide v1.0. Configurable.',
          },
          {
            name: 'claudecertifiedarchitects.com',
            href: 'https://www.claudecertifiedarchitects.com/',
            note: 'Free readiness diagnostic plus 400 scenario questions.',
          },
          {
            name: 'open-exam-prep.com',
            href: 'https://open-exam-prep.com/',
            note: 'Free CCAR-F questions aligned to v1.0.',
          },
          {
            name: 'daronyondem/claude-architect-exam-guide',
            href: 'https://github.com/daronyondem/claude-architect-exam-guide',
            note: 'Community study guide. PDF and EPUB builds.',
          },
          {
            name: 'OlivierAlter — practice exam + skill',
            href: 'https://github.com/OlivierAlter/Claude-Certified-Architect-Foundations-Certification-Exam',
            note: '77 scenario questions plus an interactive Claude Code skill.',
          },
          {
            name: 'krog.app',
            href: 'https://krog.app/exam/6a1a0c49ca96069990f7e8bc',
            note: '113 questions by domain.',
          },
        ],
      },
      {
        group: 'Video',
        items: [
          {
            name: 'CCAF study playlist',
            href: 'https://www.youtube.com/playlist?list=PLmiDJB5zE0KGwFtDCSqHfQG7SV6VeQ_31',
            note: 'Community-curated audiovisual material.',
          },
        ],
      },
    ],
  },
  {
    slug: 'architect-professional',
    files: ['architect-professional.html'],
    storageKey: 'ccarp-preflight:state',
    title: 'Preflight checklist — Claude Certified Architect – Professional · Ravn',
    eyebrow: 'Architect &mdash; Professional &middot; CCAR-P',
    heading: 'Ten checks before <span class="accent">you book the slot.</span>',
    lede: 'Retakes wait 14, then 30, then 90 days &mdash; four attempts maximum per year, $175 each. Tick what is true and see what is left.',
    scope: 'This checklist is for <strong>Architect &mdash; Professional</strong> only. <a href="preflight/architect-foundations.html">Architect &mdash; Foundations</a> and <a href="preflight/developer-foundations.html">Developer &mdash; Foundations</a> are separate exams with their own blueprints, so the domains and prep courses below do not carry over.',
    note: 'Multiple-choice <em>and</em> multiple-response; every item states how many responses to select. Closed book, English only. Delivered by Pearson VUE — online proctored or at a test centre.',
    facts: [
      { k: 'Code', v: 'CCAR-P' },
      { k: 'Questions', v: '63' },
      { k: 'Time', v: '120 min' },
      { k: 'Pass', v: '720 / 1000' },
      { k: 'Fee', v: '$175' },
      { k: 'Valid', v: '12 months' },
    ],
    domains: [
      { n: '01', name: 'Solution Design &amp; Architecture', weight: 17 },
      { n: '02', name: 'Claude Models, Prompting &amp; Context Engineering', weight: 13 },
      { n: '03', name: 'Integration', weight: 19 },
      { n: '04', name: 'Evaluation, Testing &amp; Optimization', weight: 16 },
      { n: '05', name: 'Governance, Safety &amp; Risk Management', weight: 14 },
      { n: '06', name: 'Stakeholder Communication &amp; Lifecycle Management', weight: 14 },
      { n: '07', name: 'Developer Productivity &amp; Operational Enablement', weight: 7 },
    ],
    items: [
      {
        n: '01',
        label: 'Official prep path finished',
        detail: `Five courses, about 12 hours. Not required, and the only material written against the Professional blueprint. ${extLink('https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional', 'Prep path')}`,
      },
      {
        n: '02',
        label: 'Read the exam guide end-to-end',
        detail: `Effective July 2026. Source of truth. Not skimmed. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification', 'Official guide')} · <a href="guides/professional-en.html">Ravn study guide</a>`,
      },
      {
        n: '03',
        label: 'Can name and explain all 7 domains',
        detail: 'Without notes. Integration and Solution Design carry 36% between them — budget your study by the weights above, not by what you enjoy.',
      },
      {
        n: '04',
        label: 'Worked the Ravn practice exam',
        detail: 'Under the 120-minute limit, then reviewed by failure type rather than topic. The community mocks listed for Foundations target CCAR-F, so they do not calibrate this exam. <a href="practical/professional-en.html">Practice exam</a>',
      },
      {
        n: '05',
        label: 'Eligibility confirmed',
        detail: 'Registration requires a recognised Claude Partner Network company email. Personal addresses are rejected, and adding a domain takes 7&ndash;10 days — start this before you plan a date.',
      },
      {
        n: '06',
        label: 'Can defend an end-to-end design out loud',
        detail: 'From a short business brief: the pattern you chose, the integration surface, how you would evaluate it, the controls, and the rollout — plus the trade-off each decision cost you.',
      },
      {
        n: '07',
        label: 'Registered and slot booked',
        detail: `Pay in Partner Academy, then schedule in Pearson VUE with the emailed credentials. Reschedule 24h+ ahead or forfeit the fee. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification', 'Register')}`,
      },
      {
        n: '08',
        label: 'OnVUE system test passed',
        detail: `On the actual machine and network you will use. Webcam, mic, and OnVUE domains reachable. Corporate networks often block them — a test centre is the safer fallback. ${extLink('https://www.pearsonvue.com/us/en/anthropic.html', 'Pearson VUE')}`,
      },
      {
        n: '09',
        label: 'Workspace ready',
        detail: 'Government photo ID matching your registration name. Quiet room, no second monitor, phone away. Allow about 135 minutes on site for a 120-minute exam.',
      },
      {
        n: '10',
        label: 'You would expect to pass right now',
        detail: 'Not hope. Expect.',
      },
    ],
    resources: [
      {
        group: 'Ravn materials',
        items: [
          { name: 'Study guide', href: 'guides/professional-en.html', note: 'The full Professional guide, English only.', internal: true },
          { name: 'Practice exam', href: 'practical/professional-en.html', note: '63 questions drawn from a bank of 126, scored to 1000.', internal: true },
        ],
      },
      {
        group: 'Official preparation',
        items: [
          {
            name: 'Professional prep path',
            href: 'https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional',
            note: 'Five courses, about 12 hours. Optional, and the only Professional-specific course material.',
          },
          {
            name: 'Certification and registration page',
            href: 'https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification',
            note: 'The exam guide and the checkout that unlocks Pearson VUE scheduling.',
          },
          {
            name: 'Certification FAQ',
            href: 'https://anthropic-partners.skilljar.com/page/faq-certifications',
            note: 'Eligibility, retakes, validity, proctoring, and badging.',
          },
          {
            name: 'Computer and network setup',
            href: 'https://anthropic-partners.skilljar.com/page/computer-and-network-setup',
            note: 'Read this before you book online proctoring.',
          },
        ],
      },
    ],
  },
  {
    slug: 'developer-foundations',
    files: ['developer-foundations.html'],
    storageKey: 'ccdvf-preflight:state',
    title: 'Preflight checklist — Claude Certified Developer – Foundations · Ravn',
    eyebrow: 'Developer &mdash; Foundations &middot; CCDV-F',
    heading: 'Ten checks before <span class="accent">you book the slot.</span>',
    lede: 'Retakes wait 14, then 30, then 90 days &mdash; four attempts maximum per year, $125 each. Tick what is true and see what is left.',
    scope: 'This checklist is for <strong>Developer &mdash; Foundations</strong> only. <a href="preflight/architect-foundations.html">Architect &mdash; Foundations</a> and <a href="preflight/architect-professional.html">Architect &mdash; Professional</a> are separate exams with their own blueprints, so the domains and prep courses below do not carry over.',
    note: 'Multiple-choice <em>and</em> multiple-response; every item states how many responses to select. Closed book, English only. Delivered by Pearson VUE — online proctored or at a test centre.',
    facts: [
      { k: 'Code', v: 'CCDV-F' },
      { k: 'Questions', v: '53' },
      { k: 'Time', v: '120 min' },
      { k: 'Pass', v: '720 / 1000' },
      { k: 'Fee', v: '$125' },
      { k: 'Valid', v: '12 months' },
    ],
    domains: [
      // Quoted so a whole-number weight keeps the blueprint's decimal — 11.0,
      // not 11 — next to the seven fractional rows.
      { n: '01', name: 'Agents and Workflows', weight: '14.7' },
      { n: '02', name: 'Applications and Integration', weight: '33.1' },
      { n: '03', name: 'Claude Code', weight: '3.1' },
      { n: '04', name: 'Eval, Testing and Debugging', weight: '2.6' },
      { n: '05', name: 'Model Selection and Optimization', weight: '16.8' },
      { n: '06', name: 'Prompt and Context Engineering', weight: '11.0' },
      { n: '07', name: 'Security and Safety', weight: '8.1' },
      { n: '08', name: 'Tools and MCPs', weight: '10.6' },
    ],
    items: [
      {
        n: '01',
        label: 'Official prep path finished',
        detail: `Five modules, about 12 hours 40 minutes. Not required, and the only material written against the Developer blueprint. ${extLink('https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations', 'Prep path')}`,
      },
      {
        n: '02',
        label: 'Read the exam guide end-to-end',
        detail: `v1.0, effective July 2026. Source of truth. Not skimmed. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-developer-foundations-certification', 'Official guide')} · <a href="guides/developer-en.html">Ravn study guide</a>`,
      },
      {
        n: '03',
        label: 'Can name and explain all 8 domains',
        detail: 'Without notes. Applications and Integration alone is a third of the exam, while Claude Code and Eval together are under 6% — study to the weights above, not to the course hours.',
      },
      {
        n: '04',
        label: 'Worked the official sample questions',
        detail: 'Three items with full rationale in Section 8 of the exam guide. Read them in the source: the answer key is the clearest signal available about how items are built.',
      },
      {
        n: '05',
        label: 'Practice material worked through',
        detail: 'Draw a full 53-question set from the <a href="practical/developer-en.html">Developer practice exam</a> under time. The CCAR-F exam is a different blueprint — do not substitute it. No cheatsheet ships for this track yet.',
      },
      {
        n: '06',
        label: 'Built it, not just read it',
        detail: 'One reference application you wrote yourself: the agent loop, a tool schema, a consumed stream, batch and caching, and a trace you read to find a failing step.',
      },
      {
        n: '07',
        label: 'Registered and slot booked',
        detail: `Pay in Partner Academy, then schedule in Pearson VUE with the emailed credentials. Reschedule 24h+ ahead or forfeit the fee — a no-show forfeits it too. ${extLink('https://anthropic-partners.skilljar.com/claude-certified-developer-foundations-certification', 'Register')}`,
      },
      {
        n: '08',
        label: 'OnVUE system test passed',
        detail: `On the actual machine and network you will use. Webcam, mic, and OnVUE domains reachable. Corporate networks often block them — a test centre is the safer fallback. ${extLink('https://www.pearsonvue.com/us/en/anthropic.html', 'Pearson VUE')}`,
      },
      {
        n: '09',
        label: 'Workspace ready',
        detail: 'Government photo ID matching your registration name, exactly. Quiet room, no second monitor, phone away. You must accept the non-disclosure agreement before the exam starts; declining ends the session with no refund.',
      },
      {
        n: '10',
        label: 'You would expect to pass right now',
        detail: 'Not hope. Expect.',
      },
    ],
    resources: [
      {
        group: 'Ravn materials',
        items: [
          { name: 'Study guide', href: 'guides/developer-en.html', note: 'The full Developer guide, English only.', internal: true },
        { name: 'Practice exam', href: 'practical/developer-en.html', note: '53 questions drawn from a bank of 106, weighted to the eight domains and scored to 1000.', internal: true },
        ],
      },
      {
        group: 'Official preparation',
        items: [
          {
            name: 'Developer prep path',
            href: 'https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations',
            note: 'Five modules, about 12 hours 40 minutes. Organised by topic, not by domain.',
          },
          {
            name: 'Certification and registration page',
            href: 'https://anthropic-partners.skilljar.com/claude-certified-developer-foundations-certification',
            note: 'The exam guide and the checkout that unlocks Pearson VUE scheduling.',
          },
          {
            name: 'Certification FAQ',
            href: 'https://anthropic-partners.skilljar.com/page/faq-certifications',
            note: 'Eligibility, retakes, validity, proctoring, and badging.',
          },
          {
            name: 'Computer and network setup',
            href: 'https://anthropic-partners.skilljar.com/page/computer-and-network-setup',
            note: 'Read this before you book online proctoring.',
          },
        ],
      },
    ],
  },
];

function extLink(href, text) {
  return `<a href="${href}" target="_blank" rel="noopener noreferrer">${text} →</a>`;
}

const CHECK_SVG = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

function preflightStyles() {
  return `<style>
.preflight { max-width: var(--max); margin: 0 auto; padding: 56px 32px 24px; }
.preflight .hero { margin-bottom: 0; }
.pf-headline { display: grid; grid-template-columns: 1fr auto; gap: 32px; align-items: end; }
.pf-count { text-align: right; line-height: 1; }
.pf-count .pf-count-n { font-size: clamp(3.4rem, 9vw, 5.6rem); font-weight: 800; color: var(--fg); font-variant-numeric: tabular-nums; }
.pf-count .pf-count-n.done { color: var(--accent); }
.pf-count .pf-count-label { display: block; margin-top: 6px; font-family: 'Source Code Pro', monospace; font-size: 0.66rem; letter-spacing: 0.167em; text-transform: uppercase; color: var(--subtle); }
.pf-scope { max-width: 68ch; margin: 0; padding: 12px 14px; border-left: 2px solid var(--accent); background: var(--bg-elev); font-size: 0.84rem; line-height: 1.6; color: var(--muted); }
.pf-scope a { color: var(--accent); }
.pf-dots { display: flex; gap: 8px; margin: 28px 0 36px; }
.pf-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--border-strong); transition: background .25s var(--ease); }
.pf-dot.on { background: var(--accent); }

.pf-panel { border: 1px solid var(--border); padding: 22px 24px; margin-bottom: 36px; }
.pf-eyebrow { font-family: 'Source Code Pro', monospace; font-size: 0.68rem; letter-spacing: 0.167em; text-transform: uppercase; color: var(--subtle); margin: 0 0 16px; }
.pf-facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(132px, 1fr)); border: 1px solid var(--border); border-radius: var(--radius-sm); overflow: hidden; margin-bottom: 22px; }
.pf-fact { display: grid; gap: 7px; padding: 14px 16px; border-right: 1px solid var(--border); }
.pf-fact:last-child { border-right: 0; }
.pf-fact-k { font-family: 'Source Code Pro', monospace; font-size: 0.62rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--subtle); }
.pf-fact-v { font-family: 'Source Code Pro', monospace; font-size: 0.95rem; color: var(--fg); font-weight: 600; }
.pf-note { font-size: 0.82rem; color: var(--muted); line-height: 1.55; margin: 0 0 18px; }
.pf-domains { display: grid; gap: 18px; }
.pf-domain-head { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; margin-bottom: 6px; }
.pf-domain-name { display: flex; gap: 14px; align-items: baseline; min-width: 0; }
.pf-domain-n { font-family: 'Source Code Pro', monospace; font-size: 0.72rem; color: var(--subtle); flex-shrink: 0; }
.pf-domain-w { font-family: 'Source Code Pro', monospace; font-size: 0.88rem; color: var(--accent); font-weight: 600; flex-shrink: 0; }
.pf-bar { height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
.pf-bar span { display: block; height: 100%; background: var(--accent); border-radius: 2px; }

.pf-list { border-top: 1px solid var(--border); }
.pf-row { display: grid; grid-template-columns: 34px 22px 1fr; gap: 18px; align-items: start; padding: 20px 14px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background .2s var(--ease); position: relative; }
.pf-row:hover { background: var(--bg-elev); }
.pf-row:has(.pf-check:checked) { background: color-mix(in srgb, var(--accent) 7%, transparent); }
.pf-check { position: absolute; opacity: 0; width: 1px; height: 1px; margin: 0; }
.pf-n { font-family: 'Source Code Pro', monospace; font-size: 0.85rem; padding-top: 2px; letter-spacing: 0.05em; color: var(--subtle); transition: color .25s var(--ease); }
.pf-row:has(.pf-check:checked) .pf-n { color: var(--accent); }
.pf-box { width: 22px; height: 22px; margin-top: 1px; border: 1.5px solid var(--border-strong); border-radius: 4px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: transparent; transition: background .18s var(--ease), border-color .18s var(--ease); }
.pf-row:hover .pf-box { border-color: var(--fg); }
.pf-row:has(.pf-check:checked) .pf-box { background: var(--accent); border-color: var(--accent); color: var(--accent-fg); }
.pf-row:has(.pf-check:focus-visible) .pf-box { outline: 2px solid var(--accent); outline-offset: 3px; }
.pf-item-label { display: block; font-size: 0.98rem; font-weight: 600; color: var(--fg); margin-bottom: 5px; }
.pf-item-detail { display: block; max-width: 72ch; font-size: 0.85rem; color: var(--muted); line-height: 1.6; }
.pf-item-detail a { color: var(--accent); }

.pf-actions { margin-top: 24px; }
.pf-reset { background: transparent; color: var(--muted); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 11px 18px; font: inherit; font-size: 0.76rem; letter-spacing: 0.06em; text-transform: uppercase; cursor: pointer; transition: color .15s var(--ease), border-color .15s var(--ease); }
.pf-reset:hover { color: var(--fg); border-color: var(--border-strong); }

.pf-resources { margin-top: 40px; border: 1px solid var(--border); }
.pf-resources > summary { padding: 14px 18px; cursor: pointer; display: flex; align-items: center; gap: 14px; color: var(--muted); font-size: 0.88rem; list-style: none; }
.pf-resources > summary::-webkit-details-marker { display: none; }
.pf-resources > summary::after { content: "▾"; margin-left: auto; color: var(--subtle); transition: transform .2s var(--ease); }
.pf-resources[open] > summary::after { transform: rotate(180deg); }
.pf-resources > summary:hover { background: var(--bg-elev); color: var(--fg); }
.pf-resources > summary .pf-eyebrow { margin: 0; }
.pf-resource-body { padding: 4px 24px 24px; display: grid; gap: 24px; }
.pf-resource-group > .pf-eyebrow { color: var(--accent); margin-bottom: 14px; }
.pf-resource-items { display: grid; gap: 14px; }
.pf-resource-items a { color: var(--accent); }
.pf-resource-note { font-size: 0.85rem; color: var(--muted); margin-top: 4px; line-height: 1.5; }

@media (max-width: 640px) {
  .preflight { padding: 40px 20px 16px; }
  .pf-headline { grid-template-columns: 1fr; align-items: start; }
  .pf-count { text-align: left; }
  .pf-row { grid-template-columns: 28px 22px 1fr; gap: 12px; padding: 16px 4px; }
  .pf-facts { grid-template-columns: repeat(2, 1fr); }
  .pf-fact { border-bottom: 1px solid var(--border); }
  .pf-fact:nth-child(odd) { border-right: 1px solid var(--border); }
  .pf-fact:nth-last-child(-n+2) { border-bottom: 0; }
}
</style>`;
}


function preflightScript(track) {
  return `<script>
(() => {
  const KEY = '${track.storageKey}';
  const boxes = [...document.querySelectorAll('.pf-check')];
  const dotFor = n => document.querySelector('.pf-dot[data-n="' + n + '"]');
  const counter = document.getElementById('pf-remaining');
  const total = boxes.length;

  const read = () => {
    try {
      const raw = localStorage.getItem(KEY);
      const data = raw ? JSON.parse(raw) : null;
      return new Set(Array.isArray(data && data.checked) ? data.checked : []);
    } catch (err) {
      return new Set();
    }
  };
  const write = () => {
    try {
      const checked = boxes.filter(b => b.checked).map(b => b.dataset.n);
      localStorage.setItem(KEY, JSON.stringify({ checked }));
    } catch (err) { /* private mode — in-session state still works */ }
  };
  const render = () => {
    const done = boxes.filter(b => b.checked).length;
    counter.textContent = String(total - done).padStart(2, '0');
    counter.classList.toggle('done', done === total);
    boxes.forEach(b => {
      const dot = dotFor(b.dataset.n);
      if (dot) dot.classList.toggle('on', b.checked);
    });
  };

  const saved = read();
  boxes.forEach(b => { b.checked = saved.has(b.dataset.n); });
  render();

  boxes.forEach(b => b.addEventListener('change', () => { write(); render(); }));

  const reset = document.getElementById('pf-reset');
  if (reset) reset.addEventListener('click', () => {
    boxes.forEach(b => { b.checked = false; });
    try { localStorage.removeItem(KEY); } catch (err) {}
    render();
  });
})();
<\/script>`;
}

function preflight(track) {
  const facts = track.facts.map(f => `
        <div class="pf-fact"><span class="pf-fact-k">${f.k}</span><span class="pf-fact-v">${f.v}</span></div>`).join('');
  const domains = track.domains.map(d => `
        <div>
          <div class="pf-domain-head">
            <span class="pf-domain-name"><span class="pf-domain-n">${d.n}</span><span>${d.name}</span></span>
            <span class="pf-domain-w">${d.weight}%</span>
          </div>
          <div class="pf-bar"><span style="width:${d.weight}%"></span></div>
        </div>`).join('');
  const dots = track.items.map(i => `<span class="pf-dot" data-n="${i.n}"></span>`).join('');
  const rows = track.items.map(i => `
      <label class="pf-row">
        <input type="checkbox" class="pf-check" data-n="${i.n}" autocomplete="off">
        <span class="pf-n">${i.n}</span>
        <span class="pf-box">${CHECK_SVG}</span>
        <span>
          <span class="pf-item-label">${i.label}</span>
          <span class="pf-item-detail">${i.detail}</span>
        </span>
      </label>`).join('');
  const resources = track.resources.map(g => `
        <div class="pf-resource-group">
          <p class="pf-eyebrow">${g.group}</p>
          <div class="pf-resource-items">${g.items.map(item => `
            <div>
              ${item.internal ? `<a href="${item.href}">${item.name}</a>` : extLink(item.href, item.name)}
              <div class="pf-resource-note">${item.note}</div>
            </div>`).join('')}
          </div>
        </div>`).join('');

  return `${preflightStyles()}
<main class="preflight">
  <section class="hero">
    <div class="pf-headline">
      <div style="display:grid;gap:16px">
        <p class="eyebrow">${track.eyebrow}</p>
        <h1>${track.heading}</h1>
        <p class="lede">${track.lede}</p>
        <p class="pf-scope">${track.scope}</p>
      </div>
      <div class="pf-count">
        <div class="pf-count-n" id="pf-remaining">${String(track.items.length).padStart(2, '0')}</div>
        <span class="pf-count-label">Left</span>
      </div>
    </div>
    <div class="pf-dots">${dots}</div>
  </section>

  <section class="pf-panel" aria-labelledby="pf-blueprint">
    <p class="pf-eyebrow" id="pf-blueprint">Exam blueprint</p>
    <div class="pf-facts">${facts}
    </div>
    <p class="pf-note">${track.note}</p>
    <div class="pf-domains">${domains}
    </div>
  </section>

  <section class="pf-list" aria-label="Readiness checklist">${rows}
  </section>

  <div class="pf-actions">
    <button type="button" id="pf-reset" class="pf-reset">Reset checklist</button>
  </div>

  <details class="pf-resources">
    <summary><span class="pf-eyebrow">Resources</span><span>Practice mocks and study materials</span></summary>
    <div class="pf-resource-body">${resources}
    </div>
  </details>
</main>
${preflightScript(track)}`;
}

async function buildPreflight() {
  const out = path.join(DOCS, 'preflight');
  await ensureDir(out);
  for (const track of PREFLIGHT_TRACKS) {
    const html = pageShell({
      title: track.title,
      lang: 'en',
      baseHref: RAVN_BASE_HREF,
      body: `${header('en')}${preflight(track)}`,
    });
    for (const file of track.files) {
      await fs.writeFile(path.join(out, file), html);
    }
  }
}

async function buildGuides() {
  const searchDocs = [];
  const guides = [
    ...LANGS.map(l => ({ ...l, output: l.code })),
    ...PROFESSIONAL_GUIDES,
    ...DEVELOPER_GUIDES,
  ];
  for (const l of guides) {
    const src = path.join(ROOT, l.guide);
    if (!(await exists(src))) {
      console.warn(`skip ${l.code}: ${l.guide} not found`);
      continue;
    }
    const md = await fs.readFile(src, 'utf8');
    headingSlug = createSlugger();
    const html = marked.parse(md);
    const out = path.join(DOCS, 'guides', `${l.output}.html`);
    await ensureDir(path.dirname(out));
    await fs.writeFile(out, pageShell({
      title: `${l.title || l.label} — Claude Certified Architect · Ravn`,
      lang: l.code,
      baseHref: RAVN_BASE_HREF,
      body: `${header(l.code)}<main class="guide">${html}</main>`,
    }));

    // index headings + lead paragraph for search
    const tokens = marked.lexer(md);
    let currentHeading = null;
    let currentHeadingId = null;
    let buffer = '';
    let id = 0;
    const searchSlug = createSlugger();
    const flush = () => {
      if (currentHeading) {
        searchDocs.push({
          id: `${l.output}#${++id}`,
          lang: l.code,
          heading: currentHeading,
          body: buffer.slice(0, 400),
          url: `guides/${l.output}.html#${currentHeadingId}`,
        });
      }
      buffer = '';
    };
    for (const t of tokens) {
      if (t.type === 'heading') {
        flush();
        currentHeading = t.text;
        const raw = t.tokens?.map(token => token.raw ?? token.text ?? '').join('') || t.text;
        currentHeadingId = searchSlug(raw);
      }
      else if (t.type === 'paragraph' || t.type === 'code') { buffer += ' ' + (t.text || t.raw || ''); }
    }
    flush();
  }

  const mini = new MiniSearch({ fields: ['heading', 'body'], storeFields: ['heading', 'lang', 'url'] });
  mini.addAll(searchDocs);
  await fs.writeFile(path.join(DOCS, 'search-index.json'), JSON.stringify(mini.toJSON()));
}

function slug(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function createSlugger() {
  const counts = new Map();
  return value => {
    const base = slug(value) || 'section';
    const count = counts.get(base) || 0;
    counts.set(base, count + 1);
    return count === 0 ? base : `${base}-${count + 1}`;
  };
}

async function copyBrowserDependencies() {
  const vendor = path.join(DOCS, 'vendor');
  await ensureDir(vendor);
  await fs.copyFile(MINISEARCH_BROWSER, path.join(vendor, 'minisearch.js'));
  await fs.copyFile(`${MINISEARCH_BROWSER}.map`, path.join(vendor, 'index.js.map'));
}

async function copyPracticalTests() {
  const out = path.join(DOCS, 'practical');
  await ensureDir(out);
  for (const l of LANGS) {
    const src = path.join(ROOT, l.test);
    const dest = path.join(out, `${l.code}.html`);
    if (await exists(src)) {
      await fs.copyFile(src, dest);
    } else {
      const body = `${header(l.code)}<main class="placeholder">
        <h1>Practical exam — ${l.label}</h1>
        <p>This practical test has not been generated yet.</p>
        <p><a href="index.html">← back to home</a></p>
      </main>`;
      await fs.writeFile(dest, pageShell({
        title: `${l.label} — Practical exam (pending) · Ravn`,
        lang: l.code,
        baseHref: RAVN_BASE_HREF,
        body,
      }));
    }
  }
}

// Professional and Developer exams are keyed on `output`
// (professional-en.html, developer-en.html), never on `code` — both entries
// use code 'en', which would overwrite the Foundations English exam that
// copyPracticalTests() just wrote.
async function copyProfessionalExams() {
  const out = path.join(DOCS, 'practical');
  await ensureDir(out);
  for (const l of [...PROFESSIONAL_GUIDES, ...DEVELOPER_GUIDES]) {
    if (!l.test) continue;
    const src = path.join(ROOT, l.test);
    const dest = path.join(out, `${l.output}.html`);
    if (await exists(src)) {
      await fs.copyFile(src, dest);
    } else {
      const body = `${header(l.code)}<main class="placeholder">
        <h1>${l.title || l.label} practice exam</h1>
        <p>This practice exam has not been generated yet.</p>
        <p><a href="index.html">← back to home</a></p>
      </main>`;
      await fs.writeFile(dest, pageShell({
        title: `${l.label} — Professional practice exam (pending) · Ravn`,
        lang: l.code,
        baseHref: RAVN_BASE_HREF,
        body,
      }));
    }
  }
}

async function copyCheatsheets() {
  const out = path.join(DOCS, 'cheatsheet');
  await ensureDir(out);
  for (const l of LANGS) {
    const src = path.join(ROOT, `cheatsheet_${l.code}.html`);
    const dest = path.join(out, `${l.code}.html`);
    if (await exists(src)) {
      await fs.copyFile(src, dest);
    } else {
      const body = `${header(l.code)}<main class="placeholder">
        <h1>Cheatsheet — ${l.label}</h1>
        <p>This cheatsheet has not been generated yet.</p>
        <p><a href="index.html">← back to home</a></p>
      </main>`;
      await fs.writeFile(dest, pageShell({
        title: `${l.label} — Cheatsheet (pending) · Ravn`,
        lang: l.code,
        baseHref: RAVN_BASE_HREF,
        body,
      }));
    }
  }
}

async function copyPdfs() {
  const src = path.join(ROOT, 'pdf');
  const dest = path.join(DOCS, 'pdf');
  if (!(await exists(src))) return;
  await ensureDir(dest);
  for (const f of await fs.readdir(src)) {
    if (f.endsWith('.pdf')) await fs.copyFile(path.join(src, f), path.join(dest, f));
  }
}

async function writeIndex() {
  await fs.writeFile(path.join(DOCS, 'index.html'), pageShell({
    title: 'Claude Certified Architect · Ravn',
    lang: 'en',
    baseHref: RAVN_BASE_HREF,
    body: `${header('en')}${landing()}`,
  }));
  await fs.writeFile(path.join(DOCS, '.nojekyll'), '');
}

async function main() {
  await ensureDir(DOCS);
  await copyBrowserDependencies();
  await writeIndex();
  await buildGuides();
  await copyPracticalTests();
  await copyProfessionalExams();
  await copyCheatsheets();
  await buildPreflight();
  await copyPdfs();
  console.log('docs/ built');
}

main().catch(e => { console.error(e); process.exit(1); });
