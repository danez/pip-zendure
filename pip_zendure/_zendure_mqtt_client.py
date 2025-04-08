import asyncio
import base64

from aiomqtt import Client, MessagesIterator, ProtocolVersion

from pip_zendure._config import CONFIG
from pip_zendure._models import AuthData, Device


class ZendureMQTTClient:
    def __init__(self, auth_data: AuthData):
        config = CONFIG[auth_data.region]

        self.client = Client(
            config.mqtt_url,
            config.mqtt_port,
            username=config.mqtt_username,
            password=base64.b64decode(config.mqtt_password).decode("utf-8"),
            identifier=auth_data.token,
            protocol=ProtocolVersion.V5,
        )

    def messages(self) -> MessagesIterator:
        """Dynamic view of the client's message queue."""
        return self.client.messages

    async def subscribe_device(self, device: Device) -> None:
        """Subscribe to a device's MQTT topics"""
        reportTopic = f"{device.product_key}/{device.key}/#"
        await self.client.subscribe(reportTopic)
        await asyncio.sleep(0.25)

        iotTopic = f"iot/${device.product_key}/${device.key}/#"
        await self.client.subscribe(iotTopic)
        await asyncio.sleep(0.25)

    async def subscribe_devices(
        self,
        devices: list[Device],
    ) -> None:
        """Subscribe to all devices' MQTT topics"""
        for device in devices:
            await self.subscribe_device(device)

    async def __aenter__(self):
        self.start()

        return self

    async def __aexit__(self):
        self.stop()

    async def start(self):
        await self.client.__aenter__()

    async def stop(self):
        await self.client.__aexit__(None, None, None)
