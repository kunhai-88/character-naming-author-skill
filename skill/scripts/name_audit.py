#!/usr/bin/env python3
"""Flag mechanical naming risks. Literary judgment remains with the author."""

from __future__ import annotations

import argparse
import itertools
import json


RISK_SURNAMES = set("顾傅霍裴沈陆")
RISK_GIVEN_CHARS = set("沉舟砚珩川夜渊知念晚微棠霜安夏意薇")


def surname(name: str) -> str:
    """Best-effort surname for ordinary names and 老陈/小赵-style labels."""
    if len(name) == 2 and name[0] in "老小阿大":
        return name[1]
    return name[0]


def audit(names: list[str]) -> dict:
    cleaned = [n.strip() for n in names if n.strip()]
    findings: list[dict] = []

    for name in cleaned:
        given_hits = sorted(set(name[1:]) & RISK_GIVEN_CHARS)
        risky_combo = surname(name) in RISK_SURNAMES and bool(given_hits)
        if given_hits or risky_combo:
            findings.append({
                "type": "template_char_hint",
                "names": [name],
                "detail": "命中高频类型组合，仅作人工复核提示：" + "、".join(given_hits),
            })

    for left, right in itertools.combinations(cleaned, 2):
        if left == right:
            findings.append({"type": "duplicate", "names": [left, right], "detail": "姓名完全重复"})
            continue
        if surname(left) == surname(right):
            findings.append({"type": "same_surname", "names": [left, right], "detail": "同姓，确认是否为亲属或有意设置"})
        shared_given = sorted(set(left[1:]) & set(right[1:]))
        if shared_given:
            findings.append({
                "type": "shared_given_char",
                "names": [left, right],
                "detail": "名字共享字，成片听感可能接近：" + "、".join(shared_given),
            })
        if len(left) == len(right) and left[-1] == right[-1]:
            findings.append({"type": "same_ending", "names": [left, right], "detail": "同长度且尾字相同"})

    return {"names": cleaned, "finding_count": len(findings), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="检查角色姓名中的机械性风险")
    parser.add_argument("names", nargs="+", help="待检查的人物姓名")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    result = audit(args.names)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"检查 {len(result['names'])} 个姓名，发现 {result['finding_count']} 条提示。")
    for item in result["findings"]:
        print(f"- {' / '.join(item['names'])}: {item['detail']}")
    if not result["findings"]:
        print("- 未发现机械性风险；仍需进行人物与对白盲审。")


if __name__ == "__main__":
    main()
