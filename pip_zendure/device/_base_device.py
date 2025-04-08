class Device:
    """Device information."""

    id: int
    name: str
    key: str
    product_key: str

    def __init__(self, id: int, name: str, key: str, product_key: str):
        self.id = id
        self.name = name
        self.key = key
        self.product_key = product_key
