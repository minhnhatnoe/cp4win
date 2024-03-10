import logging
import subprocess
import requests
from .base import BaseComponent

# URL from https://code.visualstudio.com/download
vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"


class VSCode(BaseComponent):
    name = "vscode"
    description = "Visual Studio Code"

    def __init__(self):
        super().__init__()
        r = requests.head(vscode_url, allow_redirects=True)
        r.raise_for_status()
        self.resource_url = r.url
        self._post_init()

    def install(self):
        super().install()

        # Enable portable mode
        # Ref: https://code.visualstudio.com/docs/editor/portable
        data_path = self.build_dir / "data"
        data_path.mkdir()

        data_path = data_path / "tmp"
        data_path.mkdir()


vscode_ext_urls = {
    "python": [
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-python/vsextensions/python/2024.3.10681011/vspackage",
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-python/vsextensions/debugpy/2024.3.10661804/vspackage?targetPlatform=win32-x64",
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-python/vsextensions/vscode-pylance/2024.2.106/vspackage"
    ],
    "cpp": [
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-vscode/vsextensions/cpptools/1.19.6/vspackage?targetPlatform=win32-x64",
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-vscode/vsextensions/cpptools-themes/2.0.0/vspackage"
    ],
    "cph": ["https://marketplace.visualstudio.com/_apis/public/gallery/publishers/DivyanshuAgrawal/vsextensions/competitive-programming-helper/6.1.0/vspackage"],
    "runner": ["https://marketplace.visualstudio.com/_apis/public/gallery/publishers/formulahendry/vsextensions/code-runner/0.12.1/vspackage"]
}


class VSCodeExt(BaseComponent):
    description = "VSCode Extension"

    def __init__(self, name: str, vscode: VSCode):
        self.name = self.distribution_name = f"vscode-extension-{name}"
        super().__init__()
        self.resource_url = vscode_ext_urls[name]
        self.vscode = vscode

    def install(self):
        super().install()
        for f in self.packages_dir.iterdir():
            subprocess.run([self.vscode.build_dir / "bin" / "code.cmd",
                           "--install-extension", f.absolute()], check=True)


# https://download.sublimetext.com/sublime_text_build_4169_x64.zip
sublime_url = "https://download.sublimetext.com/sublime_text_build_4169_x64.zip"


class Sublime(BaseComponent):
    name = "sublime"
    description = "Sublime Text 4"

    def __init__(self):
        super().__init__()
        self.resource_url = sublime_url
        super()._post_init()


codeblocks_url = "https://downloads.sourceforge.net/project/codeblocks/Binaries/20.03/Windows/codeblocks-20.03mingw-setup.exe"


class CodeBlocks(BaseComponent):
    name = "codeblocks"
    description = "Code::Blocks"

    def __init__(self):
        super().__init__()
        self.resource_url = codeblocks_url
        super()._post_init()


devcpp_url = "https://nchc.dl.sourceforge.net/project/dev-cpp/Binaries/Dev-C%2B%2B%204.9.9.2/devcpp-4.9.9.2_setup.exe"


class DevCpp(BaseComponent):
    name = "devcpp"
    description = "Dev-C++"

    def __init__(self):
        super().__init__()
        self.resource_url = devcpp_url
        super()._post_init()

    def install(self):
        super().install()
        logging.info(f"Running installer for {self.name}")
        subprocess.run([self.resource_file, "/S",
                       f'/D="{self.build_dir}"'], check=True)
