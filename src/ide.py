import logging
from .base import BaseComponent, SingleComponent, ZipComponent

# URL from https://code.visualstudio.com/download
vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"


class VSCode(ZipComponent):
    name = "vscode"
    add_path = True

    def __init__(self):
        super().__init__(vscode_url)
        self.shortcut = (self.build_dir / "Code.exe", "Visual Studio Code")

    def install(self):
        super().install()

        # Enable portable mode
        # Ref: https://code.visualstudio.com/docs/editor/portable
        self._mkdir(self.build_dir / "data" / "tmp")


class VSCodeExt(BaseComponent):
    name = distribution_name = "vscode-extensions"
    resource_urls = []

    def __init__(self, vscode: VSCode):
        self.vscode = vscode
        super().__init__()

    def prepare(self):
        super().prepare(False)
        extension_list = [*self.packages_dir.iterdir()]
        if len(extension_list) == 0:
            logging.warning("No extension found")
        else:
            logging.info(f"Extensions found: {extension_list}")

    def install(self):
        super().install()
        code_command = self.vscode.build_dir / "bin" / "code.cmd"
        for f in self.packages_dir.iterdir():
            if f.suffix == ".vsix":
                self._run(code_command, "--install-extension", f)


# https://download.sublimetext.com/sublime_text_build_4169_x64.zip
sublime_url = "https://download.sublimetext.com/sublime_text_build_4169_x64.zip"


class Sublime(ZipComponent):
    name = "sublime"

    def __init__(self):
        super().__init__(sublime_url)
        self.shortcut = (self.build_dir / "sublime_text.exe", "Sublime Text 4")


codeblocks_url = "https://zenlayer.dl.sourceforge.net/project/codeblocks/Binaries/20.03/Windows/codeblocks-20.03mingw-nosetup.zip"


class CodeBlocks(ZipComponent):
    name = "codeblocks"

    def __init__(self):
        super().__init__(codeblocks_url)
        self.shortcut = (self.build_dir / "codeblocks.exe", "Code::Blocks")


devcpp_url = "https://nchc.dl.sourceforge.net/project/dev-cpp/Binaries/Dev-C%2B%2B%204.9.9.2/devcpp-4.9.9.2_setup.exe"


class DevCpp(SingleComponent):
    name = "devcpp"

    def __init__(self):
        super().__init__(devcpp_url)
        self.shortcut = (self.build_dir / "devcpp.exe", "Dev-C++")

    def install(self):
        super().install()
        self._run(self.packages_dir.iterdir().__next__(),
                  "/S", f"/D={self.build_dir}")
