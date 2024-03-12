import subprocess
from pathlib import Path


def create_shortcut(target: str, name: str):
    assert target.count(" ") == 0 and name.count(" ") == 0
    subprocess.run(["powershell", "-Command", Path(__file__).parent /
                    "shortcut.ps1", target, name], check=True)


def copy_desktop(name: str):
    assert name.count(" ") == 0
    subprocess.run(["powershell", "-Command", Path(__file__).parent /
                   "copy_desktop.ps1", name], check=True)


def add_path(path: Path):
    assert path.count(" ") == 0
    subprocess.run(["powershell", "-Command", Path(__file__).parent /
                   "add_path.ps1", path], check=True)
