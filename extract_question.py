#!/usr/bin/env python3
"""Extract practice-test questions from guide_<lang>.md as JSON.

Usage:  python3 extract_question.py <lang> [all]

Reads ./guide_<lang>.md (case-insensitive extension) and emits a JSON
array on stdout with the schema consumed by utils/build_practical_test_html.py:

    [
      {
        "n": 1,                         # question number within scenario
        "scenario": "Multi-agent Research System",
        "situation": "...",             # the **Situation:** paragraph
        "question": "...",              # the bold prompt that follows
        "options": [
          {"letter": "A", "text": "...", "correct": false},
          ...
        ],
        "correct": "D",
        "explanation": "...",           # the **Why X:** paragraph, prefix stripped
        "global_n": 1                   # 1-based across all scenarios
      },
      ...
    ]

Markdown shape (recovered from guide_en.MD):

    ## Scenario: <name>
    ---
    ## Question <n> (Scenario: <name>)

    **Situation:** <one or more paragraphs>

    **<question prompt — usually ends with ?>**

    - A) <option text>
    - B) <option text>
    - C) <option text> **[CORRECT]**
    - D) <option text>

    **Why <letter>:** <explanation>

    ---
"""
from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def find_guide(lang: str) -> str:
    for ext in ("md", "MD", "Md", "mD"):
        p = os.path.join(ROOT, f"guide_{lang}.{ext}")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"No guide_{lang}.md/.MD next to {ROOT}")


# Question header: `## Question 12 (Scenario: Multi-agent Research System)`
# (some translations may use a different word for "Scenario" — we match by the
# parenthesised hint, falling back to the most recent `## Scenario:` heading.)
RE_SCENARIO_HDR = re.compile(r"^##\s+(?:Scenario|Escenario|Cenário)\s*:\s*(.+?)\s*$", re.M)
RE_QUESTION_HDR = re.compile(
    r"^##\s+(?:Question|Pregunta|Questão)\s+(\d+)\s*(?:\(([^)]*)\))?\s*$", re.M
)
RE_SITUATION = re.compile(
    r"\*\*(?:Situation|Situación|Situação)\s*:\*\*\s*(.+?)(?=\n\n)",
    re.S,
)
# A bold prompt line (usually contains a "?" for English/Spanish/Portuguese).
RE_PROMPT = re.compile(r"^\*\*(.+?)\*\*\s*$", re.M)
# Option list: `- A) ...` (also tolerates `* A)` and `- A.` / `- A:`)
RE_OPTION = re.compile(
    r"^[-*]\s+([A-D])\s*[\).:]\s*(.+?)\s*$",
    re.M,
)
RE_CORRECT_TAG = re.compile(r"\s*\*\*\[(?:CORRECT|CORRECTA|CORRETA)\]\*\*\s*$")
RE_EXPLANATION = re.compile(
    r"\*\*(?:Why|Por qué|Por que|Porquê)\s+([A-D])\s*:\*\*\s*(.+?)(?=\n(?:---|##|$))",
    re.S,
)


def split_question_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return [(scenario, n, body)] for every `## Question` block."""
    matches = list(RE_QUESTION_HDR.finditer(text))
    scenarios = list(RE_SCENARIO_HDR.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        n = m.group(1)
        scenario_hint = (m.group(2) or "").strip()
        # Strip a leading "Scenario:" / "Escenario:" / "Cenário:" prefix.
        scenario = re.sub(
            r"^(?:Scenario|Escenario|Cenário)\s*:\s*", "", scenario_hint, flags=re.I
        ).strip()
        if not scenario:
            # Fall back to the most recent `## Scenario:` header before this question.
            preceding = [s for s in scenarios if s.start() < m.start()]
            scenario = preceding[-1].group(1).strip() if preceding else ""
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        blocks.append((scenario, n, body))
    return blocks


def parse_question(scenario: str, n: str, body: str) -> dict:
    sit_m = RE_SITUATION.search(body)
    situation = (sit_m.group(1).strip() if sit_m else "").replace("\n", " ")

    # The first bold line *after* the situation is the question prompt.
    after_sit = body[sit_m.end():] if sit_m else body
    prompt = ""
    for pm in RE_PROMPT.finditer(after_sit):
        cand = pm.group(1).strip()
        # Skip the "Why X:" line, which also matches RE_PROMPT.
        if re.match(r"^(?:Why|Por qué|Por que|Porquê)\s+[A-D]\s*:", cand, re.I):
            continue
        prompt = cand
        break

    options = []
    correct_letter = ""
    for om in RE_OPTION.finditer(body):
        letter = om.group(1)
        raw = om.group(2)
        is_correct = bool(RE_CORRECT_TAG.search(raw))
        text_clean = RE_CORRECT_TAG.sub("", raw).strip()
        options.append({"letter": letter, "text": text_clean, "correct": is_correct})
        if is_correct:
            correct_letter = letter

    expl_m = RE_EXPLANATION.search(body)
    if expl_m:
        if not correct_letter:
            correct_letter = expl_m.group(1)
        explanation = re.sub(r"\s+", " ", expl_m.group(2).strip())
    else:
        explanation = ""

    return {
        "n": int(n),
        "scenario": scenario,
        "situation": situation,
        "question": prompt,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation,
    }


RE_PRACTICE_TEST_H1 = re.compile(
    r"^#\s+(?:Practice\s+Test|Examen\s+Práctico|Teste\s+Prático|Prueba\s+Práctica)\s*$",
    re.M | re.I,
)
RE_NEXT_H1 = re.compile(r"^#\s+\S", re.M)


def practice_test_region(text: str) -> str:
    """Return the slice of `text` under the `# Practice Test` H1, or the full
    text if the heading is absent. Excludes earlier sections like
    `# Examples of Exam Questions with Explanations` that also contain
    `## Question N (Scenario: ...)` blocks but are not the canonical exam set."""
    m = RE_PRACTICE_TEST_H1.search(text)
    if not m:
        return text
    after = text[m.end():]
    nxt = RE_NEXT_H1.search(after)
    return after[: nxt.start()] if nxt else after


def extract(lang: str) -> list[dict]:
    text = open(find_guide(lang), encoding="utf-8").read()
    region = practice_test_region(text)
    questions = []
    for scenario, n, body in split_question_blocks(region):
        # Skip blocks that don't have a situation (e.g. introductory chatter).
        if not RE_SITUATION.search(body):
            continue
        questions.append(parse_question(scenario, n, body))
    # Renumber globally, preserving discovery order.
    for i, q in enumerate(questions, 1):
        q["global_n"] = i
    return questions


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    lang = sys.argv[1]
    # The "all" positional is accepted for compatibility with the upstream
    # build_practical_test_html.py call signature; it is currently a no-op.
    questions = extract(lang)
    json.dump(questions, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
