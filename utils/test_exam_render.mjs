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
    id, textContent: '', innerHTML: '', children: [], disabled: false, value: '',
    classList: {
      _s: new Set(),
      add(...c) { c.forEach(x => this._s.add(x)); },
      remove(...c) { c.forEach(x => this._s.delete(x)); },
      toggle(c, on) { on ? this._s.add(c) : this._s.delete(c); },
      contains(c) { return this._s.has(c); },
    },
    setAttribute() {},
    appendChild(c) { this.children.push(c); },
    addEventListener() {},
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
      removeItem: k => store.delete(k),
    },
    // The browse search debounces; running it inline keeps the check
    // synchronous without letting the engine skip the debounce path.
    setTimeout: fn => { fn(); return 0; },
    clearTimeout() {},
  };
  vm.createContext(ctx);
  vm.runInContext(script +
    '\nthis.__api = { state, showSummary, renderQuestion, answer, orderedQuestions,' +
    ' selectCount, isMulti, T, DOMAINS, QUESTIONS, shuffleOrder, qById, restart, setFocus,' +
    ' examSize, toggleBrowse, renderBrowse, filteredBank, browseBody, setBrowseDomain,' +
    ' onBrowseSearch, toggleMisses, updateMissesUI, missedIds, saveMisses, MISS_KEY };', ctx);
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
    const perLetter = (out.match(/<strong>Why [A-H]:<\/strong>/g) || []).length;
    check(`each correct letter gets its own rationale (${perLetter} found, ${need} needed)`,
      perLetter >= need);
    check('no merged multi-letter rationale heading remains',
      !/<strong>Why [A-H], /.test(out));
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
    // The attribute, not the word: imported option text says "disabled" often
    // enough that a substring search fails on the prose instead of the markup.
    check('an at-capacity option keeps its place in the tab order',
      !/<button[^>]*\sdisabled[\s>]/.test(card));
    check('the page explains why the other options are unavailable',
      card.includes(api.T.select_full.replace('{n}', api.selectCount(multi))));

    // The counterpart, which also proves the check above is not vacuous: once
    // study mode reveals the answer the options are inert for good, and there
    // `disabled` is exactly right.
    api.state.mode = 'study';
    api.renderQuestion(idx);
    check('a revealed option is disabled outright',
      /<button[^>]*\sdisabled[\s>]/.test(el('qCard').innerHTML));
    api.state.mode = 'exam';
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
  check('the full draw returns to the blueprint size',
    api.orderedQuestions().length === api.examSize('full', 'all'),
    `${api.orderedQuestions().length} vs ${api.examSize('full', 'all')}`);
  check('the draw note returns to the full-draw text',
    el('drawNote').innerHTML.includes(api.T.draw_note_full.split('{n}')[0]));
}

// The imported banks carry items with six, seven and eight options and select
// counts up to five. The engine letters and renders whatever an item holds, so
// the check is against the widest item the page actually ships.
function checkWideItems(file) {
  const { api, el } = loadPage(file);
  const byWidth = api.QUESTIONS.slice().sort((a, b) => b.options.length - a.options.length);
  const wide = byWidth[0];
  const most = api.QUESTIONS.slice().sort((a, b) => api.selectCount(b) - api.selectCount(a))[0];
  console.log(`\nWide items (${file})`);
  if (wide.options.length <= 5 && api.selectCount(most) <= 3) {
    console.log(`  --   this bank tops out at ${wide.options.length} options / ` +
      `select ${api.selectCount(most)}; the wide-item checks did not run`);
    return;
  }

  const renderOnly = q => {
    api.state.order = [q.id];
    api.state.current = 0;
    api.state.answers = {};
    api.state.mode = 'study';
    api.renderQuestion(0);
    return el('qCard').innerHTML;
  };

  const card = renderOnly(wide);
  const drawn = (card.match(/class='opt-letter'>[^<]+</g) || []).length;
  check(`every option renders on a ${wide.options.length}-option item (${wide.id})`,
    drawn === wide.options.length, `${drawn} rendered`);
  check('each option keeps its own letter',
    wide.options.every(o => card.includes("data-letter='" + o.letter + "'")),
    wide.options.map(o => o.letter).join(''));
  check('letters stay inside A..H',
    wide.options.every(o => 'ABCDEFGH'.includes(o.letter)));

  const need = api.selectCount(most);
  const wideCard = renderOnly(most);
  check(`the select badge states the real count (${most.id}, ${need})`,
    wideCard.includes(api.T.select_n.replace('{n}', need)));

  // All-or-nothing still holds at five: picking N-1 of N leaves the item
  // editable and unscored, and the Nth click completes it.
  if (!api.isMulti(most)) return;
  most.correct.slice(0, need - 1).forEach(L => api.answer(most.id, L));
  check('a wide multi item is not answered one letter short',
    api.state.answers[most.id].length === need - 1);
  api.answer(most.id, most.correct[need - 1]);
  check('a wide multi item completes at its full select count',
    api.state.answers[most.id].length === need);
  api.state.mode = 'exam';
  api.showSummary();
  check('a wide multi item answered in full stays out of the review pane',
    !el('summaryContent').innerHTML.includes(most.id.toUpperCase()));
}

// Browse mode: the whole bank, filtered by domain and free text, each item
// expandable to its full answer key. The filter is pure, so it is checked
// directly; the row body is checked through the same function the DOM calls.
function checkBrowse(file) {
  console.log(`\nBrowse mode (${file})`);
  const { api, el } = loadPage(file);

  api.toggleBrowse();
  check('the browse screen opens', el('browseScreen').classList.contains('active'));
  check('opening browse hides the question screen',
    !el('questionScreen').classList.contains('active'));
  check('browse lists the whole bank unfiltered',
    api.filteredBank().length === api.QUESTIONS.length);
  check('the count line names the bank size',
    el('browseCount').textContent.includes(String(api.QUESTIONS.length)));
  const listed = (el('browseList').innerHTML.match(/<details /g) || []).length;
  check('every bank item gets a row', listed === api.QUESTIONS.length, `${listed} rows`);
  check('rows ship closed, so 500 answer keys are not rendered at once',
    !el('browseList').innerHTML.includes('br-opt'));

  const d = Object.keys(api.DOMAINS).sort((a, b) => a - b)[0];
  const inD = api.QUESTIONS.filter(q => String(q.domain) === String(d)).length;
  api.setBrowseDomain(d);
  check(`the domain filter scopes the list to D${d} (${inD} items)`,
    api.filteredBank().length === inD &&
    api.filteredBank().every(r => String(r.q.domain) === String(d)));

  // A term drawn from one item's own explanation must find that item, and the
  // domain filter must still apply on top of it.
  const target = api.QUESTIONS.find(q => String(q.domain) === String(d) &&
    q.options.some(o => o.explanation));
  const word = target.question.split(/\s+/).find(w => w.length > 7).replace(/[^\w]/g, '');
  api.onBrowseSearch(word);
  const hits = api.filteredBank();
  check(`a search term narrows the list ("${word}": ${hits.length} of ${inD})`,
    hits.length > 0 && hits.length <= inD && hits.some(r => r.q.id === target.id));
  check('search stacks on the domain filter',
    hits.every(r => String(r.q.domain) === String(d)));

  // Searching the blueprint subdomain id gathers every item on that objective.
  const withTask = api.QUESTIONS.find(x => x.task_id);
  if (withTask) {
    const want = api.QUESTIONS.filter(x => x.task_id === withTask.task_id).length;
    api.setBrowseDomain('all');
    api.onBrowseSearch(withTask.task_id);
    const byTask = api.filteredBank();
    check(`a task id finds its objective's items (${withTask.task_id}: ${want})`,
      byTask.length >= want && byTask.some(r => r.q.id === withTask.id));
  } else {
    console.log('  --   this bank ships no task ids');
  }

  api.setBrowseDomain(d);
  api.onBrowseSearch('zzz-no-such-term-zzz');
  check('a term nothing matches empties the list', api.filteredBank().length === 0);
  check('an empty list says so', el('browseList').innerHTML.includes(api.T.browse_none));

  api.onBrowseSearch('');
  api.setBrowseDomain('all');

  // The expanded body: every option, the correct ones marked, every rationale.
  const q = api.QUESTIONS.find(x => x.options.every(o => o.explanation)) || api.QUESTIONS[0];
  const body = api.browseBody(q.id);
  const shown = (body.match(/class='opt-letter'>/g) || []).length;
  check(`an expanded item shows all ${q.options.length} options (${q.id})`,
    shown === q.options.length, `${shown} shown`);
  check('the correct options are marked',
    q.options.filter(o => o.correct).every(o =>
      body.includes("<span class='opt-letter'>" + o.letter + "</span>")) &&
    (body.match(/is-correct/g) || []).length === q.options.filter(o => o.correct).length);
  // md() rewrites backticks and bold, so compare on a run of plain prose.
  const plain = t => (String(t).match(/[A-Za-z][A-Za-z ,.]{19,}/) || [''])[0];
  check('every explanation is visible',
    q.options.filter(o => plain(o.explanation)).every(o => body.includes(plain(o.explanation))));
  check('no unescaped item text reached the browse body', !/<img|<iframe|onerror=/i.test(body));

  // Provenance travels with an imported item, on the card and in browse.
  const imported = api.QUESTIONS.find(x => x.source === 'certsafari');
  if (imported) {
    check('an imported item is labelled in browse',
      api.browseBody(imported.id).includes(api.T.source_note));
    check('the browse row tags the source',
      api.filteredBank('all', '').length > 0 &&
      el('browseList').innerHTML.includes(api.T.source_label));
    api.state.order = [imported.id];
    api.state.current = 0;
    api.renderQuestion(0);
    check('an imported item is labelled on the question card',
      el('qCard').innerHTML.includes(api.T.source_note));
  }

  // Clusters share a stem, so each row says which variant of it this is.
  const clustered = api.QUESTIONS.find(x => x.cluster &&
    api.QUESTIONS.filter(y => y.cluster === x.cluster).length > 1);
  if (clustered) {
    const n = api.QUESTIONS.filter(y => y.cluster === clustered.cluster).length;
    api.setBrowseDomain('all');
    api.renderBrowse();
    check(`a clustered item says which variant it is (${clustered.cluster}, ${n} variants)`,
      el('browseList').innerHTML.includes(
        api.T.cluster_note.replace('{i}', 1).replace('{n}', n)));
  } else {
    console.log('  --   this bank ships no clustered items');
  }

  api.toggleBrowse();
  check('browse closes back to the attempt',
    el('questionScreen').classList.contains('active') &&
    !el('browseScreen').classList.contains('active'));

  const rawHtml = fs.readFileSync(path.join(ROOT, file), 'utf8');
  check('a browse entry point sits in the always-on header',
    rawHtml.includes('id="browseBtn"') && rawHtml.includes(api.T.browse_btn));
  check('a weak-spot entry point sits in the always-on header',
    rawHtml.includes('id="missesBtn"') && rawHtml.includes(api.T.misses_label));
}

// The weak-spot drill's UI half: the button counts what is stored, the drill
// scopes to it, and clearing the record is offered where the drill is running.
function checkMissesUI(file) {
  console.log(`\nWeak-spot drill (${file})`);
  const { api, el } = loadPage(file);

  api.updateMissesUI();
  check('with nothing missed the entry point is disabled',
    el('missesBtn').disabled === true);
  check('the disabled entry point still names itself',
    el('missesBtn').textContent === api.T.misses_empty);

  const picks = api.QUESTIONS.slice(0, 3);
  const misses = {};
  picks.forEach((q, i) => { misses[q.id] = { n: 3 - i, t: i }; });
  api.saveMisses(misses);
  api.updateMissesUI();
  check('the entry point counts the stored misses',
    el('missesBtn').textContent === api.T.misses_btn.replace('{n}', 3));
  check('the entry point is enabled once something has been missed',
    el('missesBtn').disabled === false);

  api.toggleMisses();
  check('the drill scopes the attempt to the missed items',
    api.state.focus === 'misses' && api.orderedQuestions().length === 3);
  check('the drill runs most-missed first',
    api.orderedQuestions()[0].id === picks[0].id, api.orderedQuestions()[0].id);
  check('the drill draws only missed items',
    api.orderedQuestions().every(q => misses[q.id] !== undefined));
  check('the question screen names the weak-spot drill',
    el('drawNote').innerHTML.includes(api.T.misses_note.replace('{n}', 3)));
  check('the drill offers a way to clear the record',
    el('drawNote').innerHTML.includes(api.T.misses_clear));
  check('the length toggle is disabled inside the weak-spot drill',
    el('lengthFull').disabled === true);
  check('the domain select goes inert inside the weak-spot drill',
    el('focusSelect').disabled === true);

  // Miss one of them again, leave the rest blank, and score the attempt.
  api.state.mode = 'exam';
  const again = api.orderedQuestions()[0];
  const wrong = Array.isArray(again.correct)
    ? again.options.filter(o => again.correct.indexOf(o.letter) < 0)
        .slice(0, again.correct.length).map(o => o.letter)
    : again.options.find(o => o.letter !== again.correct).letter;
  api.state.answers[again.id] = wrong;
  api.showSummary();
  const out = el('summaryContent').innerHTML;
  check('a weak-spot summary reports a raw score', out.includes(api.T.misses_score));
  check('a weak-spot summary shows no scaled score', !out.includes('/1000'));
  check('a weak-spot summary still lists the review pane', out.includes(api.T.review_wrong));

  // Scoring is a grading moment: the item missed again climbs the ranking,
  // and the two left blank are skipped rather than recorded.
  api.updateMissesUI();
  check('finishing an attempt records the miss it just scored',
    api.missedIds()[0] === again.id, api.missedIds()[0]);
  check('finishing does not record the questions left blank',
    el('missesBtn').textContent === api.T.misses_btn.replace('{n}', 3));

  api.toggleMisses();
  check('leaving the weak-spot drill restores the full draw',
    api.state.focus === 'all' &&
    api.orderedQuestions().length === api.examSize('full', 'all'));
}

// Every shipped page, so a UI string missing from one language cannot pass.
checkPage('ccaf/dist/exam_en.html');
checkPage('ccaf/dist/exam_es.html');
checkPage('ccaf/dist/exam_pt.html');
checkPage('ccap/dist/exam_en.html');
checkPage('ccdf/dist/exam_en.html');
checkDrill('ccaf/dist/exam_en.html');
checkDrill('ccaf/dist/exam_es.html');
checkDrill('ccaf/dist/exam_pt.html');
checkDrill('ccap/dist/exam_en.html');
checkDrill('ccdf/dist/exam_en.html');
checkWideItems('ccap/dist/exam_en.html');
checkWideItems('ccdf/dist/exam_en.html');
checkBrowse('ccaf/dist/exam_en.html');
checkBrowse('ccaf/dist/exam_pt.html');
checkBrowse('ccap/dist/exam_en.html');
checkBrowse('ccdf/dist/exam_en.html');
checkMissesUI('ccaf/dist/exam_es.html');
checkMissesUI('ccap/dist/exam_en.html');
checkMissesUI('ccdf/dist/exam_en.html');

console.log(failures === 0 ? '\nAll render checks passed.' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
