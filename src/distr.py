import logging
from pathlib import Path
from zipfile import ZipFile
from .base import packages_dir, temp_dir, download_file, unzip_dir


def walk_dir_skip(root: Path):
    for p in root.iterdir():
        if p.is_dir():
            if p.name == '__pycache__':
                continue
            yield from walk_dir_skip(p)
        else:
            if p.suffix in [".gitignore", ".json"]:
                continue
            yield p


def walk_dir_nonskip(root: Path):
    for p in root.iterdir():
        if p.is_dir():
            yield from walk_dir_nonskip(p)
        else:
            yield p


def create_python_embed():
    logging.info("Downloading and extracting python embeddable")

    python_embed = download_file(
        "https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip", temp_dir)
    unzip_dir(python_embed, temp_dir / python_embed.stem)

    python_embed_dir = python_embed.parent / python_embed.stem

    # Delete the ._pth file
    pth = [p for p in python_embed_dir.iterdir() if p.suffix == "._pth"]
    assert len(pth) == 1
    pth[0].unlink()

    return python_embed_dir


def create_distr():
    python_embed_dir = create_python_embed()
    with ZipFile(Path.cwd() / "artefacts" / "dstr.zip", 'w') as zf:
        # packages folder
        logging.info("Adding /packages to the distribution")
        for p in walk_dir_skip(packages_dir):
            logging.info(f"Adding {p} to the distribution")
            zf.write(p, arcname=p.relative_to(Path.cwd()))

        # src folder
        logging.info("Adding /src to the distribution")
        src = Path.cwd() / "src"
        for p in walk_dir_skip(src):
            logging.info(f"Adding {p} to the distribution")
            zf.write(p, arcname=p.relative_to(Path.cwd()))

        # run.py
        logging.info("Adding run.py to the distribution")
        zf.write(Path.cwd() / "run.py", arcname="run.py")

        # build folder
        zf.mkdir("build")

        # python embeddable
        logging.info("Adding python embeddable to the distribution")
        for p in walk_dir_nonskip(python_embed_dir):
            logging.info(f"Adding {p} to the distribution")
            zf.write(p, arcname="python-embed" /
                     p.relative_to(python_embed_dir))
