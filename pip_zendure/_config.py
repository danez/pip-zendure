from typing import TypedDict


class ConfigType(TypedDict):
    base_url: str
    mqtt_url: str
    mqtt_port: int
    mqtt_username: str
    mqtt_password: str


CONFIG: dict[str, ConfigType] = {
    "eu": {
        "base_url": "https://app.zendure.tech/eu/",
        "mqtt_url": "mqtteu.zen-iot.com",
        "mqtt_port": 1883,
        "mqtt_username": "zenApp",
        "mqtt_password": "SDZzJGo5Q3ROYTBO",
    },
    "global": {
        "base_url": "https://app.zendure.tech/v2/",
        "mqtt_url": "mq.zen-iot.com",
        "mqtt_port": 1883,
        "mqtt_username": "zenApp",
        "mqtt_password": "b0sjUENneTZPWnhk",
    },
}
