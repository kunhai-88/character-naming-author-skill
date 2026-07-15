#!/usr/bin/env python3
"""Validate the repository's Agent Skill without third-party dependencies."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skill"
SKILL_MD = SKILL_ROOT / "SKILL.md"
EXPECTED_NAME = "character-naming-author"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    if not SKILL_MD.is_file():
        fail("skill/SKILL.md is missing")

    text = SKILL_MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) >= 500:
        fail(f"SKILL.md has {len(lines)} lines; expected fewer than 500")
    if not lines or lines[0] != "---":
        fail("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail("SKILL.md frontmatter is not closed")

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-zA-Z][\w-]*):\s*(.+)", line)
        if not match:
            fail(f"unsupported frontmatter line: {line!r}")
        fields[match.group(1)] = match.group(2).strip().strip('"\'')

    if set(fields) != {"name", "description"}:
        fail("frontmatter must contain only name and description")
    if fields["name"] != EXPECTED_NAME:
        fail(f"name must be {EXPECTED_NAME!r}")
    if len(fields["description"]) < 40:
        fail("description is too short to be a useful trigger")

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for target in link_pattern.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        path = (SKILL_ROOT / target).resolve()
        if SKILL_ROOT.resolve() not in path.parents and path != SKILL_ROOT.resolve():
            fail(f"link escapes skill directory: {target}")
        if not path.exists():
            fail(f"linked resource does not exist: {target}")

    expected = [
        SKILL_ROOT / "references" / "author-naming-method.md",
        SKILL_ROOT / "references" / "anti-ai-audit.md",
        SKILL_ROOT / "references" / "memorability-and-ownership.md",
        SKILL_ROOT / "references" / "candidate-selection.md",
        SKILL_ROOT / "references" / "reality-calibration.md",
        SKILL_ROOT / "references" / "naming-mechanism-library.md",
        SKILL_ROOT / "references" / "human-evaluation.md",
        SKILL_ROOT / "scripts" / "name_audit.py",
        SKILL_ROOT / "scripts" / "voice_audit.py",
        SKILL_ROOT / "scripts" / "install_voice_dependency.py",
        SKILL_ROOT / "scripts" / "blind_test.py",
        SKILL_ROOT / "requirements-voice.txt",
    ]
    for path in expected:
        if not path.is_file():
            fail(f"required resource is missing: {path.relative_to(ROOT)}")

    print(f"OK: {EXPECTED_NAME} ({len(lines)} SKILL.md lines)")


if __name__ == "__main__":
    main()
