from pathlib import Path
import logging
from .base import BaseComponent, SingleComponent, ZipComponent
from .cpl import Python

ggb_url = "https://download.geogebra.org/installers/6.0/suite/GeoGebraCalculator-Windows-Installer-6-0-829-0.exe"


class GGB(SingleComponent):
    name = "geogebra-collection-6"

    def __init__(self):
        super().__init__(ggb_url)

    def install(self):
        name = self.packages_dir.iterdir().__next__()
        self.shortcut = (name, "GeoGebra")
        super().install()
        self._copy(name, self.build_dir)


graph_editor_url = "https://github.com/mxwell/mxwell.github.io/archive/refs/heads/master.zip"


class Graph(ZipComponent):
    name = "graph-editor"

    def __init__(self):
        super().__init__(graph_editor_url)
        self.shortcut = (self.build_dir / "mxwell.github.io-master" / "draw-graph" / "index.html", "GraphEditor")

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
        
        license_file = self.assets_dir / "gurobi.lic"
        assert license_file.exists()
        logging.info("Found gurobi.lic")

        examples = self.assets_dir / "mip1.py"
        assert examples.exists()
        logging.info("Found mip1.py")

        import sys
        host_python = Path(sys.executable)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self._run(host_python, "-m", "pip", "download",
                  f"--python-version={self.python.version}", "--only-binary=:all:", *gurobi_deps, cwd=self.packages_dir)

    def install(self):
        super().install()
        pkgs = [name for name in self.packages_dir.iterdir()
                if name.suffix == ".whl"]

        self._run(self.python.build_dir / "python.exe",
                  "-m", "pip", "install", *pkgs)
        self._copy(self.assets_dir / "gurobi.lic", Path("C:\\gurobi\\gurobi.lic"))
        self._copy_desktop(self.packages_dir / "mip1.py")
