import shutil
import subprocess
import logging
import cgi
from pathlib import Path
import requests


def purge_dir(directory: Path):
    if directory.exists():
        logging.info(f"Purging {directory}")
        shutil.rmtree(directory)

    logging.info(f"Creating {directory}")
    directory.mkdir()


class BaseComponent:
    name: str
    description: str
    resource_url: str
    distribution_name: str

    def __init__(self):
        self.packages_dir = Path.cwd() / "packages" / self.name
        self.build_dir = Path.cwd() / "build" / self.name
        self.temp_dir = Path.cwd() / "temp" / self.name
    
    def _post_init(self):
        self.distribution_name = self.resource_url.split("/")[-1].split("?")[0]
        self.resource_file = self.packages_dir / self.distribution_name

    def _7z_replace_zip(self, resource_file: Path):
        """Python libraries do not support BCJ2."""
        unzip_dir = self.temp_dir / resource_file.stem
        
        subprocess.run(["7z", "x", resource_file, f"-o{unzip_dir}"], check=True,
                       stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.make_archive(resource_file.parent / resource_file.stem, "zip", unzip_dir)
        resource_file.unlink()

    def prepare(self):
        """Download and the component."""
        purge_dir(self.packages_dir)
        logging.info(f"Preparing {self.distribution_name}")

        if isinstance(self.resource_url, str):
            with open(self.resource_file, "wb") as f:
                r = requests.get(self.resource_url, stream=True)
                r.raise_for_status()
                f.write(r.content)

            if self.resource_file.suffix == ".7z":
                self._7z_replace_zip(self.resource_file)
                self.resource_file = self.resource_file.with_suffix(".zip")
        else:
            for resource in self.resource_url:
                r = requests.get(resource, stream=True)
                r.raise_for_status()
                _, params = cgi.parse_header(r.headers["Content-Disposition"])
                with open(self.packages_dir / params["filename"], "wb") as f:
                    f.write(r.content)

    def _unzip_build(self, resource_file: Path):
        logging.info(f"Unzipping {resource_file} to {self.build_dir}")
        shutil.unpack_archive(resource_file, self.build_dir)

    def install(self):
        """Install the component."""
        purge_dir(self.build_dir)
        logging.info(f"Installing {self.name}")

        if isinstance(self.resource_url, str) and self.resource_file.suffix == ".zip":
            self._unzip_build(self.resource_file)
