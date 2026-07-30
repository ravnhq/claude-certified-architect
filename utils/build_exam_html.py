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

This module also hosts the quiz engine itself: render_page() below is shared with
build_professional_exam.py, so a change here affects both tracks. Check both with
`node utils/test_exam_engine.mjs`.
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
        "select_n": "Select {n} responses.",
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
        "select_n": "Selecciona {n} respuestas.",
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
        "select_n": "Selecione {n} respostas.",
    },
}

_FAVICON_PATH = os.path.join(ROOT_DIR, "docs", "assets", "favicon.png")
try:
    _FAVICON_DATA_URI = "data:image/png;base64," + base64.b64encode(
        open(_FAVICON_PATH, "rb").read()).decode()
except FileNotFoundError:
    _FAVICON_DATA_URI = ""

# Official RAVN wordmark — inlined so fill:currentColor follows the brand bar color.
RAVN_LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 148 33" '
    'aria-label="Ravn" role="img" height="20" fill="currentColor">'
    '<path d="M147.001 0.000976562H139.097V21.1196L120.763 0.00198534H112.859V32.9979H120.763V11.8853L139.095 33.001L139.098 32.9979H147.001V0.000976562Z"/>'
    '<path d="M94.3156 33H85.8811L73.0273 0H81.4608L90.0978 22.1056L98.7348 0H107.169L94.3156 33Z"/>'
    '<path d="M64.4406 0H56.0061L43.1523 33H51.5868L60.2238 10.8934L68.8598 33H77.2943L64.4406 0Z"/>'
    '<path d="M28.8517 22.5101C33.8779 21.1825 37.5735 16.7376 37.5735 11.4583C37.5735 5.23989 32.4481 0.178564 26.0589 0.00605301V0H7.64995H0L6.34956 7.63688H7.64995V7.6389H25.7781C27.9333 7.66916 29.671 9.36703 29.671 11.4573C29.671 13.5668 27.902 15.2768 25.7197 15.2768H22.8382H12.7002L27.4355 33H37.5724L28.8517 22.5101Z"/>'
    '<path d="M8.53644 32.9974C11.4172 32.9974 13.7526 30.7402 13.7526 27.9557C13.7526 25.1713 11.4172 22.9141 8.53644 22.9141C5.65565 22.9141 3.32031 25.1713 3.32031 27.9557C3.32031 30.7402 5.65565 32.9974 8.53644 32.9974Z"/></svg>'
)

CSS = """
/* Ravn Brand System — dark canvas, white text, muted gray, single gold accent.
   Flat (no shadows/gradients), Work Sans + Source Code Pro. Functional red is
   kept only for wrong-answer / fail feedback; green marks correct answers;
   gold carries selection / emphasis. */
:root {
  --bg: #161616; --surface: #1d1d1d; --surface-2: #222222;
  --fg: #FFFFFF; --fg-soft: #D4D4D4; --muted: #ADB5BD; --subtle: #8B949E;
  --border: #2A2A2A; --border-strong: #3A3A3A;
  --gold: #B7986A; --gold-soft: rgba(183,152,106,0.12); --gold-fg: #161616;
  --bad: #C16B57; --bad-soft: rgba(193,107,87,0.14);
  --good: #6FA97C; --good-soft: rgba(111,169,124,0.14); --good-fg: #161616;
  --r-sm: 4px; --r-md: 8px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body { font-family: "Work Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 16px; line-height: 1.6; background: var(--bg); color: var(--fg);
  height: 100vh; overflow: hidden; display: flex; flex-direction: column;
  -webkit-font-smoothing: antialiased; }

.ravn-topbar { position: sticky; top: 0; z-index: 20; display: flex; align-items: center;
  justify-content: space-between; padding: 12px 32px; background: var(--bg); color: var(--fg);
  border-bottom: 1px solid var(--border); flex-shrink: 0; }
.ravn-brand { display: inline-flex; align-items: center; gap: 16px; color: var(--fg);
  text-decoration: none; font-weight: 600; }
.ravn-brand:hover { color: var(--gold); }
.ravn-brand svg { height: 20px; width: auto; fill: currentColor; flex-shrink: 0; }
.ravn-brand-tagline { font-size: 12px; color: var(--muted); text-transform: uppercase;
  letter-spacing: 0.167em; font-weight: 600; }

/* Mode toggle in the brand bar */
.mode-toggle { display: inline-flex; align-items: center; gap: 0; background: transparent;
  border: 1px solid var(--border-strong); border-radius: var(--r-md); overflow: hidden; }
.mode-toggle button { background: none; border: none; color: var(--muted); cursor: pointer;
  font-family: inherit; font-size: 11.5px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.1em; padding: 6px 14px; transition: background .15s, color .15s; }
.mode-toggle button.active { background: var(--gold); color: var(--gold-fg); }
.mode-hint { font-size: 11.5px; color: var(--subtle); margin-left: 12px; }
.mode-controls { display: flex; align-items: center; }

.shell { display: flex; flex: 1; min-height: 0; overflow: hidden; }

.sidebar { width: 272px; min-width: 272px; background: var(--surface); color: var(--muted);
  display: flex; flex-direction: column; overflow: hidden; min-height: 0;
  border-right: 1px solid var(--border); }
.sidebar-header { padding: 18px 16px 12px; font-size: 11.5px; font-weight: 600;
  letter-spacing: .167em; text-transform: uppercase; color: var(--gold);
  border-bottom: 1px solid var(--border); flex-shrink: 0; }
.sidebar-progress { padding: 10px 16px; font-size: 12px; color: var(--muted);
  border-bottom: 1px solid var(--border); flex-shrink: 0; }
.sidebar-progress span { color: var(--fg); font-weight: 600; }
.sidebar-scroll { overflow-y: auto; flex: 1; padding: 8px 0; }
.sidebar-scroll::-webkit-scrollbar { width: 4px; }
.sidebar-scroll::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 2px; }

.domain-group { margin-bottom: 6px; }
.domain-label { padding: 8px 16px 5px; font-size: 10px; font-weight: 600;
  letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
  display: flex; justify-content: space-between; gap: 8px; }
.domain-label .dl-weight { color: var(--subtle); font-weight: 600; }
.q-btn { display: flex; align-items: center; gap: 8px; width: 100%; padding: 6px 16px;
  background: none; border: none; cursor: pointer; font-size: 13.5px; color: var(--muted);
  font-family: inherit; text-align: left; transition: background .15s, color .15s;
  border-left: 3px solid transparent; }
.q-btn:hover { background: var(--surface-2); color: var(--fg); }
.q-btn.active { background: var(--gold-soft); color: var(--gold); border-left-color: var(--gold); }
.q-btn.answered .q-dot { background: var(--gold); }
.q-btn.answered-correct { color: var(--good); }
.q-btn.answered-correct .q-dot { background: var(--good); }
.q-btn.answered-wrong { color: var(--bad); }
.q-btn.answered-wrong .q-dot { background: var(--bad); }
.q-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--subtle);
  flex-shrink: 0; transition: background .2s; }

.main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-height: 0; min-width: 0; }
.topbar { background: var(--bg); border-bottom: 1px solid var(--border); padding: 12px 32px;
  display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
.topbar-title { font-size: 15px; font-weight: 600; color: var(--fg); }
.topbar-nav { display: flex; gap: 10px; align-items: center; }
.nav-btn { padding: 8px 18px; border-radius: var(--r-md); border: 1px solid var(--border-strong);
  background: transparent; font-family: inherit; font-size: 12px; cursor: pointer; color: var(--muted);
  font-weight: 600; text-transform: uppercase; letter-spacing: .1em; transition: all .15s; }
.nav-btn:hover { color: var(--fg); border-color: var(--gold); }
.nav-btn:disabled { opacity: .35; cursor: default; }
.nav-btn.finish { background: var(--fg); color: var(--bg); border-color: var(--fg); }
.nav-btn.finish:hover { background: var(--gold); border-color: var(--gold); color: var(--gold-fg); }
.q-counter { font-size: 13px; color: var(--muted); font-weight: 500; }

.content { flex: 1; overflow-y: auto; padding: 36px 48px; }
.content::-webkit-scrollbar { width: 6px; }
.content::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }

.q-card { max-width: 820px; margin: 0 auto; }
.q-domain { display: inline-block; background: transparent; color: var(--fg); font-size: 11px;
  font-weight: 600; letter-spacing: .12em; text-transform: uppercase; padding: 4px 11px;
  border: 1px solid var(--border-strong); border-radius: var(--r-sm); margin-bottom: 8px; }
.q-scenario { display: inline-block; background: transparent; color: var(--gold); font-size: 11px;
  font-weight: 600; letter-spacing: .12em; text-transform: uppercase; padding: 4px 11px;
  border: 1px solid var(--gold); border-radius: var(--r-sm); margin-bottom: 16px; margin-left: 8px; }
.q-number { font-size: 11px; color: var(--subtle); margin-bottom: 6px; font-weight: 600;
  letter-spacing: .12em; text-transform: uppercase; }
.q-situation { font-size: 16.5px; color: var(--fg-soft); font-weight: 400; line-height: 1.7;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-md);
  padding: 16px 20px; margin-bottom: 22px; }
.q-situation code, .opt-text code, .explanation code, .opt-expl code {
  background: var(--surface-2); padding: 1px 5px; border-radius: var(--r-sm);
  font-family: "Source Code Pro", ui-monospace, Menlo, Monaco, monospace; font-size: 13.5px; color: var(--gold); }
.q-prompt { font-size: 17px; font-weight: 700; color: var(--fg); margin-bottom: 20px; }

.q-select { display: inline-block; background: var(--gold-soft); color: var(--gold); font-size: 11.5px;
  font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: 5px 12px;
  border-radius: var(--r-sm); margin-bottom: 16px; }
.options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }
.option { border: 1px solid var(--border-strong); border-radius: var(--r-md); background: var(--surface);
  transition: border-color .15s, background .15s; overflow: hidden; }
.option-head { display: flex; align-items: flex-start; gap: 14px; width: 100%; padding: 14px 18px;
  border: 0; background: transparent; color: inherit; font: inherit; text-align: left; cursor: pointer; }
.option-head:focus-visible { outline: 2px solid var(--gold); outline-offset: -3px; }
.option:hover:not(.locked):not(.dimmed) .option-head { background: var(--surface-2); }
.option:hover:not(.locked):not(.dimmed) { border-color: var(--gold); }
.option.locked .option-head, .option.dimmed .option-head:disabled { cursor: default; }
.option.locked .option-head:disabled { opacity: 1; }
.option.selected { border-color: var(--gold); }
.opt-letter { width: 30px; height: 30px; min-width: 30px; border-radius: 50%; background: var(--surface-2);
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px;
  color: var(--muted); transition: background .2s, color .2s; flex-shrink: 0; }
.option.selected .opt-letter { background: var(--gold); color: var(--gold-fg); }
.opt-text { font-size: 15px; color: var(--fg-soft); line-height: 1.55; padding-top: 3px; }
.option.correct { border-color: var(--good); background: var(--good-soft); }
.option.correct .opt-letter { background: var(--good); color: var(--good-fg); }
.option.wrong { border-color: var(--bad); background: var(--bad-soft); }
.option.wrong .opt-letter { background: var(--bad); color: #fff; }
.option.dimmed { opacity: .5; }
.opt-expl { display: none; font-size: 13.5px; line-height: 1.6; color: var(--muted);
  padding: 0 18px 14px 62px; }
.option.locked .opt-expl.show { display: block; }
.option.correct .opt-expl { color: var(--good); }
.option.wrong .opt-expl { color: var(--bad); }

.explanation { margin-top: 4px; padding: 14px 18px; background: var(--surface);
  border-left: 3px solid var(--gold); border-radius: 0 var(--r-md) var(--r-md) 0; font-size: 14.5px;
  color: var(--muted); line-height: 1.65; display: none; }
.explanation.show { display: block; }
.explanation strong { color: var(--gold); }

.summary { max-width: 860px; margin: 0 auto; display: none; }
.summary.show { display: block; }
.summary h1 { font-size: 26px; font-weight: 800; color: var(--fg); margin-bottom: 6px; }
.summary-subtitle { color: var(--muted); font-size: 15px; margin-bottom: 22px; }
.verdict { display: inline-block; font-size: 13px; font-weight: 700; letter-spacing: .12em;
  text-transform: uppercase; padding: 7px 18px; border-radius: var(--r-sm); margin-bottom: 22px; }
.verdict.pass { background: var(--gold-soft); color: var(--gold); border: 1px solid var(--gold); }
.verdict.fail { background: var(--bad-soft); color: var(--bad); border: 1px solid var(--bad); }
.score-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-bottom: 14px; }
.score-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-md);
  padding: 20px; text-align: center; }
.score-card .big { font-size: 38px; font-weight: 800; line-height: 1; margin-bottom: 6px; }
.score-card .label { font-size: 11px; color: var(--muted); font-weight: 600;
  text-transform: uppercase; letter-spacing: .12em; }
.score-card.total .big { color: var(--fg); }
.score-card.correct-c .big { color: var(--good); }
.score-card.wrong-c .big { color: var(--bad); }
.threshold-note { font-size: 12.5px; color: var(--subtle); margin-bottom: 26px; }

.domain-scores { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-md);
  padding: 8px 20px; margin-bottom: 26px; }
.ds-row { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-bottom: 1px solid var(--border); }
.ds-row:last-child { border-bottom: none; }
.ds-name { flex: 1; font-size: 14px; font-weight: 600; color: var(--fg); }
.ds-name small { color: var(--subtle); font-weight: 500; }
.ds-bar { width: 160px; height: 8px; background: var(--surface-2); border-radius: 999px; overflow: hidden; }
.ds-bar > div { height: 100%; background: var(--gold); }
.ds-bar > div.low { background: var(--muted); }
.ds-bar > div.bad { background: var(--bad); }
.ds-pct { width: 92px; text-align: right; font-size: 13px; color: var(--muted); font-weight: 600; }

.section-title { font-size: 18px; font-weight: 700; color: var(--fg); margin-bottom: 12px;
  padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.group-block { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-md);
  padding: 18px 20px; margin-bottom: 16px; }
.group-title { font-size: 15px; font-weight: 700; color: var(--fg); margin-bottom: 12px;
  display: flex; align-items: center; gap: 10px; }
.group-badge { font-size: 10px; padding: 3px 10px; border-radius: var(--r-sm); font-weight: 600;
  letter-spacing: .1em; text-transform: uppercase; background: var(--bad-soft); color: var(--bad); }
.wrong-item { display: flex; gap: 10px; align-items: flex-start; padding: 12px 0;
  border-bottom: 1px solid var(--border); font-size: 14px; color: var(--muted); }
.wrong-item:last-child { border-bottom: none; }
.wrong-item .wi-n { min-width: 36px; font-weight: 700; color: var(--subtle); font-size: 12px; padding-top: 2px; }
.wrong-item .wi-q { flex: 1; }
.wrong-item .wi-situation { font-size: 13.5px; color: var(--fg-soft); font-weight: 500; margin-bottom: 4px; line-height: 1.5; }
.wrong-item .wi-prompt { font-size: 13px; color: var(--muted); font-style: italic; margin-bottom: 4px; }
.wrong-item .wi-ans { font-size: 12.5px; margin-top: 3px; color: var(--muted); }
.wi-wrong-tag { color: var(--bad); font-weight: 700; }
.wi-correct-tag { color: var(--good); font-weight: 700; }
.wi-expl { font-size: 12.5px; color: var(--muted); background: var(--surface-2); border-radius: var(--r-sm);
  padding: 8px 10px; margin-top: 6px; line-height: 1.55; }

.restart-btn { margin-top: 28px; padding: 12px 32px; background: var(--fg); color: var(--bg);
  border: none; border-radius: var(--r-md); font-family: inherit; font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: .1em; cursor: pointer; transition: background .15s, color .15s; }
.restart-btn:hover { background: var(--gold); color: var(--gold-fg); }
.screen { display: none; }
.screen.active { display: block; }

@media (max-width: 760px) {
  html, body { height: auto; }
  body { min-height: 100vh; height: auto; overflow: auto; display: block; }
  .ravn-topbar { position: static; padding: 10px 16px; gap: 10px; flex-wrap: wrap; }
  .ravn-brand-tagline { display: none; }
  .mode-controls { max-width: 100%; flex-wrap: wrap; gap: 6px 0; }
  .mode-hint { margin-left: 8px; }
  .shell { display: block; overflow: visible; }
  .sidebar { width: 100%; min-width: 0; height: 220px; min-height: 0;
    border-right: 0; border-bottom: 1px solid var(--border); }
  .main { overflow: visible; }
  .topbar { padding: 12px 16px; gap: 10px; flex-wrap: wrap; }
  .topbar-title { width: 100%; }
  .topbar-nav { width: 100%; flex-wrap: wrap; gap: 8px; }
  .content { overflow: visible; padding: 24px 16px 48px; }
  .q-scenario { display: block; width: fit-content; margin-left: 0; }
  .score-grid { grid-template-columns: 1fr; }
  .ds-row { flex-wrap: wrap; }
  .ds-name { flex-basis: 100%; }
  .ds-bar { flex: 1; min-width: 140px; }
}

@media (max-width: 420px) {
  .mode-hint { width: 100%; margin-left: 0; }
  .nav-btn { padding: 7px 11px; }
  .q-counter { width: 100%; }
  .wrong-item { display: block; }
  .wrong-item .wi-n { margin-bottom: 4px; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; }
}
"""

JS = r"""
const QUESTIONS = __DATA__;
const DOMAINS = __DOMAINS__;
const T = __UI__;
const PASS_PCT = __PASS__;          // per-domain bar coloring threshold (%)
const PASS_SCORE = __PASS_SCORE__;  // overall cut score on the 100–1000 scale
// Questions drawn per domain each attempt. Either a single number applied to
// every domain (Foundations: 12 across 5 domains) or a { domain: count } map
// when the draw is weighted (Professional: 11/8/12/10/9/9/4 across 7 domains).
const PER_DOMAIN = __PER_DOMAIN__;
const STORE_KEY = "__STOREKEY__";

function drawCount(domain) {
  return (typeof PER_DOMAIN === "number") ? PER_DOMAIN : (PER_DOMAIN[domain] ?? 0);
}

// Number of questions in one attempt: the per-domain draw, capped by how many
// that domain actually has (so it never over-draws a small domain).
function examSize() {
  const byDomain = {};
  QUESTIONS.forEach(q => { byDomain[q.domain] = (byDomain[q.domain] || 0) + 1; });
  return Object.entries(byDomain)
    .reduce((s, [d, c]) => s + Math.min(c, drawCount(d)), 0);
}

// ---- answer shape --------------------------------------------------------
// Single-response items store a letter ("B"); multiple-response items store an
// array of letters (["A","C"]) and carry an array `correct`. Everything below
// branches on that so both shapes share one engine.
function isMulti(q) { return Array.isArray(q.correct); }
function selectCount(q) { return isMulti(q) ? q.correct.length : 1; }

function asLetters(v) {
  if (v === undefined || v === null) return [];
  return (Array.isArray(v) ? v.slice() : [v]).sort();
}

// "Answered" means a *complete* answer of the shape this item expects: one
// letter, or exactly the required number of letters. A partly-filled multi item
// does not count as answered, and neither does a stored value of the wrong
// shape — that is stale state from an item that changed response type.
function hasAnswer(q, ans) {
  if (ans === undefined || ans === null) return false;
  if (Array.isArray(ans) !== isMulti(q)) return false;
  return Array.isArray(ans) ? ans.length === selectCount(q) : true;
}

// Multiple-response items are scored all-or-nothing, like the real exam.
function isCorrect(q, ans) {
  if (!hasAnswer(q, ans)) return false;
  const a = asLetters(ans), c = asLetters(q.correct);
  return a.length === c.length && a.every((v, i) => v === c[i]);
}

function isChosenLetter(ans, letter) {
  if (ans === undefined || ans === null) return false;
  return Array.isArray(ans) ? ans.indexOf(letter) >= 0 : ans === letter;
}

function letterLabel(v) { return asLetters(v).join(", "); }

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
    order.push(...ids.slice(0, drawCount(d)));
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
    btn.type = "button";
    btn.className = "q-btn";
    btn.id = "sb-" + idx;
    btn.onclick = () => goto(idx);
    btn.innerHTML = "<span class='q-dot'></span> " + (idx + 1);
    groupEl.appendChild(btn);
  });
}

function updateSidebar() {
  const qs = orderedQuestions();
  let answeredCount = 0;
  qs.forEach((q, idx) => {
    const btn = document.getElementById("sb-" + idx);
    if (!btn) return;
    btn.className = "q-btn";
    if (idx === state.current) btn.classList.add("active");
    const ans = state.answers[q.id];
    if (hasAnswer(q, ans)) {
      answeredCount++;
      if (state.mode === "exam") btn.classList.add("answered");
      else btn.classList.add(isCorrect(q, ans) ? "answered-correct" : "answered-wrong");
    }
  });
  document.getElementById("answeredCount").textContent = answeredCount;
}

// ---- question render -----------------------------------------------------
function renderQuestion(idx) {
  const qs = orderedQuestions();
  const q = qs[idx];
  const chosen = state.answers[q.id];
  // Study mode reveals only once the answer is complete — for a multi item that
  // means all N letters are selected, so partial picks stay editable.
  const reveal = hasAnswer(q, chosen) && state.mode === "study";

  document.getElementById("qCounter").textContent = (idx + 1) + " / " + qs.length;
  document.getElementById("prevBtn").disabled = idx === 0;
  document.getElementById("nextBtn").disabled = idx === qs.length - 1;

  const dm = DOMAINS[q.domain];
  const scenarioTag = q.scenario ? "<span class='q-scenario'>" + q.scenario + "</span>" : "";
  const situation = q.situation ? "<div class='q-situation'>" + md(q.situation) + "</div>" : "";

  // A multi item with all N picks in place: the remaining options are dimmed
  // and inert, so it reads as "deselect one first" instead of a dead click.
  const atCapacity = !reveal && isMulti(q) && hasAnswer(q, chosen);

  const optionsHtml = q.options.map(opt => {
    let cls = "option";
    const isChosen = isChosenLetter(chosen, opt.letter);
    if (reveal) {
      cls += " locked";
      if (opt.correct) cls += " correct";
      else if (isChosen) cls += " wrong";
      else cls += " dimmed";
    } else if (isChosen) {
      cls += " selected";
    } else if (atCapacity) {
      cls += " dimmed";
    }
    // In study mode after answering, show explanation for the correct option
    // and for the (wrong) one the user picked.
    const showExpl = reveal && opt.explanation && (opt.correct || isChosen);
    const disabled = (reveal || (atCapacity && !isChosen)) ? " disabled" : "";
    const expl = opt.explanation
      ? "<div class='opt-expl" + (showExpl ? " show" : "") + "'>" + md(opt.explanation) + "</div>"
      : "";
    return "<div class='" + cls + "' data-letter='" + opt.letter + "'>" +
      "<button type='button' class='option-head' aria-pressed='" + String(isChosen) + "'" + disabled +
        " onclick=\"answer('" + q.id + "','" + opt.letter + "')\">" +
        "<span class='opt-letter'>" + opt.letter + "</span>" +
        "<span class='opt-text'>" + md(opt.text) + "</span>" +
      "</button>" + expl + "</div>";
  }).join("");

  document.getElementById("qCard").innerHTML =
    "<div class='q-number'>" + T.question + " " + (idx + 1) + "</div>" +
    "<div><span class='q-domain'>" + T.domain + " " + q.domain + " · " + dm.name + "</span>" +
    scenarioTag + "</div>" +
    situation +
    "<div class='q-prompt'>" + md(q.question) + "</div>" +
    (isMulti(q)
      ? "<div class='q-select'>" + T.select_n.replace("{n}", selectCount(q)) + "</div>"
      : "") +
    "<div class='options'>" + optionsHtml + "</div>";
}

function answer(id, letter) {
  const q = qById(id);
  const n = selectCount(q);
  const locked = state.mode === "study" && hasAnswer(q, state.answers[id]);
  if (locked) return;

  if (n === 1) {
    state.answers[id] = letter;
  } else {
    // Toggle within the allowed number of selections. Re-clicking a chosen
    // letter removes it, so a candidate can correct a pick before completing.
    const cur = Array.isArray(state.answers[id]) ? state.answers[id].slice() : [];
    const at = cur.indexOf(letter);
    if (at >= 0) cur.splice(at, 1);
    else if (cur.length < n) cur.push(letter);
    state.answers[id] = cur;
  }
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
  document.getElementById("modeStudy").setAttribute("aria-pressed", String(mode === "study"));
  document.getElementById("modeExam").setAttribute("aria-pressed", String(mode === "exam"));
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
  let answered = 0;
  let correct = 0;
  const wrongByDomain = {};
  const domStat = {};

  active.forEach(q => {
    domStat[q.domain] = domStat[q.domain] || { correct: 0, total: 0 };
    domStat[q.domain].total++;
    const ans = state.answers[q.id];
    if (!hasAnswer(q, ans)) return;   // incomplete multi answers count as unanswered
    answered++;
    if (isCorrect(q, ans)) { correct++; domStat[q.domain].correct++; }
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
      // Both shapes resolve to a list of letters, so a multi item shows every
      // letter it needed and every letter the candidate actually picked.
      const optText = letters => letters
        .map(L => { const o = item.q.options.find(x => x.letter === L); return o ? md(o.text) : ""; })
        .filter(Boolean).join("<br>");
      const chosenLetters = asLetters(item.chosen);
      const correctLetters = asLetters(item.q.correct);
      const explText = correctLetters
        .map(L => { const o = item.q.options.find(x => x.letter === L); return o ? o.explanation : ""; })
        .filter(Boolean).map(md).join(" ");
      const expl = explText
        ? "<div class='wi-expl'><strong>" + T.why + " " + letterLabel(correctLetters) + ":</strong> " +
          explText + "</div>" : "";
      return "<div class='wrong-item'>" +
        "<div class='wi-n'>" + item.q.id.toUpperCase() + "</div>" +
        "<div class='wi-q'>" +
          (item.q.situation ? "<div class='wi-situation'>" + md(item.q.situation) + "</div>" : "") +
          "<div class='wi-prompt'>" + md(item.q.question) + "</div>" +
          "<div class='wi-ans'>" + T.your_answer + ": <span class='wi-wrong-tag'>" +
            (letterLabel(chosenLetters) || "—") + "</span> — " + optText(chosenLetters) + "<br>" +
            T.correct + ": <span class='wi-correct-tag'>" + letterLabel(correctLetters) + "</span> — " +
            optText(correctLetters) + "</div>" + expl +
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
    "<button type='button' class='restart-btn' onclick='restart()'>" + T.restart + "</button>";
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


def render_page(*, questions, domains_js, ui, per_domain, store_key, lang_attr,
                title, page_title, out_path):
    """Render one self-contained quiz page.

    Shared by the Foundations builder below and by build_professional_exam.py,
    so both tracks stay on one engine. `per_domain` is either an int (same draw
    for every domain) or a {domain: count} map for a weighted draw.
    """
    # The data-driven payloads go in last: question and objective text can hold
    # anything, and an earlier injection would let it be rewritten by a later
    # replace. Among the fixed tokens the only ordering rule is that
    # __PASS_SCORE__ must precede __PASS__, which is a prefix of it.
    js = (JS.replace("__PER_DOMAIN__", json.dumps(per_domain))
            .replace("__PASS_SCORE__", str(PASS_SCORE))
            .replace("__STOREKEY__", store_key)
            .replace("__PASS__", str(PASS_PCT))
            .replace("__UI__", json.dumps(ui, ensure_ascii=False))
            .replace("__DOMAINS__", json.dumps(domains_js, ensure_ascii=False))
            .replace("__DATA__", json.dumps(questions, ensure_ascii=False)))

    favicon_tag = (f'<link rel="icon" type="image/png" href="{_FAVICON_DATA_URI}">'
                   if _FAVICON_DATA_URI else "")
    lang = lang_attr

    ravn_topbar = (
        '<header class="ravn-topbar">'
        '<a class="ravn-brand" href="../index.html" aria-label="Ravn — Claude Certified Architect">'
        f'{RAVN_LOGO_SVG}<span class="ravn-brand-tagline">Claude Certified Architect</span></a>'
        '<div class="mode-controls">'
        '<div class="mode-toggle">'
        f'<button type="button" id="modeStudy" aria-pressed="false" onclick="setMode(\'study\')">{ui["mode_study"]}</button>'
        f'<button type="button" id="modeExam" aria-pressed="false" onclick="setMode(\'exam\')">{ui["mode_exam"]}</button>'
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;700;800&family=Source+Code+Pro:wght@400;600&display=swap">
<style>{CSS}</style>
</head>
<body>
{ravn_topbar}
<div class="shell">
  <nav class="sidebar" aria-label="{ui['questions']}">
    <div class="sidebar-header">{ui['questions']}</div>
    <div class="sidebar-progress">{ui['answered']}: <span id="answeredCount">0</span> / <span id="totalCount">0</span></div>
    <div class="sidebar-scroll" id="sidebarList"></div>
  </nav>
  <main class="main">
    <div class="topbar">
      <div class="topbar-title">{title}</div>
      <div class="topbar-nav">
        <span class="q-counter" id="qCounter"></span>
        <button type="button" class="nav-btn" id="prevBtn" onclick="navigate(-1)" disabled>{ui['prev']}</button>
        <button type="button" class="nav-btn" id="nextBtn" onclick="navigate(1)">{ui['next']}</button>
        <button type="button" class="nav-btn finish" id="finishBtn" onclick="showSummary()">{ui['finish']}</button>
      </div>
    </div>
    <div class="content">
      <div class="screen active" id="questionScreen"><div class="q-card" id="qCard"></div></div>
      <div class="screen" id="summaryScreen"><div class="summary show" id="summaryContent"></div></div>
    </div>
  </main>
</div>
<script>{js}</script>
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HTML)
    name = os.path.basename(out_path)
    print(f"Written: {name}  ({len(HTML):,} bytes, {len(questions)} questions)")


def build(lang):
    """Foundations track: 5 domains, 12 questions drawn per domain (60 total)."""
    questions = exam_data.load(lang)
    domains_js = {
        str(d): {"name": exam_data.DOMAIN_NAMES[lang][d], "weight": w}
        for d, (_, w) in exam_data.DOMAINS.items()
    }
    render_page(
        questions=questions,
        domains_js=domains_js,
        ui=UI[lang],
        per_domain=PER_DOMAIN,
        store_key=f"ccaf-exam-{lang}",
        lang_attr=lang,
        title=LANG_TITLES[lang],
        page_title=f"{LANG_LABELS[lang]} — Practice Exam · Ravn",
        out_path=os.path.join(ROOT_DIR, f"exam_{lang}.html"),
    )


def main():
    langs = sys.argv[1:] if len(sys.argv) > 1 else list(LANG_TITLES.keys())
    for lang in langs:
        build(lang)


if __name__ == "__main__":
    main()
