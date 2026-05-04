#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { marked } from 'marked';
import MiniSearch from 'minisearch';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const DOCS = path.join(ROOT, 'docs');

const LANGS = [
  { code: 'en', label: 'English',    guide: 'guide_en.MD',  test: 'practical_test_en.html' },
  { code: 'es', label: 'Español',    guide: 'guide_es.md',  test: 'practical_test_es.html' },
  { code: 'pt', label: 'Português',  guide: 'guide_pt.md',  test: 'practical_test_pt.html' },
];

const RAVN_BASE_HREF = process.env.RAVN_BASE_HREF || '/claude-certified-architect/';

marked.use({
  useNewRenderer: true,
  renderer: {
    heading({ tokens, depth }) {
      const raw = tokens.map(t => t.raw ?? t.text ?? '').join('');
      const id = slug(raw);
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap">
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
    <img src="assets/ravn-logo.svg" alt="Ravn" width="86" height="22">
    <span>Claude Certified Architect</span>
  </a>
  <nav class="topbar-actions">
    <button id="search-toggle" class="icon-btn" aria-label="Search">⌕</button>
    <button id="theme-toggle" class="icon-btn" aria-label="Toggle theme">◐</button>
  </nav>
</header>
<dialog id="search-dialog">
  <div class="search-filter" role="group" aria-label="Filter by language">
    <button class="search-lang active" data-lang="all">All</button>
    <button class="search-lang" data-lang="en">EN</button>
    <button class="search-lang" data-lang="es">ES</button>
    <button class="search-lang" data-lang="pt">PT</button>
  </div>
  <input id="search-input" type="search" placeholder="Search the guide…" autocomplete="off">
  <ul id="search-results"></ul>
</dialog>`;
}

function landing() {
  const cards = LANGS.map(l => `
    <article class="card" data-lang="${l.code}">
      <h2>${l.code.toUpperCase()}</h2>
      <div class="lang-name">${l.label}</div>
      <ul>
        <li><a href="guides/${l.code}.html">Read the guide</a></li>
        <li><a href="practical/${l.code}.html">Practical exam</a></li>
        <li><a href="pdf/guide_${l.code}.pdf">PDF download</a></li>
      </ul>
    </article>`).join('');
  return `<main class="landing">
  <section class="hero">
    <p class="eyebrow">Ravn study materials</p>
    <h1>Claude Certified Architect <span class="accent">— Foundations.</span></h1>
    <p class="lede">Curated study materials for the Anthropic certification, in the languages our teams ship in. Read online, take the practical exam, or grab the PDF.</p>
  </section>
  <section class="cards">${cards}</section>
</main>`;
}

async function buildGuides() {
  const searchDocs = [];
  for (const l of LANGS) {
    const src = path.join(ROOT, l.guide);
    if (!(await exists(src))) {
      console.warn(`skip ${l.code}: ${l.guide} not found`);
      continue;
    }
    const md = await fs.readFile(src, 'utf8');
    const html = marked.parse(md);
    const out = path.join(DOCS, 'guides', `${l.code}.html`);
    await ensureDir(path.dirname(out));
    await fs.writeFile(out, pageShell({
      title: `${l.label} — Claude Certified Architect · Ravn`,
      lang: l.code,
      baseHref: RAVN_BASE_HREF,
      body: `${header(l.code)}<main class="guide">${html}</main>`,
    }));

    // index headings + lead paragraph for search
    const tokens = marked.lexer(md);
    let currentHeading = null;
    let buffer = '';
    let id = 0;
    const flush = () => {
      if (currentHeading) {
        searchDocs.push({
          id: `${l.code}#${++id}`,
          lang: l.code,
          heading: currentHeading,
          body: buffer.slice(0, 400),
          url: `guides/${l.code}.html#${slug(currentHeading)}`,
        });
      }
      buffer = '';
    };
    for (const t of tokens) {
      if (t.type === 'heading') { flush(); currentHeading = t.text; }
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
  await writeIndex();
  await buildGuides();
  await copyPracticalTests();
  await copyPdfs();
  console.log('docs/ built');
}

main().catch(e => { console.error(e); process.exit(1); });
