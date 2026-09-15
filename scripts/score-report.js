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

  function mapRowsToObjectives(rows) {
    const match = reportMatches(state.data);
    return rows.map(row => {
      const objectiveId = match(row.text);
      return {
        ...row,
        objectiveId,
        matchType: objectiveId
          ? (normalizeObjectiveText(state.data.objectives[objectiveId]) === normalizeObjectiveText(row.text) ? "exact" : "alias")
          : "unknown",
      };
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
    return Boolean(summary.unknown || summary.invalid || summary.duplicateIds.size);
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
    const unknown = state.rows.length - matched;
    const invalid = state.rows.filter(row => !validScore(row.score)).length;
    const duplicateIds = new Set();
    const seen = new Set();
    state.rows.forEach(row => {
      if (row.objectiveId && seen.has(row.objectiveId)) duplicateIds.add(row.objectiveId);
      if (row.objectiveId) seen.add(row.objectiveId);
    });
    return { matched, unknown, invalid, duplicateIds };
  }

  function renderReviewSummary({ updateVisibility = true } = {}) {
    const summary = reviewSummary();
    const messages = [];
    if (summary.unknown) messages.push(`${summary.unknown} row${summary.unknown === 1 ? "" : "s"} need an objective selection.`);
    if (summary.invalid) messages.push(`${summary.invalid} percentage${summary.invalid === 1 ? "" : "s"} need a value from 0 to 100.`);
    if (summary.duplicateIds.size) messages.push(`${summary.duplicateIds.size} objective${summary.duplicateIds.size === 1 ? " is" : "s are"} assigned more than once.`);
    const summaryElement = el("review-summary");
    if (summaryElement) summaryElement.textContent = messages.length ? messages.join(" ") : `${summary.matched} rows are ready.`;
    const canBuild = state.rows.length > 0 && !summary.unknown && !summary.invalid && !summary.duplicateIds.size;
    const buildButton = el("build-plan");
    if (buildButton) buildButton.disabled = !canBuild;
    updatePracticeLink(canBuild);
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
      ? state.rows.filter(row => !row.objectiveId || !validScore(row.score) || summary.duplicateIds.has(row.objectiveId))
      : state.rows;
    const reviewList = el("review-list");
    if (!reviewList) return;
    reviewList.innerHTML = rowsToRender.map(row => {
      const index = state.rows.indexOf(row);
      const label = row.objectiveId
        ? `${row.objectiveId} · ${state.data.themes[state.data.objectiveThemes[row.objectiveId]]}`
        : "Unmatched row";
      return `<article class="report-row ${priority(row.score)}" data-row="${index}">
        <div class="report-row-copy">
          <div class="report-row-meta">${row.page ? `Page ${row.page} · ` : ""}${escapeHtml(label)}</div>
          <p>${escapeHtml(row.text)}</p>
          ${row.objectiveId ? `<small>Matched ${row.matchType === "alias" ? "with the documented wording alias" : "to the objective metadata"}.</small>` : "<small class=\"report-unknown\">No safe metadata match. Choose the objective that describes this row.</small>"}
        </div>
        <label class="report-score-field">Percent correct
          <input type="number" min="0" max="100" step="1" value="${row.score ?? ""}" data-score="${index}">
        </label>
        <label class="report-objective-field">Objective
          <select data-objective="${index}">${objectiveOptions(row.objectiveId)}</select>
        </label>
      </article>`;
    }).join("");
    renderReviewSummary();
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

    if (reviewHasIssues()) {
      showStatus("A few rows need correction before your guide is ready.", "error");
      return;
    }
    showStatus("Report loaded.", "success");
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
    if (summary.unknown || summary.invalid || summary.duplicateIds.size || !state.rows.length) return false;
    const scores = {};
    state.rows.forEach(row => { scores[row.objectiveId] = row.score; });
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

  function renderPlan() {
    const matched = state.rows.filter(row => row.objectiveId && validScore(row.score))
      .sort((a, b) => a.score - b.score || a.objectiveId.localeCompare(b.objectiveId));
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
      return `<article class="study-card ${level}" data-objective="${escapeHtml(id)}">
        <div class="study-card-head"><span class="study-rank">${String(index + 1).padStart(2, "0")}</span><span class="study-priority">${escapeHtml(priorityLabel(row.score))}</span><strong>${row.score}%</strong></div>
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

    const sections = [];
    if (!weak.length && other.length) sections.push('<p class="study-positive">Strong work so far. Keep these topics warm:</p>');
    sections.push(weak.map(renderCard).join(""));
    if (other.length) {
      sections.push(`<details><summary>Other topics</summary>${other.map((row, index) => renderCard(row, weak.length + index)).join("")}</details>`);
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
  }

  function buildPlan() {
    const summary = reviewSummary();
    if (summary.unknown || summary.invalid || summary.duplicateIds.size || !state.rows.length) return;
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
    state.rows[index].objectiveId = target.value || null;
    state.rows[index].matchType = target.value ? "manual" : "unknown";
  }

  function refreshVisiblePlan() {
    if (!state.planVisible) return;
    const summary = reviewSummary();
    if (summary.unknown || summary.invalid || summary.duplicateIds.size) {
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
    updateResultVisibility();
    updatePracticeLink(false);
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
      el("review-list").addEventListener("input", handleReviewChange);
      el("review-list").addEventListener("change", handleReviewChange);
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
      restoreSavedPlan();
    } catch (error) {
      console.error("Score report feature failed to load", error);
      showStatus("The score-report tool could not load its local PDF reader. Refresh the page or rebuild the site.", "error");
    }
  }

  init();
})();
