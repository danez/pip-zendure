import httpx

from ._abstract_http_adapter import HTTP_METHOD, AbstractHTTPAdapter

ZENDURE_UNSIGNED_APP_VERSION = "4.4.1"


class UnsignedHTTPAdapter(AbstractHTTPAdapter):
    def __init__(self):
        super().__init__()
        self._http_client.headers["appVersion"] = ZENDURE_UNSIGNED_APP_VERSION

    async def request(
        self, method: HTTP_METHOD, url: str, payload: dict = None
    ) -> httpx.Response:
        if self._http_client is None:
            raise RuntimeError("HTTP Client is closed")

        response = await self._http_client.request(method.value, url, json=payload)

        return response
