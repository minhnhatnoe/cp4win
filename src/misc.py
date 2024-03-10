from .base import BaseComponent

ggb_url = "https://download.geogebra.org/package/win-port6"

class GGB(BaseComponent):
    name = f"Geogebra 6"
    description = "Geogebra Collection 6"
    distribution_name = "geogebra6"

    def __init__(self):
        super().__init__()
        self.resource_url = ggb_url
        super()._post_init()
