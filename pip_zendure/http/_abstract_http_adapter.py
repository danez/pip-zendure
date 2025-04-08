from abc import ABC, abstractmethod
from enum import Enum

import httpx
from httpx_retry import AsyncRetryTransport, RetryPolicy

from pip_zendure._config import CONFIG

from .._const import REGION, USER_AGENT


ExponentialRetryPolicy = (
    RetryPolicy()
    .with_attempts(3)
    .with_min_delay(10)
    .with_multiplier(2)
    .with_retry_on(lambda code: code >= 500)
)

DefaultHeaders = {
    "Accept-Language": "en-US",
    "Content-Type": "application/json; charset=UTF-8",
    "User-Agent": USER_AGENT,
}


class HTTP_METHOD(Enum):
    GET = "GET"
    POST = "POST"


class AbstractHTTPAdapter(ABC):
    def __init__(self):
        self._config = CONFIG[REGION.GLOBAL.value]

        self._http_client = httpx.AsyncClient(
            transport=AsyncRetryTransport(policy=ExponentialRetryPolicy),
            headers=DefaultHeaders,
        )

    def switch_region(self, region: REGION):
        self._config = CONFIG[region.value]

    @abstractmethod
    async def request(
        self, method: HTTP_METHOD, url: str, payload: dict = None
    ) -> httpx.Response:
        pass

    async def aclose(self):
        await self._http_client.aclose()
        self._http_client = None

    def set_token(self, token):
        if token:
            self._http_client.headers["Blade-Auth"] = f"bearer {token}"
        else:
            self._http_client.headers.pop("Blade-Auth", None)
