#!/usr/bin/env python3
"""Audit Mandarin pronunciation collisions between Chinese character names."""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import itertools
import json
import re
from typing import Iterable

try:
    from pypinyin import Style, lazy_pinyin
    from pypinyin.contrib.tone_convert import to_finals, to_initials
except ImportError as exc:  # pragma: no cover - exercised by CLI environments
    raise SystemExit("需要可选依赖 pypinyin：python3 -m pip install 'pypinyin>=0.55,<0.56'") from exc


COMPOUND_SURNAMES = {
    "欧阳", "太史", "端木", "上官", "司马", "东方", "独孤", "南宫",
    "万俟", "闻人", "夏侯", "诸葛", "尉迟", "公羊", "赫连", "澹台",
    "皇甫", "宗政", "濮阳", "公冶", "太叔", "申屠", "公孙", "慕容",
    "仲孙", "钟离", "长孙", "宇文", "司徒", "鲜于", "司空", "闾丘",
    "子车", "亓官", "司寇", "巫马", "公西", "颛孙", "壤驷", "公良",
    "漆雕", "乐正", "宰父", "谷梁", "拓跋", "夹谷", "轩辕", "令狐",
    "段干", "百里", "呼延", "东郭", "南门", "羊舌", "微生", "梁丘",
    "左丘", "东门", "西门", "南宫",
}
TONE_RE = re.compile(r"^([a-züv]+?)([1-5])?$")


def surname_length(name: str) -> int:
    return 2 if name[:2] in COMPOUND_SURNAMES else 1


def parse_syllable(value: str) -> tuple[str, int]:
    match = TONE_RE.fullmatch(value.lower())
    if not match:
        return value.lower(), 0
    return match.group(1).replace("v", "ü"), int(match.group(2) or 5)


def parse_overrides(values: Iterable[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"读音覆盖格式应为 姓名=pin1,yin1：{value}")
        name, raw = value.split("=", 1)
        syllables = [item.strip().lower() for item in raw.split(",") if item.strip()]
        if not name or not syllables:
            raise ValueError(f"无效读音覆盖：{value}")
        result[name] = syllables
    return result


def reading(name: str, overrides: dict[str, list[str]] | None = None) -> dict:
    overrides = overrides or {}
    tone3 = overrides.get(name)
    if tone3 is None:
        tone3 = lazy_pinyin(
            name,
            style=Style.TONE3,
            strict=False,
            neutral_tone_with_five=True,
            errors="default",
        )
    parsed = [parse_syllable(item) for item in tone3]
    bases = [item[0] for item in parsed]
    tones = [item[1] for item in parsed]
    initials = [to_initials(base, strict=False) for base in bases]
    finals = [to_finals(base, strict=False, v_to_u=True) for base in bases]
    start = surname_length(name)
    return {
        "name": name,
        "tone3": tone3,
        "bases": bases,
        "tones": tones,
        "initials": initials,
        "finals": finals,
        "given_bases": bases[start:],
        "given_initials": initials[start:],
        "given_finals": finals[start:],
        "given_tones": tones[start:],
        "overridden": name in overrides,
    }


def compare(left: dict, right: dict) -> dict | None:
    signals: list[str] = []
    if left["bases"] == right["bases"] and left["tones"] == right["tones"]:
        signals.append("full_homophone")
    if left["given_bases"] and left["given_bases"] == right["given_bases"]:
        signals.append("same_given_pronunciation")
    if left["given_initials"] and left["given_initials"] == right["given_initials"]:
        signals.append("same_given_initials")
    if left["given_finals"] and left["given_finals"] == right["given_finals"]:
        signals.append("same_given_finals")
    if left["given_tones"] and left["given_tones"] == right["given_tones"]:
        signals.append("same_given_tone_pattern")
    if left["given_bases"] and right["given_bases"] and left["given_bases"][-1] == right["given_bases"][-1]:
        signals.append("same_final_syllable")
    similarity = SequenceMatcher(None, " ".join(left["bases"]), " ".join(right["bases"])).ratio()
    if similarity >= 0.82:
        signals.append("high_pronunciation_similarity")

    strong = (
        "full_homophone" in signals
        or "same_given_pronunciation" in signals
        or "high_pronunciation_similarity" in signals
        or ("same_given_finals" in signals and "same_given_tone_pattern" in signals)
        or ("same_final_syllable" in signals and "same_given_tone_pattern" in signals)
        or ("same_given_initials" in signals and "same_given_finals" in signals)
    )
    if not strong:
        return None
    if "full_homophone" in signals or "same_given_pronunciation" in signals:
        severity = "high"
    elif "high_pronunciation_similarity" in signals or len(signals) >= 3:
        severity = "medium"
    else:
        severity = "hint"
    return {
        "names": [left["name"], right["name"]],
        "severity": severity,
        "signals": signals,
        "similarity": round(similarity, 3),
    }


def audit(names: list[str], overrides: dict[str, list[str]] | None = None) -> dict:
    cleaned = list(dict.fromkeys(name.strip() for name in names if name.strip()))
    readings = [reading(name, overrides) for name in cleaned]
    findings = [item for pair in itertools.combinations(readings, 2) if (item := compare(*pair))]
    return {"names": cleaned, "readings": readings, "finding_count": len(findings), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="检查普通话姓名的同音、声母、韵母和声调碰撞")
    parser.add_argument("names", nargs="+", help="待检查的人物姓名")
    parser.add_argument(
        "--pronunciation",
        action="append",
        default=[],
        metavar="姓名=pin1,yin1",
        help="覆盖多音字或特殊姓名读音，可重复",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    try:
        overrides = parse_overrides(args.pronunciation)
    except ValueError as exc:
        parser.error(str(exc))
    result = audit(args.names, overrides)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    for item in result["readings"]:
        suffix = "（人工覆盖）" if item["overridden"] else ""
        print(f"- {item['name']}: {' '.join(item['tone3'])}{suffix}")
    print(f"发现 {result['finding_count']} 组语音提示。")
    for item in result["findings"]:
        print(f"- {' / '.join(item['names'])} [{item['severity']}]: {', '.join(item['signals'])}")
    print("语音提示采用普通话字典读音，不自动处理姓名习惯读法、方言或表演中的变调；结果不是改名结论。")


if __name__ == "__main__":
    main()
