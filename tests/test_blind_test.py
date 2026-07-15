import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "skill" / "scripts" / "blind_test.py"
SPEC = importlib.util.spec_from_file_location("blind_test", SCRIPT)
BLIND_TEST = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BLIND_TEST)


class BlindTestTests(unittest.TestCase):
    def setUp(self):
        self.spec = {
            "case_id": "case-1",
            "character_context": "匿名人物资料",
            "dialogue": ["一句匿名对白"],
            "candidates": [
                {"name": "赵建军", "family_call": "建军", "explanation": "不得进入盲测"},
                {"name": "梁二", "social_call": "二哥", "explanation": "不得进入盲测"},
                {"name": "陈静", "social_call": "陈师傅", "explanation": "不得进入盲测"},
            ],
        }

    def test_prepare_is_deterministic_and_hides_explanations(self):
        first = BLIND_TEST.prepare(self.spec, seed=7)
        second = BLIND_TEST.prepare(self.spec, seed=7)
        self.assertEqual(first, second)
        self.assertNotIn("explanation", json.dumps(first, ensure_ascii=False))

    def test_record_and_summary(self):
        session = BLIND_TEST.prepare(self.spec, seed=7)
        args = argparse.Namespace(
            winner="A",
            most_real="A",
            most_memorable="A",
            most_owned="B",
            most_ai="C",
            recalled_name=next(item["name"] for item in session["candidates"] if item["alias"] == "A"),
            reason_code=["memorable_real"],
            note="匿名反馈",
        )
        record = BLIND_TEST.make_record(session, args)
        self.assertTrue(record["delayed_recall_matches_winner"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "feedback.jsonl"
            BLIND_TEST.append_jsonl(path, record)
            summary = BLIND_TEST.summarize(path)
        self.assertEqual(summary["record_count"], 1)
        self.assertEqual(summary["reason_counts"], {"memorable_real": 1})
        self.assertEqual(summary["stable_reason_patterns"], {})

    def test_summary_requires_cross_case_evidence_for_stable_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "feedback.jsonl"
            for index in range(3):
                BLIND_TEST.append_jsonl(path, {
                    "case_id": f"case-{index}",
                    "reason_codes": ["too_bland"],
                    "delayed_recall_matches_winner": False,
                })
            summary = BLIND_TEST.summarize(path)
        self.assertEqual(summary["stable_reason_patterns"]["too_bland"]["unique_case_count"], 3)


if __name__ == "__main__":
    unittest.main()
