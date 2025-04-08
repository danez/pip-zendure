import unittest
from unittest.mock import patch

from pip_zendure._const import REGION
from pip_zendure.http._signed_http_adapter import SignedHTTPAdapter

ASSERT_APP_VERSION = "5.4.2"


class TestSignedHTTPAdapter(unittest.TestCase):

    def test_app_version(self):
        adapter = SignedHTTPAdapter()

        self.assertEqual(adapter._http_client.headers["appVersion"], ASSERT_APP_VERSION)

    @patch.object(SignedHTTPAdapter, "_encrypt")
    def test_signed_header_global(self, encrypt_mock):
        adapter = SignedHTTPAdapter()
        adapter._create_signed_header("https://app.zendure.tech/test", 1234567890)

        encrypt_mock.assert_called_with(f"{ASSERT_APP_VERSION}./test/1234567890")

    @patch.object(SignedHTTPAdapter, "_encrypt")
    def test_signed_header_eu(self, encrypt_mock):
        adapter = SignedHTTPAdapter()
        adapter.switch_region(REGION.EUROPE)
        adapter._create_signed_header("https://app.zendure.tech/eu/test", 1234567890)

        encrypt_mock.assert_called_with(f"{ASSERT_APP_VERSION}./test/1234567890")

    @patch.object(SignedHTTPAdapter, "_encrypt")
    def test_signed_header_eu_global_url(self, encrypt_mock):
        adapter = SignedHTTPAdapter()
        adapter.switch_region(REGION.EUROPE)
        adapter._create_signed_header("https://app.zendure.tech/v2/test", 1234567890)

        encrypt_mock.assert_called_with(f"{ASSERT_APP_VERSION}./v2/test/1234567890")
