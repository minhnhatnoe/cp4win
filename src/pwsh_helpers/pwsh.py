import subprocess
from pathlib import Path


def create_shortcut(target: Path, name: Path):
    assert str(target).count(" ") == 0 and str(name).count(" ") == 0
    subprocess.run(["powershell", "-Command", Path(__file__).parent /
                    "shortcut.ps1", target, name], check=True)


def copy_desktop(name: Path):
    assert str(name).count(" ") == 0
    subprocess.run(["powershell", "-Command", Path(__file__).parent /
                   "copy_desktop.ps1", name], check=True)


def add_path(path: Path):
    assert str(path).count(" ") == 0
    subprocess.run(["powershell", "-Command", Path(__file__).parent /
                   "add_path.ps1", path], check=True)
