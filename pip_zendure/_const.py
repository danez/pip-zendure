import platform
import sys
from enum import Enum

ZENDURE_API_BASE_URL = "https://app.zendure.tech/"

ZENDURE_ENCRYPTION_KEY = "TUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDd29xQXJuVks1Y3VTSEwzdDl1ZjNkMUNHbG1jYUZFL05UK3Q4NFJ1TWZMWnpmdVpibUVsUDNYbXl5d3ZUa05VbEJkcjZaYTJ0alZLUXFLbzVBVlYxY3hWcGErR0xyTHBTdUg0VS96ZUx6ZUtMcE55OWsrQjlGb0xYQkRUNExhSm9JY2o5VkxobFpXTVRMeFZ3WFU1TmhJL2x4V2o3Y0szMzdkdXg3TmJLbHR3SURBUUFC"

USER_AGENT = f"ZendureAPI/0.1.0 (python {platform.python_version()}; {sys.platform})"


class SUPPORTED_PRODUCT_KEYS(Enum):
    # ACE_15000 = "8bM93H"
    # AIO_2400 = "yWF7hV"
    HUB_1200 = "73bkTV"
    HUB_2000 = "A8yh63"
    # HYPER_2000 = "ja72U0ha"
    # SOLARFLOW_800 = "?"


class REGION(Enum):
    EUROPE = "eu"
    GLOBAL = "global"
