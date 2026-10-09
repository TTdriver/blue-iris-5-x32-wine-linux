import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


configure = load("configure-test")
filter_export = load("filter-camera-export")
from wine_registry import CAMERA_ROOT, FOLDER_ROOT, ensure_stopped


def fixture():
    text = "WINE REGISTRY Version 2\n#arch=win32\n\n"
    for name in ("Example Camera A", "Example Camera B"):
        key = (CAMERA_ROOT + "\\" + name).replace("\\", "\\\\")
        text += ('[' + key + '] 0\n"enabled"=dword:00000001\n'
                 '"ippw"="PRIVATE_PLACEHOLDER"\n"ip"="198.51.100.20/old-path"\n'
                 '"xres"=dword:00000f00\n"yres"=dword:00000870\n\n')
        text += '[' + key + '\\\\Clips\\\\1] 0\n"continuous"=dword:00000000\n\n'
    for number in ("0", "1", "2", "16"):
        key = (FOLDER_ROOT + "\\" + number).replace("\\", "\\\\")
        text += '[' + key + '] 0\n"archmb"=dword:00010000\n\n'
    text += '[Software\\\\Unrelated] 0\n"value"="keep-me"\n'
    return text


def settings():
    return {"Example Camera A": {"camera": "Example Camera A", "address": "198.51.100.20",
                                "path": "/h264Preview_01_sub", "width": 640,
                                "height": 480, "enabled": True}}


class RegistryTests(unittest.TestCase):
    def test_reduces_all_cached_dimensions_and_preserves_credentials(self):
        result = configure.transform(fixture(), settings())
        blocks = configure.sections(result)
        target = next(b for b in blocks if configure.camera_name(configure.section_key(b)) == "Example Camera A")
        for field in ("xres", "fullxres", "zrect_right"):
            self.assertIn('"' + field + '"=dword:00000280', target)
        for field in ("yres", "fullyres", "zrect_bottom"):
            self.assertIn('"' + field + '"=dword:000001e0', target)
        self.assertIn('"ip"="198.51.100.20"', target)
        self.assertIn('"ip_path"="/h264Preview_01_sub"', target)
        self.assertIn('"ippw"="PRIVATE_PLACEHOLDER"', target)
        self.assertIn('"value"="keep-me"', result)

    def test_unselected_camera_disabled_and_folder_deletion_configured(self):
        result = configure.transform(fixture(), settings())
        blocks = configure.sections(result)
        unselected = next(b for b in blocks if configure.camera_name(configure.section_key(b)) == "Example Camera B")
        self.assertIn('"enabled"=dword:00000000', unselected)
        folder = next(b for b in blocks if configure.section_key(b) == FOLDER_ROOT + "\\0")
        self.assertIn('"archmb"=dword:00000100', folder)
        self.assertIn('"action"=dword:00000000', folder)
        self.assertIn('"path"="C:\\\\BlueIris\\\\New"', folder)

    def test_wrong_architecture_and_unmatched_names_refused(self):
        with self.assertRaises(ValueError):
            configure.transform(fixture().replace("#arch=win32", "#arch=win64"), settings())
        with self.assertRaises(ValueError):
            configure.transform(fixture(), {"Unknown Camera": settings()["Example Camera A"]})

    def test_dry_run_has_no_writes_and_apply_makes_private_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prefix = root / "prefix"
            prefix.mkdir()
            original = fixture()
            (prefix / "system.reg").write_text(original)
            (prefix / "user.reg").write_text("user-original")
            (prefix / "userdef.reg").write_text("defaults-original")
            streams = root / "streams.json"
            streams.write_text(json.dumps(list(settings().values())))
            backup = root / "private-backup"
            command = [sys.executable, str(SCRIPTS / "configure-test.py"), "--prefix", str(prefix),
                       "--streams", str(streams), "--backup-dir", str(backup)]
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual((prefix / "system.reg").read_text(), original)
            self.assertFalse(backup.exists())
            subprocess.run(command + ["--apply"], check=True, capture_output=True)
            saved = next(backup.iterdir())
            self.assertEqual((saved / "system.reg").read_text(), original)
            self.assertEqual((saved / "system.reg").stat().st_mode & 0o777, 0o600)
            self.assertTrue((prefix / "drive_c/BlueIris/New").is_dir())

    def test_running_prefix_is_refused(self):
        if sys.platform != "linux":
            self.skipTest("Linux /proc guard")
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, WINEPREFIX=directory)
            child = subprocess.Popen([sys.executable, "-c",
                "import ctypes,time;ctypes.CDLL(None).prctl(15,b'BlueIris.exe',0,0,0);print('ready',flush=True);time.sleep(30)"],
                env=env, stdout=subprocess.PIPE, text=True)
            try:
                self.assertEqual(child.stdout.readline().strip(), "ready")
                with self.assertRaises(RuntimeError):
                    ensure_stopped(Path(directory))
            finally:
                child.terminate()
                child.wait(timeout=5)
                child.stdout.close()

    def test_filter_excludes_license_and_actions_disables_cameras(self):
        source = r'''Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\Software\Wow6432Node\Perspective Software\Blue Iris\Registration]
"license"="PLACEHOLDER"

[HKEY_LOCAL_MACHINE\Software\Wow6432Node\Perspective Software\Blue Iris\Cameras\Example Camera A]
"enabled"=dword:00000001
"ippw"="PRIVATE_PLACEHOLDER"

[HKEY_LOCAL_MACHINE\Software\Wow6432Node\Perspective Software\Blue Iris\Cameras\Example Camera A\Motion\1]
"enabled"=dword:00000001

[HKEY_LOCAL_MACHINE\Software\Wow6432Node\Perspective Software\Blue Iris\Cameras\Example Camera A\PTZ]
"action"="excluded"

[HKEY_LOCAL_MACHINE\Software\Wow6432Node\Perspective Software\Blue Iris\Cameras\Example Camera A\Alerts]
"email"="excluded"
'''
        result, count = filter_export.filtered(source)
        self.assertEqual(count, 1)
        self.assertNotIn("Registration", result)
        self.assertNotIn("Wow6432Node", result)
        self.assertNotIn("\\PTZ]", result)
        self.assertNotIn("\\Alerts]", result)
        self.assertIn("\\Motion\\1]", result)
        self.assertIn('"ippw"="PRIVATE_PLACEHOLDER"', result)
        first_camera = result.split("\\Motion\\1]")[0]
        self.assertIn('"enabled"=dword:00000000', first_camera)


if __name__ == "__main__":
    unittest.main()
