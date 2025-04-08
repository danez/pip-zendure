import unittest
from pip_zendure.http._unsigned_http_adapter import UnsignedHTTPAdapter

ASSERT_APP_VERSION = "4.4.1"


class TestUnsignedHTTPAdapter(unittest.TestCase):

    def test_app_version(self):
        adapter = UnsignedHTTPAdapter()

        self.assertEqual(adapter._http_client.headers["appVersion"], ASSERT_APP_VERSION)
