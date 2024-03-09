from pathlib import Path
import zipfile

import shutil
import logging


def purge_dir(directory: Path):
    if directory.exists():
        logging.info(f"Purging {directory}")
        shutil.rmtree(directory)

    logging.info(f"Creating {directory}")
    directory.mkdir()


class BaseComponent:
    name: str
    description: str
    distribution_name: str

    def __init__(self):
        self.packages_dir = Path.cwd() / "packages" / self.name
        self.build_dir = Path.cwd() / "build" / self.name

    def prepare(self):
        """Download and prepare the component."""
        purge_dir(self.packages_dir)
        logging.info(f"Preparing {self.distribution_name}")

    def _unzip_build(self, zip_name: Path):
        logging.info(f"Unzipping {zip_name} to {self.build_dir}")
        shutil.unpack_archive(zip_name, self.build_dir)

    def install(self):
        """Install the component."""
        purge_dir(self.build_dir)
        logging.info(f"Installing {self.name}")
