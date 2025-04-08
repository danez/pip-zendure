from .features._power_limit import Feature_Power_Limit
from .features._ac import Feature_AC
from .._const import SUPPORTED_PRODUCT_KEYS
from ._base_device import Device


class Hub2000(Feature_AC, Feature_Power_Limit, Device):
    """Hub 2000 device information."""

    def __init__(self, id: int, name: str, key: str):
        super().__init__(
            id=id,
            name=name,
            key=key,
            product_key=SUPPORTED_PRODUCT_KEYS.HUB_2000,
            mqtt_client=None,
        )
