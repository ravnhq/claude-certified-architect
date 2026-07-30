#!/usr/bin/env python3
"""Validate data/professional_questions.json against the official CCAR-P blueprint.

Fails loudly on anything that would produce a wrong or unusable practice item:
schema drift, an answer key that disagrees with the option flags, an objective
string that is not in the official exam guide, or a domain left uncovered.

Usage: python3 utils/validate_professional_bank.py [path]
"""
from __future__ import annotations
import json, os, re, sys
from collections import Counter

# Option letters are reassigned when the bank is rebalanced, so an explanation
# that points at "option D" or "C below" silently becomes wrong. Explanations
# must stand on their own.
CROSS_REF = re.compile(r'\b(?:option|options|see)\s+[A-E]\b|\b[A-E]\s+(?:below|above)\b')

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Bank size per domain, ~2x the per-attempt draw so repeat attempts vary.
BANK_TARGET = {1: 22, 2: 16, 3: 24, 4: 20, 5: 18, 6: 18, 7: 8}
# Per-attempt draw, matching the official weights: 63 items total.
DRAW = {1: 11, 2: 8, 3: 12, 4: 10, 5: 9, 6: 9, 7: 4}

LETTERS = "ABCDE"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DATA_DIR, "professional_questions.json")
    blueprint = json.load(open(os.path.join(DATA_DIR, "professional_objectives.json"), encoding="utf-8"))
    official = {int(d): set(v["objectives"]) for d, v in blueprint["domains"].items()}

    items = json.load(open(path, encoding="utf-8"))
    errors, seen_ids = [], set()

    def err(item_id, msg):
        errors.append(f"{item_id}: {msg}")

    for q in items:
        qid = q.get("id", "<no id>")
        if qid in seen_ids:
            err(qid, "duplicate id")
        seen_ids.add(qid)

        dom = q.get("domain")
        if dom not in official:
            err(qid, f"domain {dom!r} is not 1-7")
            continue
        if not qid.startswith(f"p{dom}-"):
            err(qid, f"id does not carry its domain prefix p{dom}-")
        if q.get("objective") not in official[dom]:
            err(qid, f"objective is not an official domain-{dom} objective: {q.get('objective')!r}")

        for field in ("situation", "question"):
            if not (q.get(field) or "").strip():
                err(qid, f"empty {field}")

        opts = q.get("options") or []
        letters = [o.get("letter") for o in opts]
        if letters != list(LETTERS[:len(opts)]):
            err(qid, f"option letters must be sequential from A, got {letters}")
        for o in opts:
            if not (o.get("text") or "").strip():
                err(qid, f"option {o.get('letter')} has empty text")
            if not (o.get("explanation") or "").strip():
                err(qid, f"option {o.get('letter')} has empty explanation")
            if CROSS_REF.search(o.get("explanation") or ""):
                err(qid, f"option {o.get('letter')} explanation references another option by letter")

        correct = q.get("correct")
        select = q.get("select")
        flagged = sorted(o["letter"] for o in opts if o.get("correct"))
        is_multi = isinstance(correct, list)

        if is_multi:
            if len(opts) != 5:
                err(qid, f"multiple-response items need 5 options, got {len(opts)}")
            if not 2 <= len(correct) <= 3:
                err(qid, f"multiple-response items select 2 or 3, got {len(correct)}")
            if "select" not in (q.get("question") or "").lower():
                err(qid, "multiple-response question does not state how many to select")
        else:
            if len(opts) != 4:
                err(qid, f"single-response items need 4 options, got {len(opts)}")

        key = sorted(correct) if is_multi else [correct]
        if key != flagged:
            err(qid, f"answer key {key} disagrees with option correct flags {flagged}")
        if select != len(key):
            err(qid, f"select={select!r} does not match {len(key)} correct answer(s)")
        for L in key:
            if L not in letters:
                err(qid, f"answer key letter {L} is not an option")

    by_domain = Counter(q.get("domain") for q in items)
    for dom, target in BANK_TARGET.items():
        if by_domain[dom] != target:
            errors.append(f"domain {dom}: expected {target} items, found {by_domain[dom]}")
        if by_domain[dom] < DRAW[dom]:
            errors.append(f"domain {dom}: bank ({by_domain[dom]}) smaller than the draw ({DRAW[dom]})")

    # Every official objective must be exercised by at least one item.
    covered = Counter((q.get("domain"), q.get("objective")) for q in items)
    for dom, objs in official.items():
        for obj in objs:
            if covered[(dom, obj)] == 0:
                errors.append(f"domain {dom}: no item covers objective {obj!r}")

    multi = sum(1 for q in items if isinstance(q.get("correct"), list))
    share = multi / len(items) * 100 if items else 0
    if not 15 <= share <= 25:
        errors.append(f"multiple-response share {share:.1f}% is outside the 15-25% band")

    single_letters = Counter(q["correct"] for q in items if isinstance(q.get("correct"), str))

    print(f"items           {len(items)} (target {sum(BANK_TARGET.values())})")
    print(f"per domain      {dict(sorted(by_domain.items()))}")
    print(f"draw per attempt{dict(sorted(DRAW.items()))} = {sum(DRAW.values())}")
    print(f"multi-response  {multi} ({share:.1f}%)")
    print(f"answer letters  {dict(sorted(single_letters.items()))}")
    print(f"objectives      {len(covered)} of {sum(len(v) for v in official.values())} covered")

    if errors:
        print(f"\nFAILED — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK — bank matches the official blueprint.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
