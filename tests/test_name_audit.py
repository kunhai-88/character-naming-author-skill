import importlib.util
import json
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "skill" / "scripts" / "name_audit.py"
SPEC = importlib.util.spec_from_file_location("name_audit", SCRIPT)
NAME_AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(NAME_AUDIT)


class NameAuditTests(unittest.TestCase):
    def test_flags_template_style_given_names(self):
        result = NAME_AUDIT.audit(["叶知意", "陆沉川"])
        kinds = [item["type"] for item in result["findings"]]
        self.assertIn("template_char_hint", kinds)

    def test_family_surname_is_a_hint(self):
        result = NAME_AUDIT.audit(["赵建军", "赵小雨"])
        self.assertTrue(any(item["type"] == "same_surname" for item in result["findings"]))

    def test_social_prefix_is_not_surname(self):
        result = NAME_AUDIT.audit(["老赵", "老梁"])
        self.assertFalse(any(item["type"] == "same_surname" for item in result["findings"]))

    def test_flags_overly_uniform_cast_length(self):
        result = NAME_AUDIT.audit(["叶知意", "陆沉川", "陆安然", "陆守诚", "乔若薇"])
        self.assertTrue(any(item["type"] == "uniform_length" for item in result["findings"]))

    def test_regression_cases_include_bland_protagonist_rejection(self):
        path = Path(__file__).parents[1] / "benchmarks" / "regression_cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        case = next(item for item in cases if item["id"] == "reject-real-but-transferable-protagonist")
        self.assertEqual(case["names"], ["周平"])
        self.assertEqual(case["expected"], "reject-protagonist")

    def test_regression_cases_protect_strong_existing_name(self):
        path = Path(__file__).parents[1] / "benchmarks" / "regression_cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        case = next(item for item in cases if item["id"] == "preserve-rank-based-worker")
        self.assertEqual(case["names"], ["梁二"])
        self.assertEqual(case["expected"], "preserve")


if __name__ == "__main__":
    unittest.main()
