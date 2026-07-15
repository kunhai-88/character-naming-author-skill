import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "skill" / "scripts" / "name_audit.py"
SPEC = importlib.util.spec_from_file_location("name_audit", SCRIPT)
NAME_AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(NAME_AUDIT)


class NameAuditTests(unittest.TestCase):
    def test_flags_template_style_given_names(self):
        result = NAME_AUDIT.audit(["林知夏", "顾泽川"])
        kinds = [item["type"] for item in result["findings"]]
        self.assertIn("template_char_hint", kinds)

    def test_family_surname_is_a_hint(self):
        result = NAME_AUDIT.audit(["陈志远", "陈晓雨"])
        self.assertTrue(any(item["type"] == "same_surname" for item in result["findings"]))

    def test_social_prefix_is_not_surname(self):
        result = NAME_AUDIT.audit(["老陈", "老梁"])
        self.assertFalse(any(item["type"] == "same_surname" for item in result["findings"]))


if __name__ == "__main__":
    unittest.main()
