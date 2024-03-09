import cgi
from os import path

import requests

from ..base import BaseComponent

vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"


class VSCode(BaseComponent):
    name = "vscode"
    description = "Visual Studio Code"

    def __init__(self):
        super().__init__()

        self.url = vscode_url
        r = requests.head(self.url, allow_redirects=True)
        r.raise_for_status()
        self.resource_url = r.url

        _, params = cgi.parse_header(r.headers['Content-Disposition'])
        self.distribution_name = params['filename']

        self.zip_name = path.join(self.packages_dir, self.distribution_name)

    def prepare(self):
        super().prepare()
        with open(self.zip_name, "wb") as f:
            f.write(requests.get(self.resource_url, stream=True).content)

    def install(self):
        super().install()
        self._unzip_build(self.zip_name)
