import httpx

from pip_zendure._config import CONFIG

from ._const import REGION, SUPPORTED_PRODUCT_KEYS
from ._models import AuthData
from .api_exception import APIException
from .http._abstract_http_adapter import HTTP_METHOD, AbstractHTTPAdapter


class APIClient:
    """An API class to expose available API endpoints"""

    def __init__(
        self, http_adapter: AbstractHTTPAdapter, region: REGION = REGION.GLOBAL
    ):
        self.http_adapter = http_adapter
        self.base_url = None
        self.region(region)

    def switch_region(self, region: REGION) -> None:
        self.base_url = CONFIG[region.value]["base_url"]

    async def get_token(self, username: str, password: str) -> AuthData:
        """Get an access token and region for the given username and password"""

        payload = {
            "account": username,
            "appType": "Android",
            "grantType": "password",
            "password": password,
            "tenantId": "",
        }

        json = await self._do_request("auth/app/token", payload)

        return AuthData(
            token=json["data"]["accessToken"],
            region=REGION(json["data"]["serverNode"]),
        )

    async def get_user_info(self) -> dict:
        """Get information about the authenticated user"""
        json = await self._do_request("consumerModule/consumer/mobile/getUserInfo")

        return json["data"]

    async def get_device_list(self, supported_only: bool = True) -> list:
        """Get a list of devices associated with the authenticated user

        If supported_only is False, all devices will be returned even non Zendure devices
        or devices that are not supported by this library.
        """
        json = await self._do_request(
            "productModule/device/queryDeviceListByConsumerId"
        )

        devices = json["data"]

        if supported_only:
            return self._filter_unsupported_devices(devices)
        else:
            return devices

    async def get_device_details(self, device_id: int) -> dict:
        """Get detailed information about a specific device"""

        payload = {"deviceId": device_id}

        json = await self._do_request("device/solarFlow/detail", payload)

        return json["data"]

    async def _do_request(self, path: str, payload: dict = None) -> dict:
        url = self._create_full_url(path)

        response = await self.http_adapter.request(HTTP_METHOD.POST, url, payload)
        if response.status_code != httpx.codes.OK or response.json()["success"] != True:
            raise self._create_api_exception(response)

        return response.json()

    def _create_full_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _create_api_exception(self, response: httpx.Response) -> APIException:
        return APIException(
            (
                response.json()["code"]
                if response.status_code == httpx.codes.OK
                else response.status_code
            ),
            str(response.url),
        )

    def _filter_unsupported_devices(self, devices: list) -> list:
        return [dev for dev in devices if dev["productKey"] in SUPPORTED_PRODUCT_KEYS]
