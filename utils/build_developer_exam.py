#!/usr/bin/env python3
"""Build developer_exam_en.html — the CCDV-F (Developer Foundations) practice exam.

Reuses the quiz engine in build_exam_html.py, the same way
build_professional_exam.py does. The differences from Architect Foundations:

  * eight domains instead of five, with the official CCDV-F weights
  * a weighted draw derived from the official domain weights, instead of a flat
    12 per domain, so an attempt matches the real exam's domain proportions
    (the split lives in developer_blueprint.py)
  * multiple-response items, scored all-or-nothing
  * English only — Anthropic delivers the exam and its prep content in English

Question bank: data/developer_questions.json (Ravn-authored practice items,
written against the official blueprint objectives — not real exam content).
Validate it with utils/validate_developer_bank.py.

Usage: python3 utils/build_developer_exam.py
"""
from __future__ import annotations
import json, os, sys

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
sys.path.insert(0, UTILS_DIR)

import build_exam_html as engine  # noqa: E402
from developer_blueprint import DRAW, EXAM_SIZE, check_draw  # noqa: E402

SPLIT = "/".join(str(DRAW[d]) for d in sorted(DRAW))

UI = dict(engine.UI["en"])
UI["threshold_note"] = (
    "Pass mark set at {p}/1000, the real CCDV-F cut score. Each attempt draws "
    + str(EXAM_SIZE) + " questions weighted to the official domain blueprint ("
    + SPLIT + "). "
    "Multiple-response items are scored all-or-nothing. The score is scaled to "
    "1000 as a study approximation of the real 100–1,000 scaled score. These are "
    "Ravn-authored practice items, not real exam content."
)


def main():
    blueprint = json.load(open(os.path.join(DATA_DIR, "developer_objectives.json"), encoding="utf-8"))
    questions = json.load(open(os.path.join(DATA_DIR, "developer_questions.json"), encoding="utf-8"))
    check_draw(blueprint)

    # Real-exam facts for the rotation strip come from the blueprint, so the
    # full-length rationale cannot drift from the transcription.
    exam = blueprint["_exam"]
    UI["draw_note_full"] = (
        "Every attempt draws a fresh random set: {n} of the {bank} bank "
        f"questions this time. Full length mirrors the real {exam['code']} "
        f"exam — {exam['items']} questions in {exam['minutes']} minutes.")

    domains_js = {d: {"name": v["name"], "weight": v["weight"]}
                  for d, v in blueprint["domains"].items()}

    # Assert the per-domain split, not just the total: a domain short of its own
    # draw silently reshapes an attempt away from the blueprint weights.
    for d, want in sorted(DRAW.items()):
        have = sum(1 for q in questions if str(q["domain"]) == d)
        if have < want:
            raise SystemExit(f"domain {d}: bank holds {have} items, the draw needs {want}")
    drawn = sum(DRAW.values())

    # The cut score comes from the CCDV-F blueprint, not from the Foundations
    # constant in the engine: the two agree today and must stay independent.
    pass_score = blueprint["_exam"]["pass_score"]
    scale_top = blueprint["_exam"]["scale"][1]

    engine.render_page(
        questions=questions,
        domains_js=domains_js,
        ui=UI,
        per_domain=DRAW,
        pass_score=pass_score,
        pass_pct=round(pass_score / scale_top * 100),
        store_key="ccdvf-exam-en",
        lang_attr="en",
        title="Claude Certified Developer — Foundations Practice Exam",
        page_title="Developer Foundations Practice Exam · Ravn",
        out_path=os.path.join(ROOT_DIR, "developer_exam_en.html"),
    )
    print(f"Draw per attempt: {drawn} questions across {len(domains_js)} domains "
          f"(bank of {len(questions)}).")


if __name__ == "__main__":
    main()
