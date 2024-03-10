from pathlib import Path
from .base import BaseComponent, SingleComponent
from .cpl import Python

ggb_url = "https://download.geogebra.org/installers/6.0/suite/GeoGebraCalculator-Windows-Installer-6-0-829-0.exe"


class GGB(SingleComponent):
    name = f"geogebra-collection-6"

    def __init__(self):
        super().__init__(ggb_url)

    def install(self):
        super().install()
        name = self.packages_dir.iterdir().__next__()
        self._copy(name, self.build_dir)


gurobi_deps = ["gurobipy==11.0.1", "numpy==1.26.4",
               "setuptools==68.2.2", "wheel==0.41.2"]


class Gurobi(BaseComponent):
    name = "gurobi"
    distribution_name = "Gurobi Optimizer"
    resource_urls = []

    def __init__(self, python: Python):
        self.python = python
        super().__init__()

    def prepare(self):
        tmp_filename = [name for name in self.packages_dir.iterdir()
               if name.name in ["gurobi.lic", "mip1.py"]]
        assert len(tmp_filename) == 2

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

        import sys
        host_python = sys.executable
        self._run(host_python, "-m", "pip", "download",
                  f"--python-version={self.python.version}", "--only-binary=:all:", *gurobi_deps, cwd=self.packages_dir)

    def install(self):
        super().install()
        pkgs = [name for name in self.packages_dir.iterdir()
                if name.suffix == ".whl"]

        lic = [name for name in self.packages_dir.iterdir()
               if name.name == "gurobi.lic"]
        assert len(lic) == 1
        lic = lic[0]

        self._run(self.python.build_dir / "python.exe",
                  "-m", "pip", "install", *pkgs)
        self._copy(lic, Path("C:\gurobi\gurobi.lic"))
        self._copy_desktop(self.packages_dir / "mip1.py")
