from .base import BaseComponent, ZipComponent
from .cpl import Python

ggb_url = "https://download.geogebra.org/package/win-port6"


class GGB(ZipComponent):
    name = f"geogebra-collection-6"

    def __init__(self):
        super().__init__(ggb_url)


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
        super().prepare()

        import sys
        host_python = sys.executable
        self._run(host_python, "-m", "pip", "download",
                  f"--python-version={self.python.version}", "--only-binary=:all:", *gurobi_deps, cwd=self.packages_dir)

    def install(self):
        super().install()
        pkgs = [name for name in self.packages_dir.iterdir()
                if name.suffix == ".whl"]
        self._run(self.python.build_dir / "python.exe",
                  "-m", "pip", "install", *pkgs)
