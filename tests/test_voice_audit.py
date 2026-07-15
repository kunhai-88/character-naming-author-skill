import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "skill" / "scripts" / "voice_audit.py"
SPEC = importlib.util.spec_from_file_location("voice_audit", SCRIPT)
VOICE_AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VOICE_AUDIT)


class VoiceAuditTests(unittest.TestCase):
    def test_finds_local_site_packages(self):
        root = Path(".voice-venv")
        candidates = VOICE_AUDIT.local_site_package_candidates(root)
        self.assertEqual(candidates[0], root / "Lib" / "site-packages")

    def test_detects_full_homophone(self):
        result = VOICE_AUDIT.audit(["章宁", "张凝"])
        finding = next(item for item in result["findings"] if item["names"] == ["章宁", "张凝"])
        self.assertEqual(finding["severity"], "high")
        self.assertIn("full_homophone", finding["signals"])

    def test_supports_pronunciation_override(self):
        result = VOICE_AUDIT.audit(["单超"], {"单超": ["shan4", "chao1"]})
        self.assertEqual(result["readings"][0]["tone3"], ["shan4", "chao1"])
        self.assertEqual(result["readings"][0]["initials"], ["sh", "ch"])
        self.assertTrue(result["readings"][0]["overridden"])

    def test_compound_surname_length(self):
        self.assertEqual(VOICE_AUDIT.surname_length("欧阳明"), 2)
        self.assertEqual(VOICE_AUDIT.surname_length("赵明"), 1)

    def test_ignores_single_weak_similarity_signal(self):
        result = VOICE_AUDIT.audit(["赵静", "周佳"])
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main()
