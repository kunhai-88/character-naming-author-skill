#!/usr/bin/env python3
"""Install the optional voice dependency into a Skill-local virtualenv."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import venv


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VENV = SKILL_ROOT / ".voice-venv"
REQUIREMENTS = SKILL_ROOT / "requirements-voice.txt"


def venv_python(venv_root: Path, platform: str = os.name) -> Path:
    return venv_root / ("Scripts/python.exe" if platform == "nt" else "bin/python")


def install(venv_root: Path = DEFAULT_VENV, recreate: bool = False) -> Path:
    if recreate and venv_root.exists():
        shutil.rmtree(venv_root)
    if not REQUIREMENTS.is_file():
        raise FileNotFoundError(f"找不到依赖清单：{REQUIREMENTS}")
    if not venv_python(venv_root).is_file():
        venv.EnvBuilder(with_pip=True).create(venv_root)
    python = venv_python(venv_root)
    subprocess.run(
        [str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(REQUIREMENTS)],
        check=True,
    )
    version = subprocess.run(
        [str(python), "-c", "import pypinyin; print(pypinyin.__version__)"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    print(f"语音依赖已安装：pypinyin {version}")
    print(f"隔离环境：{venv_root}")
    return python


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recreate", action="store_true", help="删除并重建隔离环境")
    args = parser.parse_args()
    try:
        install(recreate=args.recreate)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"语音依赖安装失败：{exc}") from exc


if __name__ == "__main__":
    main()
