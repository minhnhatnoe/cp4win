import subprocess
from pathlib import Path


def create_shortcut(target: str, name: str):
    subprocess.run(["pwsh", "-Command", Path(__file__).parent /
                    "shortcut.ps1", target, name], check=True)


def copy_desktop(name: str):
    subprocess.run(["pwsh", "-Command", Path(__file__).parent /
                   "copy_desktop.ps1", name], check=True)


def add_path(path: Path):
    subprocess.run(["pwsh", "-Command", Path(__file__).parent /
                   "add_path.ps1", path], check=True)
