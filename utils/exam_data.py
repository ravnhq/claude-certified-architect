#!/usr/bin/env python3
"""Build the unified, merged question set for one language.

Merges two sources into a single schema:
  * the 76 scenario questions extracted from guide_<lang>.md (utils/extract_question.py)
  * the 60 domain questions parsed from the mock-exam .txt (utils/parse_mock_exam.py)

Unified question schema:
  {
    "id": "g12" | "m7",        # stable id, independent of display order
    "source": "guide" | "mock",
    "domain": 1..5,             # CCAF exam domain
    "scenario": "..." | None,   # scenario name (guide questions only)
    "situation": "..." | None,  # context paragraph
    "question": "...",          # the prompt
    "options": [{ "letter", "text", "correct", "explanation" }],
    "correct": "C"
  }

Reviewable sidecars (so classification/dedup decisions live in data/, not code):
  data/domains.json     { "<id>": <1..5>, ... }   — domain per question
  data/duplicates.json  [ "<mock id>", ... ]      — mock ids dropped as dupes of guide qs
  data/mock_<lang>.json [ <unified mock question>, ... ] — translated mock set (es/pt)
"""
from __future__ import annotations
import json, os, subprocess

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")

DOMAINS = {
    1: ("Agent Architecture and Orchestration", 27),
    2: ("Tool Design and MCP Integration", 18),
    3: ("Claude Code Configuration and Workflows", 20),
    4: ("Prompt Engineering and Structured Output", 20),
    5: ("Context Management and Reliability", 15),
}

# Localized domain names (weights are language-independent).
DOMAIN_NAMES = {
    "en": {1: "Agent Architecture and Orchestration", 2: "Tool Design and MCP Integration",
           3: "Claude Code Configuration and Workflows", 4: "Prompt Engineering and Structured Output",
           5: "Context Management and Reliability"},
    "es": {1: "Arquitectura y Orquestación de Agentes", 2: "Diseño de Herramientas e Integración MCP",
           3: "Configuración y Flujos de Claude Code", 4: "Ingeniería de Prompts y Salida Estructurada",
           5: "Gestión de Contexto y Confiabilidad"},
    "pt": {1: "Arquitetura e Orquestração de Agentes", 2: "Design de Ferramentas e Integração MCP",
           3: "Configuração e Fluxos do Claude Code", 4: "Engenharia de Prompts e Saída Estruturada",
           5: "Gerenciamento de Contexto e Confiabilidade"},
}

# Heuristic fallback when a question is not yet in data/domains.json. Scenario
# names map to their dominant domain; mock questions fall back to keyword scan.
SCENARIO_DOMAIN = {
    "multi-agent research system": 1, "sistema de investigación multiagente": 1, "sistema de pesquisa multiagente": 1,
    "customer support agent": 2, "agente de soporte al cliente": 2, "agente de suporte ao cliente": 2,
    "claude code for continuous integration": 3, "claude code para integración continua": 3, "claude code para integração contínua": 3,
    "code generation with claude code": 3, "generación de código con claude code": 3, "geração de código com claude code": 3,
    "conversational ai architecture patterns": 1, "patrones de arquitectura de ia conversacional": 1, "padrões de arquitetura de ia conversacional": 1,
}
KEYWORD_DOMAIN = [
    (5, ("context window", "context length", "/compact", "/clear", "context_length", "batch", "retry", "reliability", "resume", "checkpoint", "degrad")),
    (2, ("mcp", "tool design", "tool definition", "json schema", "isError", "tool_choice", "structured output")),
    (3, ("claude code", "claude.md", "slash command", "hooks", "ci/cd", "--resume", "--continue", "session", "skill")),
    (4, ("prompt", "few-shot", "self-correct", "chaining", "system prompt", "interview pattern")),
    (1, ("subagent", "coordinator", "orchestrat", "agent sdk", "spawn", "task tool", "multi-agent", "delegat")),
]


def _read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def _guide_questions(lang):
    out = subprocess.run(
        ["python3", "utils/extract_question.py", lang, "all"],
        capture_output=True, text=True, cwd=ROOT_DIR,
    ).stdout
    raw = json.loads(out)
    questions = []
    for q in raw:
        # Guide format carries one explanation (for the correct answer only).
        opts = [
            {"letter": o["letter"], "text": o["text"], "correct": o["correct"],
             "explanation": q.get("explanation", "") if o["correct"] else ""}
            for o in q["options"]
        ]
        questions.append({
            "id": f"g{q['global_n']}",
            "source": "guide",
            "domain": None,
            "scenario": q.get("scenario") or None,
            "situation": q.get("situation") or None,
            "question": q.get("question") or "",
            "options": opts,
            "correct": q.get("correct", ""),
        })
    return questions


def _mock_questions(lang):
    # Translated set if present; otherwise parse the English source .txt.
    translated = _read_json(os.path.join(DATA_DIR, f"mock_{lang}.json"), None)
    if translated is not None:
        return translated
    out = subprocess.run(
        ["python3", "utils/parse_mock_exam.py"],
        capture_output=True, text=True, cwd=ROOT_DIR,
    ).stdout
    return json.loads(out)


def _infer_domain(q):
    scn = (q.get("scenario") or "").strip().lower()
    if scn in SCENARIO_DOMAIN:
        return SCENARIO_DOMAIN[scn]
    blob = " ".join([q.get("question") or "", q.get("situation") or "",
                     " ".join(o["text"] for o in q["options"])]).lower()
    for dom, kws in KEYWORD_DOMAIN:
        if any(k in blob for k in kws):
            return dom
    return 1


def load(lang):
    """Return the merged, domain-tagged, deduped question list for `lang`."""
    domain_map = _read_json(os.path.join(DATA_DIR, "domains.json"), {})
    dupes = set(_read_json(os.path.join(DATA_DIR, "duplicates.json"), []))

    questions = _guide_questions(lang) + _mock_questions(lang)
    merged = []
    for q in questions:
        if q["id"] in dupes:
            continue
        q["domain"] = domain_map.get(q["id"]) or q.get("domain") or _infer_domain(q)
        merged.append(q)

    # Group by domain (1..5), preserving discovery order within each domain.
    merged.sort(key=lambda q: q["domain"])
    return merged


if __name__ == "__main__":
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    qs = load(lang)
    from collections import Counter
    c = Counter(q["domain"] for q in qs)
    print(f"[{lang}] total={len(qs)}  by-domain=" +
          ", ".join(f"D{d}:{c[d]}" for d in sorted(DOMAINS)))
