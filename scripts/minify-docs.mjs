#!/usr/bin/env node
// Minify the published HTML. Runs last, after scripts/build-pages.mjs has
// written every page: it rewrites docs/ in place, so anything that reads the
// generated markup would be reading minified output. Nothing does — the two
// former HTML scrapers read the question bank from <track>/dist/banks.json.
//
// Usage: node scripts/minify-docs.mjs
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { minify } from 'html-minifier-terser';

const DOCS = path.join(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'), 'docs');

const OPTIONS = {
  collapseWhitespace: true,
  conservativeCollapse: false,
  removeComments: true,
  minifyCSS: true,
  // toplevel stays off: the exam pages call their engine from inline onclick
  // attributes, so the global function names have to survive.
  minifyJS: true,
  removeScriptTypeAttributes: true,
  removeStyleLinkTypeAttributes: true,
  sortAttributes: true,
  sortClassName: true,
};

async function* htmlFiles(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(full);
    else if (entry.name.endsWith('.html')) yield full;
  }
}

let before = 0;
let after = 0;
let count = 0;
for await (const file of htmlFiles(DOCS)) {
  const src = await fs.readFile(file, 'utf8');
  const out = await minify(src, OPTIONS);
  before += Buffer.byteLength(src);
  after += Buffer.byteLength(out);
  count++;
  await fs.writeFile(file, out);
}
console.log(`Minified ${count} pages: ${(before / 1024).toFixed(0)} KB -> ${(after / 1024).toFixed(0)} KB`);
