#!/usr/bin/env node
// Regression harness for the parts of the engine that write the DOM.
//
// test_exam_engine.mjs stops at the sidebar boundary, so it covers the pure
// logic only. The summary screen is where a scoring rule turns into something
// the candidate can read, and a defect there is silent: an item can be counted
// as incorrect and still never appear in the review pane. This file runs the
// whole engine against a stub DOM, drives it, and reads the HTML it produced.
//
// Usage: node utils/test_exam_render.mjs

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

let failures = 0;
function check(name, cond, detail = '') {
  if (cond) { console.log(`  ok   ${name}`); }
  else { console.log(`  FAIL ${name}${detail ? ' — ' + detail : ''}`); failures++; }
}

// Stub DOM: only what init(), renderQuestion() and showSummary() touch.
function makeEl(id) {
  const el = {
    id, textContent: '', innerHTML: '', children: [], disabled: false,
    classList: {
      _s: new Set(),
      add(...c) { c.forEach(x => this._s.add(x)); },
      remove(...c) { c.forEach(x => this._s.delete(x)); },
      toggle(c, on) { on ? this._s.add(c) : this._s.delete(c); },
      contains(c) { return this._s.has(c); },
    },
    setAttribute() {},
    appendChild(c) { this.children.push(c); },
  };
  Object.defineProperty(el, 'className', {
    get() { return [...el.classList._s].join(' '); },
    set(v) { el.classList._s = new Set(String(v).split(/\s+/).filter(Boolean)); },
  });
  return el;
}

function loadPage(file) {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const script = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
  const els = new Map();
  const store = new Map();
  const ctx = {
    console,
    document: {
      getElementById(id) { if (!els.has(id)) els.set(id, makeEl(id)); return els.get(id); },
      createElement() { return makeEl(''); },
    },
    localStorage: {
      getItem: k => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
    },
  };
  vm.createContext(ctx);
  vm.runInContext(script +
    '\nthis.__api = { state, showSummary, renderQuestion, answer, orderedQuestions,' +
    ' selectCount, isMulti, T, DOMAINS, QUESTIONS, shuffleOrder, qById, restart, setFocus };', ctx);
  return { api: ctx.__api, el: id => ctx.document.getElementById(id) };
}

function checkPage(file) {
  console.log(`\nSummary screen (${file})`);
  const { api, el } = loadPage(file);
  const drawn = api.orderedQuestions();
  const multi = drawn.find(q => api.isMulti(q));

  // Leave everything blank except one half-picked multiple-response item.
  api.state.mode = 'exam';
  api.state.answers = {};
  if (multi) {
    api.state.answers[multi.id] = multi.correct.slice(0, multi.correct.length - 1);
  }
  api.showSummary();
  const out = el('summaryContent').innerHTML;

  check('the review section renders', out.includes(api.T.review_wrong));
  check('an unanswered item is listed in the review pane',
    out.includes(drawn.find(q => !multi || q.id !== multi.id).id.toUpperCase()));
  check('an unanswered row says so instead of showing an empty dash',
    out.includes(api.T.not_answered));
  // Compare against the page's own string, so es and pt are checked too.
  check('the unanswered warning still renders',
    out.includes(api.T.unanswered.split('{n}').pop().trim()));

  if (multi) {
    const need = api.selectCount(multi);
    const picked = api.state.answers[multi.id].slice().sort().join(', ');
    // The defect this file exists for: a half-picked item was counted as
    // incorrect and dropped from the review pane, so no rationale was shown.
    check(`a half-picked item (${multi.id}, ${need} needed) is listed in the review pane`,
      out.includes(multi.id.toUpperCase()));
    check('a half-picked row is tagged as incomplete',
      out.includes(api.T.incomplete_answer));
    check('a half-picked row shows the letters it did pick', out.includes(picked));

    // Each correct letter gets its own rationale, not one merged paragraph.
    const perLetter = (out.match(/<strong>Why [A-E]:<\/strong>/g) || []).length;
    check(`each correct letter gets its own rationale (${perLetter} found, ${need} needed)`,
      perLetter >= need);
    check('no merged multi-letter rationale heading remains',
      !/<strong>Why [A-E], /.test(out));
  }

  // Nothing may escape as markup. Look for a tag no template writes.
  check('no unescaped item text reached the page', !/<img|<iframe|onerror=/i.test(out));

  // Rotation must be stated where it matters: on the question screen (the
  // strip under the brand bar) and again at the end of an attempt.
  check('the summary says the questions rotate',
    out.includes(api.T.summary_rotate.split('{n}')[0]));
  check('the question screen carries the fresh-draw note',
    el('drawNote').innerHTML.includes(api.T.draw_note_full.split('{n}')[0]));
  check('the length toggle shows both draw sizes',
    el('lengthFull').textContent.length > 0 && el('lengthQuick').textContent.length > 0);
  // The new-set control is server-rendered into the always-on header, so it is
  // visible from the first question on — check the shipped markup itself.
  // Same for the domain-drill selector: its options are built at runtime, so
  // only the empty select and its accessible label can be checked here.
  const rawHtml = fs.readFileSync(path.join(ROOT, file), 'utf8');
  check('a new-set control sits in the always-on header',
    rawHtml.includes('id="newDrawBtn"') && rawHtml.includes(api.T.new_set));
  check('a domain-drill selector sits in the always-on header',
    rawHtml.includes('id="focusSelect"') && rawHtml.includes(api.T.focus_label));
  check('the drill strings ship on this page',
    typeof api.T.focus_all === 'string' && typeof api.T.focus_note === 'string' &&
    typeof api.T.drill_score === 'string');

  // At-capacity options stay reachable: aria-disabled, not disabled.
  if (multi) {
    console.log(`Question screen (${file})`);
    api.state.answers[multi.id] = multi.correct.slice();   // complete: at capacity
    const idx = drawn.findIndex(q => q.id === multi.id);
    api.renderQuestion(idx);
    const card = el('qCard').innerHTML;
    check('an at-capacity option reports itself unavailable',
      card.includes("aria-disabled='true'"));
    check('an at-capacity option keeps its place in the tab order',
      !card.includes(' disabled'));
    check('the page explains why the other options are unavailable',
      card.includes(api.T.select_full.replace('{n}', api.selectCount(multi))));
  }
}

// A drill attempt holds one domain's whole bank and scores it raw: no scaled
// score, no pass/fail verdict — but the review pane and the unanswered warning
// must still render, and leaving the drill must restore the full draw.
function checkDrill(file) {
  console.log(`\nDrill mode (${file})`);
  const { api, el } = loadPage(file);
  const d = Object.keys(api.DOMAINS).sort((a, b) => a - b)[0];

  api.setFocus(d);   // no answers yet, so no discard prompt
  check('focusing a domain scopes the attempt', String(api.state.focus) === String(d));
  const drilled = api.orderedQuestions();
  const bank = api.QUESTIONS.filter(q => String(q.domain) === String(d)).length;
  check('a drill holds the whole domain bank and only that domain',
    drilled.length === bank && drilled.every(q => String(q.domain) === String(d)),
    `${drilled.length} vs bank ${bank}`);
  check('a new drill set keeps the same bank',
    (() => {
      const before = new Set(api.orderedQuestions().map(q => q.id));
      api.restart();   // the "New set" button: reshuffle, same questions
      const after = api.orderedQuestions();
      return after.length === bank && after.every(q => before.has(q.id));
    })());
  check('the question screen names the drill',
    el('drawNote').innerHTML.includes(
      api.T.focus_note.replace('{n}', drilled.length).replace('{d}', d)));
  check('the length toggle is disabled mid-drill',
    el('lengthFull').disabled === true && el('lengthQuick').disabled === true);

  api.state.mode = 'exam';
  api.showSummary();
  const out = el('summaryContent').innerHTML;
  check('a drill summary reports the raw domain score',
    out.includes(api.T.drill_score.replace('{d}', d)));
  check('a drill summary shows no scaled score', !out.includes('/1000'));
  check('a drill summary shows no pass/fail verdict',
    !out.includes('verdict pass') && !out.includes('verdict fail'));
  check('a drill summary still lists the review pane', out.includes(api.T.review_wrong));
  check('a drill summary still warns about unanswered items',
    out.includes(api.T.unanswered.split('{n}').pop().trim()));

  api.setFocus('all');
  check('leaving the drill restores the full draw', api.state.focus === 'all');
  check('the full draw is larger than any single drill',
    api.orderedQuestions().length >= drilled.length);
  check('the draw note returns to the full-draw text',
    el('drawNote').innerHTML.includes(api.T.draw_note_full.split('{n}')[0]));
}

// Every shipped page, so a UI string missing from one language cannot pass.
checkPage('exam_en.html');
checkPage('exam_es.html');
checkPage('exam_pt.html');
checkPage('professional_exam_en.html');
checkPage('developer_exam_en.html');
checkDrill('exam_en.html');
checkDrill('exam_es.html');
checkDrill('exam_pt.html');
checkDrill('professional_exam_en.html');
checkDrill('developer_exam_en.html');

console.log(failures === 0 ? '\nAll render checks passed.' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
