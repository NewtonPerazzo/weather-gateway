class APIIntegration():
    def __init__(
            self, 
            weather_url: str, 
            authentication_url: str,
            request_timeout_seconds: float,
        ):
        self.authentication_url = authentication_url
        self.weather_url = weather_url
        self.request_timeout_seconds = request_timeout_seconds
