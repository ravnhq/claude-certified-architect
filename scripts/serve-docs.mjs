#!/usr/bin/env node
// Static server for docs/, used by the Lighthouse budget and for local checks.
//
// Two things the stock python3 -m http.server cannot do, both of which decide
// whether a measurement means anything:
//   * gzip — GitHub Pages compresses text, so an uncompressed local server
//     reports a 356 KB guide as 356 KB and every byte budget becomes fiction.
//   * the base path — every page carries <base href="/claude-certified-architect/">,
//     so the site has to be mounted there rather than at the server root.
//
// Usage: node scripts/serve-docs.mjs [port]
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = path.join(ROOT, 'docs');
const PORT = Number(process.argv[2] || 8099);
const BASE = '/claude-certified-architect/';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.pdf': 'application/pdf',
  '.woff2': 'font/woff2',
};
// What Pages compresses: text, and never the already-compressed assets.
const COMPRESSIBLE = new Set(['.html', '.js', '.mjs', '.css', '.json', '.svg']);

http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  let rel = decodeURIComponent(url.pathname);
  if (!rel.startsWith(BASE)) { res.writeHead(404).end('not found'); return; }
  rel = rel.slice(BASE.length) || 'index.html';
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.join(DOCS, rel);
  if (!file.startsWith(DOCS)) { res.writeHead(403).end('forbidden'); return; }
  let body;
  try { body = await fs.readFile(file); } catch { res.writeHead(404).end('not found'); return; }
  const ext = path.extname(file);
  const headers = { 'content-type': TYPES[ext] || 'application/octet-stream' };
  if (COMPRESSIBLE.has(ext) && /\bgzip\b/.test(req.headers['accept-encoding'] || '')) {
    body = zlib.gzipSync(body, { level: 6 });
    headers['content-encoding'] = 'gzip';
  }
  headers['content-length'] = body.length;
  res.writeHead(200, headers).end(body);
}).listen(PORT, () => console.log(`Serving docs on http://localhost:${PORT}${BASE}`));
