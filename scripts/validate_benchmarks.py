#!/usr/bin/env python3
"""Validate public qualitative regression case metadata."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "benchmarks" / "regression_cases.json"
ALLOWED = {
    "reject-system",
    "reject-protagonist",
    "preserve",
    "strengthen-calls",
    "transform-system",
    "conditional",
}


def main() -> None:
    cases = json.loads(PATH.read_text(encoding="utf-8"))
    if not isinstance(cases, list) or len(cases) < 5:
        raise SystemExit("ERROR: expected at least five regression cases")
    ids: set[str] = set()
    for case in cases:
        if set(case) != {"id", "genre", "names", "expected", "reason"}:
            raise SystemExit(f"ERROR: invalid fields in {case.get('id', '<unknown>')}")
        if case["id"] in ids:
            raise SystemExit(f"ERROR: duplicate id {case['id']}")
        ids.add(case["id"])
        if not case["names"] or not all(isinstance(name, str) and name for name in case["names"]):
            raise SystemExit(f"ERROR: invalid names in {case['id']}")
        if case["expected"] not in ALLOWED:
            raise SystemExit(f"ERROR: invalid expected decision in {case['id']}")
        if len(case["reason"]) < 12:
            raise SystemExit(f"ERROR: reason too short in {case['id']}")
    print(f"OK: {len(cases)} qualitative regression cases")


if __name__ == "__main__":
    main()
