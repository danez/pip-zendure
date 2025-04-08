import base64
import logging
import time

import httpx
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from .._const import (
    ZENDURE_API_BASE_URL,
    ZENDURE_ENCRYPTION_KEY,
)
from ._abstract_http_adapter import HTTP_METHOD, AbstractHTTPAdapter

ZENDURE_SIGNED_APP_VERSION = "5.4.2"


class SignedHTTPAdapter(AbstractHTTPAdapter):
    def __init__(self):
        super().__init__()
        self._http_client.headers["appVersion"] = ZENDURE_SIGNED_APP_VERSION

    def _encrypt(self, data: str) -> str:
        logging.getLogger(__name__).debug(f"Encrypting sign header {data}")

        public_key_bytes = base64.b64decode(
            base64.b64decode(ZENDURE_ENCRYPTION_KEY).decode("utf-8")
        )
        public_key = RSA.import_key(public_key_bytes)
        encrypted_data = PKCS1_v1_5.new(public_key).encrypt(data.encode("utf-8"))
        encoded_data = base64.b64encode(encrypted_data).decode("utf-8")

        return encoded_data

    def _create_signed_header(self, url: str, timestamp: int) -> dict:
        path = self._extract_url_path(url)
        version = ZENDURE_SIGNED_APP_VERSION

        return self._encrypt(f"{version}./{path}/{timestamp}")

    def _extract_url_path(self, url: str) -> str:
        if url.startswith(self._config["base_url"]):
            return url[len(self._config["base_url"]) :]

        # If the URL does not start with the base URL from the config,
        # it is a non region URL.
        # The token/login endpoint is an example of this as it exists only on global.
        return url[len(ZENDURE_API_BASE_URL) :]

    async def request(
        self, method: HTTP_METHOD, url: str, payload: dict = None
    ) -> httpx.Response:
        if self._http_client is None:
            raise RuntimeError("HTTP Client is closed")

        timestamp = int(time.time()) - 5
        sign_header = self._create_signed_header(url, timestamp)

        logging.getLogger(__name__).debug(f"Requesting {method.value} {url}")

        return await self._http_client.request(
            method.value,
            url,
            json=payload,
            headers={"sign": sign_header, "timestamps": str(timestamp)},
        )
