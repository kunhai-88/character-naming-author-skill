#!/usr/bin/env python3
"""Build a deterministic .skill archive from the validated skill directory."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skill"
DIST = ROOT / "dist"
NAME = "character-naming-author"
OUTPUT = DIST / f"{NAME}.skill"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_skill.py")], check=True)
    DIST.mkdir(exist_ok=True)
    OUTPUT.unlink(missing_ok=True)

    files = sorted(path for path in SOURCE.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(SOURCE)
            info = zipfile.ZipInfo(str(Path(NAME) / relative), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())

    print(f"Built {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
