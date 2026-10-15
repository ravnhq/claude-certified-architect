#!/usr/bin/env python3
"""Shared CCAO-F blueprint facts and weighted 60-item practice draw."""
from __future__ import annotations
import json, os

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "ccaof", "data")
BLUEPRINT_PATH = os.path.join(DATA_DIR, "objectives.json")

EXAM_SIZE = 60
DRAW = {"1": 8, "2": 13, "3": 7, "4": 10, "5": 7, "6": 9, "7": 6}


def load_blueprint(path: str = BLUEPRINT_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def draw_by_int_domain() -> dict:
    return {int(d): n for d, n in DRAW.items()}


def expected_draw(domains: dict, size: int = EXAM_SIZE) -> dict:
    keys = sorted(domains, key=int)
    exact = {d: domains[d]["weight"] / 100 * size for d in keys}
    seats = {d: int(exact[d]) for d in keys}
    leftover = size - sum(seats.values())
    ranked = sorted(keys, key=lambda d: (-(exact[d] - seats[d]), int(d)))
    for d in ranked[:leftover]:
        seats[d] += 1
    return seats


def check_draw(blueprint: dict) -> None:
    domains = blueprint["domains"]
    if set(DRAW) != set(domains):
        raise SystemExit(f"draw covers {sorted(DRAW)}, blueprint has {sorted(domains)}")
    total_weight = sum(v["weight"] for v in domains.values())
    if total_weight != 100:
        raise SystemExit(f"blueprint weights total {total_weight}%, expected 100%")
    if sum(DRAW.values()) != EXAM_SIZE:
        raise SystemExit(f"draw totals {sum(DRAW.values())}, expected {EXAM_SIZE}")
    expected = expected_draw(domains)
    for d, n in sorted(DRAW.items(), key=lambda kv: int(kv[0])):
        if n != expected[d]:
            raise SystemExit(
                f"domain {d}: draw {n} does not match its {domains[d]['weight']}% "
                f"weight over {EXAM_SIZE} items (expected {expected[d]})")
