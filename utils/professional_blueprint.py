#!/usr/bin/env python3
"""Shared CCAR-P blueprint facts: the official domains and the per-attempt draw.

data/professional_objectives.json is a pure transcription of Section 6 of the
official exam guide, so the draw — a property of this practice exam, not of the
guide — lives here instead. The builder and the validator both import it, so the
split cannot drift between the shipped page and the gate that checks it.

Usage: imported by build_professional_exam.py and validate_professional_bank.py.
"""
from __future__ import annotations
import json, os

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
BLUEPRINT_PATH = os.path.join(DATA_DIR, "professional_objectives.json")

EXAM_SIZE = 63

# Per-attempt draw per domain, from the official weights against 63 items:
# 17/13/19/16/14/14/7 % → 11 + 8 + 12 + 10 + 9 + 9 + 4 = 63. Keys are strings,
# matching the JSON blueprint; use draw_by_int_domain() where domains are ints.
DRAW = {"1": 11, "2": 8, "3": 12, "4": 10, "5": 9, "6": 9, "7": 4}


def load_blueprint(path: str = BLUEPRINT_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def draw_by_int_domain() -> dict:
    return {int(d): n for d, n in DRAW.items()}


def check_draw(blueprint: dict) -> None:
    """Fail loudly if DRAW stops describing the official blueprint."""
    domains = blueprint["domains"]
    if set(DRAW) != set(domains):
        raise SystemExit(f"draw covers {sorted(DRAW)}, blueprint has {sorted(domains)}")
    if sum(DRAW.values()) != EXAM_SIZE:
        raise SystemExit(f"draw totals {sum(DRAW.values())}, expected {EXAM_SIZE}")
    for d, n in DRAW.items():
        expected = round(domains[d]["weight"] / 100 * EXAM_SIZE)
        if n != expected:
            raise SystemExit(
                f"domain {d}: draw {n} does not match its {domains[d]['weight']}% "
                f"weight over {EXAM_SIZE} items (expected {expected})")
