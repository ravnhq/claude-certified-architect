#!/usr/bin/env python3
"""Validate the imported CCAO-F bank against the official Associate blueprint."""
from __future__ import annotations
import os, sys

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
sys.path.insert(0, UTILS_DIR)

import validate_developer_bank as validator  # noqa: E402
from associate_blueprint import check_draw, draw_by_int_domain  # noqa: E402

stated_select_counts = validator.stated_select_counts
validator.DATA_DIR = os.path.join(ROOT_DIR, "ccaof", "data")
validator.DRAW = draw_by_int_domain()
validator.check_draw = check_draw
validator.ID_PREFIX = "a"

if __name__ == "__main__":
    sys.exit(validator.main())
