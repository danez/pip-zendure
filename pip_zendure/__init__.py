from pip_zendure._const import REGION
from pip_zendure._models import AuthData
from pip_zendure._zendure_mqtt_client import ZendureMQTTClient

from ._api_client import APIClient
from .api_exception import APIException
from .http._chain_http_adapter import ChainHTTPAdapter
from .http._signed_http_adapter import SignedHTTPAdapter
from .http._unsigned_http_adapter import UnsignedHTTPAdapter


class ZendureAPI:
    """An API class to handle communication with the Zendure API"""

    def __init__(self):
        self._api_client = None
        self._mqtt_client = None
        self._auth_data = None

        # Use the UnsignedHTTPAdapter first because it is faster
        self._http_adapter = ChainHTTPAdapter(
            [UnsignedHTTPAdapter(), SignedHTTPAdapter()]
        )

    @property
    def auth_data(self) -> AuthData:
        return self._auth_data

    @auth_data.setter
    def auth_data(self, auth_data: AuthData) -> None:
        self._auth_data = auth_data
        self._http_adapter.set_token(auth_data.token)
        self._http_adapter.switch_region(auth_data.region)
        if self._api_client:
            self._api_client.region(auth_data.region)

    async def login(self, username: str, password: str) -> AuthData:
        """Login to the Zendure API with the given username and password"""

        api_client = APIClient(self._http_adapter)
        self.auth_data = await api_client.get_token(username, password)

        return self.auth_data

    async def use_token(self, token: str) -> bool:
        """Use a token to authenticate with the Zendure API"""

        self._http_adapter.set_token(token)
        try:
            api_client = APIClient(self._http_adapter)
            user_info = await api_client.get_user_info()

            self.auth_data = AuthData(
                token=token, region=REGION(user_info["serverNode"])
            )

            return True
        except APIException:
            self._http_adapter.set_token(None)

            return False

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.aclose()

    async def aclose(self) -> None:
        await self._http_adapter.aclose()
        self._http_adapter = None
        self._api_client = None
        self._mqtt_client = None  # stop it also

    @property
    def api_client(self) -> APIClient:
        return (
            self._api_client
            if self._api_client
            else APIClient(
                self._http_adapter, self._auth_data.region if self._auth_data else None
            )
        )

    @property
    def get_mqtt_client(self):
        return (
            self._mqtt_client
            if self._mqtt_client
            else ZendureMQTTClient(
                self._auth_data,  # missing things here
            )
        )
