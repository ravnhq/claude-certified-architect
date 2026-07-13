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
        <li><a href="https://anthropic-partners.skilljar.com/claude-certified-architect-professional-certification">Official registration</a></li>
      </ul>
    </article>`).join('');
  return `<main class="landing">
  <section class="hero">
    <p class="eyebrow">Ravn study materials</p>
    <h1>Claude Certified Architect <span class="accent">— choose your track.</span></h1>
    <p class="lede">Prepare for Foundations in English, Spanish, or Portuguese, or use the Professional blueprint to practice production architecture and lifecycle decisions.</p>
  </section>
  <section class="track">
    <div class="track-heading">
      <p class="track-label">Foundations</p>
      <h2>Build the core skills</h2>
      <p>Guides, practice exams, and cheatsheets for the five-domain Foundations certification.</p>
    </div>
    <div class="cards">${foundationCards}</div>
  </section>
  <section class="track">
    <div class="track-heading">
      <p class="track-label">Professional</p>
      <h2>Own the production architecture</h2>
      <p>Guidance for the seven-domain CCAR-P blueprint, effective July 2026.</p>
    </div>
    <div class="cards cards-single">${professionalCards}</div>
  </section>
</main>`;
}

async function buildGuides() {
  const searchDocs = [];
  const guides = [
    ...LANGS.map(l => ({ ...l, output: l.code })),
    ...PROFESSIONAL_GUIDES,
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
  await copyCheatsheets();
  await copyPdfs();
  console.log('docs/ built');
}

main().catch(e => { console.error(e); process.exit(1); });
