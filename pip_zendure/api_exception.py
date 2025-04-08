class APIException(Exception):
    def __init__(
        self,
        http_code: int,
        route: str,
        message: str = "An Error occurred while calling the Zendure API.",
    ):
        self.http_code = http_code
        self.route = route
        self.add_note(f"HTTP Code: {http_code}")
        self.add_note(f"Route: {route}")
        super().__init__(message)
