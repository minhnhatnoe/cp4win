import logging
from .base import BaseComponent, SingleComponent, ZipComponent
from .cpl import GCC

# URL from https://code.visualstudio.com/download
vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"


class VSCode(ZipComponent):
    name = "vscode"
    add_path = True

    def __init__(self):
        super().__init__(vscode_url)
        self.shortcut = (self.build_dir / "Code.exe", "VisualStudioCode")

    def install(self):
        super().install()

        # Enable portable mode
        # Ref: https://code.visualstudio.com/docs/editor/portable
        self._mkdir(self.build_dir / "data" / "tmp")

settings_json = '{"C_Cpp.default.compilerPath": "fname"}'
class VSCodeExt(BaseComponent):
    name = distribution_name = "vscode-extensions"
    resource_urls = []

    def __init__(self, vscode: VSCode, gcc: GCC):
        self.vscode = vscode
        self.gcc = gcc
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
        
        self._write(self.vscode.build_dir / "data" / "user-data" / "User" / "settings.json", 
            settings_json.replace("fname", str(self.gcc.build_dir / "bin" / "g++.exe").replace("\\", "\\\\")).encode())


# https://download.sublimetext.com/sublime_text_build_4169_x64.zip
sublime_url = "https://download.sublimetext.com/sublime_text_build_4169_x64.zip"


class Sublime(ZipComponent):
    name = "sublime"

    def __init__(self):
        super().__init__(sublime_url)
        self.shortcut = (self.build_dir / "sublime_text.exe", "SublimeText4")
    
    def prepare(self):
        tmp_filename = [name for name in self.packages_dir.iterdir()
               if name.suffix == ".sublime-build"]
        assert len(tmp_filename) == 1

        tmp_file = []
        for filename in tmp_filename:
            with open(filename, "rb") as f:
                tmp_file.append((filename, f.read()))

        try:
            super().prepare()
        finally:
            for filename, content in tmp_file:
                with open(filename, "wb") as lic_file:
                    lic_file.write(content)
    
    def install(self):
        super().install(relax_single_check=True)
        slbuild = [name for name in self.packages_dir.iterdir()
            if name.suffix == ".sublime-build"]
        assert len(slbuild) == 1
        for f in slbuild:
            self._copy(f, self.build_dir / "Data" / "Packages" / "User" / f.name)



codeblocks_url = "https://zenlayer.dl.sourceforge.net/project/codeblocks/Binaries/20.03/Windows/codeblocks-20.03mingw-nosetup.zip"


class CodeBlocks(ZipComponent):
    name = "codeblocks"

    def __init__(self):
        super().__init__(codeblocks_url)
        self.shortcut = (self.build_dir / "codeblocks.exe", "CodeBlocks")


devcpp_url = "https://zenlayer.dl.sourceforge.net/project/orwelldevcpp/Portable%20Releases/Dev-Cpp%205.11%20TDM-GCC%20x64%204.9.2%20Portable.7z"


class DevCpp(ZipComponent):
    name = "devcpp"

    def __init__(self):
        super().__init__(devcpp_url)
        self.shortcut = (self.build_dir / "devcpp.exe", "DevCpp")
