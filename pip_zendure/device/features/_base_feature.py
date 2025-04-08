class Base_Feature:
    def __init__(self, mqtt_client, **kwargs):
        super().__init__(**kwargs)
        self.mqtt_client = mqtt_client
