(() => {
  const PDF_WORKER = new URL("./vendor/pdfjs/pdf.worker.min.mjs", import.meta.url).toString();
  const REPORT_TARGET_KEY = "ccaf-score-report-target";
  const REPORT_CLEARED_KEY = "ccaf-score-report-target:cleared";
  const REPORT_VERSION = 2;
  // Every targeted practice page whose saved attempt this feature owns. The
  // report reader launches the English page per exam, and the localized
  // Foundations pages share the Foundations attempt. Keep this list explicit
  // so clearing report data cannot touch normal (untargeted) exams.
  const TARGETED_STORE_KEYS = Object.freeze([
    "ccaf-exam-en:targeted",
    "ccaf-exam-es:targeted",
    "ccaf-exam-pt:targeted",
    "ccarp-exam-en:targeted",
    "ccdvf-exam-en:targeted",
  ]);
  const MAX_FILE_BYTES = 20 * 1024 * 1024;
  const LINE_TOLERANCE = 4;
  const EXAM_DEFINITIONS = Object.freeze({
    "CCAR-F": Object.freeze({ code: "CCAR-F", name: "Claude Certified Architect Foundations" }),
    "CCAR-P": Object.freeze({ code: "CCAR-P", name: "Claude Certified Architect Professional" }),
    "CCDV-F": Object.freeze({ code: "CCDV-F", name: "Claude Certified Developer Foundations" }),
  });

  const state = {
    exams: null,
    data: null,
    examIdentity: null,
    pendingRows: null,
    selectedExamCode: null,
    rows: [],
    planVisible: false,
    storageUnavailable: false,
    uploadGeneration: 0,
  };

  let savedReportCache;
  let savedReportSource = null;

  const el = id => document.getElementById(id);

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function cleanObjectiveSpacing(value) {
    return String(value || "")
      .normalize("NFKC")
      .replace(/[\u2010-\u2015\u2212]/g, "-")
      .replace(/\s*-\s*/g, "-")
      .replace(/([,;:!?])\s*/g, "$1 ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function normalizeObjectiveText(value) {
    return cleanObjectiveSpacing(value)
      .toLowerCase()
  }

  function normalizeExamCode(value) {
    return normalizeExamText(value).replace(/\s+/g, "-");
  }

  function normalizeExamText(value) {
    return String(value ?? "")
      .normalize("NFKC")
      .toUpperCase()
      .replace(/[^A-Z0-9]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function detectExamIdentity(pageTexts) {
    const reportText = pageTexts.join("\n");
    const normalizedReportText = normalizeExamText(reportText);
    const explicitCodes = [...reportText.matchAll(
      /\bEXAM\s+CODE\b\s*[:#]?\s*([A-Z0-9]{2,}(?:\s*[-‐‑‒–—−]\s*[A-Z0-9]+)*)\b/gi,
    )]
      .map(match => normalizeExamCode(match[1]))
      .filter(Boolean)
      .filter((code, index, values) => values.indexOf(code) === index);
    const titleCodes = Object.values(EXAM_DEFINITIONS)
      .filter(exam => normalizedReportText.includes(normalizeExamText(exam.name)))
      .map(exam => exam.code);
    const uniqueTitleCodes = [...new Set(titleCodes)];

    if (explicitCodes.length > 1 || uniqueTitleCodes.length > 1) {
      return { status: "conflicting", message: "Exam details conflict. Choose the exam shown on your report." };
    }

    const explicitCode = explicitCodes[0] || null;
    const titleCode = uniqueTitleCodes[0] || null;
    if (explicitCode && titleCode && explicitCode !== titleCode) {
      return { status: "conflicting", message: "Exam details conflict. Choose the exam shown on your report." };
    }

    const code = explicitCode || titleCode;
    if (!code || !EXAM_DEFINITIONS[code]) {
      return {
        status: "unknown",
        message: code
          ? `Unknown exam code (${code}). Choose the exam shown on your report.`
          : "Couldn’t identify the exam. Choose the exam shown on your report.",
      };
    }
    return { status: "recognized", ...EXAM_DEFINITIONS[code] };
  }

  function median(numbers) {
    if (!numbers.length) return 0;
    const ordered = numbers.slice().sort((a, b) => a - b);
    const middle = Math.floor(ordered.length / 2);
    return ordered.length % 2 ? ordered[middle] : (ordered[middle - 1] + ordered[middle]) / 2;
  }

  function priority(score) {
    if (score === null || score === undefined || Number.isNaN(score)) return "unknown";
    if (score <= 50) return "focus";
    if (score <= 79) return "next";
    return "maintain";
  }

  function priorityLabel(score) {
    return ({ focus: "Focus now", next: "Practice next", maintain: "Keep warm", unknown: "Needs review" })[priority(score)];
  }

  function reportMatches(data) {
    const byText = new Map();
    Object.entries(data.objectives).forEach(([id, text]) => {
      byText.set(normalizeObjectiveText(text), id);
    });
    Object.entries(data.aliases || {}).forEach(([id, aliases]) => {
      aliases.forEach(text => byText.set(normalizeObjectiveText(text), id));
    });
    return text => byText.get(normalizeObjectiveText(text)) || null;
  }

  function tokenizeObjective(value) {
    return normalizeObjectiveText(value).split(/[^a-z0-9]+/).filter(token => token.length > 2);
  }

  function suggestObjectiveId(text) {
    if (!state.data) return null;
    const tokens = new Set(tokenizeObjective(text));
    if (!tokens.size) return null;
    let best = null;
    Object.entries(state.data.objectives).forEach(([id, objective]) => {
      const objectiveTokens = new Set(tokenizeObjective(objective));
      let overlap = 0;
      tokens.forEach(token => { if (objectiveTokens.has(token)) overlap += 1; });
      const score = overlap / Math.sqrt(tokens.size * Math.max(objectiveTokens.size, 1));
      if (!best || score > best.score) best = { id, score, overlap };
    });
    if (!best || best.overlap < 3 || best.score < 0.25) return null;
    return best;
  }

  function encodeSharePayload(record) {
    const json = JSON.stringify({ v: REPORT_VERSION, examIdentity: record.examIdentity, scores: record.scores });
    return btoa(unescape(encodeURIComponent(json))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function decodeSharePayload(value) {
    const padded = String(value || "").replace(/-/g, "+").replace(/_/g, "/");
    const json = decodeURIComponent(escape(atob(padded)));
    const payload = JSON.parse(json);
    if (!payload || typeof payload !== "object") return null;
    return JSON.stringify(payload);
  }

  function showShareStatus(message, kind = "") {
    const status = el("share-status");
    if (!status) return;
    status.textContent = message;
    status.className = `report-status ${kind}`.trim();
  }

  function mapRowsToObjectives(rows) {
    const match = reportMatches(state.data);
    return rows.map(row => {
      const objectiveId = match(row.text);
      if (objectiveId) {
        return {
          ...row,
          objectiveId,
          matchType: normalizeObjectiveText(state.data.objectives[objectiveId]) === normalizeObjectiveText(row.text) ? "exact" : "alias",
          suggestedId: null,
        };
      }
      const suggestion = suggestObjectiveId(row.text);
      return { ...row, objectiveId: null, matchType: "unknown", suggestedId: suggestion ? suggestion.id : null };
    });
  }

  function itemGeometry(item, viewport) {
    const transform = item.transform || [];
    const x = Number(transform[4]);
    const y = Number(transform[5]);
    if (!Number.isFinite(x) || !Number.isFinite(y)) return null;
    const width = Math.max(Number(item.width) || 0, 1);
    const height = Math.max(Number(item.height) || Math.abs(Number(transform[3])) || 10, 1);
    const rectangle = viewport.convertToViewportRectangle([x, y, x + width, y + height]);
    const left = Math.min(rectangle[0], rectangle[2]);
    const right = Math.max(rectangle[0], rectangle[2]);
    const top = Math.min(rectangle[1], rectangle[3]);
    const bottom = Math.max(rectangle[1], rectangle[3]);
    return { text: item.str.trim().replace(/\s+/g, " "), left, right, top, bottom, centerY: (top + bottom) / 2 };
  }

  function groupLines(items) {
    const lines = [];
    items.slice().sort((a, b) => a.centerY - b.centerY || a.left - b.left).forEach(item => {
      let line = lines[lines.length - 1];
      if (!line || Math.abs(line.y - item.centerY) > LINE_TOLERANCE) {
        line = { y: item.centerY, items: [] };
        lines.push(line);
      }
      line.items.push(item);
    });
    return lines.map(line => line.items.sort((a, b) => a.left - b.left).map(item => item.text).join(" "));
  }

  function objectiveText(items) {
    return cleanObjectiveSpacing(groupLines(items).join(" "));
  }

  async function extractReportRows(pdfjsLib, bytes) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = PDF_WORKER;
    const loadingTask = pdfjsLib.getDocument({ data: bytes });
    const pdf = await loadingTask.promise;
    const rows = [];
    const pageTexts = [];

    try {
      for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber += 1) {
        const page = await pdf.getPage(pageNumber);
        const viewport = page.getViewport({ scale: 1 });
        const content = await page.getTextContent();
        const items = content.items
          .filter(item => typeof item.str === "string" && item.str.trim())
          .map(item => itemGeometry(item, viewport))
          .filter(Boolean);
        pageTexts.push(items.map(item => item.text).join(" "));
        const percentages = items
          .map((item, index) => ({ ...item, index, value: Number(item.text.replace(/\s/g, "").replace("%", "")) }))
          .filter(item => /^\d{1,3}%$/.test(item.text.replace(/\s/g, "")) && item.value >= 0 && item.value <= 100)
          .sort((a, b) => a.centerY - b.centerY);
        if (!percentages.length) continue;

        const spacing = median(percentages.slice(1).map((item, index) => item.centerY - percentages[index].centerY));
        const edge = Math.max(18, Math.min(54, (spacing || 56) * 0.65));
        const percentColumn = Math.min(...percentages.map(item => item.left));
        const leftColumn = items.filter(item => item.right < percentColumn - 18);

        percentages.forEach((percent, index) => {
          const top = index === 0
            ? Math.max(0, percent.centerY - edge)
            : (percentages[index - 1].centerY + percent.centerY) / 2;
          const bottom = index === percentages.length - 1
            ? Math.min(viewport.height, percent.centerY + edge)
            : (percent.centerY + percentages[index + 1].centerY) / 2;
          const objective = objectiveText(leftColumn.filter(item => item.centerY >= top && item.centerY < bottom));
          if (objective) rows.push({ page: pageNumber, text: objective, score: percent.value });
        });
      }
      return { identity: detectExamIdentity(pageTexts), rows };
    } finally {
      await pdf.destroy();
    }
  }

  function showStatus(message, kind = "") {
    const status = el("report-status");
    if (!status) return;
    status.textContent = message;
    status.className = `report-status ${kind}`.trim();
  }

  function showPlanStatus(message, kind = "") {
    const status = el("plan-status");
    if (!status) return;
    status.textContent = message;
    status.className = `report-status ${kind}`.trim();
  }

  function validScore(score) {
    return Number.isInteger(score) && score >= 0 && score <= 100;
  }

  function getStorage(kind) {
    try {
      if (typeof window !== "undefined") return kind === "local" ? window.localStorage : window.sessionStorage;
      return kind === "local" && typeof localStorage !== "undefined" ? localStorage
        : (kind === "session" && typeof sessionStorage !== "undefined" ? sessionStorage : null);
    } catch {
      return null;
    }
  }

  function readStorage(kind, key) {
    const store = getStorage(kind);
    if (!store) return { available: false, raw: null };
    try {
      return { available: true, raw: store.getItem(key) };
    } catch {
      return { available: false, raw: null };
    }
  }

  function writeStorage(kind, key, raw) {
    const store = getStorage(kind);
    if (!store) return false;
    try {
      store.setItem(key, raw);
      return store.getItem(key) === raw;
    } catch {
      return false;
    }
  }

  function removeStorage(kind, key) {
    const store = getStorage(kind);
    if (!store) return false;
    try {
      store.removeItem(key);
      return store.getItem(key) === null;
    } catch {
      return false;
    }
  }

  function setPersistenceNote(saved) {
    const note = el("persistence-note");
    if (note) note.textContent = saved ? "Saved on this device" : "";
  }

  function clearTargetedAttempts() {
    let cleared = true;
    TARGETED_STORE_KEYS.forEach(key => {
      if (!removeStorage("local", key)) cleared = false;
      if (!removeStorage("session", key)) cleared = false;
    });
    return cleared;
  }

  function clearSavedStudyStorage() {
    let cleared = true;
    if (!removeStorage("local", REPORT_TARGET_KEY)) cleared = false;
    if (!removeStorage("session", REPORT_TARGET_KEY)) cleared = false;
    TARGETED_STORE_KEYS.forEach(key => {
      if (!removeStorage("local", key)) cleared = false;
      if (!removeStorage("session", key)) cleared = false;
      if (!removeStorage("local", `${key}:misses`)) cleared = false;
      if (!removeStorage("session", `${key}:misses`)) cleared = false;
    });
    // A local tombstone prevents a stale session copy in an already-open tab
    // from becoming a new report after the user explicitly deleted this one.
    if (!writeStorage("local", REPORT_CLEARED_KEY, "1")) cleared = false;
    return cleared;
  }

  function setExamData(code) {
    const exam = state.exams && state.exams[code];
    if (!exam) return false;
    state.data = exam;
    return true;
  }

  function reportIdentity(identity) {
    const definition = identity && EXAM_DEFINITIONS[identity.code];
    return definition ? { code: definition.code, name: definition.name } : null;
  }

  function parseSavedReport(raw) {
    if (!raw) return null;
    try {
      const payload = JSON.parse(raw);
      // v1 was the session-only format and implied the supported CCAF-F guide.
      // Accepting it here lets the first durable read migrate old candidates.
      const identity = payload && payload.v === 1
        ? reportIdentity(EXAM_DEFINITIONS["CCAR-F"])
        : (payload && payload.v === REPORT_VERSION ? reportIdentity(payload.examIdentity) : null);
      const entries = payload && payload.scores && typeof payload.scores === "object" && !Array.isArray(payload.scores)
        ? Object.entries(payload.scores)
        : [];
      const exam = identity && state.exams ? state.exams[identity.code] : null;
      if (!exam || !entries.length) return null;
      const scores = {};
      if (!entries.every(([id, score]) => {
        if (!Object.prototype.hasOwnProperty.call(exam.objectives, id) || !validScore(score)) return false;
        scores[id] = score;
        return true;
      })) return null;
      return { examIdentity: identity, scores };
    } catch {
      return null;
    }
  }

  function serializeSavedReport(record) {
    return JSON.stringify({ v: REPORT_VERSION, examIdentity: record.examIdentity, scores: record.scores });
  }

  // Keep the signature stable with the existing targeted-attempt payloads.
  // It is deliberately derived only from validated objective scores.
  function savedReportSignature(record) {
    return record
      ? JSON.stringify(Object.keys(record.scores).sort().map(id => [id, record.scores[id]]))
      : null;
  }

  function migrateSessionTargetedAttempts(forceSession) {
    const session = getStorage("session");
    if (!session) return;
    TARGETED_STORE_KEYS.forEach(key => {
      let sessionRaw = null;
      let localRaw = null;
      try {
        sessionRaw = session.getItem(key);
        localRaw = getStorage("local")?.getItem(key) ?? null;
      } catch {
        state.storageUnavailable = true;
        return;
      }
      if (!sessionRaw || (!forceSession && localRaw)) return;
      if (writeStorage("local", key, sessionRaw)) removeStorage("session", key);
      else state.storageUnavailable = true;
    });
  }

  function savedReport() {
    if (savedReportCache !== undefined) return savedReportCache;
    savedReportCache = null;
    savedReportSource = null;

    const durable = readStorage("local", REPORT_TARGET_KEY);
    if (!durable.available) state.storageUnavailable = true;
    const durableRecord = parseSavedReport(durable.raw);
    if (durableRecord) {
      savedReportCache = durableRecord;
      savedReportSource = "local";
      const canonical = serializeSavedReport(durableRecord);
      if (durable.raw !== canonical && !writeStorage("local", REPORT_TARGET_KEY, canonical)) {
        state.storageUnavailable = true;
      }
      // A durable report wins over any stale prototype session copies. The
      // targeted page uses the same rule, so those copies cannot reappear if
      // this tab later drops the durable report.
      removeStorage("session", REPORT_TARGET_KEY);
      TARGETED_STORE_KEYS.forEach(key => removeStorage("session", key));
      return savedReportCache;
    }

    const cleared = readStorage("local", REPORT_CLEARED_KEY);
    if (cleared.raw) {
      removeStorage("session", REPORT_TARGET_KEY);
      TARGETED_STORE_KEYS.forEach(key => removeStorage("session", key));
      return null;
    }

    const session = readStorage("session", REPORT_TARGET_KEY);
    const sessionRecord = parseSavedReport(session.raw);
    if (!sessionRecord) return null;
    savedReportCache = sessionRecord;
    savedReportSource = "session";
    const canonical = serializeSavedReport(sessionRecord);
    // A report and the in-progress targeted attempt are one migration unit.
    // If an old local attempt exists, the session attempt is the candidate's
    // current progress and must win over that stale prototype payload.
    if (writeStorage("local", REPORT_TARGET_KEY, canonical)) {
      savedReportSource = "local";
      removeStorage("session", REPORT_TARGET_KEY);
      migrateSessionTargetedAttempts(true);
    } else {
      state.storageUnavailable = true;
    }
    return savedReportCache;
  }

  function reviewHasIssues(summary = reviewSummary()) {
    return Boolean(summary.invalid || summary.duplicateIds.size);
  }

  function canBuildPlan(summary = reviewSummary()) {
    return Boolean(state.rows.length) && summary.matchedValid > 0 && !summary.invalid && !summary.duplicateIds.size;
  }

  function updateReviewVisibility(summary = reviewSummary()) {
    const review = el("review");
    if (!review) return;
    const hasRows = state.rows.length > 0;
    const isDetails = String(review.tagName || "").toLowerCase() === "details" || "open" in review;
    review.hidden = isDetails ? !hasRows : !reviewHasIssues(summary);
    if (isDetails) review.open = hasRows && (reviewHasIssues(summary) || !state.planVisible);
  }

  function updatePracticeLink(canBuild = !reviewHasIssues()) {
    const practice = el("practice-link");
    if (!practice) return;
    const practiceDisabled = !canBuild || !state.planVisible || state.storageUnavailable;
    practice.classList.toggle("disabled", practiceDisabled);
    practice.setAttribute("aria-disabled", String(practiceDisabled));
    if (state.storageUnavailable) {
      practice.title = "Targeted practice is unavailable because this browser blocked saving.";
    } else {
      practice.removeAttribute("title");
    }
  }

  function updateResultVisibility() {
    const intro = el("report-intro");
    if (intro) intro.hidden = state.planVisible;
  }

  function resetExamChoice() {
    state.pendingRows = null;
    state.selectedExamCode = null;
    const choice = el("exam-choice");
    const select = el("exam-select");
    const confirm = el("confirm-exam");
    const message = el("exam-choice-message");
    if (choice) choice.hidden = true;
    if (select) select.value = "";
    if (confirm) confirm.disabled = true;
    if (message) message.textContent = "";
  }

  function showExamChoice(message, rows) {
    state.pendingRows = rows;
    state.selectedExamCode = null;
    const choice = el("exam-choice");
    const select = el("exam-select");
    const confirm = el("confirm-exam");
    const messageElement = el("exam-choice-message");
    if (choice) choice.hidden = false;
    if (select) select.value = "";
    if (confirm) confirm.disabled = true;
    if (messageElement) messageElement.textContent = message;
  }

  function reviewSummary() {
    const matched = state.rows.filter(row => row.objectiveId).length;
    const matchedValid = state.rows.filter(row => row.objectiveId && validScore(row.score)).length;
    const unknown = state.rows.length - matched;
    const invalid = state.rows.filter(row => row.objectiveId && !validScore(row.score)).length;
    const duplicateIds = new Set();
    const seen = new Set();
    state.rows.forEach(row => {
      if (row.objectiveId && seen.has(row.objectiveId)) duplicateIds.add(row.objectiveId);
      if (row.objectiveId) seen.add(row.objectiveId);
    });
    return { matched, matchedValid, unknown, invalid, duplicateIds };
  }

  function renderReviewSummary({ updateVisibility = true } = {}) {
    const summary = reviewSummary();
    const messages = [];
    if (summary.unknown) messages.push(`${summary.unknown} row${summary.unknown === 1 ? "" : "s"} will be skipped (no objective match).`);
    if (summary.invalid) messages.push(`${summary.invalid} percentage${summary.invalid === 1 ? "" : "s"} need a value from 0 to 100.`);
    if (summary.duplicateIds.size) messages.push(`${summary.duplicateIds.size} objective${summary.duplicateIds.size === 1 ? " is" : "s are"} assigned more than once.`);
    const summaryElement = el("review-summary");
    if (summaryElement) summaryElement.textContent = messages.length ? messages.join(" ") : `${summary.matched} rows are ready.`;
    const canBuild = canBuildPlan(summary);
    const buildButton = el("build-plan");
    if (buildButton) buildButton.disabled = !canBuild;
    updatePracticeLink(canBuild);
    updateShareButtons();
    if (updateVisibility) updateReviewVisibility(summary);
  }

  function objectiveOptions(selected) {
    const options = Object.entries(state.data.objectives)
      .map(([id, text]) => `<option value="${escapeHtml(id)}"${selected === id ? " selected" : ""}>${escapeHtml(id)} · ${escapeHtml(text)}</option>`)
      .join("");
    return `<option value=""${selected ? "" : " selected"}>Needs objective match</option>${options}`;
  }

  function renderReview() {
    const summary = reviewSummary();
    const rowsToRender = reviewHasIssues(summary)
      ? state.rows.filter(row => !row.objectiveId || (row.objectiveId && !validScore(row.score)) || summary.duplicateIds.has(row.objectiveId))
      : state.rows;
    const reviewList = el("review-list");
    if (!reviewList) return;
    reviewList.innerHTML = rowsToRender.map(row => {
      const index = state.rows.indexOf(row);
      const label = row.objectiveId
        ? `${row.objectiveId} · ${state.data.themes[state.data.objectiveThemes[row.objectiveId]]}`
        : "Unmatched row";
      const suggestion = !row.objectiveId && row.suggestedId
        ? `<button type="button" class="report-text-button" data-apply-suggestion="${index}">Use suggested: ${escapeHtml(row.suggestedId)} · ${escapeHtml(state.data.objectives[row.suggestedId])}</button>`
        : "";
      const matchNote = row.objectiveId
        ? `<small>Matched ${row.matchType === "alias" ? "with the documented wording alias" : row.matchType === "suggested" ? "from a keyword suggestion" : row.matchType === "manual" ? "by your selection" : "to the objective metadata"}.</small>`
        : '<small class="report-unknown">No safe metadata match. This row will be skipped unless you choose the objective that describes it.</small>';
      return `<article class="report-row ${priority(row.score)}" data-row="${index}">
        <div class="report-row-copy">
          <div class="report-row-meta">${row.page ? `Page ${row.page} · ` : ""}${escapeHtml(label)}</div>
          <p>${escapeHtml(row.text)}</p>
          ${matchNote}
          ${suggestion}
        </div>
        <label class="report-score-field">Percent correct
          <input type="number" min="0" max="100" step="1" value="${row.score ?? ""}" data-score="${index}">
        </label>
        <div class="report-objective-field">
          <label for="objective-search-${index}">Objective</label>
          <input id="objective-search-${index}" type="search" placeholder="Search objectives…" autocomplete="off" data-objective-search="${index}" value="">
          <select data-objective="${index}">${objectiveOptions(row.objectiveId)}</select>
          <button type="button" class="report-text-button" data-browse-objectives="${index}">Browse all</button>
        </div>
      </article>`;
    }).join("");
    renderReviewSummary();
  }

  function filterObjectiveSelect(index, query) {
    const reviewList = el("review-list");
    if (!reviewList) return;
    const select = reviewList.querySelector(`select[data-objective="${index}"]`);
    if (!select) return;
    const needle = normalizeObjectiveText(query);
    Array.from(select.options).forEach(option => {
      if (!option.value) {
        option.hidden = false;
        return;
      }
      const haystack = normalizeObjectiveText(`${option.value} ${option.textContent}`);
      option.hidden = Boolean(needle) && !needle.split(/[^a-z0-9]+/).filter(Boolean).every(token => haystack.includes(token));
    });
  }

  let pickerRowIndex = null;

  function pickerEntries(query) {
    const needle = normalizeObjectiveText(query);
    const tokens = needle.split(/[^a-z0-9]+/).filter(token => token.length > 2);
    return Object.entries(state.data.objectives)
      .filter(([id, text]) => {
        if (!tokens.length) return true;
        const haystack = normalizeObjectiveText(`${id} ${text} ${state.data.themes[state.data.objectiveThemes[id]] || ""}`);
        return tokens.every(token => haystack.includes(token));
      })
      .slice(0, 30);
  }

  function renderPickerResults(query) {
    const results = el("objective-picker-results");
    const status = el("objective-picker-status");
    if (!results) return;
    const entries = state.data ? pickerEntries(query) : [];
    results.innerHTML = entries.map(([id, text]) => (
      `<li><button type="button" data-pick-objective="${escapeHtml(id)}"><strong>${escapeHtml(id)}</strong> · ${escapeHtml(text)}</button></li>`
    )).join("");
    if (status) status.textContent = entries.length ? `${entries.length} objective${entries.length === 1 ? "" : "s"}` : "No objectives match that search.";
  }

  function openObjectivePicker(index) {
    if (!state.data || !state.rows[index]) return;
    pickerRowIndex = index;
    const dialog = el("objective-picker");
    const search = el("objective-picker-search");
    if (search) search.value = "";
    renderPickerResults("");
    if (dialog && typeof dialog.showModal === "function") dialog.showModal();
    if (search) search.focus();
  }

  function applyObjectiveSelection(index, objectiveId, matchType = "manual") {
    if (!state.rows[index]) return;
    state.rows[index].objectiveId = objectiveId || null;
    state.rows[index].matchType = objectiveId ? matchType : "unknown";
    if (!objectiveId) {
      const suggestion = suggestObjectiveId(state.rows[index].text);
      state.rows[index].suggestedId = suggestion ? suggestion.id : null;
    } else {
      state.rows[index].suggestedId = null;
    }
  }

  function useParsedRows(identity, rows) {
    state.examIdentity = identity;
    setExamData(identity.code);
    state.rows = mapRowsToObjectives(rows);
    state.pendingRows = null;
    const choice = el("exam-choice");
    const messageElement = el("exam-choice-message");
    if (choice) choice.hidden = true;
    if (messageElement) messageElement.textContent = "";
    renderReview();

    const summary = reviewSummary();
    if (!canBuildPlan(summary)) {
      showStatus("A few rows need correction before your guide is ready.", "error");
      return;
    }
    if (summary.unknown) {
      showStatus(`Report loaded with ${summary.matchedValid} matched row${summary.matchedValid === 1 ? "" : "s"}. ${summary.unknown} unmatched row${summary.unknown === 1 ? "" : "s"} will be skipped.`, "success");
    } else {
      showStatus("Report loaded.", "success");
    }
    buildPlan();
  }

  function restoreSavedPlan() {
    const saved = savedReport();
    if (!saved) return false;
    state.examIdentity = { status: "restored", ...saved.examIdentity };
    state.rows = Object.entries(saved.scores).map(([id, score]) => ({
      page: null,
      text: state.data.objectives[id],
      score,
      objectiveId: id,
      matchType: "exact",
    }));
    state.planVisible = true;
    if (savedReportSource === "local") setPersistenceNote(true);
    renderReview();
    renderPlan();
    showStatus("");
    return true;
  }

  function saveTarget() {
    const summary = reviewSummary();
    if (!canBuildPlan(summary)) return false;
    const scores = {};
    state.rows.forEach(row => { if (row.objectiveId && validScore(row.score)) scores[row.objectiveId] = row.score; });
    const identity = reportIdentity(state.examIdentity);
    if (!identity || !setExamData(identity.code)) return false;
    const next = { examIdentity: identity, scores };
    const previousRaw = readStorage("local", REPORT_TARGET_KEY);
    const previous = parseSavedReport(previousRaw.raw);
    const changed = !previous || savedReportSignature(previous) !== savedReportSignature(next);
    const raw = serializeSavedReport(next);
    if (!writeStorage("local", REPORT_TARGET_KEY, raw)) {
      state.storageUnavailable = true;
      setPersistenceNote(false);
      renderReviewSummary();
      return false;
    }
    // Only invalidate an old targeted attempt after the replacement report is
    // durably verified. Failed or abandoned uploads therefore leave it intact.
    const targetedCleared = !changed || clearTargetedAttempts();
    const markerCleared = removeStorage("local", REPORT_CLEARED_KEY);
    savedReportCache = next;
    savedReportSource = "local";
    state.storageUnavailable = !targetedCleared || !markerCleared;
    setPersistenceNote(true);
    renderReviewSummary();
    return true;
  }

  function readingLinks(row) {
    const reading = state.data.readings[row.objectiveId];
    const broad = state.data.themeReadings[state.data.objectiveThemes[row.objectiveId]] || [];
    const links = [reading, ...broad].filter(Boolean).filter((item, index, all) => all.findIndex(other => other.href === item.href) === index);
    return links.map(item => `<a href="${escapeHtml(item.href)}">${escapeHtml(item.label)}</a>`).join(" · ");
  }

  function practiceLink(row) {
    const subdomain = state.data.objectiveSubdomains[row.objectiveId];
    const href = `${state.data.practice.bank.href}#${encodeURIComponent(subdomain || "")}`;
    const count = state.data.questionCounts[row.objectiveId] || 0;
    return `<a href="${href}">${count ? `${count} related bank questions` : "Browse the question bank"}</a>`;
  }

  function readingText(row) {
    const reading = state.data.readings[row.objectiveId];
    const broad = state.data.themeReadings[state.data.objectiveThemes[row.objectiveId]] || [];
    const links = [reading, ...broad].filter(Boolean).filter((item, index, all) => all.findIndex(other => other.href === item.href) === index);
    return links.map(item => `${item.label} (${item.href})`).join("; ");
  }

  function orderedPlanRows() {
    const rows = state.rows.filter(row => row.objectiveId && validScore(row.score));
    const weighted = rows.length > 0 && rows.every(row => recoverable(row) !== null);
    return rows.sort(weighted
      ? (a, b) => recoverable(b) - recoverable(a) || a.score - b.score ||
                  a.objectiveId.localeCompare(b.objectiveId)
      : (a, b) => a.score - b.score || a.objectiveId.localeCompare(b.objectiveId));
  }

  function buildStudyGuideMarkdown() {
    const rows = orderedPlanRows();
    const exam = state.examIdentity ? `${state.examIdentity.code} · ${state.examIdentity.name}` : "";
    const date = new Date().toISOString().slice(0, 10);
    const weighted = rows.length > 0 && rows.every(row => recoverable(row) !== null);
    const orderNote = weighted
      ? "Ordered by how much of the exam each objective still has available, not by raw score."
      : "Ordered weakest first.";
    const lines = [`# Personalized study guide — ${exam}`, ``,
                   `Exported ${date}. Scores are percent correct per objective. ${orderNote}`, ``];
    const groups = planGroups(rows, weighted);
    let index = 0;
    groups.forEach(group => {
      if (group.meta) {
        lines.push(`# ${group.meta.name} — ${group.meta.weight}% of the exam`);
        lines.push(``);
      }
      group.rows.forEach(row => {
      const id = row.objectiveId;
      const guidance = state.data.guidance[id] || {};
      const gain = recoverable(row);
      const gainNote = gain === null ? "" : `, up to ${formatPoints(gain)} of the exam`;
      lines.push(`## ${String(++index).padStart(2, "0")} · ${id} — ${row.score}% (${priorityLabel(row.score)})${gainNote}`);
      lines.push(``);
      lines.push(`${state.data.objectives[id]}`);
      lines.push(``);
      if (guidance.explanation) lines.push(`Concept: ${guidance.explanation}`);
      if (guidance.example) lines.push(`Example: ${guidance.example}`);
      if (guidance.guidance) lines.push(`What to look for: ${guidance.guidance}`);
      lines.push(``);
      const reading = readingText(row);
      if (reading) lines.push(`Further reading: ${reading}`);
      const count = state.data.questionCounts[id] || 0;
      lines.push(`Related questions: ${count ? `${count} bank questions` : "question bank"} (${state.data.practice.bank.href}#${id})`);
      lines.push(``);
      });
    });
    return lines.join("\n");
  }

  function downloadBlob(filename, text, type) {
    const blob = new Blob([text], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function currentSavedRecord() {
    const summary = reviewSummary();
    if (!canBuildPlan(summary)) return null;
    const scores = {};
    state.rows.forEach(row => { if (row.objectiveId && validScore(row.score)) scores[row.objectiveId] = row.score; });
    const identity = reportIdentity(state.examIdentity);
    if (!identity) return null;
    return { examIdentity: identity, scores };
  }

  function updateShareButtons() {
    const ready = Boolean(currentSavedRecord()) && state.planVisible && !state.storageUnavailable;
    ["download-guide", "copy-guide-link", "copy-exam-link", "save-exam-file"].forEach(id => {
      const button = el(id);
      if (button) button.disabled = !ready;
    });
  }

  // How much of the exam one objective is worth: its domain's published weight
  // split evenly across that domain's objectives. The report scores objectives,
  // not domains, and nothing published says how the weight divides inside a
  // domain, so an even split is the honest assumption rather than a guess
  // dressed up as precision.
  function objectiveShare(objectiveId) {
    const data = state.data;
    if (!data || !data.domains || !data.objectiveDomains) return null;
    const domain = data.objectiveDomains[objectiveId];
    const meta = domain ? data.domains[domain] : null;
    if (!meta || typeof meta.weight !== "number") return null;
    const siblings = Object.values(data.objectiveDomains).filter(d => d === domain).length;
    return siblings ? meta.weight / siblings : null;
  }

  // Percentage points of the whole exam still on the table for this objective.
  // Ordering by this rather than by raw score is the difference between "your
  // worst score" and "where studying actually moves the number".
  function recoverable(row) {
    const share = objectiveShare(row.objectiveId);
    if (share === null) return null;
    return share * (100 - row.score) / 100;
  }

  function formatPoints(value) {
    return (value >= 10 ? Math.round(value) : Math.round(value * 10) / 10) + " pts";
  }

  // Groups rows by exam domain, heaviest recoverable total first. Rows whose
  // domain cannot be resolved stay in one trailing group with no heading.
  function planGroups(rows, weighted) {
    if (!weighted) return [{ meta: null, rows }];
    const domainOf = row => (state.data.objectiveDomains || {})[row.objectiveId] || null;
    const buckets = new Map();
    rows.forEach(row => {
      const key = domainOf(row);
      if (!buckets.has(key)) buckets.set(key, []);
      buckets.get(key).push(row);
    });
    const total = list => list.reduce((sum, row) => sum + (recoverable(row) || 0), 0);
    return [...buckets.entries()]
      .sort((a, b) => total(b[1]) - total(a[1]))
      .map(([key, list]) => ({ meta: key ? state.data.domains[key] : null, rows: list, total: total(list) }));
  }

  function renderPlan() {
    const matched = orderedPlanRows();
    // Weighted ordering needs every row to resolve a domain weight; without it
    // the plan falls back to weakest-first and the domain grouping is skipped.
    const weighted = matched.length > 0 && matched.every(row => recoverable(row) !== null);
    const weak = matched.filter(row => row.score < 80);
    const other = matched.filter(row => row.score >= 80);
    const planCount = el("plan-count");
    if (planCount) {
      planCount.textContent = weak.length
        ? `${weak.length} priority topic${weak.length === 1 ? "" : "s"}${other.length ? ` · ${other.length} other` : ""}`
        : `${other.length} topic${other.length === 1 ? "" : "s"} to maintain`;
    }

    const renderCard = (row, index) => {
      const id = row.objectiveId;
      const guidance = state.data.guidance[id];
      const level = priority(row.score);
      const gain = recoverable(row);
      const gainHtml = gain === null ? "" :
        `<strong class="study-gain" title="Estimated share of the exam still available on this objective">${formatPoints(gain)}</strong>`;
      return `<article class="study-card ${level}" data-objective="${escapeHtml(id)}">
        <div class="study-card-head"><span class="study-priority">${escapeHtml(priorityLabel(row.score))}</span><span class="study-score">scored ${row.score}%</span>${gainHtml}</div>
        <h3>${escapeHtml(state.data.objectives[id])}</h3>
        <details class="study-guidance">
          <summary>Explanation, example &amp; guidance</summary>
          <h4>The concept</h4><p>${escapeHtml(guidance.explanation)}</p>
          <h4>Example</h4><p>${escapeHtml(guidance.example)}</p>
          <h4>What to look for</h4><p>${escapeHtml(guidance.guidance)}</p>
          <p class="study-links"><strong>Further reading:</strong> ${readingLinks(row)}<br><strong>Related questions:</strong> ${practiceLink(row)}</p>
        </details>
      </article>`;
    };

    // The plan is grouped by exam domain and the domains are ordered by how much
    // of the score sits in each, so reading top to bottom is the study order.
    // A flat list of 26 equal cards gave a candidate no way to see that four of
    // their gaps were in one domain worth a quarter of the exam.
    const ordered = planGroups(weak, weighted);

    const sections = [];
    if (!weak.length && other.length) {
      sections.push('<p class="study-positive">Strong work so far. Keep these topics warm:</p>');
    }
    if (weak.length && weighted && ordered.length && ordered[0].meta) {
      const topMeta = ordered[0].meta, topRows = ordered[0].rows;
      sections.push(
        `<p class="plan-lede">Your biggest gain is in <strong>${escapeHtml(topMeta.name)}</strong> — ` +
        `${topMeta.weight}% of the exam, with ${topRows.length} topic${topRows.length === 1 ? "" : "s"} ` +
        `to fix. Topics below are ordered by how much of the score each one puts back.</p>`);
    }

    let index = 0;
    ordered.forEach(group => {
      const meta = group.meta, rows = group.rows, total = group.total || 0;
      const cards = rows.map(row => renderCard(row, index++)).join("");
      if (!meta) { sections.push(cards); return; }
      sections.push(
        `<section class="plan-domain">` +
          `<h2 class="plan-domain-name">${escapeHtml(meta.name)}</h2>` +
          `<p class="plan-domain-meta">${meta.weight}% of the exam · ` +
            `${rows.length} topic${rows.length === 1 ? "" : "s"} to fix` +
            (total > 0 ? ` · up to ${formatPoints(total)} back` : "") + `</p>` +
          cards +
        `</section>`);
    });
    if (other.length) {
      sections.push(`<details class="plan-strong"><summary>Topics you already have (${other.length})</summary>${other.map((row, i) => renderCard(row, weak.length + i)).join("")}</details>`);
    }
    if (weak.length && weighted) {
      sections.push('<p class="plan-estimate-note">Points are an estimate: each domain\u2019s published ' +
        'weight split evenly across its objectives, times the share you missed. Nothing published says how ' +
        'the weight divides inside a domain, so treat the order as guidance rather than arithmetic.</p>');
    }
    const planList = el("plan-list");
    if (planList) planList.innerHTML = sections.join("");
    const plan = el("plan");
    if (plan) plan.hidden = !state.planVisible;
    const resultExam = el("result-exam");
    if (resultExam) resultExam.textContent = state.examIdentity ? `${state.examIdentity.code} · ${state.examIdentity.name}` : "";
    const practice = el("practice-link");
    if (practice && state.data && state.data.practice) practice.href = `${state.data.practice.href}?targeted=1`;
    const practiceNote = el("practice-note");
    if (practiceNote && state.data && state.data.practice) practiceNote.textContent = `${state.data.practice.questions} questions focused on your weak areas`;
    updateResultVisibility();
    updateReviewVisibility();
    showPlanStatus(
      state.planVisible && state.storageUnavailable
        ? "Targeted practice is unavailable because this browser blocked saving."
        : "",
      state.planVisible && state.storageUnavailable ? "error" : "",
    );
    updatePracticeLink(!reviewHasIssues());
    updateShareButtons();
  }

  function buildPlan() {
    const summary = reviewSummary();
    if (!canBuildPlan(summary)) return;
    const targetSaved = saveTarget();
    state.planVisible = true;
    renderPlan();
    const plan = el("plan");
    if (plan && typeof plan.scrollIntoView === "function") plan.scrollIntoView({ behavior: "smooth", block: "start" });
    if (!targetSaved) showPlanStatus("Targeted practice is unavailable because this browser blocked saving.", "error");
  }

  function applyReviewChange(target, index) {
    if (target.dataset.score !== undefined) {
      const value = target.value === "" ? null : Number(target.value);
      state.rows[index].score = Number.isInteger(value) && value >= 0 && value <= 100 ? value : null;
      return;
    }
    if (target.dataset.objective !== undefined) {
      applyObjectiveSelection(index, target.value || null, target.value ? "manual" : "unknown");
    }
  }

  function refreshVisiblePlan() {
    if (!state.planVisible) return;
    const summary = reviewSummary();
    if (!canBuildPlan(summary)) {
      state.planVisible = false;
      renderPlan();
      return;
    }
    saveTarget();
    renderPlan();
  }

  function handleReviewChange(event) {
    const target = event.target;
    const index = Number(target.dataset.score ?? target.dataset.objective);
    if (!Number.isInteger(index) || !state.rows[index]) return;
    const before = reviewSummary();
    applyReviewChange(target, index);
    const after = reviewSummary();
    const correctionStateChanged = reviewHasIssues(before) !== reviewHasIssues(after);
    const scoreEdit = target.dataset.score !== undefined;
    const deferScoreCommit = scoreEdit && event.type === "input";
    if (!scoreEdit && (target.dataset.objective !== undefined || correctionStateChanged)) renderReview();
    else renderReviewSummary({ updateVisibility: !deferScoreCommit });
    const commit = !scoreEdit || event.type === "change";
    if (!reviewHasIssues(after) && !state.planVisible) {
      if (commit) buildPlan();
    } else if (commit || !scoreEdit) {
      refreshVisiblePlan();
    }
  }

  function handleReviewSearch(event) {
    const target = event.target;
    if (target.dataset && target.dataset.objectiveSearch !== undefined) {
      filterObjectiveSelect(Number(target.dataset.objectiveSearch), target.value);
    }
  }

  function handleReviewClick(event) {
    const suggestion = event.target.closest("[data-apply-suggestion]");
    if (suggestion) {
      const index = Number(suggestion.dataset.applySuggestion);
      const row = state.rows[index];
      if (row && row.suggestedId) {
        applyObjectiveSelection(index, row.suggestedId, "suggested");
        renderReview();
        refreshVisiblePlan();
        if (!reviewHasIssues() && !state.planVisible) buildPlan();
      }
      return;
    }
    const browse = event.target.closest("[data-browse-objectives]");
    if (browse) {
      openObjectivePicker(Number(browse.dataset.browseObjectives));
      return;
    }
    const pick = event.target.closest("[data-pick-objective]");
    if (pick && pickerRowIndex !== null) {
      const index = pickerRowIndex;
      applyObjectiveSelection(index, pick.dataset.pickObjective, "manual");
      const dialog = el("objective-picker");
      if (dialog && typeof dialog.close === "function") dialog.close();
      pickerRowIndex = null;
      renderReview();
      refreshVisiblePlan();
      if (!reviewHasIssues() && !state.planVisible) buildPlan();
    }
  }

  function handleDownloadGuide() {
    const record = currentSavedRecord();
    if (!record || !state.planVisible) return;
    downloadBlob(`${record.examIdentity.code.toLowerCase()}-study-guide.md`, buildStudyGuideMarkdown(), "text/markdown");
    showShareStatus("Study guide downloaded.", "success");
  }

  function practiceUrlForRecord(record) {
    const path = (state.data && state.data.practice && state.data.practice.href) || "practical/en.html";
    const url = new URL(path, window.location.href);
    url.searchParams.set("targeted", "1");
    url.hash = `r=${encodeSharePayload(record)}`;
    return url.toString();
  }

  function guideUrlForRecord(record) {
    const url = new URL(window.location.pathname, window.location.href);
    url.hash = `r=${encodeSharePayload(record)}`;
    return url.toString();
  }

  async function handleCopyGuideLink() {
    const record = currentSavedRecord();
    if (!record) return;
    const url = guideUrlForRecord(record);
    try {
      await navigator.clipboard.writeText(url);
      showShareStatus("Study guide link copied. Opening it restores this exact study guide.", "success");
    } catch {
      showShareStatus(url, "");
    }
  }

  async function handleCopyExamLink() {
    const record = currentSavedRecord();
    if (!record) return;
    const url = practiceUrlForRecord(record);
    try {
      await navigator.clipboard.writeText(url);
      showShareStatus("Custom exam link copied. Opening it restores this exact targeted set.", "success");
    } catch {
      showShareStatus(url, "");
    }
  }

  function handleSaveExamFile() {
    const record = currentSavedRecord();
    if (!record) return;
    downloadBlob(`${record.examIdentity.code.toLowerCase()}-custom-exam.json`, serializeSavedReport(record), "application/json");
    showShareStatus("Custom exam saved.", "success");
  }

  function importSharedRecord(raw, sourceLabel) {
    const parsed = parseSavedReport(raw);
    if (!parsed) {
      showShareStatus("That custom exam file or link is not valid for this site.", "error");
      return false;
    }
    if (!setExamData(parsed.examIdentity.code)) return false;
    state.examIdentity = { status: "restored", ...parsed.examIdentity };
    state.rows = Object.entries(parsed.scores).map(([id, score]) => ({
      page: null,
      text: state.data.objectives[id],
      score,
      objectiveId: id,
      matchType: "exact",
      suggestedId: null,
    }));
    savedReportCache = parsed;
    savedReportSource = "local";
    if (!writeStorage("local", REPORT_TARGET_KEY, serializeSavedReport(parsed))) state.storageUnavailable = true;
    removeStorage("local", REPORT_CLEARED_KEY);
    state.planVisible = true;
    renderReview();
    renderPlan();
    showShareStatus(sourceLabel ? `Custom exam loaded from ${sourceLabel}.` : "Custom exam loaded.", "success");
    return true;
  }

  function handleLoadExamFile(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => importSharedRecord(String(reader.result || ""), "file");
    reader.readAsText(file);
    event.target.value = "";
  }

  function importHashRecord() {
    const hash = String(window.location.hash || "");
    const match = hash.match(/#r=([A-Za-z0-9\-_]+)/);
    if (!match) return false;
    try {
      return importSharedRecord(decodeSharePayload(match[1]), "link");
    } catch {
      return false;
    }
  }

  function confirmExamSelection() {
    const select = el("exam-select");
    const code = select ? select.value : "";
    const identity = EXAM_DEFINITIONS[code];
    if (!identity || !state.pendingRows) return;

    state.selectedExamCode = code;
    state.examIdentity = { status: "selected", ...identity };

    if (!state.pendingRows.length) {
      const message = "No score rows found. Choose the original score report PDF.";
      const messageElement = el("exam-choice-message");
      if (messageElement) messageElement.textContent = message;
      showStatus(message, "error");
      return;
    }

    useParsedRows({ status: "selected", ...identity }, state.pendingRows);
  }

  function resetReport() {
    state.uploadGeneration += 1;
    state.examIdentity = null;
    state.pendingRows = null;
    state.selectedExamCode = null;
    state.rows = [];
    state.planVisible = false;
    state.storageUnavailable = false;
    setPersistenceNote(false);

    resetExamChoice();
    const file = el("report-file");
    if (file) file.value = "";
    const review = el("review");
    if (review) {
      review.hidden = true;
      if ("open" in review) review.open = false;
    }
    const plan = el("plan");
    if (plan) plan.hidden = true;
    const reviewList = el("review-list");
    if (reviewList) reviewList.innerHTML = "";
    const planList = el("plan-list");
    if (planList) planList.innerHTML = "";
    const resultExam = el("result-exam");
    if (resultExam) resultExam.textContent = "";
    showStatus("");
    showPlanStatus("");
    showShareStatus("");
    updateResultVisibility();
    updatePracticeLink(false);
    updateShareButtons();
  }

  function deleteSavedStudy() {
    state.uploadGeneration += 1;
    const cleared = clearSavedStudyStorage();
    savedReportCache = undefined;
    savedReportSource = null;
    resetReport();
    if (cleared) {
      showStatus("Saved study data deleted.", "success");
    } else {
      state.storageUnavailable = true;
      showStatus("Saved study data was cleared where possible, but this browser blocked some storage changes.", "error");
    }
  }

  function replaceReport() {
    const file = el("report-file");
    if (file && typeof file.click === "function") file.click();
  }

  async function handleFile(file) {
    if (!file) return;
    const uploadGeneration = ++state.uploadGeneration;
    state.examIdentity = null;
    resetExamChoice();
    state.rows = [];
    state.planVisible = false;
    state.storageUnavailable = false;
    setPersistenceNote(false);
    const review = el("review");
    if (review) {
      review.hidden = true;
      if ("open" in review) review.open = false;
    }
    const plan = el("plan");
    if (plan) plan.hidden = true;
    showPlanStatus("");
    updateResultVisibility();
    renderReviewSummary();
    if (file.size > MAX_FILE_BYTES) {
      showStatus("This PDF is larger than 20 MB. Choose the score-report PDF only.", "error");
      return;
    }
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      showStatus("Choose a PDF score report.", "error");
      return;
    }
    showStatus("Reading the PDF locally…", "busy");
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (uploadGeneration !== state.uploadGeneration) return;
      const { identity, rows } = await extractReportRows(window.pdfjsLib, bytes);
      if (uploadGeneration !== state.uploadGeneration) return;
      if (identity.status !== "recognized") {
        showStatus(identity.message, "error");
        showExamChoice(identity.message, rows);
        return;
      }
      state.examIdentity = identity;
      if (!rows.length) {
        showStatus("No score rows found. Choose the original score report PDF.", "error");
        return;
      }
      useParsedRows(identity, rows);
    } catch (error) {
      if (uploadGeneration !== state.uploadGeneration) return;
      console.error("Score report parsing failed", error);
      showStatus("Couldn’t read this as a score report. Try the original PDF export.", "error");
    }
  }

  async function init() {
    try {
      const response = await fetch("score-report-data.json");
      if (!response.ok) throw new Error(`Data request failed: ${response.status}`);
      state.exams = (await response.json()).exams;
      const saved = savedReport();
      if (saved) setExamData(saved.examIdentity.code);
      const pdfjs = await import("./vendor/pdfjs/pdf.min.mjs");
      window.pdfjsLib = pdfjs;
      el("report-file").addEventListener("change", event => handleFile(event.target.files[0]));
      el("review-list").addEventListener("input", handleReviewSearch);
      el("review-list").addEventListener("input", handleReviewChange);
      el("review-list").addEventListener("change", handleReviewChange);
      el("review-list").addEventListener("click", handleReviewClick);
      const pickerSearch = el("objective-picker-search");
      if (pickerSearch) pickerSearch.addEventListener("input", event => renderPickerResults(event.target.value));
      const pickerClose = el("objective-picker-close");
      if (pickerClose) pickerClose.addEventListener("click", () => {
        const dialog = el("objective-picker");
        if (dialog && typeof dialog.close === "function") dialog.close();
        pickerRowIndex = null;
      });
      const picker = el("objective-picker");
      if (picker) picker.addEventListener("click", handleReviewClick);
      const examSelect = el("exam-select");
      const confirmExam = el("confirm-exam");
      if (examSelect) {
        examSelect.addEventListener("change", event => {
          if (confirmExam) confirmExam.disabled = !EXAM_DEFINITIONS[event.target.value];
        });
      }
      if (confirmExam) confirmExam.addEventListener("click", confirmExamSelection);
      const buildButton = el("build-plan");
      if (buildButton) buildButton.addEventListener("click", buildPlan);
      const practice = el("practice-link");
      if (practice) practice.addEventListener("click", event => {
        if (practice.classList.contains("disabled") || !saveTarget()) event.preventDefault();
      });
      const replace = el("replace-report");
      if (replace) replace.addEventListener("click", replaceReport);
      const deleteSaved = el("delete-saved-study");
      if (deleteSaved) deleteSaved.addEventListener("click", deleteSavedStudy);
      const download = el("download-guide");
      if (download) download.addEventListener("click", handleDownloadGuide);
      const copyGuideLink = el("copy-guide-link");
      if (copyGuideLink) copyGuideLink.addEventListener("click", handleCopyGuideLink);
      const copyLink = el("copy-exam-link");
      if (copyLink) copyLink.addEventListener("click", handleCopyExamLink);
      const saveFile = el("save-exam-file");
      if (saveFile) saveFile.addEventListener("click", handleSaveExamFile);
      const loadFile = el("load-exam-file");
      if (loadFile) loadFile.addEventListener("change", handleLoadExamFile);
      if (typeof window !== "undefined" && window.addEventListener) {
        window.addEventListener("storage", event => {
          if (event.key !== REPORT_TARGET_KEY && event.key !== REPORT_CLEARED_KEY) return;
          savedReportCache = undefined;
          savedReportSource = null;
          resetReport();
          if (event.key === REPORT_TARGET_KEY && event.newValue) {
            const saved = parseSavedReport(event.newValue);
            if (saved) setExamData(saved.examIdentity.code);
            restoreSavedPlan();
          }
        });
      }
      showStatus("");
      renderReviewSummary();
      if (!importHashRecord()) restoreSavedPlan();
      updateShareButtons();
      // A share link opened while this page is already at score-report.html is a
      // same-document navigation: nothing re-runs init, so without this the
      // second link silently kept showing the first one's plan.
      if (typeof window !== "undefined" && window.addEventListener) {
        window.addEventListener("hashchange", () => {
          if (importHashRecord()) updateShareButtons();
        });
      }
    } catch (error) {
      console.error("Score report feature failed to load", error);
      showStatus("The score-report tool could not load its local PDF reader. Refresh the page or rebuild the site.", "error");
    }
  }

  init();
})();
