import subprocess
import logging
from .base import SingleComponent, ZipComponent

# URL from https://sourceforge.net/projects/mingw-w64/files/ and https://winlibs.com/
gcc_urls = {
    "13.2.0": "https://github.com/brechtsanders/winlibs_mingw/releases/download/13.2.0posix-17.0.6-11.0.1-ucrt-r5/winlibs-x86_64-posix-seh-gcc-13.2.0-llvm-17.0.6-mingw-w64ucrt-11.0.1-r5.zip",
    "11.2.0": "https://github.com/brechtsanders/winlibs_mingw/releases/download/11.2.0-10.0.0-ucrt-r1/winlibs-x86_64-posix-seh-gcc-11.2.0-mingw-w64ucrt-10.0.0-r1.zip",
    "8.1.0": "https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-posix/seh/x86_64-8.1.0-release-posix-seh-rt_v6-rev0.7z"
}


class GCC(ZipComponent):
    def __init__(self, version: str, add_path: bool = False):
        self.name = f"gcc-{version}"
        self.add_path = add_path
        self.gpp_dir = self.build_dir / "mingw64" / "bin" / "g++.exe"
        super().__init__(gcc_urls[version])


# URL from https://sourceforge.net/projects/mingw-w64/files/ and https://winlibs.com/
py_urls = {
    "3.12.2": "https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe"
}


class Python(SingleComponent):
    def __init__(self, version: str):
        self.name = f"python-{version}"
        self.version = version
        super().__init__(py_urls[version])

    def prepare(self):
        super().prepare()
        installer = self.packages_dir.iterdir().__next__()
        self._run(installer, "/layout", "/quiet")

    def install(self):
        installer = [name for name in self.packages_dir.iterdir()
                     if name.suffix != ".msi"]
        assert len(installer) == 1
        installer = installer[0]

        try:
            # Will terminate gracefully if Python is not installed
            self._run(installer, "/uninstall", "/quiet")
        except subprocess.CalledProcessError as e:
            logging.warning(
                f"Failed to uninstall existing Python. Check if current Python is corrupted?")
            raise e

        super().install(relax_single_check=True)
        self._run(installer, "/passive", "/quiet", f"TargetDir={self.build_dir}",
                  "CompileAll=1", "PrependPath=1", "Include_debug=1", "Include_symbols=1")
