#!/usr/bin/env python3
"""Build exam_<lang>.html — the unified CCAF practice quiz.

Usage: python3 utils/build_exam_html.py [lang ...]   (lang: en es pt — default: all)

Merges the 76 scenario questions and the 60 domain questions (see exam_data.py)
into one quiz per language with:
  * sidebar grouped by CCAF domain
  * study mode (reveal on answer) vs exam mode (reveal at the end)
  * per-option explanations
  * randomized question order within each domain (persisted, so a refresh keeps
    the same order and answers)
  * scoring over the full total with a pass threshold and a per-domain breakdown
"""
import base64, json, os, sys

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
sys.path.insert(0, UTILS_DIR)
import exam_data  # noqa: E402

PASS_PCT = 72  # per-domain bar coloring threshold (study approximation)
PASS_SCORE = 720  # overall cut score on the 100–1000 scale (real exam cut)
PER_DOMAIN = 12  # questions drawn per domain each attempt → 5 × 12 = 60 total

LANG_TITLES = {
    "en": "Claude Certified Architect — Practice Exam",
    "es": "Claude Certified Architect — Examen de Práctica",
    "pt": "Claude Certified Architect — Exame de Prática",
}
LANG_LABELS = {"en": "English", "es": "Español", "pt": "Português"}

# All user-facing UI strings, per language.
UI = {
    "en": {
        "questions": "Questions", "answered": "Answered", "mode_study": "Study",
        "mode_exam": "Exam", "mode_hint_study": "Answers reveal as you go",
        "mode_hint_exam": "Answers reveal at the end",
        "prev": "← Prev", "next": "Next →", "finish": "Finish &amp; Review",
        "question": "Question", "your_answer": "Your answer", "correct": "Correct",
        "why": "Why", "complete": "Exam Complete", "answered_of":
        "You answered {a} of {t} questions.", "unanswered":
        "&#9888; {n} question(s) not answered (counted as incorrect).",
        "score": "Score", "pass": "PASS", "fail": "FAIL", "by_domain":
        "Score by domain", "review_wrong": "Review incorrect answers",
        "all_correct": "Every question correct — outstanding!",
        "restart": "Restart (new draw)", "weight": "weight",
        "threshold_note": ("Pass mark set at {p}/1000. Each attempt draws 12 "
                           "random questions per domain (60 total); the score "
                           "is scaled to 1000 as a study approximation of the "
                           "real 100–1000 scaled score."),
        "incorrect": "incorrect", "domain": "Domain",
    },
    "es": {
        "questions": "Preguntas", "answered": "Respondidas", "mode_study": "Estudio",
        "mode_exam": "Examen", "mode_hint_study": "Las respuestas se revelan al instante",
        "mode_hint_exam": "Las respuestas se revelan al final",
        "prev": "← Anterior", "next": "Siguiente →", "finish": "Finalizar y revisar",
        "question": "Pregunta", "your_answer": "Tu respuesta", "correct": "Correcta",
        "why": "Por qué", "complete": "Examen completado", "answered_of":
        "Respondiste {a} de {t} preguntas.", "unanswered":
        "&#9888; {n} pregunta(s) sin responder (cuentan como incorrectas).",
        "score": "Puntaje", "pass": "APROBADO", "fail": "REPROBADO", "by_domain":
        "Puntaje por dominio", "review_wrong": "Revisar respuestas incorrectas",
        "all_correct": "¡Todas correctas — excelente!",
        "restart": "Reiniciar (nuevo sorteo)", "weight": "peso",
        "threshold_note": ("Aprobación fijada en {p}/1000. Cada intento sortea "
                           "12 preguntas aleatorias por dominio (60 en total); "
                           "el puntaje se escala sobre 1000 como aproximación "
                           "de estudio de la escala real de 100–1000."),
        "incorrect": "incorrectas", "domain": "Dominio",
    },
    "pt": {
        "questions": "Perguntas", "answered": "Respondidas", "mode_study": "Estudo",
        "mode_exam": "Exame", "mode_hint_study": "As respostas aparecem na hora",
        "mode_hint_exam": "As respostas aparecem no final",
        "prev": "← Anterior", "next": "Próxima →", "finish": "Finalizar e revisar",
        "question": "Pergunta", "your_answer": "Sua resposta", "correct": "Correta",
        "why": "Por que", "complete": "Exame concluído", "answered_of":
        "Você respondeu {a} de {t} perguntas.", "unanswered":
        "&#9888; {n} pergunta(s) sem resposta (contam como incorretas).",
        "score": "Pontuação", "pass": "APROVADO", "fail": "REPROVADO", "by_domain":
        "Pontuação por domínio", "review_wrong": "Revisar respostas incorretas",
        "all_correct": "Todas corretas — excelente!",
        "restart": "Reiniciar (novo sorteio)", "weight": "peso",
        "threshold_note": ("Aprovação definida em {p}/1000. Cada tentativa "
                           "sorteia 12 perguntas aleatórias por domínio (60 no "
                           "total); a pontuação é escalada para 1000 como "
                           "aproximação de estudo da escala real de 100–1000."),
        "incorrect": "incorretas", "domain": "Domínio",
    },
}

_FAVICON_PATH = os.path.join(ROOT_DIR, "docs", "assets", "favicon.png")
try:
    _FAVICON_DATA_URI = "data:image/png;base64," + base64.b64encode(
        open(_FAVICON_PATH, "rb").read()).decode()
except FileNotFoundError:
    _FAVICON_DATA_URI = ""

RAVN_LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 64" '
    'aria-label="Ravn" role="img" width="86" height="22">'
    '<text x="0" y="48" font-family="Inter, -apple-system, BlinkMacSystemFont, '
    "'Segoe UI', Roboto, system-ui, sans-serif\" font-size=\"52\" "
    'font-weight="800" letter-spacing="-2" fill="currentColor">ravn</text></svg>'
)

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body { font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 16px; line-height: 1.6; background: #f0f2f5; color: #1a1a2e;
  height: 100vh; overflow: hidden; display: flex; flex-direction: column; }

.ravn-topbar { position: sticky; top: 0; z-index: 20; display: flex; align-items: center;
  justify-content: space-between; padding: 12px 32px; background: #0f1019; color: #f5f5f0;
  border-bottom: 1px solid #2c2c4a; flex-shrink: 0; }
.ravn-brand { display: inline-flex; align-items: baseline; gap: 14px; color: #f5f5f0;
  text-decoration: none; font-weight: 600; letter-spacing: -0.01em; }
.ravn-brand:hover { color: #f6c87a; }
.ravn-brand svg { color: currentColor; flex-shrink: 0; }
.ravn-brand-tagline { font-size: 13px; color: #9aa0b3; text-transform: uppercase; letter-spacing: 0.14em; }

/* Mode toggle in the brand bar */
.mode-toggle { display: inline-flex; align-items: center; gap: 0; background: #1a1a2e;
  border: 1px solid #2c2c4a; border-radius: 8px; overflow: hidden; }
.mode-toggle button { background: none; border: none; color: #9aa0b3; cursor: pointer;
  font-size: 12.5px; font-weight: 600; padding: 6px 14px; transition: background .15s, color .15s; }
.mode-toggle button.active { background: #2b6cb0; color: #fff; }
.mode-hint { font-size: 11.5px; color: #6b7280; margin-left: 12px; }

.shell { display: flex; flex: 1; min-height: 0; overflow: hidden; }

.sidebar { width: 272px; min-width: 272px; background: #1a1a2e; color: #cdd3de;
  display: flex; flex-direction: column; overflow: hidden; min-height: 0; }
.sidebar-header { padding: 18px 16px 12px; font-size: 13px; font-weight: 700;
  letter-spacing: .06em; text-transform: uppercase; color: #7f8fa6;
  border-bottom: 1px solid #2c2c4a; flex-shrink: 0; }
.sidebar-progress { padding: 10px 16px; font-size: 12px; color: #7f8fa6;
  border-bottom: 1px solid #2c2c4a; flex-shrink: 0; }
.sidebar-progress span { color: #e2e8f0; font-weight: 600; }
.sidebar-scroll { overflow-y: auto; flex: 1; padding: 8px 0; }
.sidebar-scroll::-webkit-scrollbar { width: 4px; }
.sidebar-scroll::-webkit-scrollbar-thumb { background: #2c2c4a; border-radius: 2px; }

.domain-group { margin-bottom: 6px; }
.domain-label { padding: 8px 16px 5px; font-size: 10.5px; font-weight: 700;
  letter-spacing: .06em; text-transform: uppercase; color: #5a6b8c;
  display: flex; justify-content: space-between; gap: 8px; }
.domain-label .dl-weight { color: #4a5568; font-weight: 600; }
.q-btn { display: flex; align-items: center; gap: 8px; width: 100%; padding: 6px 16px;
  background: none; border: none; cursor: pointer; font-size: 13.5px; color: #a0aec0;
  text-align: left; transition: background .15s, color .15s; border-left: 3px solid transparent; }
.q-btn:hover { background: #242447; color: #e2e8f0; }
.q-btn.active { background: #1e3a5f; color: #63b3ed; border-left-color: #63b3ed; }
.q-btn.answered .q-dot { background: #63b3ed; }
.q-btn.answered-correct { color: #68d391; }
.q-btn.answered-correct .q-dot { background: #68d391; }
.q-btn.answered-wrong { color: #fc8181; }
.q-btn.answered-wrong .q-dot { background: #fc8181; }
.q-dot { width: 7px; height: 7px; border-radius: 50%; background: #4a5568;
  flex-shrink: 0; transition: background .2s; }

.main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-height: 0; min-width: 0; }
.topbar { background: #fff; border-bottom: 1px solid #e2e8f0; padding: 12px 32px;
  display: flex; align-items: center; justify-content: space-between; flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0,0,0,.06); }
.topbar-title { font-size: 15px; font-weight: 600; color: #2d3748; }
.topbar-nav { display: flex; gap: 10px; align-items: center; }
.nav-btn { padding: 7px 18px; border-radius: 8px; border: 1.5px solid #cbd5e0; background: #fff;
  font-size: 14px; cursor: pointer; color: #4a5568; font-weight: 500; transition: all .15s; }
.nav-btn:hover { background: #edf2f7; border-color: #a0aec0; }
.nav-btn:disabled { opacity: .35; cursor: default; }
.nav-btn.finish { background: #2b6cb0; color: #fff; border-color: #2b6cb0; }
.nav-btn.finish:hover { background: #2c5282; }
.q-counter { font-size: 13px; color: #718096; font-weight: 500; }

.content { flex: 1; overflow-y: auto; padding: 36px 48px; }
.content::-webkit-scrollbar { width: 6px; }
.content::-webkit-scrollbar-thumb { background: #cbd5e0; border-radius: 3px; }

.q-card { max-width: 820px; margin: 0 auto; }
.q-domain { display: inline-block; background: #ebf8ff; color: #2b6cb0; font-size: 12px;
  font-weight: 700; letter-spacing: .04em; text-transform: uppercase; padding: 4px 12px;
  border-radius: 20px; margin-bottom: 8px; }
.q-scenario { display: inline-block; background: #f0eaff; color: #6b46c1; font-size: 11.5px;
  font-weight: 700; letter-spacing: .04em; padding: 4px 12px; border-radius: 20px;
  margin-bottom: 16px; margin-left: 8px; }
.q-number { font-size: 13px; color: #a0aec0; margin-bottom: 6px; font-weight: 600; }
.q-situation { font-size: 16.5px; color: #1a202c; font-weight: 500; line-height: 1.7;
  background: #fff; border: 1.5px solid #d0dff0; border-radius: 10px; padding: 16px 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06); margin-bottom: 22px; }
.q-situation code, .opt-text code, .explanation code, .opt-expl code {
  background: #e2e8f0; padding: 1px 5px; border-radius: 4px;
  font-family: "SF Mono", Menlo, Monaco, monospace; font-size: 13.5px; color: #2d3748; }
.q-prompt { font-size: 17px; font-weight: 700; color: #1a202c; margin-bottom: 20px; }

.options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }
.option { border: 2px solid #e2e8f0; border-radius: 12px; background: #fff;
  transition: border-color .15s, background .15s; overflow: hidden; }
.option-head { display: flex; align-items: flex-start; gap: 14px; padding: 14px 18px; cursor: pointer; }
.option:hover:not(.locked) .option-head { background: #ebf8ff; }
.option.locked .option-head { cursor: default; }
.option.selected { border-color: #90cdf4; }
.opt-letter { width: 30px; height: 30px; min-width: 30px; border-radius: 50%; background: #edf2f7;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px;
  color: #4a5568; transition: background .2s, color .2s; flex-shrink: 0; }
.option.selected .opt-letter { background: #90cdf4; color: #1a365d; }
.opt-text { font-size: 15px; color: #2d3748; line-height: 1.55; padding-top: 3px; }
.option.correct { border-color: #48bb78; background: #f0fff4; }
.option.correct .opt-letter { background: #48bb78; color: #fff; }
.option.wrong { border-color: #fc8181; background: #fff5f5; }
.option.wrong .opt-letter { background: #fc8181; color: #fff; }
.option.dimmed { opacity: .6; }
.opt-expl { display: none; font-size: 13.5px; line-height: 1.6; color: #4a5568;
  padding: 0 18px 14px 62px; }
.option.locked .opt-expl.show { display: block; }
.option.correct .opt-expl { color: #276749; }
.option.wrong .opt-expl { color: #9b2c2c; }

.explanation { margin-top: 4px; padding: 14px 18px; background: #fffbeb;
  border-left: 4px solid #f6ad55; border-radius: 0 10px 10px 0; font-size: 14.5px;
  color: #744210; line-height: 1.65; display: none; }
.explanation.show { display: block; }
.explanation strong { color: #744210; }

.summary { max-width: 860px; margin: 0 auto; display: none; }
.summary.show { display: block; }
.summary h1 { font-size: 26px; font-weight: 800; color: #1a202c; margin-bottom: 6px; }
.summary-subtitle { color: #718096; font-size: 15px; margin-bottom: 22px; }
.verdict { display: inline-block; font-size: 15px; font-weight: 800; letter-spacing: .08em;
  padding: 6px 18px; border-radius: 24px; margin-bottom: 22px; }
.verdict.pass { background: #c6f6d5; color: #22543d; }
.verdict.fail { background: #fed7d7; color: #822727; }
.score-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-bottom: 14px; }
.score-card { background: #fff; border-radius: 14px; padding: 20px; text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,.07); }
.score-card .big { font-size: 38px; font-weight: 800; line-height: 1; margin-bottom: 6px; }
.score-card .label { font-size: 13px; color: #718096; font-weight: 600;
  text-transform: uppercase; letter-spacing: .05em; }
.score-card.total .big { color: #2b6cb0; }
.score-card.correct-c .big { color: #38a169; }
.score-card.wrong-c .big { color: #e53e3e; }
.threshold-note { font-size: 12.5px; color: #a0aec0; margin-bottom: 26px; }

.domain-scores { background: #fff; border-radius: 12px; padding: 8px 20px; margin-bottom: 26px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.ds-row { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-bottom: 1px solid #f0f0f0; }
.ds-row:last-child { border-bottom: none; }
.ds-name { flex: 1; font-size: 14px; font-weight: 600; color: #2d3748; }
.ds-name small { color: #a0aec0; font-weight: 500; }
.ds-bar { width: 160px; height: 8px; background: #edf2f7; border-radius: 5px; overflow: hidden; }
.ds-bar > div { height: 100%; background: #48bb78; }
.ds-bar > div.low { background: #f6ad55; }
.ds-bar > div.bad { background: #fc8181; }
.ds-pct { width: 92px; text-align: right; font-size: 13px; color: #4a5568; font-weight: 600; }

.section-title { font-size: 18px; font-weight: 700; color: #2d3748; margin-bottom: 12px;
  padding-bottom: 6px; border-bottom: 2px solid #e2e8f0; }
.group-block { background: #fff; border-radius: 12px; padding: 18px 20px; margin-bottom: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.group-title { font-size: 15px; font-weight: 700; color: #2d3748; margin-bottom: 12px;
  display: flex; align-items: center; gap: 10px; }
.group-badge { font-size: 11px; padding: 2px 10px; border-radius: 20px; font-weight: 700;
  background: #fff5f5; color: #c53030; }
.wrong-item { display: flex; gap: 10px; align-items: flex-start; padding: 12px 0;
  border-bottom: 1px solid #f0f0f0; font-size: 14px; color: #4a5568; }
.wrong-item:last-child { border-bottom: none; }
.wrong-item .wi-n { min-width: 36px; font-weight: 700; color: #a0aec0; font-size: 12px; padding-top: 2px; }
.wrong-item .wi-q { flex: 1; }
.wrong-item .wi-situation { font-size: 13.5px; color: #2d3748; font-weight: 500; margin-bottom: 4px; line-height: 1.5; }
.wrong-item .wi-prompt { font-size: 13px; color: #718096; font-style: italic; margin-bottom: 4px; }
.wrong-item .wi-ans { font-size: 12.5px; margin-top: 3px; color: #718096; }
.wi-wrong-tag { color: #e53e3e; font-weight: 700; }
.wi-correct-tag { color: #38a169; font-weight: 700; }
.wi-expl { font-size: 12.5px; color: #744210; background: #fffbeb; border-radius: 6px;
  padding: 8px 10px; margin-top: 6px; line-height: 1.55; }

.restart-btn { margin-top: 28px; padding: 12px 32px; background: #2b6cb0; color: #fff;
  border: none; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer;
  transition: background .15s; }
.restart-btn:hover { background: #2c5282; }
.screen { display: none; }
.screen.active { display: block; }
"""

JS = r"""
const QUESTIONS = __DATA__;
const DOMAINS = __DOMAINS__;
const T = __UI__;
const PASS_PCT = __PASS__;          // per-domain bar coloring threshold (%)
const PASS_SCORE = __PASS_SCORE__;  // overall cut score on the 100–1000 scale
const PER_DOMAIN = __PER_DOMAIN__;  // questions drawn per domain each attempt
const STORE_KEY = "ccaf-exam-__LANG__";

// Number of questions in one attempt: PER_DOMAIN per domain, capped by how many
// that domain actually has (so it never over-draws a small domain).
function examSize() {
  const byDomain = {};
  QUESTIONS.forEach(q => { byDomain[q.domain] = (byDomain[q.domain] || 0) + 1; });
  return Object.values(byDomain).reduce((s, c) => s + Math.min(c, PER_DOMAIN), 0);
}

const state = { current: 0, answers: {}, order: [], mode: "study" };

// ---- persistence ---------------------------------------------------------
function save() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(
    { answers: state.answers, order: state.order, mode: state.mode, current: state.current })); } catch (e) {}
}
function load() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return null;
    const d = JSON.parse(raw);
    // Order is valid only if it still matches the current attempt size.
    if (!Array.isArray(d.order) || d.order.length !== examSize()) return null;
    const ids = new Set(QUESTIONS.map(q => q.id));
    if (!d.order.every(id => ids.has(id))) return null;
    return d;
  } catch (e) { return null; }
}

// ---- order ---------------------------------------------------------------
// Draw PER_DOMAIN random questions from each domain (the "question bank"
// behavior), keeping domains in order. Within a domain the drawn questions are
// already in random order from the shuffle. Option order is never shuffled (the
// answer key is by letter).
function shuffleOrder() {
  const byDomain = {};
  QUESTIONS.forEach(q => { (byDomain[q.domain] = byDomain[q.domain] || []).push(q.id); });
  const order = [];
  Object.keys(byDomain).sort((a, b) => a - b).forEach(d => {
    const ids = byDomain[d].slice();
    for (let i = ids.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [ids[i], ids[j]] = [ids[j], ids[i]];
    }
    order.push(...ids.slice(0, PER_DOMAIN));
  });
  return order;
}
function qById(id) { return QUESTIONS.find(q => q.id === id); }
function orderedQuestions() { return state.order.map(qById); }

function md(text) {
  if (!text) return "";
  return text.replace(/`([^`]+)`/g, "<code>$1</code>")
             .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
             .replace(/\n/g, " ");
}

// ---- sidebar -------------------------------------------------------------
function buildSidebar() {
  const list = document.getElementById("sidebarList");
  list.innerHTML = "";
  document.getElementById("totalCount").textContent = state.order.length;
  const qs = orderedQuestions();
  let curDomain = null, groupEl = null;
  qs.forEach((q, idx) => {
    if (q.domain !== curDomain) {
      curDomain = q.domain;
      const sg = document.createElement("div");
      sg.className = "domain-group";
      const lbl = document.createElement("div");
      lbl.className = "domain-label";
      const dm = DOMAINS[q.domain];
      lbl.innerHTML = "<span>" + T.domain + " " + q.domain + " · " + dm.name +
        "</span><span class='dl-weight'>" + dm.weight + "%</span>";
      sg.appendChild(lbl);
      groupEl = sg;
      list.appendChild(sg);
    }
    const btn = document.createElement("button");
    btn.className = "q-btn";
    btn.id = "sb-" + idx;
    btn.onclick = () => goto(idx);
    btn.innerHTML = "<span class='q-dot'></span> " + (idx + 1);
    groupEl.appendChild(btn);
  });
}

function updateSidebar() {
  const qs = orderedQuestions();
  qs.forEach((q, idx) => {
    const btn = document.getElementById("sb-" + idx);
    if (!btn) return;
    btn.className = "q-btn";
    if (idx === state.current) btn.classList.add("active");
    const ans = state.answers[q.id];
    if (ans !== undefined) {
      if (state.mode === "exam") btn.classList.add("answered");
      else btn.classList.add(ans === q.correct ? "answered-correct" : "answered-wrong");
    }
  });
  document.getElementById("answeredCount").textContent = Object.keys(state.answers).length;
}

// ---- question render -----------------------------------------------------
function renderQuestion(idx) {
  const qs = orderedQuestions();
  const q = qs[idx];
  const chosen = state.answers[q.id];
  const reveal = chosen !== undefined && state.mode === "study";

  document.getElementById("qCounter").textContent = (idx + 1) + " / " + qs.length;
  document.getElementById("prevBtn").disabled = idx === 0;
  document.getElementById("nextBtn").disabled = idx === qs.length - 1;

  const dm = DOMAINS[q.domain];
  const scenarioTag = q.scenario ? "<span class='q-scenario'>" + q.scenario + "</span>" : "";
  const situation = q.situation ? "<div class='q-situation'>" + md(q.situation) + "</div>" : "";

  const optionsHtml = q.options.map(opt => {
    let cls = "option";
    const isChosen = opt.letter === chosen;
    if (reveal) {
      cls += " locked";
      if (opt.correct) cls += " correct";
      else if (isChosen) cls += " wrong";
      else cls += " dimmed";
    } else if (isChosen) {
      cls += " selected";
    }
    // In study mode after answering, show explanation for the correct option
    // and for the (wrong) one the user picked.
    const showExpl = reveal && opt.explanation && (opt.correct || isChosen);
    const expl = opt.explanation
      ? "<div class='opt-expl" + (showExpl ? " show" : "") + "'>" + md(opt.explanation) + "</div>"
      : "";
    return "<div class='" + cls + "' data-letter='" + opt.letter + "'>" +
      "<div class='option-head' onclick=\"answer('" + q.id + "','" + opt.letter + "')\">" +
        "<div class='opt-letter'>" + opt.letter + "</div>" +
        "<div class='opt-text'>" + md(opt.text) + "</div>" +
      "</div>" + expl + "</div>";
  }).join("");

  document.getElementById("qCard").innerHTML =
    "<div class='q-number'>" + T.question + " " + (idx + 1) + "</div>" +
    "<div><span class='q-domain'>" + T.domain + " " + q.domain + " · " + dm.name + "</span>" +
    scenarioTag + "</div>" +
    situation +
    "<div class='q-prompt'>" + md(q.question) + "</div>" +
    "<div class='options'>" + optionsHtml + "</div>";
}

function answer(id, letter) {
  if (state.mode === "study" && state.answers[id] !== undefined) return; // locked
  state.answers[id] = letter;
  save();
  renderQuestion(state.current);
  updateSidebar();
}

function navigate(dir) { goto(state.current + dir); }
function goto(idx) {
  const qs = orderedQuestions();
  if (idx < 0 || idx >= qs.length) return;
  document.getElementById("questionScreen").classList.add("active");
  document.getElementById("summaryScreen").classList.remove("active");
  state.current = idx;
  save();
  renderQuestion(idx);
  updateSidebar();
}

function setMode(mode) {
  state.mode = mode;
  document.getElementById("modeStudy").classList.toggle("active", mode === "study");
  document.getElementById("modeExam").classList.toggle("active", mode === "exam");
  document.getElementById("modeHint").textContent =
    mode === "study" ? T.mode_hint_study : T.mode_hint_exam;
  save();
  renderQuestion(state.current);
  updateSidebar();
}

// ---- summary -------------------------------------------------------------
function showSummary() {
  document.getElementById("questionScreen").classList.remove("active");
  document.getElementById("summaryScreen").classList.add("active");

  // Only the questions in this attempt (PER_DOMAIN per domain) count.
  const active = orderedQuestions();
  const total = active.length;
  const answered = Object.keys(state.answers).length;
  let correct = 0;
  const wrongByDomain = {};
  const domStat = {};

  active.forEach(q => {
    domStat[q.domain] = domStat[q.domain] || { correct: 0, total: 0 };
    domStat[q.domain].total++;
    const ans = state.answers[q.id];
    if (ans === undefined) return;
    if (ans === q.correct) { correct++; domStat[q.domain].correct++; }
    else { (wrongByDomain[q.domain] = wrongByDomain[q.domain] || []).push({ q, chosen: ans }); }
  });

  const wrong = answered - correct;
  const unanswered = total - answered;
  const pct = total ? Math.round(correct / total * 100) : 0;
  const score = total ? Math.round(correct / total * 1000) : 0; // scaled to 1000
  const passed = score >= PASS_SCORE;

  let domainScoresHtml = "";
  Object.keys(domStat).sort((a, b) => a - b).forEach(d => {
    const s = domStat[d], dm = DOMAINS[d];
    const dpct = s.total ? Math.round(s.correct / s.total * 100) : 0;
    const barCls = dpct >= PASS_PCT ? "" : (dpct >= 50 ? "low" : "bad");
    domainScoresHtml +=
      "<div class='ds-row'>" +
        "<div class='ds-name'>" + T.domain + " " + d + " · " + dm.name +
          " <small>(" + dm.weight + "% " + T.weight + ")</small></div>" +
        "<div class='ds-bar'><div class='" + barCls + "' style='width:" + dpct + "%'></div></div>" +
        "<div class='ds-pct'>" + s.correct + "/" + s.total + " · " + dpct + "%</div>" +
      "</div>";
  });

  let wrongGroupsHtml = "";
  Object.keys(wrongByDomain).sort((a, b) => a - b).forEach(d => {
    const items = wrongByDomain[d], dm = DOMAINS[d];
    const rows = items.map(item => {
      const chosenOpt = item.q.options.find(o => o.letter === item.chosen);
      const correctOpt = item.q.options.find(o => o.letter === item.q.correct);
      const expl = correctOpt && correctOpt.explanation
        ? "<div class='wi-expl'><strong>" + T.why + " " + item.q.correct + ":</strong> " +
          md(correctOpt.explanation) + "</div>" : "";
      return "<div class='wrong-item'>" +
        "<div class='wi-n'>" + item.q.id.toUpperCase() + "</div>" +
        "<div class='wi-q'>" +
          (item.q.situation ? "<div class='wi-situation'>" + md(item.q.situation) + "</div>" : "") +
          "<div class='wi-prompt'>" + md(item.q.question) + "</div>" +
          "<div class='wi-ans'>" + T.your_answer + ": <span class='wi-wrong-tag'>" + item.chosen +
            "</span> — " + md(chosenOpt ? chosenOpt.text : "") + "<br>" +
            T.correct + ": <span class='wi-correct-tag'>" + item.q.correct + "</span> — " +
            md(correctOpt ? correctOpt.text : "") + "</div>" + expl +
        "</div></div>";
    }).join("");
    wrongGroupsHtml += "<div class='group-block'><div class='group-title'>" +
      T.domain + " " + d + " · " + dm.name +
      "<span class='group-badge'>" + items.length + " " + T.incorrect + "</span></div>" + rows + "</div>";
  });

  const unansweredNote = unanswered > 0
    ? "<p style='color:#e53e3e;font-size:14px;margin-bottom:18px;font-weight:600;'>" +
      T.unanswered.replace("{n}", unanswered) + "</p>" : "";

  document.getElementById("summaryContent").innerHTML =
    "<h1>" + T.complete + "</h1>" +
    "<p class='summary-subtitle'>" + T.answered_of.replace("{a}", answered).replace("{t}", total) + "</p>" +
    "<div class='verdict " + (passed ? "pass" : "fail") + "'>" + (passed ? T.pass : T.fail) + "</div>" +
    unansweredNote +
    "<div class='score-grid'>" +
      "<div class='score-card total'><div class='big'>" + score +
        "<span style='font-size:18px;color:#a0aec0;font-weight:700;'>/1000</span></div>" +
        "<div class='label'>" + T.score + "</div></div>" +
      "<div class='score-card correct-c'><div class='big'>" + correct + "</div><div class='label'>" + T.correct + "</div></div>" +
      "<div class='score-card wrong-c'><div class='big'>" + (wrong + unanswered) + "</div><div class='label'>" + T.incorrect + "</div></div>" +
    "</div>" +
    "<p class='threshold-note'>" + T.threshold_note.replace("{p}", PASS_SCORE) + "</p>" +
    "<div class='section-title'>" + T.by_domain + "</div>" +
    "<div class='domain-scores'>" + domainScoresHtml + "</div>" +
    ((wrong + unanswered) > 0
      ? "<div class='section-title'>" + T.review_wrong + "</div>" + wrongGroupsHtml
      : "<p style='color:#38a169;font-weight:700;font-size:17px;'>" + T.all_correct + "</p>") +
    "<button class='restart-btn' onclick='restart()'>" + T.restart + "</button>";
}

function restart() {
  state.answers = {};
  state.current = 0;
  state.order = shuffleOrder();
  save();
  buildSidebar();
  document.getElementById("questionScreen").classList.add("active");
  document.getElementById("summaryScreen").classList.remove("active");
  renderQuestion(0);
  updateSidebar();
}

// ---- init ----------------------------------------------------------------
(function init() {
  const saved = load();
  if (saved) {
    state.answers = saved.answers || {};
    state.order = saved.order;
    state.mode = saved.mode || "study";
    state.current = Math.min(saved.current || 0, state.order.length - 1);
  } else {
    state.order = shuffleOrder();
  }
  setMode(state.mode);
  buildSidebar();
  renderQuestion(state.current);
  updateSidebar();
})();
"""


def build(lang):
    questions = exam_data.load(lang)
    ui = UI[lang]
    domains_js = {
        str(d): {"name": exam_data.DOMAIN_NAMES[lang][d], "weight": w}
        for d, (_, w) in exam_data.DOMAINS.items()
    }

    js = (JS.replace("__DATA__", json.dumps(questions, ensure_ascii=False))
            .replace("__DOMAINS__", json.dumps(domains_js, ensure_ascii=False))
            .replace("__UI__", json.dumps(ui, ensure_ascii=False))
            .replace("__PASS__", str(PASS_PCT))
            .replace("__PASS_SCORE__", str(PASS_SCORE))
            .replace("__PER_DOMAIN__", str(PER_DOMAIN))
            .replace("__LANG__", lang))

    title = LANG_TITLES[lang]
    page_title = f"{LANG_LABELS[lang]} — Practice Exam · Ravn"
    favicon_tag = (f'<link rel="icon" type="image/png" href="{_FAVICON_DATA_URI}">'
                   if _FAVICON_DATA_URI else "")

    ravn_topbar = (
        '<header class="ravn-topbar">'
        '<a class="ravn-brand" href="../index.html" aria-label="Ravn — Claude Certified Architect">'
        f'{RAVN_LOGO_SVG}<span class="ravn-brand-tagline">Claude Certified Architect</span></a>'
        '<div style="display:flex;align-items:center;">'
        '<div class="mode-toggle">'
        f'<button id="modeStudy" onclick="setMode(\'study\')">{ui["mode_study"]}</button>'
        f'<button id="modeExam" onclick="setMode(\'exam\')">{ui["mode_exam"]}</button>'
        '</div><span class="mode-hint" id="modeHint"></span>'
        '</div></header>'
    )

    HTML = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
{favicon_tag}
<style>{CSS}</style>
</head>
<body>
{ravn_topbar}
<div class="shell">
  <nav class="sidebar">
    <div class="sidebar-header">{ui['questions']}</div>
    <div class="sidebar-progress">{ui['answered']}: <span id="answeredCount">0</span> / <span id="totalCount">0</span></div>
    <div class="sidebar-scroll" id="sidebarList"></div>
  </nav>
  <div class="main">
    <div class="topbar">
      <div class="topbar-title">{title}</div>
      <div class="topbar-nav">
        <span class="q-counter" id="qCounter"></span>
        <button class="nav-btn" id="prevBtn" onclick="navigate(-1)" disabled>{ui['prev']}</button>
        <button class="nav-btn" id="nextBtn" onclick="navigate(1)">{ui['next']}</button>
        <button class="nav-btn finish" id="finishBtn" onclick="showSummary()">{ui['finish']}</button>
      </div>
    </div>
    <div class="content">
      <div class="screen active" id="questionScreen"><div class="q-card" id="qCard"></div></div>
      <div class="screen" id="summaryScreen"><div class="summary show" id="summaryContent"></div></div>
    </div>
  </div>
</div>
<script>{js}</script>
</body>
</html>"""

    out = os.path.join(ROOT_DIR, f"exam_{lang}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Written: exam_{lang}.html  ({len(HTML):,} bytes, {len(questions)} questions)")


def main():
    langs = sys.argv[1:] if len(sys.argv) > 1 else list(LANG_TITLES.keys())
    for lang in langs:
        build(lang)


if __name__ == "__main__":
    main()
