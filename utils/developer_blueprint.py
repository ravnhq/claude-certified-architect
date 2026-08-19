#!/usr/bin/env python3
"""Shared CCDV-F blueprint facts: the official domains and the per-attempt draw.

data/developer_objectives.json is a pure transcription of Section 6 of the
official exam guide, so the draw — a property of this practice exam, not of the
guide — lives here instead. The builder and the validator both import it, so the
split cannot drift between the shipped page and the gate that checks it.

Mirrors utils/professional_blueprint.py; the two tracks differ only in their
blueprint file, exam size, and domain count.

Usage: imported by build_developer_exam.py and validate_developer_bank.py.
"""
from __future__ import annotations
import json, os

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
BLUEPRINT_PATH = os.path.join(DATA_DIR, "developer_objectives.json")

EXAM_SIZE = 53

# Per-attempt draw per domain, from the official weights against 53 items:
# 14.7/33.1/3.1/2.6/16.8/11.0/8.1/10.6 % → 8 + 17 + 2 + 1 + 9 + 6 + 4 + 6 = 53.
# Keys are strings, matching the JSON blueprint; use draw_by_int_domain() where
# domains are ints.
DRAW = {"1": 8, "2": 17, "3": 2, "4": 1, "5": 9, "6": 6, "7": 4, "8": 6}


def load_blueprint(path: str = BLUEPRINT_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def draw_by_int_domain() -> dict:
    return {int(d): n for d, n in DRAW.items()}


def expected_draw(domains: dict, size: int = EXAM_SIZE) -> dict:
    """Apportion `size` items over the official domain weights.

    Largest remainder (Hare-Niemeyer): give every domain its whole part, then
    hand the leftover seats to the largest fractions. Per-domain round() cannot
    be used here — rounded shares need not add up to `size`, so a later weight
    revision would leave no draw able to satisfy both the per-domain check and
    the total, and the gate would reject every possible fix.
    """
    keys = sorted(domains, key=int)
    exact = {d: domains[d]["weight"] / 100 * size for d in keys}
    seats = {d: int(exact[d]) for d in keys}
    leftover = size - sum(seats.values())
    # Ties break on domain order, so the result is stable run to run.
    ranked = sorted(keys, key=lambda d: (-(exact[d] - seats[d]), int(d)))
    for d in ranked[:leftover]:
        seats[d] += 1
    return seats


def check_draw(blueprint: dict) -> None:
    """Fail loudly if DRAW stops describing the official blueprint."""
    domains = blueprint["domains"]
    if set(DRAW) != set(domains):
        raise SystemExit(f"draw covers {sorted(DRAW)}, blueprint has {sorted(domains)}")
    # The CCDV-F weights are given to one decimal, so compare with a tolerance
    # rather than ==: 14.7 + 33.1 + ... is 100.00000000000001 in binary floats.
    total_weight = sum(v["weight"] for v in domains.values())
    if abs(total_weight - 100) > 0.05:
        raise SystemExit(f"blueprint weights total {total_weight}%, expected 100%")
    if sum(DRAW.values()) != EXAM_SIZE:
        raise SystemExit(f"draw totals {sum(DRAW.values())}, expected {EXAM_SIZE}")
    expected = expected_draw(domains)
    for d, n in sorted(DRAW.items(), key=lambda kv: int(kv[0])):
        if n != expected[d]:
            raise SystemExit(
                f"domain {d}: draw {n} does not match its {domains[d]['weight']}% "
                f"weight over {EXAM_SIZE} items (expected {expected[d]})")
