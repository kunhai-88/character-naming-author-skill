import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "skill" / "scripts" / "install_voice_dependency.py"
SPEC = importlib.util.spec_from_file_location("install_voice_dependency", SCRIPT)
INSTALLER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(INSTALLER)


class InstallVoiceDependencyTests(unittest.TestCase):
    def test_posix_python_path(self):
        self.assertEqual(INSTALLER.venv_python(Path("env"), "posix"), Path("env/bin/python"))

    def test_windows_python_path(self):
        self.assertEqual(INSTALLER.venv_python(Path("env"), "nt"), Path("env/Scripts/python.exe"))


if __name__ == "__main__":
    unittest.main()
