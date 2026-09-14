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
  * two attempt lengths: full (default, mirrors the real exam's size) and a
    quick drill of about a third of the draw, still weighted per domain
  * a domain drill: scope the attempt to one domain to work its whole bank,
    scored raw (no scaled pass/fail verdict)
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
        "restart": "New attempt — new random draw", "weight": "weight",
        "threshold_note": ("Pass mark set at {p}/1000. Each attempt draws 12 "
                           "random questions per domain (60 total); the score "
                           "is scaled to 1000 as a study approximation of the "
                           "real 100–1000 scaled score."),
        "incorrect": "incorrect", "domain": "Domain",
        "select_n": "Select {n} responses.",
        "select_full": "All {n} responses chosen. Deselect one to change your answer.",
        "not_answered": "Not answered", "incomplete_answer": "incomplete answer",
        "length_full": "Full · {n}", "length_quick": "Quick · {n}",
        "length_aria": "Attempt length",
        "new_set": "New set",
        "focus_all": "All domains",
        "focus_label": "Drill one domain",
        "focus_note": ("Domain {d} drill: all {n} questions from this domain, "
                       "reshuffled every attempt. Switch back to All domains "
                       "for a full exam draw."),
        "drill_score": "Domain {d} score",
        "new_draw_confirm": ("Start a new attempt with a fresh random draw? "
                             "Your current answers will be cleared."),
        "draw_note_full": ("Every attempt draws a fresh random set: {n} of the "
                           "{bank} bank questions this time. Full length "
                           "mirrors the real exam — 60 questions in 120 "
                           "minutes."),
        "draw_note_quick": ("Quick drill: {n} questions drawn at random, "
                            "weighted across domains — a fresh set every "
                            "attempt."),
        "summary_rotate": ("This attempt was one random draw of {n} questions "
                           "from the {bank}-question bank. Start a new attempt "
                           "for a different set — the questions rotate every "
                           "time."),
        "threshold_note_quick": ("Pass mark set at {p}/1000. A quick drill "
                                 "draws a shorter random set weighted across "
                                 "domains and scales the score to 1000 the "
                                 "same way; use the full length for a "
                                 "realistic rehearsal."),
        "misses_btn": "My misses · {n}",
        "misses_label": "Drill my misses",
        "misses_empty": "No misses yet",
        "misses_note": ("Weak-spot drill: the {n} question(s) you have "
                        "answered wrong before, most-missed first."),
        "misses_score": "Weak-spot score",
        "misses_clear": "Clear my misses",
        "misses_clear_confirm": ("Clear the record of every question you have "
                                 "missed? This also ends the attempt in "
                                 "progress."),
        "browse_btn": "Browse the bank",
        "browse_title": "Browse the bank",
        "browse_search": "Search questions, options and explanations",
        "browse_domain": "Filter by domain",
        "browse_count": "{n} of {bank} questions",
        "browse_none": "No question matches this filter.",
        "cluster_note": "{i} of {n} variants of this scenario",
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
        "restart": "Nuevo intento — nuevo sorteo aleatorio", "weight": "peso",
        "threshold_note": ("Aprobación fijada en {p}/1000. Cada intento sortea "
                           "12 preguntas aleatorias por dominio (60 en total); "
                           "el puntaje se escala sobre 1000 como aproximación "
                           "de estudio de la escala real de 100–1000."),
        "incorrect": "incorrectas", "domain": "Dominio",
        "select_n": "Selecciona {n} respuestas.",
        "select_full": "Ya elegiste las {n} respuestas. Deselecciona una para cambiar tu respuesta.",
        "not_answered": "Sin responder", "incomplete_answer": "respuesta incompleta",
        "length_full": "Completo · {n}", "length_quick": "Rápido · {n}",
        "length_aria": "Duración del intento",
        "new_set": "Nuevo sorteo",
        "focus_all": "Todos los dominios",
        "focus_label": "Practicar un dominio",
        "focus_note": ("Práctica del dominio {d}: las {n} preguntas de este "
                       "dominio, reordenadas en cada intento. Vuelve a Todos "
                       "los dominios para un sorteo completo."),
        "drill_score": "Puntaje del dominio {d}",
        "new_draw_confirm": ("¿Iniciar un nuevo intento con un nuevo sorteo "
                             "aleatorio? Tus respuestas actuales se borrarán."),
        "draw_note_full": ("Cada intento sortea un conjunto aleatorio nuevo: "
                           "esta vez, {n} de las {bank} preguntas del banco. "
                           "La duración completa refleja el examen real: 60 "
                           "preguntas en 120 minutos."),
        "draw_note_quick": ("Práctica rápida: {n} preguntas sorteadas al azar, "
                            "ponderadas entre dominios — un conjunto nuevo en "
                            "cada intento."),
        "summary_rotate": ("Este intento fue un sorteo aleatorio de {n} "
                           "preguntas de un banco de {bank}. Inicia un nuevo "
                           "intento para recibir un conjunto distinto: las "
                           "preguntas rotan cada vez."),
        "threshold_note_quick": ("Aprobación fijada en {p}/1000. La práctica "
                                 "rápida sortea un conjunto aleatorio más "
                                 "corto ponderado entre dominios y escala el "
                                 "puntaje a 1000 de la misma forma; usa la "
                                 "duración completa para un ensayo realista."),
        "misses_btn": "Mis fallos · {n}",
        "misses_label": "Practicar mis fallos",
        "misses_empty": "Sin fallos aún",
        "misses_note": ("Práctica de puntos débiles: las {n} pregunta(s) que "
                        "ya respondiste mal, empezando por las más falladas."),
        "misses_score": "Puntaje de puntos débiles",
        "misses_clear": "Borrar mis fallos",
        "misses_clear_confirm": ("¿Borrar el registro de todas las preguntas "
                                 "que fallaste? También termina el intento en "
                                 "curso."),
        "browse_btn": "Explorar el banco",
        "browse_title": "Explorar el banco",
        "browse_search": "Buscar en preguntas, opciones y explicaciones",
        "browse_domain": "Filtrar por dominio",
        "browse_count": "{n} de {bank} preguntas",
        "browse_none": "Ninguna pregunta coincide con este filtro.",
        "cluster_note": "{i} de {n} variantes de este escenario",
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
        "restart": "Nova tentativa — novo sorteio aleatório", "weight": "peso",
        "threshold_note": ("Aprovação definida em {p}/1000. Cada tentativa "
                           "sorteia 12 perguntas aleatórias por domínio (60 no "
                           "total); a pontuação é escalada para 1000 como "
                           "aproximação de estudo da escala real de 100–1000."),
        "incorrect": "incorretas", "domain": "Domínio",
        "select_n": "Selecione {n} respostas.",
        "select_full": "As {n} respostas já foram escolhidas. Desmarque uma para alterar sua resposta.",
        "not_answered": "Sem resposta", "incomplete_answer": "resposta incompleta",
        "length_full": "Completo · {n}", "length_quick": "Rápido · {n}",
        "length_aria": "Duração da tentativa",
        "new_set": "Novo sorteio",
        "focus_all": "Todos os domínios",
        "focus_label": "Treinar um domínio",
        "focus_note": ("Treino do domínio {d}: as {n} perguntas deste domínio, "
                       "reordenadas a cada tentativa. Volte a Todos os domínios "
                       "para um sorteio completo."),
        "drill_score": "Pontuação do domínio {d}",
        "new_draw_confirm": ("Iniciar uma nova tentativa com um novo sorteio "
                             "aleatório? Suas respostas atuais serão "
                             "apagadas."),
        "draw_note_full": ("Cada tentativa sorteia um conjunto aleatório novo: "
                           "desta vez, {n} das {bank} perguntas do banco. A "
                           "duração completa espelha o exame real: 60 "
                           "perguntas em 120 minutos."),
        "draw_note_quick": ("Treino rápido: {n} perguntas sorteadas ao acaso, "
                            "ponderadas entre os domínios — um conjunto novo "
                            "a cada tentativa."),
        "summary_rotate": ("Esta tentativa foi um sorteio aleatório de {n} "
                           "perguntas de um banco de {bank}. Inicie uma nova "
                           "tentativa para receber um conjunto diferente: as "
                           "perguntas mudam a cada vez."),
        "threshold_note_quick": ("Aprovação definida em {p}/1000. O treino "
                                 "rápido sorteia um conjunto aleatório mais "
                                 "curto ponderado entre os domínios e escala "
                                 "a pontuação para 1000 da mesma forma; use a "
                                 "duração completa para um ensaio realista."),
        "misses_btn": "Meus erros · {n}",
        "misses_label": "Treinar meus erros",
        "misses_empty": "Sem erros ainda",
        "misses_note": ("Treino de pontos fracos: as {n} pergunta(s) que você "
                        "já errou, começando pelas mais erradas."),
        "misses_score": "Pontuação dos pontos fracos",
        "misses_clear": "Limpar meus erros",
        "misses_clear_confirm": ("Limpar o registro de todas as perguntas que "
                                 "você errou? Isso também encerra a tentativa "
                                 "em curso."),
        "browse_btn": "Explorar o banco",
        "browse_title": "Explorar o banco",
        "browse_search": "Buscar em perguntas, opções e explicações",
        "browse_domain": "Filtrar por domínio",
        "browse_count": "{n} de {bank} perguntas",
        "browse_none": "Nenhuma pergunta corresponde a este filtro.",
        "cluster_note": "{i} de {n} variantes deste cenário",
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
.mode-controls { display: flex; align-items: center; flex-wrap: wrap; gap: 6px 0;
  min-width: 0; justify-content: flex-end; }
.mode-toggle, .new-draw-btn, .misses-btn, .browse-btn { flex-shrink: 0; }
.length-toggle { margin-left: 10px; }
.mode-toggle button:disabled { opacity: .35; cursor: default; }
.focus-select { margin-left: 10px; background: var(--surface); color: var(--fg);
  border: 1px solid var(--border-strong); border-radius: var(--r-md);
  font-family: inherit; font-size: 11.5px; font-weight: 600;
  text-transform: uppercase; letter-spacing: .08em; padding: 6px 8px;
  /* A select sizes to its longest option, and the domain names are long
     enough to push the rest of the header off the row. */
  max-width: 220px; min-width: 0; cursor: pointer; }
.focus-select:focus-visible { outline: 2px solid var(--gold); outline-offset: 1px; }
.focus-select:disabled { opacity: .35; cursor: default; }
.new-draw-btn { margin-left: 10px; }
.new-draw-btn .dn-icon { margin-right: 5px; }

/* Rotation notice — the strip under the brand bar and the summary callout both
   say the same thing: every attempt is a fresh random draw from the bank. */
.draw-note { padding: 8px 32px; background: var(--surface); color: var(--muted);
  font-size: 12.5px; line-height: 1.5; border-bottom: 1px solid var(--border);
  flex-shrink: 0; }
.dn-icon { color: var(--gold); font-weight: 700; margin-right: 7px; }
.rotate-note { margin-top: 26px; padding: 14px 18px; background: var(--gold-soft);
  border: 1px solid var(--gold); border-radius: var(--r-md); font-size: 13.5px;
  color: var(--fg-soft); line-height: 1.6; }

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
.q-select-hint { font-size: 12.5px; color: var(--subtle); margin: -8px 0 16px; }
.options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }
.option { border: 1px solid var(--border-strong); border-radius: var(--r-md); background: var(--surface);
  transition: border-color .15s, background .15s; overflow: hidden; }
.option-head { display: flex; align-items: flex-start; gap: 14px; width: 100%; padding: 14px 18px;
  border: 0; background: transparent; color: inherit; font: inherit; text-align: left; cursor: pointer; }
.option-head:focus-visible { outline: 2px solid var(--gold); outline-offset: -3px; }
.option:hover:not(.locked):not(.dimmed) .option-head { background: var(--surface-2); }
.option:hover:not(.locked):not(.dimmed) { border-color: var(--gold); }
.option.locked .option-head, .option-head[aria-disabled="true"] { cursor: default; }
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

/* Weak-spot drill + browse entry points share the nav-btn shape; `active`
   marks the one currently scoping the page. */
.nav-btn.active { background: var(--gold); color: var(--gold-fg); border-color: var(--gold); }
.dn-action { margin-left: 10px; background: none; border: 0; padding: 0; color: var(--gold);
  font: inherit; font-size: 12.5px; text-decoration: underline; cursor: pointer; }

/* Browse the bank — every question, filtered by domain and free text. Bodies
   are filled on expand, so a 500-item list paints one <summary> row each. */
.browse-head { max-width: 980px; margin: 0 auto 16px; display: flex; flex-wrap: wrap;
  align-items: center; gap: 10px; }
.browse-head h1 { flex: 1 1 100%; font-size: 22px; font-weight: 800; color: var(--fg); }
.browse-head .focus-select { margin-left: 0; }
.browse-search { flex: 1 1 240px; min-width: 0; background: var(--surface); color: var(--fg);
  border: 1px solid var(--border-strong); border-radius: var(--r-md);
  font-family: inherit; font-size: 14px; padding: 8px 12px; }
.browse-search:focus-visible { outline: 2px solid var(--gold); outline-offset: 1px; }
.browse-count { flex: 0 0 auto; font-size: 12.5px; color: var(--subtle); }
.browse-list, .br-empty { max-width: 980px; margin: 0 auto; }
.br-empty { color: var(--muted); font-size: 14px; }
.br-item { background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-md); margin-bottom: 8px; }
.br-item[open] { border-color: var(--border-strong); }
.br-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px;
  padding: 12px 16px; cursor: pointer; list-style: none; }
.br-head::-webkit-details-marker { display: none; }
.br-head:hover { background: var(--surface-2); }
.br-id { flex: 0 0 auto; font-family: "Source Code Pro", ui-monospace, Menlo, monospace;
  font-size: 11.5px; font-weight: 600; color: var(--gold); }
.br-stem { flex: 1 1 260px; font-size: 14.5px; line-height: 1.5; color: var(--fg-soft); }
.br-hint { display: block; margin-top: 3px; font-size: 12.5px; color: var(--subtle);
  line-height: 1.45; }
/* The full situation sits right below once the item is open, so the preview
   in the clickable head would only repeat itself. */
.br-item[open] .br-hint { display: none; }
.br-tags { flex: 0 0 auto; display: flex; flex-wrap: wrap; gap: 6px; }
.br-tag { padding: 3px 8px; border: 1px solid var(--border-strong); border-radius: var(--r-sm);
  font-size: 10px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
  color: var(--muted); white-space: nowrap; }
.br-tag.cluster { border-color: var(--gold); color: var(--gold);
  font-size: 11px; letter-spacing: normal; text-transform: none; }
.br-tag.src { border-style: dashed; }
.br-body { padding: 0 16px 14px; }
.br-situation { margin-bottom: 12px; padding-left: 12px; font-size: 14px; line-height: 1.6;
  color: var(--fg-soft); border-left: 2px solid var(--border-strong); }
.br-opt { display: flex; gap: 10px; padding: 8px 0; border-top: 1px solid var(--border); }
.br-opt .opt-letter { width: 24px; height: 24px; min-width: 24px; font-size: 12px; }
.br-opt.is-correct .opt-letter { background: var(--good); color: var(--good-fg); }
.br-opt-text { font-size: 14px; line-height: 1.5; color: var(--fg-soft); }
.br-opt.is-correct .br-opt-text { color: var(--fg); font-weight: 600; }
.br-opt-expl { margin-top: 4px; font-size: 12.5px; line-height: 1.55; color: var(--muted); }

@media (max-width: 760px) {
  html, body { height: auto; }
  body { min-height: 100vh; height: auto; overflow: auto; display: block; }
  .ravn-topbar { position: static; padding: 10px 16px; gap: 10px; flex-wrap: wrap; }
  .draw-note { padding: 8px 16px; }
  .ravn-brand-tagline { display: none; }
  .mode-controls { max-width: 100%; justify-content: flex-start; }
  .mode-hint { margin-left: 8px; }
  /* Phone order: question first. The navigator and the page title used to
     push the question ~590px down an 844px screen. */
  .shell { display: flex; flex-direction: column; overflow: visible; }
  .main { order: 1; display: flex; flex-direction: column; overflow: visible; }
  .sidebar { order: 2; width: 100%; min-width: 0; height: auto; max-height: 260px;
    min-height: 0; border-right: 0; border-top: 1px solid var(--border);
    border-bottom: 0; }
  .content { order: 1; overflow: visible; padding: 20px 16px 16px; }
  .topbar { order: 2; padding: 12px 16px; gap: 10px; flex-wrap: wrap;
    border-top: 1px solid var(--border); border-bottom: 0;
    position: sticky; bottom: 0; background: var(--surface); z-index: 5; }
  .topbar-title { display: none; }
  .topbar-nav { width: 100%; flex-wrap: nowrap; gap: 8px; }
  .topbar-nav .nav-btn { flex: 1; text-align: center; }
  .q-scenario { display: block; width: fit-content; margin-left: 0; }
  .score-grid { grid-template-columns: 1fr; }
  .ds-row { flex-wrap: wrap; }
  .ds-name { flex-basis: 100%; }
  .ds-bar { flex: 1; min-width: 140px; }
  .browse-head, .browse-list, .br-empty { max-width: none; }
  .br-head { padding: 10px 12px; gap: 8px; }
  .br-stem { flex-basis: 100%; }
}

@media (max-width: 420px) {
  .mode-hint { width: 100%; margin-left: 0; order: 99; }
  .nav-btn { padding: 8px 10px; }
  /* Fit all three controls on one row at 390px instead of orphaning New set
     onto its own line: trim padding, tracking and the gaps between groups. */
  .mode-controls { gap: 6px; justify-content: flex-start; }
  .mode-toggle button { padding: 5px 7px; font-size: 0.66rem; letter-spacing: 0.04em; }
  .length-toggle, .new-draw-btn { margin-left: 4px; }
  .focus-select { margin-left: 4px; max-width: 140px; }
  .new-draw-btn { padding: 5px 8px; font-size: 0.66rem; }
  .new-draw-btn .dn-icon { margin-right: 3px; }
  .draw-note { font-size: 0.78rem; line-height: 1.45; padding: 8px 16px; }
  .q-counter { width: 100%; }
  .wrong-item { display: block; }
  .wrong-item .wi-n { margin-bottom: 4px; }
  .browse-head h1 { font-size: 1.15rem; }
  .br-tag { font-size: 0.6rem; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; }
}
"""

JS = r"""
const QUESTIONS = __DATA__;
// Option letters come from the bank, but an imported item may ship without
// them. Filling them in here — A..H, in the order the options are written —
// is what lets everything downstream (the answer key, the review pane, browse
// mode) key on a letter regardless of how many options an item carries.
const LETTERS = "ABCDEFGH";
QUESTIONS.forEach(q => (q.options || []).forEach((o, i) => {
  if (!o.letter) o.letter = LETTERS.charAt(i) || String(i + 1);
}));
const DOMAINS = __DOMAINS__;
const T = __UI__;
const PASS_PCT = __PASS__;          // per-domain bar coloring threshold (%)
const PASS_SCORE = __PASS_SCORE__;  // overall cut score on the 100–1000 scale
// Questions drawn per domain each attempt. Either a single number applied to
// every domain (Foundations: 12 across 5 domains) or a { domain: count } map
// when the draw is weighted (Professional: 11/8/12/10/9/9/4 across 7 domains).
const PER_DOMAIN = __PER_DOMAIN__;
// A quick drill draws about a third of the full attempt: per domain, the full
// count over QUICK_DIVISOR, rounded, floored at one item so every domain the
// full draw covers stays present. Deriving it from PER_DOMAIN keeps the full
// draw the single source of the weighting.
const QUICK_DIVISOR = 3;
const STORE_KEY = "__STOREKEY__";
// Bumped when a saved attempt stops being valid — a blueprint revision that
// changes the per-domain draw, a change to the shape of a stored answer, or a
// new field the order validation depends on (the domain focus in version 3).
// An older payload is dropped, which resets an attempt in progress once.
const STORE_VERSION = 3;
// Per-question miss counts, namespaced under the page's own store key so the
// three tracks never read each other's weak spots. `{ id: { n, t } }`: how
// many times the item was answered wrong, and when it was last graded.
const MISS_KEY = STORE_KEY + ":misses";
const MISS_VERSION = 1;

function loadMisses() {
  try {
    const raw = localStorage.getItem(MISS_KEY);
    if (!raw) return {};
    const d = JSON.parse(raw);
    if (!d || d.v !== MISS_VERSION || !d.items || typeof d.items !== "object") return {};
    return d.items;
  } catch (e) { return {}; }
}
function saveMisses(items) {
  try {
    localStorage.setItem(MISS_KEY, JSON.stringify({ v: MISS_VERSION, items: items }));
  } catch (e) {}
}

// The weak-spot draw: every question missed at least once, most-missed first,
// oldest first among ties so a stale miss resurfaces before a fresh one. It is
// capped at the full draw size — a candidate with 200 misses still gets an
// attempt the length of a real one.
function missedIds() {
  const m = loadMisses();
  const ids = Object.keys(m).filter(id => (m[id] && m[id].n > 0) && qById(id));
  ids.sort((a, b) => (m[b].n - m[a].n) || ((m[a].t || 0) - (m[b].t || 0)) ||
                     (a < b ? -1 : a > b ? 1 : 0));
  return ids.slice(0, examSize("full", "all"));
}

// Record one graded item. Called once per question per attempt (state.graded
// is the guard, and it is saved with the attempt so a reload cannot double
// count): in study mode the moment the answer completes and reveals, in exam
// mode when the attempt is scored.
function noteResult(q, ans) {
  if (!q || state.graded[q.id]) return;
  const touched = Array.isArray(ans) ? ans.length > 0 : (ans !== undefined && ans !== null);
  if (!touched) return;
  state.graded[q.id] = true;
  const m = loadMisses();
  const cur = m[q.id];
  if (!isCorrect(q, ans)) m[q.id] = { n: ((cur && cur.n) || 0) + 1, t: Date.now() };
  else if (cur) cur.t = Date.now();
  else return;   // a first-time correct answer is not a weak spot to remember
  saveMisses(m);
}

// `length` ("full" | "quick") defaults to the attempt in progress. load()
// passes it explicitly: a saved payload must be checked against its own
// length, never against whatever the live state happens to be.
function drawCount(domain, length) {
  const full = (typeof PER_DOMAIN === "number") ? PER_DOMAIN : (PER_DOMAIN[domain] ?? 0);
  if ((length || state.length) !== "quick") return full;
  return full > 0 ? Math.max(1, Math.round(full / QUICK_DIVISOR)) : 0;
}

// The draw actually achievable per domain: the requested count, capped by how
// many questions that domain holds (so it never over-draws a small domain).
// A domain focus overrides the draw: the attempt holds every bank question of
// that one domain, so the candidate can drill it exhaustively. `focus`
// defaults to the attempt in progress; pass "all" explicitly to describe the
// full-draw lengths regardless of the live state (the length toggle labels).
function drawPerDomain(length, focus) {
  if (focus === undefined) focus = state.focus;
  if (focus === "misses") {
    const out = {};
    missedIds().forEach(id => { const d = qById(id).domain; out[d] = (out[d] || 0) + 1; });
    return out;
  }
  if (focus !== "all") {
    const out = {};
    out[focus] = QUESTIONS.filter(q => String(q.domain) === String(focus)).length;
    return out;
  }
  const byDomain = {};
  QUESTIONS.forEach(q => { byDomain[q.domain] = (byDomain[q.domain] || 0) + 1; });
  const out = {};
  Object.keys(byDomain).forEach(d => { out[d] = Math.min(byDomain[d], drawCount(d, length)); });
  return out;
}

// Number of questions in one attempt.
function examSize(length, focus) {
  return Object.values(drawPerDomain(length, focus)).reduce((s, c) => s + c, 0);
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

// ---- grading -------------------------------------------------------------
// "incomplete" is a multiple-response item with some but not all of its letters
// picked. It is not an answer, so it scores as incorrect — and it must still
// reach the review pane, or the candidate never sees the rationale.
function classify(q, ans) {
  if (!hasAnswer(q, ans)) return "incomplete";
  return isCorrect(q, ans) ? "correct" : "incorrect";
}

// Tally one attempt. Pure on purpose: the summary screen below only renders
// what this returns, so the regression harness can check the bucketing.
function tallyAttempt(active, answers) {
  const domStat = {}, wrongByDomain = {};
  let answered = 0, correct = 0;
  active.forEach(q => {
    domStat[q.domain] = domStat[q.domain] || { correct: 0, total: 0 };
    domStat[q.domain].total++;
    const ans = answers[q.id];
    const verdict = classify(q, ans);
    if (verdict !== "incomplete") answered++;
    if (verdict === "correct") { correct++; domStat[q.domain].correct++; return; }
    (wrongByDomain[q.domain] = wrongByDomain[q.domain] || [])
      .push({ q: q, chosen: ans, verdict: verdict });
  });
  const total = active.length;
  return { total: total, answered: answered, correct: correct,
           wrong: answered - correct, unanswered: total - answered,
           domStat: domStat, wrongByDomain: wrongByDomain };
}

// `focus` ("all" | a domain id | "misses") scopes an attempt: "all" draws
// across every domain, a domain id drills that domain's whole bank, "misses"
// draws the questions this candidate has answered wrong before. It persists
// like the attempt length, and the order validation below reads it from the
// payload.
// `graded` holds the ids already folded into the miss counts for this attempt,
// so answering in study mode and then finishing cannot count one item twice.
// `browse` is the bank-browser filter; it is view state, so it is not saved.
const state = { current: 0, answers: {}, order: [], mode: "study", length: "full",
                focus: "all", graded: {}, browse: { domain: "all", q: "" } };

// ---- persistence ---------------------------------------------------------
function save() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(
    { v: STORE_VERSION, answers: state.answers, order: state.order,
      mode: state.mode, length: state.length, focus: state.focus,
      graded: state.graded, current: state.current })); } catch (e) {}
}
function load() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return null;
    const d = JSON.parse(raw);
    // A payload from a different version is discarded, not migrated. A payload
    // written before versioning existed carries no stamp: it is still accepted,
    // because nothing about it is known to be stale and the checks below
    // validate it on its own terms. That keeps attempts in progress alive.
    if (d.v !== undefined && d.v !== STORE_VERSION) return null;
    // The payload's own length decides which draw the order must match, so a
    // saved attempt of one length can never be misread as the other. A payload
    // from before the quick drill existed carries no length: it is a full
    // attempt, the only length that engine could draw.
    const length = d.length === "quick" ? "quick" : "full";
    // Same for the focus: a drill of one domain must be checked against that
    // domain's bank, never against the full draw. A payload from before the
    // domain drill existed carries no focus: it drew across every domain.
    const focus = d.focus === undefined ? "all" : d.focus;
    if (focus !== "all" && focus !== "misses" &&
        !QUESTIONS.some(q => String(q.domain) === String(focus))) return null;
    const ids = new Set(QUESTIONS.map(q => q.id));
    if (!Array.isArray(d.order) || !d.order.every(id => ids.has(id))) return null;
    if (focus === "misses") {
      // A weak-spot drill is drawn from a set that grows as the candidate
      // answers, so its composition cannot be recomputed and compared — doing
      // so would throw the attempt away on the first new miss. What still
      // holds: real ids, no repeats, and never longer than a full draw.
      if (!d.order.length || d.order.length > examSize("full", "all")) return null;
      if (new Set(d.order).size !== d.order.length) return null;
    } else {
      // Order is valid only if it still matches that length's attempt size.
      if (d.order.length !== examSize(length, focus)) return null;
      // The total survives a blueprint revision that only moves items between
      // domains, so check the per-domain mix too. Without this a returning
      // candidate keeps the old weighting under a note that claims the new one.
      // In a drill the same check pins the order to the focused domain's bank.
      const want = drawPerDomain(length, focus), got = {};
      d.order.forEach(id => { const q = qById(id); if (q) got[q.domain] = (got[q.domain] || 0) + 1; });
      if (Object.keys(want).some(d2 => (got[d2] || 0) !== want[d2])) return null;
    }
    d.length = length;
    d.focus = focus;
    return d;
  } catch (e) { return null; }
}

// ---- order ---------------------------------------------------------------
// Draw PER_DOMAIN random questions from each domain (the "question bank"
// behavior), keeping domains in order. Within a domain the drawn questions are
// already in random order from the shuffle. Option order is never shuffled (the
// answer key is by letter). A domain focus instead shuffles that domain's whole
// bank: the drill is exhaustive, so a new set only reorders it.
function shuffleOrder() {
  // Weak-spot order is ranked, not random: most-missed first is the point.
  if (state.focus === "misses") return missedIds();
  const byDomain = {};
  QUESTIONS.forEach(q => { (byDomain[q.domain] = byDomain[q.domain] || []).push(q.id); });
  const order = [];
  const domains = state.focus !== "all"
    ? [String(state.focus)].filter(d => byDomain[d] || byDomain[Number(d)] !== undefined)
    : Object.keys(byDomain).sort((a, b) => a - b);
  domains.forEach(d => {
    const key = byDomain[d] !== undefined ? d : Number(d);
    const ids = byDomain[key].slice();
    for (let i = ids.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [ids[i], ids[j]] = [ids[j], ids[i]];
    }
    order.push(...(state.focus !== "all" ? ids : ids.slice(0, drawCount(key))));
  });
  return order;
}
function qById(id) { return QUESTIONS.find(q => q.id === id); }
function orderedQuestions() { return state.order.map(qById); }

// Everything below writes into innerHTML, and every string it writes is
// authored data. esc() runs first so a raw "<" in an item ("latency < 500 ms")
// stays text instead of becoming markup.
function esc(text) {
  if (text === undefined || text === null) return "";
  return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function md(text) {
  if (!text) return "";
  return esc(text).replace(/`([^`]+)`/g, "<code>$1</code>")
                  .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
                  .replace(/\n/g, " ");
}

// ---- sidebar -------------------------------------------------------------
function buildSidebar() {
  const list = document.getElementById("sidebarList");
  list.innerHTML = "";
  document.getElementById("totalCount").textContent = state.order.length;
  const qs = orderedQuestions();
  // A weak-spot drill is ordered by miss count, so its domains interleave:
  // grouping it by domain would produce a column of one-item headings. It gets
  // a single group instead, under the drill's own name.
  const weak = state.focus === "misses";
  let curDomain = null, groupEl = null;
  qs.forEach((q, idx) => {
    const groupKey = weak ? "misses" : q.domain;
    if (groupKey !== curDomain) {
      curDomain = groupKey;
      const sg = document.createElement("div");
      sg.className = "domain-group";
      const lbl = document.createElement("div");
      lbl.className = "domain-label";
      const dm = DOMAINS[q.domain];
      lbl.innerHTML = weak
        ? "<span>" + esc(T.misses_label) + "</span><span class='dl-weight'>" + qs.length + "</span>"
        : "<span>" + T.domain + " " + q.domain + " · " + esc(dm.name) +
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
  const scenarioTag = q.scenario ? "<span class='q-scenario'>" + esc(q.scenario) + "</span>" : "";
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
    // A revealed option is inert for good, so `disabled` fits. An at-capacity
    // option is not: it becomes selectable again as soon as the candidate
    // deselects a letter, so it stays in the tab order and only reports itself
    // as unavailable. `disabled` here would hide it from keyboard and screen
    // reader users, and the visible hint below explains the state.
    const disabled = reveal ? " disabled"
                   : ((atCapacity && !isChosen) ? " aria-disabled='true'" : "");
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
    "<div><span class='q-domain'>" + T.domain + " " + q.domain + " · " + esc(dm.name) + "</span>" +
    scenarioTag + "</div>" +
    situation +
    "<div class='q-prompt'>" + md(q.question) + "</div>" +
    (isMulti(q)
      ? "<div class='q-select'>" + T.select_n.replace("{n}", selectCount(q)) + "</div>" +
        (atCapacity
          ? "<div class='q-select-hint'>" + T.select_full.replace("{n}", selectCount(q)) + "</div>"
          : "")
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
    // At capacity on an unpicked letter: nothing changes, so return before the
    // re-render. Repainting the card would throw away the keyboard focus.
    else return;
    state.answers[id] = cur;
  }
  // Study mode reveals the answer as soon as it is complete — that reveal is
  // the grading the candidate sees, so the weak-spot record follows it. Exam
  // mode stays editable until the attempt is scored, so it records there.
  if (state.mode === "study" && hasAnswer(q, state.answers[id])) {
    noteResult(q, state.answers[id]);
    updateMissesUI();
  }
  save();
  renderQuestion(state.current);
  updateSidebar();
}

function navigate(dir) { goto(state.current + dir); }

// Three screens now share the content pane, so showing one always hides the
// other two: a half-hidden browse list under a summary was the failure mode.
function showScreen(name) {
  ["questionScreen", "summaryScreen", "browseScreen"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle("active", id === name);
  });
  const btn = document.getElementById("browseBtn");
  if (btn) btn.classList.toggle("active", name === "browseScreen");
}

function goto(idx) {
  const qs = orderedQuestions();
  if (idx < 0 || idx >= qs.length) return;
  showScreen("questionScreen");
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

// ---- new draw ------------------------------------------------------------
// Drawing a different set is available at all times: the header button, the
// length toggle, and the summary's restart all end in restart(). The first
// two run while an attempt may be in progress, so they share one guard that
// asks before discarding it. The summary's button stays unguarded, as it
// always was: that attempt is already finished and scored.
function confirmDiscard() {
  return Object.keys(state.answers).length === 0 ||
    typeof confirm !== "function" || confirm(T.new_draw_confirm);
}

function newDraw() {
  if (confirmDiscard()) restart();
}

// ---- attempt length ------------------------------------------------------
// "full" mirrors the real exam's draw; "quick" is a short drill for a spare
// twenty minutes. Switching lengths redraws, so a started attempt asks first.
// Length is meaningless while a domain is focused (the drill holds the whole
// domain bank), so the toggle is disabled there and this is unreachable.
function setLength(length) {
  if (state.focus !== "all") return;
  if (length === state.length) return;
  if (!confirmDiscard()) return;
  state.length = length;
  restart();
}

function updateLengthUI() {
  [["lengthFull", "full", T.length_full], ["lengthQuick", "quick", T.length_quick]]
    .forEach(([id, len, label]) => {
      const btn = document.getElementById(id);
      // The toggle labels always describe the full draw, even mid-drill.
      btn.textContent = label.replace("{n}", examSize(len, "all"));
      btn.classList.toggle("active", state.length === len);
      btn.setAttribute("aria-pressed", String(state.length === len));
      btn.disabled = state.focus !== "all";
    });
  // The weak-spot drill reads its size off the order in play, not off a
  // recomputed draw: answering during the drill adds misses, and the strip
  // must keep describing the attempt the candidate is actually taking.
  const note = state.focus === "misses"
    ? T.misses_note.replace("{n}", state.order.length)
    : (state.focus !== "all"
        ? T.focus_note.replace("{n}", examSize()).replace("{d}", state.focus)
        : (state.length === "quick" ? T.draw_note_quick : T.draw_note_full)
            .replace("{n}", examSize())
            .replace("{bank}", QUESTIONS.length));
  document.getElementById("drawNote").innerHTML =
    "<span class='dn-icon'>&#10227;</span>" + note +
    (state.focus === "misses"
      ? "<button type='button' class='dn-action' onclick='clearMisses()'>" +
        esc(T.misses_clear) + "</button>"
      : "");
  updateFocusUI();
}

// ---- domain focus ----------------------------------------------------------
// Scoping an attempt to one domain drills its whole bank: every question in
// the domain, shuffled. Switching scope redraws, so a started attempt asks
// first, through the same guard a new draw uses.
function setFocus(focus) {
  if (String(focus) === String(state.focus)) return;
  if (focus === "misses" && missedIds().length === 0) return;
  if (!confirmDiscard()) { updateFocusUI(); return; }
  state.focus = focus;
  restart();
}

// ---- weak-spot drill -------------------------------------------------------
// Only the questions this candidate has answered wrong before, most-missed
// first. It is a scope like the domain drill, so it goes through setFocus and
// inherits the discard guard, the disabled length toggle and the raw scoring.
function toggleMisses() {
  setFocus(state.focus === "misses" ? "all" : "misses");
}

function updateMissesUI() {
  const btn = document.getElementById("missesBtn");
  if (!btn) return;
  const n = missedIds().length;
  btn.textContent = n ? T.misses_btn.replace("{n}", n) : T.misses_empty;
  btn.disabled = n === 0 && state.focus !== "misses";
  btn.classList.toggle("active", state.focus === "misses");
  btn.setAttribute("aria-pressed", String(state.focus === "misses"));
}

// Clearing the weak-spot record also ends the attempt in progress: a drill
// scoped to misses that no longer exist is not an attempt anyone can finish.
function clearMisses() {
  if (typeof confirm === "function" && !confirm(T.misses_clear_confirm)) return;
  clearProgress();
}

function clearProgress() {
  try { localStorage.removeItem(MISS_KEY); localStorage.removeItem(STORE_KEY); } catch (e) {}
  state.answers = {};
  state.graded = {};
  state.current = 0;
  state.focus = "all";
  restart();
}

function fillDomainOptions(sel) {
  if (!sel) return;
  sel.innerHTML = "";
  const all = document.createElement("option");
  all.value = "all";
  all.textContent = T.focus_all;
  sel.appendChild(all);
  Object.keys(DOMAINS).sort((a, b) => a - b).forEach(d => {
    const opt = document.createElement("option");
    opt.value = d;
    opt.textContent = T.domain + " " + d + " · " + DOMAINS[d].name;
    sel.appendChild(opt);
  });
}

function buildFocusOptions() {
  fillDomainOptions(document.getElementById("focusSelect"));
  fillDomainOptions(document.getElementById("browseDomain"));
}

function updateFocusUI() {
  updateMissesUI();
  const sel = document.getElementById("focusSelect");
  if (!sel) return;
  // The weak-spot drill is not a domain, so the domain select has nothing
  // truthful to show: it goes inert for the duration, the way the length
  // toggle already does inside a drill.
  sel.disabled = state.focus === "misses";
  sel.value = state.focus === "misses" ? "all" : String(state.focus);
}

// ---- browse the bank -------------------------------------------------------
// Every question in the bank, filtered by domain and free text, each one
// expandable to its full answer key. Built for ~500 items on a phone: the
// index is computed once, a filter paints one <summary> row per match, and an
// item's options and explanations are rendered only when it is opened.
let BROWSE_INDEX = null;

function browseIndex() {
  if (BROWSE_INDEX) return BROWSE_INDEX;
  // Items that share a stem are imported as a cluster. Counting the cluster up
  // front is what lets each row say which variant of the scenario it is, so a
  // reader who meets the same setup three times knows why.
  const size = {}, seen = {};
  QUESTIONS.forEach(q => { if (q.cluster) size[q.cluster] = (size[q.cluster] || 0) + 1; });
  BROWSE_INDEX = QUESTIONS.map(q => {
    // `task_id` is the blueprint subdomain ("3.2"), so typing it finds every
    // item on that objective. The objective *text* is deliberately left out:
    // every item in a domain repeats it, so it would match half the bank on a
    // common word and drown the question the reader was actually looking for.
    const hay = [q.id, q.task_id, q.situation, q.question]
      .concat(q.options.map(o => o.text))
      .concat(q.options.map(o => o.explanation))
      .filter(Boolean).join(" ").toLowerCase();
    const n = q.cluster ? size[q.cluster] : 0;
    const i = q.cluster ? (seen[q.cluster] = (seen[q.cluster] || 0) + 1) : 0;
    return { q: q, hay: hay, ci: i, cn: n };
  });
  return BROWSE_INDEX;
}

// Pure, so the filter can be checked without a DOM. Every whitespace-separated
// term must appear somewhere in the item — question, options or explanations.
function filteredBank(domain, query) {
  if (domain === undefined) domain = state.browse.domain;
  if (query === undefined) query = state.browse.q;
  const terms = String(query || "").toLowerCase().split(/\s+/).filter(Boolean);
  return browseIndex().filter(r =>
    (String(domain) === "all" || String(r.q.domain) === String(domain)) &&
    terms.every(t => r.hay.indexOf(t) >= 0));
}

function browseRowHtml(r) {
  const q = r.q;
  const tags =
    "<span class='br-tag'>" + T.domain + " " + esc(q.domain) + "</span>" +
    (r.cn > 1
      ? "<span class='br-tag cluster'>" +
        esc(T.cluster_note.replace("{i}", r.ci).replace("{n}", r.cn)) + "</span>" : "");
  const hint = (q.situation && q.question.length < 90)
    ? "<span class='br-hint'>" + md(q.situation.slice(0, 110)) +
      (q.situation.length > 110 ? "…" : "") + "</span>" : "";
  return "<details class='br-item' data-id='" + esc(q.id) + "'>" +
    "<summary class='br-head'>" +
      "<span class='br-id'>" + esc(q.id).toUpperCase() + "</span>" +
      "<span class='br-stem'>" + md(q.question) + hint + "</span>" +
      "<span class='br-tags'>" + tags + "</span>" +
    "</summary><div class='br-body'></div></details>";
}

// The expensive half: options, correctness marks and every explanation. Kept
// out of the list render so the cost is paid per opened item, not per bank.
function browseBody(id) {
  const q = qById(id);
  if (!q) return "";
  const opts = q.options.map(o =>
    "<div class='br-opt" + (o.correct ? " is-correct" : "") + "'>" +
      "<span class='opt-letter'>" + esc(o.letter) + "</span>" +
      "<span><span class='br-opt-text'>" + md(o.text) +
        (o.correct ? " <span class='wi-correct-tag'>&#10003; " + T.correct + "</span>" : "") +
      "</span>" +
      (o.explanation ? "<div class='br-opt-expl'>" + md(o.explanation) + "</div>" : "") +
      "</span></div>").join("");
  return (q.situation ? "<div class='br-situation'>" + md(q.situation) + "</div>" : "") +
    (isMulti(q) ? "<div class='q-select'>" + T.select_n.replace("{n}", selectCount(q)) + "</div>" : "") +
    opts;
}

function renderBrowse() {
  const rows = filteredBank();
  const count = document.getElementById("browseCount");
  if (count) {
    count.textContent = T.browse_count.replace("{n}", rows.length)
                                      .replace("{bank}", QUESTIONS.length);
  }
  const list = document.getElementById("browseList");
  if (!list) return;
  list.innerHTML = rows.length
    ? rows.map(browseRowHtml).join("")
    : "<p class='br-empty'>" + esc(T.browse_none) + "</p>";
}

// One delegated listener for the whole list, so 500 rows cost 500 strings and
// no handlers. `toggle` does not bubble, hence the capture phase.
function wireBrowse() {
  const list = document.getElementById("browseList");
  if (!list || list.__wired || typeof list.addEventListener !== "function") return;
  list.__wired = true;
  list.addEventListener("toggle", ev => {
    const d = ev.target;
    if (!d || !d.open || !d.getAttribute) return;
    const body = d.lastElementChild;
    if (body && !body.innerHTML) body.innerHTML = browseBody(d.getAttribute("data-id"));
  }, true);
}

function setBrowseDomain(d) {
  state.browse.domain = d;
  renderBrowse();
}

// The search box repaints the list, so it waits for a pause in typing. On a
// phone that is the difference between a smooth field and a stuttering one.
let browseTimer = null;
function onBrowseSearch(v) {
  state.browse.q = v;
  if (typeof setTimeout !== "function") { renderBrowse(); return; }
  if (browseTimer) clearTimeout(browseTimer);
  browseTimer = setTimeout(renderBrowse, 120);
}

function toggleBrowse() {
  const screen = document.getElementById("browseScreen");
  if (screen && screen.classList.contains("active")) { goto(state.current); return; }
  showScreen("browseScreen");
  wireBrowse();
  renderBrowse();
}

// ---- summary -------------------------------------------------------------
function showSummary() {
  showScreen("summaryScreen");

  // Only the questions in this attempt (PER_DOMAIN per domain) count. The
  // review pane lists every item that did not score, including the ones left
  // blank or half-picked: those count as incorrect, so they need a rationale.
  const active = orderedQuestions();
  const tally = tallyAttempt(active, state.answers);
  // Scoring is the grading a candidate sees in exam mode, so the weak-spot
  // record is written here. noteResult() skips anything study mode already
  // counted, so finishing after answering cannot double-count an item.
  active.forEach(q => noteResult(q, state.answers[q.id]));
  save();
  updateMissesUI();
  const total = tally.total, answered = tally.answered, correct = tally.correct;
  const wrong = tally.wrong, unanswered = tally.unanswered;
  const domStat = tally.domStat, wrongByDomain = tally.wrongByDomain;

  const pct = total ? Math.round(correct / total * 100) : 0;
  const score = total ? Math.round(correct / total * 1000) : 0; // scaled to 1000
  const passed = score >= PASS_SCORE;
  // A domain drill covers one domain only, so the 100–1000 scaled score and
  // its pass/fail verdict would mislead: the summary reports the raw domain
  // result instead, with the same review pane below.
  const drilling = state.focus !== "all";
  const weak = state.focus === "misses";

  // What this attempt was scoped to, in the scope's own words — the sentence
  // is repeated under the score and again at the foot of the review pane.
  const scopeNote = weak
    ? T.misses_note.replace("{n}", total)
    : T.focus_note.replace("{n}", total).replace("{d}", state.focus);

  let domainScoresHtml = "";
  Object.keys(domStat).sort((a, b) => a - b).forEach(d => {
    const s = domStat[d], dm = DOMAINS[d];
    const dpct = s.total ? Math.round(s.correct / s.total * 100) : 0;
    const barCls = dpct >= PASS_PCT ? "" : (dpct >= 50 ? "low" : "bad");
    domainScoresHtml +=
      "<div class='ds-row'>" +
        "<div class='ds-name'>" + T.domain + " " + d + " · " + esc(dm.name) +
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
      // One block per correct letter. Joining them into a single paragraph left
      // the reader unable to tell which rationale explained which letter.
      const expl = correctLetters.map(L => {
        const o = item.q.options.find(x => x.letter === L);
        return (o && o.explanation)
          ? "<div class='wi-expl'><strong>" + T.why + " " + L + ":</strong> " + md(o.explanation) + "</div>"
          : "";
      }).join("");
      // Nothing picked reads as "Not answered" rather than an empty dash; a
      // half-picked multi item shows its letters and says it is incomplete.
      const yours = chosenLetters.length
        ? "<span class='wi-wrong-tag'>" + letterLabel(chosenLetters) + "</span>" +
          (item.verdict === "incomplete"
            ? " <span class='wi-wrong-tag'>(" + T.incomplete_answer + ")</span>" : "") +
          " — " + optText(chosenLetters)
        : "<span class='wi-wrong-tag'>" + T.not_answered + "</span>";
      return "<div class='wrong-item'>" +
        "<div class='wi-n'>" + esc(item.q.id).toUpperCase() + "</div>" +
        "<div class='wi-q'>" +
          (item.q.situation ? "<div class='wi-situation'>" + md(item.q.situation) + "</div>" : "") +
          "<div class='wi-prompt'>" + md(item.q.question) + "</div>" +
          "<div class='wi-ans'>" + T.your_answer + ": " + yours + "<br>" +
            T.correct + ": <span class='wi-correct-tag'>" + letterLabel(correctLetters) + "</span> — " +
            optText(correctLetters) + "</div>" + expl +
        "</div></div>";
    }).join("");
    wrongGroupsHtml += "<div class='group-block'><div class='group-title'>" +
      T.domain + " " + d + " · " + esc(dm.name) +
      "<span class='group-badge'>" + items.length + " " + T.incorrect + "</span></div>" + rows + "</div>";
  });

  const unansweredNote = unanswered > 0
    ? "<p style='color:#e53e3e;font-size:14px;margin-bottom:18px;font-weight:600;'>" +
      T.unanswered.replace("{n}", unanswered) + "</p>" : "";

  // Raw-only head for a drill; the scaled head for a full draw.
  const headHtml = drilling
    ? "<div class='score-grid'>" +
        "<div class='score-card total'><div class='big'>" + correct + "/" + total + "</div>" +
          "<div class='label'>" +
            (weak ? T.misses_score : T.drill_score.replace("{d}", state.focus)) +
            " · " + pct + "%</div></div>" +
        "<div class='score-card correct-c'><div class='big'>" + correct + "</div>" +
          "<div class='label'>" + T.correct + "</div></div>" +
        "<div class='score-card wrong-c'><div class='big'>" + (wrong + unanswered) + "</div>" +
          "<div class='label'>" + T.incorrect + "</div></div>" +
      "</div>" +
      "<p class='threshold-note'>" + scopeNote + "</p>"
    : "<div class='verdict " + (passed ? "pass" : "fail") + "'>" + (passed ? T.pass : T.fail) + "</div>" +
      unansweredNote +
      "<div class='score-grid'>" +
        "<div class='score-card total'><div class='big'>" + score +
          "<span style='font-size:18px;color:#a0aec0;font-weight:700;'>/1000</span></div>" +
          "<div class='label'>" + T.score + "</div></div>" +
        "<div class='score-card correct-c'><div class='big'>" + correct + "</div><div class='label'>" + T.correct + "</div></div>" +
        "<div class='score-card wrong-c'><div class='big'>" + (wrong + unanswered) + "</div><div class='label'>" + T.incorrect + "</div></div>" +
      "</div>" +
      "<p class='threshold-note'>" +
        (state.length === "quick" ? T.threshold_note_quick : T.threshold_note)
          .replace("{p}", PASS_SCORE) + "</p>";

  // In a drill the unanswered warning still matters, so it comes back below
  // the head: the raw branch above skips it, prepending it here keeps both
  // heads honest without duplicating it in the full-draw branch.
  const drillUnanswered = (drilling && unanswered > 0) ? unansweredNote : "";

  document.getElementById("summaryContent").innerHTML =
    "<h1>" + T.complete + "</h1>" +
    "<p class='summary-subtitle'>" + T.answered_of.replace("{a}", answered).replace("{t}", total) + "</p>" +
    headHtml + drillUnanswered +
    "<div class='section-title'>" + T.by_domain + "</div>" +
    "<div class='domain-scores'>" + domainScoresHtml + "</div>" +
    ((wrong + unanswered) > 0
      ? "<div class='section-title'>" + T.review_wrong + "</div>" + wrongGroupsHtml
      : "<p style='color:#38a169;font-weight:700;font-size:17px;'>" + T.all_correct + "</p>") +
    "<div class='rotate-note'><span class='dn-icon'>&#10227;</span>" +
      (drilling ? scopeNote
                : T.summary_rotate.replace("{n}", total).replace("{bank}", QUESTIONS.length)) + "</div>" +
    "<button type='button' class='restart-btn' onclick='restart()'>" + T.restart + "</button>";
}

function restart() {
  state.answers = {};
  // A fresh attempt has graded nothing yet, so every item in it can record a
  // miss again — that is what makes a repeated mistake count twice.
  state.graded = {};
  state.current = 0;
  state.order = shuffleOrder();
  if (!state.order.length && state.focus !== "all") {
    state.focus = "all";
    state.order = shuffleOrder();
  }
  save();
  updateLengthUI();
  buildSidebar();
  showScreen("questionScreen");
  renderQuestion(0);
  updateSidebar();
}

// ---- init ----------------------------------------------------------------
(function init() {
  buildFocusOptions();
  const saved = load();
  if (saved) {
    state.answers = saved.answers || {};
    state.order = saved.order;
    state.mode = saved.mode || "study";
    // load() normalized the length, so a pre-quick payload restores as "full".
    state.length = saved.length;
    // Same for the focus: a pre-drill payload restores as the full draw.
    state.focus = saved.focus;
    state.graded = saved.graded || {};
    state.current = Math.min(saved.current || 0, state.order.length - 1);
  } else {
    state.order = shuffleOrder();
  }
  setMode(state.mode);
  updateLengthUI();
  buildSidebar();
  renderQuestion(state.current);
  updateSidebar();
})();
"""


# Import bookkeeping stays in the bank file; the page only needs what it renders.
_INTERNAL_FIELDS = ("source", "source_url", "fingerprint", "stem_note")


def _public(q):
    return {k: v for k, v in q.items() if k not in _INTERNAL_FIELDS}


def _payload(obj):
    """JSON for embedding in an inline <script> block.

    "<" becomes an escape so authored text holding "</script>" cannot close the
    block early, and U+2028 / U+2029 are escaped because ensure_ascii=False
    emits them raw while JS reads them as line terminators. All three only ever
    occur inside JSON string values, so no replacement can break the structure.
    """
    return (json.dumps(obj, ensure_ascii=False)
            .replace("<", "\\u003c")
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def render_page(*, questions, domains_js, ui, per_domain, pass_score, pass_pct,
                store_key, lang_attr, title, page_title, out_path):
    """Render one self-contained quiz page.

    Shared by the Foundations builder below and by build_professional_exam.py,
    so both tracks stay on one engine. `per_domain` is either an int (same draw
    for every domain) or a {domain: count} map for a weighted draw. Each track
    supplies its own `pass_score` / `pass_pct`: the two cut scores are equal
    today, but Professional's authority is its own blueprint, not this module.
    """
    # The data-driven payloads go in last: question and objective text can hold
    # anything, and an earlier injection would let it be rewritten by a later
    # replace.
    js = (JS.replace("__PER_DOMAIN__", _payload(per_domain))
            .replace("__PASS_SCORE__", str(pass_score))
            .replace("__STOREKEY__", store_key)
            .replace("__PASS__", str(pass_pct))
            .replace("__UI__", _payload(ui))
            .replace("__DOMAINS__", _payload(domains_js))
            .replace("__DATA__", _payload([_public(q) for q in questions])))

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
        '</div>'
        f'<div class="mode-toggle length-toggle" role="group" aria-label="{ui["length_aria"]}">'
        '<button type="button" id="lengthFull" aria-pressed="false" onclick="setLength(\'full\')"></button>'
        '<button type="button" id="lengthQuick" aria-pressed="false" onclick="setLength(\'quick\')"></button>'
        '</div>'
        f'<select class="focus-select" id="focusSelect" aria-label="{ui["focus_label"]}" onchange="setFocus(this.value)"></select>'
        '<button type="button" class="nav-btn new-draw-btn" id="newDrawBtn" onclick="newDraw()">'
        f'<span class="dn-icon">&#10227;</span>{ui["new_set"]}</button>'
        f'<button type="button" class="nav-btn misses-btn" id="missesBtn" '
        f'aria-pressed="false" aria-label="{ui["misses_label"]}" '
        f'title="{ui["misses_label"]}" onclick="toggleMisses()" disabled></button>'
        f'<button type="button" class="nav-btn browse-btn" id="browseBtn" '
        f'aria-pressed="false" onclick="toggleBrowse()">{ui["browse_btn"]}</button>'
        '<span class="mode-hint" id="modeHint"></span>'
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
<div class="draw-note" id="drawNote"></div>
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
      <div class="screen" id="browseScreen">
        <div class="browse-head">
          <h1>{ui['browse_title']}</h1>
          <select class="focus-select" id="browseDomain" aria-label="{ui['browse_domain']}" onchange="setBrowseDomain(this.value)"></select>
          <input type="search" class="browse-search" id="browseSearch" placeholder="{ui['browse_search']}" aria-label="{ui['browse_search']}" oninput="onBrowseSearch(this.value)">
          <span class="browse-count" id="browseCount"></span>
        </div>
        <div class="browse-list" id="browseList"></div>
      </div>
    </div>
  </main>
</div>
<script>{js}</script>
</body>
</html>"""

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
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
        pass_score=PASS_SCORE,
        pass_pct=PASS_PCT,
        store_key=f"ccaf-exam-{lang}",
        lang_attr=lang,
        title=LANG_TITLES[lang],
        page_title=f"{LANG_LABELS[lang]} — Practice Exam · Ravn",
        out_path=os.path.join(ROOT_DIR, "ccaf", "dist", f"exam_{lang}.html"),
    )


def main():
    langs = sys.argv[1:] if len(sys.argv) > 1 else list(LANG_TITLES.keys())
    for lang in langs:
        build(lang)


if __name__ == "__main__":
    main()
