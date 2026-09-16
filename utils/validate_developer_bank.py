#!/usr/bin/env python3
"""Validate ccdf/data/questions.json against the official CCDV-F blueprint.

Fails loudly on anything that would produce a wrong or unusable practice item:
schema drift, an answer key that disagrees with the option flags, an objective
string that is not in the official exam guide, or a stem whose stated number of
answers disagrees with its key. Shape drift the imported practice-bank corpus does
not control — an uncovered objective, an unusual multiple-response share — is
reported as a warning instead.

Mirrors utils/validate_professional_bank.py.

Usage: python3 utils/validate_developer_bank.py [path]
"""
from __future__ import annotations
import json, os, re, sys
from collections import Counter

# Option letters are reassigned when the bank is rebalanced, so an explanation
# that points at "option D" or "C below" silently becomes wrong. The keyword is
# matched in both cases, because "Option D fails because..." at the start of a
# sentence is the usual way to write it; the letter stays uppercase on purpose.
# re.IGNORECASE over the whole pattern would flag the ordinary phrase "see a
# cost spike".
#
# A reference to a letter the item does not have is broken today and fails. One
# that resolves is only a hazard: utils/import_practice_bank.py keeps the practice bank's
# option order, and the exam engine never shuffles options, so the reference is
# still accurate — it warns instead, because a handful of imported explanations
# use it and rewriting third-party rationale to satisfy a style rule would be a
# worse trade than flagging it.
CROSS_REF = re.compile(r'\b(?:[Oo]ptions?|[Ss]ee)\s+([A-H])\b|\b([A-H])\s+(?:below|above)\b')

# The stem of a multiple-response item must state the same count the item is
# keyed to. A stem that says "(Select TWO.)" on an item keyed to three answers
# renders under a "Select 3 responses." badge, and all-or-nothing scoring then
# marks a candidate who obeys the stem wrong.
SELECT_WORD = re.compile(r'\bselect\b', re.IGNORECASE)
NUMBER_RE = re.compile(r'\b(one|two|three|four|five|[1-5])\b', re.IGNORECASE)
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def stated_select_counts(question: str) -> list[int]:
    """Every count the stem states after the word "select".

    The number is not always the token right after "select" — a stem may write
    "Select the TWO configuration changes" — so read the rest of that sentence
    and take its first number. Prose elsewhere in the stem is ignored.
    """
    counts = []
    for m in SELECT_WORD.finditer(question):
        sentence = re.split(r'[.?!)]', question[m.end():m.end() + 60], maxsplit=1)[0]
        found = NUMBER_RE.search(sentence)
        if found:
            word = found.group(1).lower()
            counts.append(NUMBER_WORDS.get(word) or int(word))
    return counts

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "ccdf", "data")
sys.path.insert(0, UTILS_DIR)

from developer_blueprint import check_draw, draw_by_int_domain  # noqa: E402

# Per-attempt draw, shared with the builder so the two cannot disagree. It is
# also the bank's floor: a domain holding fewer items than its draw cannot fill
# an attempt.
DRAW = draw_by_int_domain()

# Eight is what the practice-bank corpus needs; two imported items run to H.
LETTERS = "ABCDEFGH"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DATA_DIR, "questions.json")
    blueprint = json.load(open(os.path.join(DATA_DIR, "objectives.json"), encoding="utf-8"))
    check_draw(blueprint)
    official = {int(d): set(v["objectives"]) for d, v in blueprint["domains"].items()}

    items = json.load(open(path, encoding="utf-8"))
    errors, warnings, seen_ids = [], [], set()

    def err(item_id, msg):
        errors.append(f"{item_id}: {msg}")

    def warn(msg):
        warnings.append(msg)

    for q in items:
        qid = q.get("id", "<no id>")
        if qid in seen_ids:
            err(qid, "duplicate id")
        seen_ids.add(qid)

        dom = q.get("domain")
        if dom not in official:
            err(qid, f"domain {dom!r} is not 1-8")
            continue
        if not qid.startswith(f"d{dom}-"):
            err(qid, f"id does not carry its domain prefix d{dom}-")
        if q.get("objective") not in official[dom]:
            err(qid, f"objective is not an official domain-{dom} objective: {q.get('objective')!r}")

        # `situation` is optional: an imported item whose stem is a single
        # sentence is all ask and no scenario, and the page omits the block.
        if not (q.get("question") or "").strip():
            err(qid, "empty question")

        opts = q.get("options") or []
        letters = [o.get("letter") for o in opts]
        if letters != list(LETTERS[:len(opts)]):
            err(qid, f"option letters must be sequential from A, got {letters}")
        for o in opts:
            if not (o.get("text") or "").strip():
                err(qid, f"option {o.get('letter')} has empty text")
            if not (o.get("explanation") or "").strip():
                err(qid, f"option {o.get('letter')} has empty explanation")
            for m in CROSS_REF.finditer(o.get("explanation") or ""):
                ref = m.group(1) or m.group(2)
                if ref not in letters:
                    err(qid, f"option {o.get('letter')} explanation references option {ref}, "
                             f"which this item does not have")
                else:
                    warn(f"{qid}: option {o.get('letter')} explanation refers to option "
                         f"{ref} by letter")

        correct = q.get("correct")
        select = q.get("select")
        flagged = sorted(o["letter"] for o in opts if o.get("correct"))
        is_multi = isinstance(correct, list)

        stem = q.get("question") or ""
        stated = stated_select_counts(stem)
        if is_multi:
            # Multiple-response items normally offer five or more, but the
            # corpus holds one four-option "pick two", which is still a real
            # item with two distractors. What is never acceptable is a key that
            # covers every option, leaving nothing to discriminate on.
            if not 4 <= len(opts) <= 8:
                err(qid, f"multiple-response items need 4-8 options, got {len(opts)}")
            if len(correct) >= len(opts):
                err(qid, f"every one of the {len(opts)} options is keyed correct")
            if not 2 <= len(correct) <= 5:
                err(qid, f"multiple-response items select 2-5, got {len(correct)}")
            if not stated:
                err(qid, "multiple-response question does not state how many to select")
            # One stated count must be the keyed one; another may be prose the
            # scan above picked up ("...neither of those two changes..." on an
            # item keyed to three). What must never happen is a stem that states
            # only a count the key contradicts.
            elif len(correct) not in stated:
                err(qid, f"stem asks the candidate to select {sorted(set(stated))}, "
                         f"but the item is keyed to {len(correct)} answer(s)")
        else:
            if not 4 <= len(opts) <= 8:
                err(qid, f"single-response items need 4-8 options, got {len(opts)}")
            if any(n != 1 for n in stated):
                err(qid, f"single-response stem asks the candidate to select {sorted(set(stated))}")

        key = sorted(correct) if is_multi else [correct]
        if key != flagged:
            err(qid, f"answer key {key} disagrees with option correct flags {flagged}")
        if select != len(key):
            err(qid, f"select={select!r} does not match {len(key)} correct answer(s)")
        for L in key:
            if L not in letters:
                err(qid, f"answer key letter {L} is not an option")

    # The bank only has to be able to fill an attempt. Its size is now a
    # property of the imported corpus, not a number this file gets to choose.
    by_domain = Counter(q.get("domain") for q in items)
    for dom in sorted(official):
        if by_domain[dom] < DRAW[dom]:
            errors.append(f"domain {dom}: bank ({by_domain[dom]}) smaller than the draw ({DRAW[dom]})")

    # Coverage is a warning, not a gate: the imported corpus is whatever
    # the practice bank publishes, and an objective nobody asked about is a study gap
    # to fill, not a reason to refuse to build the page.
    covered = Counter((q.get("domain"), q.get("objective")) for q in items)
    for dom, objs in sorted(official.items()):
        for obj in sorted(objs):
            if covered[(dom, obj)] == 0:
                warn(f"domain {dom}: no item covers objective {obj!r}")

    multi = sum(1 for q in items if isinstance(q.get("correct"), list))
    share = multi / len(items) * 100 if items else 0
    if not 10 <= share <= 35:
        warn(f"multiple-response share {share:.1f}% is outside the usual 10-35% band")

    single_letters = Counter(q["correct"] for q in items if isinstance(q.get("correct"), str))

    print(f"items           {len(items)} (draw {sum(DRAW.values())} per attempt)")
    print(f"per domain      {dict(sorted(by_domain.items()))}")
    print(f"draw per attempt{dict(sorted(DRAW.items()))} = {sum(DRAW.values())}")
    print(f"multi-response  {multi} ({share:.1f}%)")
    print(f"answer letters  {dict(sorted(single_letters.items()))}")
    print(f"objectives      {len(covered)} of {sum(len(v) for v in official.values())} covered")

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  ! {w}")

    if errors:
        print(f"\nFAILED — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK — bank matches the official blueprint.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
