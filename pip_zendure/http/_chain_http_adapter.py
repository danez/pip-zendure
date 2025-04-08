import logging
import httpx

from ._abstract_http_adapter import HTTP_METHOD, AbstractHTTPAdapter


class ChainHTTPAdapter(AbstractHTTPAdapter):
    def __init__(self, adapters: list[AbstractHTTPAdapter]):
        self.adapters = adapters

    async def request(
        self, method: HTTP_METHOD, url: str, payload: dict = None
    ) -> httpx.Response:
        for adapter in self.adapters:
            logging.getLogger(__name__).debug(
                f"Trying adapter: {adapter.__class__.__name__}"
            )
            response = await adapter.request(method, url, payload)

            if (
                # on success return response
                response.status_code < httpx.codes.BAD_REQUEST
                # last iteration, return response in any case
                or adapter == self.adapters[-1]
            ):
                return response

    async def aclose(self):
        for adapter in self.adapters:
            await adapter.aclose()

    def set_token(self, token):
        for adapter in self.adapters:
            adapter.set_token(token)

    def switch_region(self, region):
        for adapter in self.adapters:
            adapter.switch_region(region)
