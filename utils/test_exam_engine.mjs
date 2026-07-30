#!/usr/bin/env node
// Regression harness for the quiz engine embedded in the generated exam pages.
//
// It pulls the real <script> out of the built HTML and evaluates the DOM-free
// part of it (constants, draw logic, answer-shape helpers). That covers the
// logic a silent bug would hide in: Foundations single-answer scoring must be
// unchanged, and the Professional weighted draw and all-or-nothing
// multiple-response scoring must be right.
//
// Usage: node utils/test_exam_engine.mjs

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

let failures = 0;
function check(name, cond, detail = '') {
  if (cond) { console.log(`  ok   ${name}`); }
  else { console.log(`  FAIL ${name}${detail ? ' — ' + detail : ''}`); failures++; }
}

// Load the engine's DOM-free prefix from a built page.
function loadEngine(file) {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const script = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
  const cut = script.indexOf('// ---- sidebar');
  if (cut < 0) throw new Error(`${file}: could not find the sidebar boundary`);
  const src = script.slice(0, cut);
  // answer() lives after the sidebar boundary and drives the DOM, so pull just
  // that function in and stub its two render calls. It holds the toggle and
  // study-mode lock logic, which is the most branched new code in the engine.
  const answerSrc = script.slice(script.indexOf('function answer(id, letter) {'));
  const answerFn = answerSrc.slice(0, answerSrc.indexOf('\n}\n') + 3);

  const store = new Map();
  const ctx = {
    localStorage: {
      getItem: k => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
    },
    console,
    renderQuestion() {},
    updateSidebar() {},
  };
  vm.createContext(ctx);
  vm.runInContext(src + '\n' + answerFn +
    '\nthis.__api = { QUESTIONS, PER_DOMAIN, DOMAINS, STORE_KEY, state, answer, drawCount, examSize, isMulti, selectCount, hasAnswer, isCorrect, isChosenLetter, letterLabel, shuffleOrder, qById };', ctx);
  return ctx.__api;
}

console.log('Foundations engine (exam_en.html)');
{
  const e = loadEngine('exam_en.html');
  check('5 domains in the bank', new Set(e.QUESTIONS.map(q => q.domain)).size === 5);
  check('flat draw of 12 per domain', e.PER_DOMAIN === 12, `got ${JSON.stringify(e.PER_DOMAIN)}`);
  check('attempt size is 60', e.examSize() === 60, `got ${e.examSize()}`);
  check('shuffleOrder draws 60', e.shuffleOrder().length === 60);
  check('store key is Foundations-scoped', e.STORE_KEY === 'ccaf-exam-en', e.STORE_KEY);

  const q = e.QUESTIONS[0];
  check('single-answer item is not multi', !e.isMulti(q));
  check('correct letter scores correct', e.isCorrect(q, q.correct));
  const wrong = q.options.find(o => o.letter !== q.correct).letter;
  check('wrong letter scores incorrect', !e.isCorrect(q, wrong));
  check('unanswered is not correct', !e.isCorrect(q, undefined));
  check('a letter counts as answered', e.hasAnswer(q, q.correct));
  check('undefined is not answered', !e.hasAnswer(q, undefined));
  check('an array is not answered on a single-response item', !e.hasAnswer(q, [q.correct]));
  check('no multi items leaked into Foundations',
    e.QUESTIONS.every(x => !Array.isArray(x.correct)));
}

console.log('Professional engine (professional_exam_en.html)');
{
  const e = loadEngine('professional_exam_en.html');
  check('7 domains in the bank', new Set(e.QUESTIONS.map(q => q.domain)).size === 7);
  check('bank holds 126 items', e.QUESTIONS.length === 126, `got ${e.QUESTIONS.length}`);
  check('weighted draw map', typeof e.PER_DOMAIN === 'object' && e.PER_DOMAIN['3'] === 12);
  check('attempt size is 63', e.examSize() === 63, `got ${e.examSize()}`);
  check('store key does not collide with Foundations', e.STORE_KEY === 'ccarp-exam-en', e.STORE_KEY);

  // The draw must match the official domain weights on every attempt.
  let drawOk = true, drawDetail = '';
  for (let i = 0; i < 50; i++) {
    const order = e.shuffleOrder();
    if (order.length !== 63) { drawOk = false; drawDetail = `length ${order.length}`; break; }
    const per = {};
    order.forEach(id => { const d = e.qById(id).domain; per[d] = (per[d] || 0) + 1; });
    const want = { 1: 11, 2: 8, 3: 12, 4: 10, 5: 9, 6: 9, 7: 4 };
    for (const d of Object.keys(want)) {
      if (per[d] !== want[d]) { drawOk = false; drawDetail = `domain ${d}: ${per[d]} != ${want[d]}`; }
    }
    if (new Set(order).size !== order.length) { drawOk = false; drawDetail = 'duplicate ids drawn'; }
    if (!drawOk) break;
  }
  check('50 draws all match the blueprint weights', drawOk, drawDetail);

  const single = e.QUESTIONS.find(q => !Array.isArray(q.correct));
  const multi = e.QUESTIONS.find(q => Array.isArray(q.correct));
  check('bank contains multiple-response items', !!multi);

  check('single: correct letter scores', e.isCorrect(single, single.correct));
  check('single: wrong letter fails',
    !e.isCorrect(single, single.options.find(o => o.letter !== single.correct).letter));

  const key = multi.correct;
  check('multi: exact set scores correct', e.isCorrect(multi, key.slice()));
  check('multi: reversed order still correct', e.isCorrect(multi, key.slice().reverse()));
  check('multi: partial answer scores incorrect', !e.isCorrect(multi, key.slice(0, key.length - 1)),
    'all-or-nothing scoring');
  check('multi: partial answer is not "answered"', !e.hasAnswer(multi, key.slice(0, key.length - 1)));
  check('multi: complete answer is "answered"', e.hasAnswer(multi, key.slice()));
  check('multi: empty selection is not answered', !e.hasAnswer(multi, []));
  // Stale state from an item that flipped response shape must not read as a
  // complete answer, or it locks study mode on a permanently wrong answer.
  check('multi: a bare letter is not answered', !e.hasAnswer(multi, key[0]));
  check('multi: a bare letter does not score', !e.isCorrect(multi, key[0]));
  check('single: an array is not answered', !e.hasAnswer(single, [single.correct]));
  check('single: an array does not score', !e.isCorrect(single, [single.correct]));
  check('multi: superset scores incorrect', (() => {
    const extra = multi.options.find(o => !key.includes(o.letter));
    return !e.isCorrect(multi, key.concat(extra.letter));
  })());
  const swapped = key.slice(0, key.length - 1)
    .concat(multi.options.find(o => !key.includes(o.letter)).letter);
  check('multi: right count but wrong letters fails', !e.isCorrect(multi, swapped));
  check('multi: selectCount matches the key', e.selectCount(multi) === key.length);
  check('multi: chosen-letter lookup works over arrays', e.isChosenLetter(key, key[0]));
  check('multi: letterLabel sorts and joins', e.letterLabel(key.slice().reverse()) === key.slice().sort().join(', '));

  check('every item declares a matching select count',
    e.QUESTIONS.every(q => q.select === (Array.isArray(q.correct) ? q.correct.length : 1)));

  // ---- answer() interaction -------------------------------------------
  const opts = multi.options.map(o => o.letter);          // A..E
  const need = e.selectCount(multi);

  e.state.mode = 'exam';
  e.state.answers = {};
  e.answer(multi.id, opts[0]);
  check('multi: first pick is recorded', e.isChosenLetter(e.state.answers[multi.id], opts[0]));
  check('multi: one pick is not yet a complete answer', !e.hasAnswer(multi, e.state.answers[multi.id]));

  e.answer(multi.id, opts[0]);
  check('multi: re-clicking a pick removes it', !e.isChosenLetter(e.state.answers[multi.id], opts[0]));
  check('multi: deselecting empties the selection', e.state.answers[multi.id].length === 0);

  e.state.answers = {};
  opts.slice(0, need).forEach(L => e.answer(multi.id, L));
  check('multi: selecting N completes the answer', e.hasAnswer(multi, e.state.answers[multi.id]));
  e.answer(multi.id, opts[need]);
  check('multi: cannot exceed N selections in exam mode',
    e.state.answers[multi.id].length === need, `got ${e.state.answers[multi.id].length}`);
  check('multi: the overflow letter was not stored',
    !e.isChosenLetter(e.state.answers[multi.id], opts[need]));

  // Exam mode stays editable: deselect one, pick another.
  e.answer(multi.id, opts[0]);
  e.answer(multi.id, opts[need]);
  check('multi: exam mode allows swapping a selection',
    e.isChosenLetter(e.state.answers[multi.id], opts[need]) &&
    e.state.answers[multi.id].length === need);

  // Study mode locks a *complete* answer, but must not lock a partial one.
  e.state.mode = 'study';
  e.state.answers = {};
  e.answer(multi.id, opts[0]);
  e.answer(multi.id, opts[1]);
  check('study: a partial multi answer stays editable',
    e.state.answers[multi.id].length === Math.min(2, need));
  e.state.answers = {};
  opts.slice(0, need).forEach(L => e.answer(multi.id, L));
  const lockedSet = e.state.answers[multi.id].slice();
  e.answer(multi.id, opts[need]);
  check('study: a complete multi answer is locked',
    JSON.stringify(e.state.answers[multi.id]) === JSON.stringify(lockedSet));

  e.state.answers = {};
  const other = single.options.find(o => o.letter !== single.correct).letter;
  e.answer(single.id, single.correct);
  e.answer(single.id, other);
  check('study: a single answer is locked after one pick',
    e.state.answers[single.id] === single.correct);
  e.state.mode = 'exam';
  e.answer(single.id, other);
  check('exam: a single answer can be changed', e.state.answers[single.id] === other);
}

console.log(failures === 0 ? '\nAll engine checks passed.' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
