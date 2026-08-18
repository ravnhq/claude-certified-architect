#!/usr/bin/env python3
"""Parse CCAF_Mock_Exam_Preguntas_y_Respuestas.txt into the unified question JSON.

Usage:  python3 utils/parse_mock_exam.py [path/to/mock.txt]   (default: ./CCAF_Mock_Exam_Preguntas_y_Respuestas.txt)

Emits a JSON array on stdout matching the unified schema consumed by
utils/build_exam_html.py:

    {
      "id": "m1",                 # stable id, independent of display order
      "source": "mock",
      "domain": null,             # CCAF domain 1-5 (filled by classify step)
      "scenario": null,           # mock questions are domain-grouped, not scenario-grouped
      "situation": "...",         # context paragraph(s) (may be null)
      "question": "...",          # the prompt (last "?" line when separable)
      "options": [
        {"letter": "A", "text": "...", "correct": false, "explanation": "..."},
        ...
      ],
      "correct": "C"
    }

Source .txt shape (one block per question, separated by a line of `═`):

    PREGUNTA 1 (Q1)
    ──────────────────────
    <context + prompt, one or more lines>

    OPCIONES:
      A) <option text, possibly multi-line>
         [✗ INCORRECTA]            (or [✓ CORRECTA])
         Explicación: <rationale, possibly multi-line>

      B) ...

    >>> RESPUESTA CORRECTA: C
"""
from __future__ import annotations
import json, os, re, sys

# Repo root: this script lives in utils/, the guides and mock bank sit one level up.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TXT = os.path.join(ROOT, "CCAF_Mock_Exam_Preguntas_y_Respuestas.txt")

# Split the file into per-question blocks on the `PREGUNTA N (QN)` header.
RE_Q_HDR = re.compile(r"^PREGUNTA\s+(\d+)\s*\(Q\d+\)\s*$", re.M)
RE_OPTION_START = re.compile(r"^\s{2}([A-D])\)\s*(.*)$")
RE_MARKER = re.compile(r"^\s*\[(✓|✗)\s*(?:CORRECTA|INCORRECTA)\]\s*$")
RE_EXPL = re.compile(r"^\s*Explicaci[oó]n:\s*(.*)$")
RE_CORRECT = re.compile(r"^>>>\s*RESPUESTA CORRECTA:\s*([A-D])\s*$", re.M)
RE_RULE = re.compile(r"^[─═]+\s*$")


def split_blocks(text: str) -> list[tuple[int, str]]:
    matches = list(RE_Q_HDR.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        n = int(m.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((n, text[m.end():end]))
    return blocks


def split_situation_prompt(stem: str) -> tuple[str | None, str]:
    """Split the question stem into (situation, prompt).

    The prompt is the trailing line that ends with '?'. Everything before it
    is the situation/context. If the stem is a single line (or doesn't end in
    '?'), the whole thing is the prompt and there's no separate situation.
    """
    lines = [ln.strip() for ln in stem.strip().split("\n") if ln.strip()]
    if not lines:
        return None, ""
    if len(lines) > 1 and lines[-1].endswith("?"):
        return " ".join(lines[:-1]), lines[-1]
    return None, " ".join(lines)


def parse_block(n: int, body: str) -> dict:
    lines = body.split("\n")

    # 1) Question stem: everything from the start until the `OPCIONES:` line,
    #    skipping the leading rule line.
    stem_lines, idx = [], 0
    while idx < len(lines):
        ln = lines[idx]
        if ln.strip() == "OPCIONES:":
            idx += 1
            break
        if not RE_RULE.match(ln):
            stem_lines.append(ln)
        idx += 1
    situation, prompt = split_situation_prompt("\n".join(stem_lines))

    # 2) Options. Walk line by line, attaching text / marker / explanation to
    #    the option currently being built.
    options: list[dict] = []
    cur: dict | None = None
    field = "text"  # which part of `cur` trailing lines append to
    correct_letter = ""

    def flush():
        if cur is not None:
            cur["text"] = re.sub(r"\s+", " ", cur["text"]).strip()
            cur["explanation"] = re.sub(r"\s+", " ", cur["explanation"]).strip()
            options.append(cur)

    for ln in lines[idx:]:
        cm = RE_CORRECT.match(ln.strip())
        if cm:
            correct_letter = cm.group(1)
            continue
        om = RE_OPTION_START.match(ln)
        if om:
            flush()
            cur = {"letter": om.group(1), "text": om.group(2), "correct": False, "explanation": ""}
            field = "text"
            continue
        if cur is None:
            continue
        mm = RE_MARKER.match(ln)
        if mm:
            cur["correct"] = mm.group(1) == "✓"
            field = "expl_pending"
            continue
        em = RE_EXPL.match(ln)
        if em:
            cur["explanation"] = em.group(1)
            field = "explanation"
            continue
        # continuation line for whatever field we're in
        if ln.strip():
            if field == "text":
                cur["text"] += " " + ln.strip()
            elif field == "explanation":
                cur["explanation"] += " " + ln.strip()
    flush()

    if not correct_letter:
        for o in options:
            if o["correct"]:
                correct_letter = o["letter"]
                break

    return {
        "id": f"m{n}",
        "source": "mock",
        "domain": None,
        "scenario": None,
        "situation": situation,
        "question": prompt,
        "options": options,
        "correct": correct_letter,
    }


def parse(path: str) -> list[dict]:
    text = open(path, encoding="utf-8").read()
    return [parse_block(n, body) for n, body in split_blocks(text)]


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TXT
    questions = parse(path)
    json.dump(questions, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
