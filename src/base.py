import shutil
import subprocess
import logging
import cgi
from pathlib import Path
from .pwsh_helpers import pwsh

temp_dir = Path.cwd() / "temp"
build_dir = Path.cwd() / "build"
packages_dir = Path.cwd() / "packages"


def purge_dir(dir: Path):
    if dir.exists():
        logging.info(f"Purging {dir}")
        shutil.rmtree(dir)

    logging.info(f"Creating {dir}")
    dir.mkdir()


def unzip_dir(fname: Path, dir: Path):
    logging.info(f"Unzipping {fname} to {dir}")
    assert fname.suffix == ".zip"
    shutil.unpack_archive(fname, dir)


def download_file(url: str, dir: Path) -> Path:
    from urllib.parse import unquote
    import requests
    logging.info(f"Downloading {url} to {dir}")

    r = requests.head(url, allow_redirects=True)
    r.raise_for_status()

    flabel: str
    if "Content-Disposition" in r.headers:
        _, params = cgi.parse_header(r.headers["Content-Disposition"])
        flabel = params["filename"]
    else:
        flabel = unquote(r.url.split("/")[-1])

    fname = dir / flabel
    logging.info(f"Resolved {url} to filename {fname}")

    from pypdl import Downloader
    dl = Downloader(timeout=300)
    dl.start(url, fname, retries=8)
    assert not dl.failed

    return fname


def sevenz_replace_zip(fname: Path) -> Path:
    """Python libraries do not support BCJ2."""
    logging.info(f"Replacing {fname} with zip")
    assert fname.suffix == ".7z"

    unzip_dir = temp_dir / fname.stem
    assert not unzip_dir.exists()

    subprocess.run(["7z", "x", fname, f"-o{unzip_dir}"], check=True,
                   stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.make_archive(fname.parent /
                        fname.stem, "zip", unzip_dir)

    fname.unlink()
    return fname.with_suffix(".zip")


class BaseComponent:
    name: str
    distribution_name: str = ""
    resource_urls: list[str]

    build_dir: Path
    packages_dir: Path

    add_path: bool = False
    shortcut: tuple[Path, str] | None = None

    def __init__(self):
        self.build_dir = build_dir / self.name
        self.packages_dir = packages_dir / self.name

    def prepare(self, purge: bool = True):
        """Download components."""
        logging.info(f"Preparing {self.distribution_name}")

        if purge:
            purge_dir(self.packages_dir)

        for url in self.resource_urls:
            fdir = download_file(url, self.packages_dir)
            if fdir.suffix == ".7z":
                sevenz_replace_zip(fdir)

    def install(self):
        """Install the component."""
        purge_dir(self.build_dir)
        logging.info(f"Installing {self.name}")

        if self.add_path:
            pwsh.add_path(self.build_dir / "bin")
        if self.shortcut is not None:
            pwsh.create_shortcut(self.shortcut[0], self.shortcut[1])

    def _run(self, *args, **kwargs):
        logging.info(f"Running {args} for {self.name}")
        subprocess.run(args, check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, **kwargs)

    def _mkdir(self, p: Path):
        logging.info(f"Creating {p} for {self.name}")
        p.mkdir(parents=True)

    def _write(self, p: Path, c: bytes):
        logging.info(f"Writing {c.decode()} to {p} for {self.name}")
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "wb") as f:
            f.write(c)

    def _copy(self, f: Path, t: Path):
        logging.info(f"Copying {f} to {t} for {self.name}")
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, t)
    
    def _copy_desktop(self, name: str):
        pwsh.copy_desktop(name)


class SingleComponent(BaseComponent):
    """Component distributed as single file."""

    def __init__(self, url: str):
        super().__init__()
        self.distribution_name = url.split("/")[-1].split("?")[0]
        self.resource_urls = [url]

    def install(self, relax_single_check: bool = False):
        """Install the component."""
        super().install()
        assert relax_single_check or len([*self.packages_dir.iterdir()]) == 1


class ZipComponent(SingleComponent):
    """Component distributed as single zip file."""

    def install(self, *args, **kwargs):
        """Install the component."""
        super().install(*args, **kwargs)

        f = [name for name in self.packages_dir.iterdir() if name.suffix == ".zip"]
        assert len(f) == 1
        unzip_dir(f[0], self.build_dir)
