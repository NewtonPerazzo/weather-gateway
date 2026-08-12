class APIIntegration():
    def __init__(
            self, 
            weather_url: str, 
            authentication_url: str,
        ):
        self.authentication_url = authentication_url
        self.weather_url = weather_url
