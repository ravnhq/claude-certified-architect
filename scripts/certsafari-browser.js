// Load in Codex's cua_repl after selecting the in-app browser.
// lanes: [{tab: <quiz tab>, exam: 'CCAR-F', end: false}, ...]
// sink: a tab opened at http://127.0.0.1:8768/ by certsafari_receiver.py.
// Run at most 15 questions per lane per call, then report the saved counts.
function createCertSafariCollector(lanes, sink) {
  const collector = { lanes, sink, batch: [], known: new Map(), repeated: 0 };
  collector.expected = { 'CCAR-F': 480, 'CCAR-P': 456, 'CCDV-F': 524 };
  const submit = /^Submit/;
  collector.normalize = text => text.replace(/^[A-Z]\)\s*/, '').replace(/\s+/g, ' ').trim();
  collector.key = record => JSON.stringify([
    record.exam, record.question.replace(/\s+/g, ' ').trim(), record.options.map(collector.normalize).sort(),
  ]);
  collector.loadKnown = async function () {
    await sink.goto('http://127.0.0.1:8768/known');
    await sink.playwright.domSnapshot();
    const rows = JSON.parse(await sink.playwright.locator('pre').innerText());
    for (const record of rows) collector.known.set(collector.key(record), record);
    return collector.known.size;
  };

  collector.capture = async function (lane) {
    const tab = lane.tab;
    const state = await tab.playwright.domSnapshot();
    const role = await tab.playwright.getByRole('radio').count() ? 'radio' : 'checkbox';
    const question = await tab.playwright.getByRole('heading').first().innerText();
    const options = await tab.playwright.getByRole(role).evaluateAll(elements => elements.map(element => element.parentElement.innerText.trim()));
    const key = collector.key({ exam: lane.exam, question, options });
    const known = collector.known.get(key);
    if (!state.includes('Copy study prompt')) {
      const count = role === 'radio' ? 1 : Number(state.match(/Select (\d+) answers/)?.[1]);
      if (!count) throw new Error('Unrecognized question format');
      // These are collection attempts, not the user's measured exam performance.
      const chosen = known ? options.map((text, i) => known.correct_answers.some(answer =>
        collector.normalize(answer) === collector.normalize(text)) ? i : -1).filter(i => i >= 0)
        : Array.from({ length: count }, (_, i) => i);
      if (chosen.length !== count) throw new Error('Answer count mismatch');
      for (const i of chosen) await tab.playwright.getByRole(role).nth(i).click();
      await tab.playwright.domSnapshot();
      await tab.playwright.getByRole('button', { name: submit }).click();
      await tab.playwright.domSnapshot();
    }
    if (known) { collector.repeated++; return null; }
    for (const button of await tab.playwright.getByRole('button', { name: 'Explanation', exact: true }).all()) {
      if (await button.getAttribute('aria-expanded') !== 'true') await button.click();
    }
    // A successful click can precede the accordion's actual expansion.
    await tab.playwright.domSnapshot();
    for (const button of await tab.playwright.getByRole('button', { name: 'Explanation', exact: true }).all()) {
      if (await button.getAttribute('aria-expanded') !== 'true') {
        await button.click();
        await tab.playwright.domSnapshot();
      }
    }
    const snapshot = await tab.playwright.domSnapshot();
    const answers = await tab.playwright.getByRole(role).evaluateAll(elements => elements.map(element => ({
      text: element.parentElement.innerText.trim(),
      correct: element.parentElement.classList.contains('border-success'),
    })));
    const correct = answers.filter(answer => answer.correct).map(answer => answer.text);
    if (!correct.length) throw new Error('Missing correct answer');
    const record = {
      exam: lane.exam,
      source: await tab.url(),
      question,
      options: answers.map(answer => answer.text),
      correct_answers: correct,
      explanations: await tab.playwright.getByRole('region', { name: 'Explanation', exact: true }).allTextContents({}),
      snapshot,
      captured_at: new Date().toISOString(),
    };
    if (record.options.length !== record.explanations.length) throw new Error('Incomplete explanations; current question retained for retry');
    collector.known.set(key, record);
    return record;
  };

  collector.save = async function () {
    if (!collector.batch.length) return 'No new records';
    await sink.goto('http://127.0.0.1:8768/');
    await sink.playwright.domSnapshot();
    await sink.playwright.getByRole('textbox', { name: 'Question batch' }).fill(JSON.stringify(collector.batch));
    await sink.playwright.getByRole('button', { name: 'Save batch', exact: true }).click();
    await sink.playwright.getByRole('heading', { name: 'Saved', exact: true }).waitFor({ state: 'visible', timeoutMs: 10000 });
    const result = await sink.playwright.domSnapshot();
    if (!result.includes('heading "Saved"')) throw new Error(result);
    collector.batch.length = 0;
    return result;
  };

  collector.runLane = async function (lane, count) {
    for (let i = 0; i < count && !lane.end; i++) {
      if ([...collector.known.values()].filter(record => record.exam === lane.exam).length >= collector.expected[lane.exam]) {
        lane.end = true;
        lane.paused = true;
        lane.complete = true;
        return;
      }
      const record = await collector.capture(lane);
      if (record) collector.batch.push(record);
      const state = await lane.tab.playwright.domSnapshot();
      if (state.includes('button "Finish Quiz"')) {
        await lane.tab.playwright.getByRole('button', { name: 'Finish Quiz', exact: true }).click();
        await lane.tab.playwright.getByRole('heading', { name: 'Quiz Complete', exact: true }).waitFor({ state: 'visible', timeoutMs: 15000 });
        lane.end = true;
        return;
      }
      await lane.tab.playwright.getByRole('button', { name: 'Next Question', exact: true }).click();
      await lane.tab.playwright.domSnapshot();
      try {
        await lane.tab.playwright.getByRole('button', { name: submit }).waitFor({ state: 'visible', timeoutMs: 15000 });
      } catch (error) {
        const fresh = await lane.tab.playwright.domSnapshot();
        if (!fresh.includes('come back tomorrow')) throw error;
        for (const session of lanes) { session.paused = true; session.end = true; }
        collector.limit = 'CertSafari daily practice limit: resume tomorrow';
        return;
      }
    }
  };

  collector.run = async function (count = 15) {
    if (!Number.isInteger(count) || count < 1 || count * lanes.length > 60) throw new Error('Batch too large');
    const results = await Promise.allSettled(lanes.map(lane => collector.runLane(lane, count)));
    const saved = await collector.save();
    return { saved, lanes: results.map((result, i) => ({
      exam: lanes[i].exam, end: lanes[i].end, status: result.status, error: result.reason?.message,
    })) };
  };

  collector.restart = async function () {
    for (const lane of lanes) {
      if (!lane.end || lane.paused) continue;
      const state = await lane.tab.playwright.domSnapshot();
      if (state.includes('button "New Quiz"') && await lane.tab.playwright.getByRole('button', { name: 'New Quiz', exact: true }).isEnabled()) {
        await lane.tab.playwright.getByRole('button', { name: 'New Quiz', exact: true }).click();
        await lane.tab.playwright.domSnapshot();
      }
      try {
        await lane.tab.playwright.getByRole('button', { name: submit }).waitFor({ state: 'visible', timeoutMs: 15000 });
      } catch (error) {
        const fresh = await lane.tab.playwright.domSnapshot();
        if (!fresh.includes('button "Submit')) { lane.pending = fresh.slice(-900); continue; }
      }
      lane.end = false;
    }
  };
  return collector;
}
