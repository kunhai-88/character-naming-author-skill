#!/usr/bin/env python3
"""Prepare local blind naming tests and record human feedback as JSONL."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import random
import string


REASON_CODES = {
    "too_ai", "too_bland", "too_designed", "wrong_era", "wrong_region",
    "hard_to_say", "cast_collision", "no_relationship", "memorable_real",
    "story_owned",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_spec(spec: dict) -> None:
    required = {"case_id", "character_context", "candidates"}
    if not required.issubset(spec):
        raise ValueError(f"输入缺少字段：{', '.join(sorted(required - set(spec)))}")
    candidates = spec["candidates"]
    if not isinstance(candidates, list) or not 2 <= len(candidates) <= 8:
        raise ValueError("candidates 必须包含 2—8 个候选")
    for candidate in candidates:
        if not isinstance(candidate, dict) or not candidate.get("name"):
            raise ValueError("每个候选必须包含 name")


def prepare(spec: dict, seed: int | None = None) -> dict:
    validate_spec(spec)
    candidates = list(spec["candidates"])
    random.Random(seed).shuffle(candidates)
    public_candidates = []
    for index, candidate in enumerate(candidates):
        alias = string.ascii_uppercase[index]
        public_candidates.append({
            "alias": alias,
            "name": candidate["name"],
            "family_call": candidate.get("family_call", ""),
            "social_call": candidate.get("social_call", ""),
        })
    return {
        "schema_version": 1,
        "case_id": spec["case_id"],
        "character_context": spec["character_context"],
        "dialogue": spec.get("dialogue", []),
        "questions": [
            "哪个最像真实存在的人？",
            "哪个最容易记住？",
            "哪个最属于这个人物？",
            "哪个最像编剧或 AI 取的？",
            "十分钟后不看选项还能写出哪个？",
        ],
        "candidates": public_candidates,
    }


def resolve_alias(session: dict, alias: str | None) -> dict | None:
    if not alias:
        return None
    value = next((item for item in session["candidates"] if item["alias"] == alias.upper()), None)
    if value is None:
        raise ValueError(f"未知候选标签：{alias}")
    return {"alias": alias.upper(), "name": value["name"]}


def make_record(session: dict, args: argparse.Namespace) -> dict:
    reasons = list(dict.fromkeys(args.reason_code))
    unknown = set(reasons) - REASON_CODES
    if unknown:
        raise ValueError(f"未知原因码：{', '.join(sorted(unknown))}")
    if not any([
        args.winner, args.most_real, args.most_memorable, args.most_owned,
        args.most_ai, args.recalled_name, reasons, args.note,
    ]):
        raise ValueError("反馈为空：至少记录一个选择、回忆、原因码或备注")
    winner = resolve_alias(session, args.winner)
    recalled = args.recalled_name.strip() if args.recalled_name else ""
    return {
        "schema_version": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "case_id": session["case_id"],
        "winner": winner,
        "most_real": resolve_alias(session, args.most_real),
        "most_memorable": resolve_alias(session, args.most_memorable),
        "most_owned": resolve_alias(session, args.most_owned),
        "most_ai": resolve_alias(session, args.most_ai),
        "recalled_name": recalled,
        "delayed_recall_matches_winner": bool(winner and recalled and recalled == winner["name"]),
        "reason_codes": reasons,
        "note": args.note or "",
    }


def append_jsonl(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def summarize(path: Path) -> dict:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    reasons = Counter(code for record in records for code in record.get("reason_codes", []))
    cases_by_reason = {
        code: {record.get("case_id") for record in records if code in record.get("reason_codes", [])}
        for code in reasons
    }
    stable_patterns = {
        code: {"count": count, "unique_case_count": len(cases_by_reason[code])}
        for code, count in reasons.items()
        if count >= 5 or len(cases_by_reason[code]) >= 3
    }
    return {
        "record_count": len(records),
        "delayed_recall_match_count": sum(bool(item.get("delayed_recall_matches_winner")) for item in records),
        "reason_counts": dict(reasons.most_common()),
        "stable_reason_patterns": stable_patterns,
        "stability_rule": "同一原因至少出现 5 次，或跨 3 个不同案例出现，才视为稳定模式",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="本地角色姓名匿名盲测")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_parser = sub.add_parser("prepare", help="随机候选并隐藏解释")
    prepare_parser.add_argument("input", type=Path)
    prepare_parser.add_argument("output", type=Path)
    prepare_parser.add_argument("--seed", type=int)

    record_parser = sub.add_parser("record", help="追加一条人类反馈")
    record_parser.add_argument("session", type=Path)
    record_parser.add_argument("output", type=Path)
    record_parser.add_argument("--winner")
    record_parser.add_argument("--most-real")
    record_parser.add_argument("--most-memorable")
    record_parser.add_argument("--most-owned")
    record_parser.add_argument("--most-ai")
    record_parser.add_argument("--recalled-name", default="")
    record_parser.add_argument("--reason-code", action="append", default=[])
    record_parser.add_argument("--note")

    summary_parser = sub.add_parser("summary", help="汇总 JSONL 反馈")
    summary_parser.add_argument("input", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "prepare":
            session = prepare(load_json(args.input), args.seed)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(session, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"已生成本地盲测：{args.output}")
        elif args.command == "record":
            record = make_record(load_json(args.session), args)
            append_jsonl(args.output, record)
            print(f"已追加反馈：{args.output}")
        else:
            print(json.dumps(summarize(args.input), ensure_ascii=False, indent=2))
    except (ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
