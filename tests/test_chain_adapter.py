import unittest
from unittest.mock import AsyncMock

import httpx

from pip_zendure.http._abstract_http_adapter import HTTP_METHOD
from pip_zendure.http._chain_http_adapter import ChainHTTPAdapter


class TestChainHTTPAdapter(unittest.IsolatedAsyncioTestCase):

    async def test_calls_next_adapter_on_400(self):
        adapter1 = AsyncMock()
        adapter1.request.return_value = httpx.Response(400)

        adapter2 = AsyncMock()
        adapter2.request.return_value = httpx.Response(200)

        chainAdapter = ChainHTTPAdapter([adapter1, adapter2])
        response = await chainAdapter.request(HTTP_METHOD.GET, "/")

        self.assertEqual(response.status_code, 200)

        adapter1.request.assert_called_with(HTTP_METHOD.GET, "/", None)
        adapter2.request.assert_called_with(HTTP_METHOD.GET, "/", None)

    async def test_calls_only_first_Adapter_on_200(self):
        adapter1 = AsyncMock()
        adapter1.request.return_value = httpx.Response(200)

        adapter2 = AsyncMock()
        adapter2.request.return_value = httpx.Response(201)

        chainAdapter = ChainHTTPAdapter([adapter1, adapter2])
        response = await chainAdapter.request(HTTP_METHOD.GET, "/")

        self.assertEqual(response.status_code, 200)

        adapter1.request.assert_called_with(HTTP_METHOD.GET, "/", None)
        adapter2.request.assert_not_called()

    async def test_returns_last_response_if_400(self):
        adapter1 = AsyncMock()
        adapter1.request.return_value = httpx.Response(400)

        adapter2 = AsyncMock()
        adapter2.request.return_value = httpx.Response(401)

        chainAdapter = ChainHTTPAdapter([adapter1, adapter2])
        response = await chainAdapter.request(HTTP_METHOD.GET, "/")

        self.assertEqual(response.status_code, 401)

        adapter1.request.assert_called_with(HTTP_METHOD.GET, "/", None)
        adapter2.request.assert_called_with(HTTP_METHOD.GET, "/", None)
