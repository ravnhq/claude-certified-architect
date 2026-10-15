#!/usr/bin/env python3
"""Build the CCAO-F Associate Foundations practice exam and bank browser."""
from __future__ import annotations
import json, os, sys

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "ccaof", "data")
sys.path.insert(0, UTILS_DIR)

import build_exam_html as engine  # noqa: E402
from associate_blueprint import DRAW, EXAM_SIZE, check_draw  # noqa: E402

SPLIT = "/".join(str(DRAW[d]) for d in sorted(DRAW))
UI = dict(engine.UI["en"])
UI["threshold_note"] = (
    "Pass mark set at {p}/1000, the real CCAO-F cut score. Each attempt draws "
    + str(EXAM_SIZE) + " questions weighted to the official domain blueprint ("
    + SPLIT + "). Multiple-response items are scored all-or-nothing. The score "
    "is scaled to 1000 as a study approximation of the real 100–1,000 scale."
)


def main():
    blueprint = json.load(open(os.path.join(DATA_DIR, "objectives.json"), encoding="utf-8"))
    questions = json.load(open(os.path.join(DATA_DIR, "questions.json"), encoding="utf-8"))
    check_draw(blueprint)
    exam = blueprint["_exam"]
    UI["draw_note_full"] = (
        "Every attempt draws a fresh random set: {n} of the {bank} bank questions "
        f"this time. Full length mirrors the real {exam['code']} exam — "
        f"{exam['items']} questions in {exam['minutes']} minutes."
    )
    domains_js = {d: {"name": v["name"], "weight": v["weight"]}
                  for d, v in blueprint["domains"].items()}
    for d, want in sorted(DRAW.items()):
        have = sum(1 for q in questions if str(q["domain"]) == d)
        if have < want:
            raise SystemExit(f"domain {d}: bank holds {have} items, the draw needs {want}")
    common = dict(
        domains_js=domains_js,
        ui=UI,
        per_domain=DRAW,
        pass_score=exam["pass_score"],
        pass_pct=round(exam["pass_score"] / exam["scale"][1] * 100),
        store_key="ccaof-exam-en",
        lang_attr="en",
        exam_code="CCAO-F",
        report_map={str(q["task_id"]): str(q["task_id"]) for q in questions},
    )
    engine.render_page(
        questions=questions,
        title="Claude Certified Associate — Foundations Practice Exam",
        page_title="Associate Foundations Practice Exam · Ravn",
        out_path=os.path.join(ROOT_DIR, "ccaof", "dist", "exam_en.html"),
        bank_href="bank-associate-en.html",
        **common,
    )
    engine.render_page(
        questions=questions,
        title=UI["browse_title"],
        page_title=f"{UI['browse_title']} · Ravn",
        out_path=os.path.join(ROOT_DIR, "ccaof", "dist", "bank_en.html"),
        view="bank",
        exam_href="associate-en.html",
        **common,
    )
    print(f"Draw per attempt: {sum(DRAW.values())} questions across "
          f"{len(domains_js)} domains (bank of {len(questions)}).")


if __name__ == "__main__":
    main()
