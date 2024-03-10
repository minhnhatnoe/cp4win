import subprocess
import logging

from .base import BaseComponent

# URL from https://sourceforge.net/projects/mingw-w64/files/ and https://winlibs.com/
gcc_urls = {
    "13.2.0": "https://github.com/brechtsanders/winlibs_mingw/releases/download/13.2.0posix-17.0.6-11.0.1-ucrt-r5/winlibs-x86_64-posix-seh-gcc-13.2.0-llvm-17.0.6-mingw-w64ucrt-11.0.1-r5.zip",
    "11.2.0": "https://github.com/brechtsanders/winlibs_mingw/releases/download/11.2.0-10.0.0-ucrt-r1/winlibs-x86_64-posix-seh-gcc-11.2.0-mingw-w64ucrt-10.0.0-r1.zip",
    "8.1.0": "https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-posix/seh/x86_64-8.1.0-release-posix-seh-rt_v6-rev0.7z"
}


class GCC(BaseComponent):
    description = "GNU Compiler Collection (GCC)"

    def __init__(self, version: str):
        self.name = f"gcc-{version}"
        super().__init__()
        self.resource_url = gcc_urls[version]
        super()._post_init()


# URL from https://sourceforge.net/projects/mingw-w64/files/ and https://winlibs.com/
py_urls = {
    "3.12.2": "https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe"
}


class Python(BaseComponent):
    description = "Python Interpreter"

    def __init__(self, version: str):
        self.name = f"python-{version}"
        super().__init__()
        self.resource_url = py_urls[version]
        super()._post_init()

    def prepare(self):
        super().prepare()
        logging.info(f"Running layout for {self.name}")
        subprocess.run([self.resource_file, "/layout", "/quiet"], check=True)

    def install(self):
        super().install()
        logging.info(f"Running installer for {self.name}")
        subprocess.run([self.resource_file, "/passive", "/quiet",
                        f"TargetDir={self.build_dir}", "CompileAll=1", "AppendPath=1", "Include_debug=1", "Include_symbols=1"], check=True)
