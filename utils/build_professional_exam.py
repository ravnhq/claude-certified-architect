#!/usr/bin/env python3
"""Build professional_exam_en.html — the CCAR-P (Professional) practice exam.

Reuses the quiz engine in build_exam_html.py. The differences from Foundations:

  * seven domains instead of five, with the official CCAR-P weights
  * a weighted draw (11/8/12/10/9/9/4 = 63) instead of a flat 12 per domain,
    so an attempt matches the real exam's domain proportions
  * multiple-response items, scored all-or-nothing
  * English only — Anthropic delivers the exam and its prep content in English

Question bank: data/professional_questions.json (Ravn-authored practice items,
written against the official blueprint objectives — not real exam content).
Validate it with utils/validate_professional_bank.py.

Usage: python3 utils/build_professional_exam.py
"""
from __future__ import annotations
import json, os, sys

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
sys.path.insert(0, UTILS_DIR)

import build_exam_html as engine  # noqa: E402

# Per-attempt draw per domain, from the official weights against 63 items:
# 17/13/19/16/14/14/7 % → 11 + 8 + 12 + 10 + 9 + 9 + 4 = 63.
DRAW = {"1": 11, "2": 8, "3": 12, "4": 10, "5": 9, "6": 9, "7": 4}

UI = dict(engine.UI["en"])
UI["threshold_note"] = (
    "Pass mark set at {p}/1000, the real CCAR-P cut score. Each attempt draws 63 "
    "questions weighted to the official domain blueprint (11/8/12/10/9/9/4). "
    "Multiple-response items are scored all-or-nothing. The score is scaled to "
    "1000 as a study approximation of the real 100–1,000 scaled score. These are "
    "Ravn-authored practice items, not real exam content."
)


def main():
    blueprint = json.load(open(os.path.join(DATA_DIR, "professional_objectives.json"), encoding="utf-8"))
    questions = json.load(open(os.path.join(DATA_DIR, "professional_questions.json"), encoding="utf-8"))

    domains_js = {d: {"name": v["name"], "weight": v["weight"]}
                  for d, v in blueprint["domains"].items()}

    drawn = sum(min(DRAW[d], sum(1 for q in questions if str(q["domain"]) == d)) for d in DRAW)
    if drawn != 63:
        raise SystemExit(f"draw is {drawn}, expected 63 — the bank is too small for the blueprint")

    engine.render_page(
        questions=questions,
        domains_js=domains_js,
        ui=UI,
        per_domain=DRAW,
        store_key="ccarp-exam-en",
        lang_attr="en",
        title="Claude Certified Architect — Professional Practice Exam",
        page_title="Professional Practice Exam · Ravn",
        out_path=os.path.join(ROOT_DIR, "professional_exam_en.html"),
    )
    print(f"Draw per attempt: {drawn} questions across {len(domains_js)} domains "
          f"(bank of {len(questions)}).")


if __name__ == "__main__":
    main()
