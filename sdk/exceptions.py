class WeatherSDKException(Exception):
    """Base exception for WeatherSDK"""
    pass

class InvalidAPIKeyError(WeatherSDKException):
    """Raised when the API key is invalid or missing"""
    pass

class CityNotFoundError(WeatherSDKException):
    """Raised when the requested city is not found"""
    pass

class RateLimitError(WeatherSDKException):
    """Raised when the API rate limit is exceeded"""
    pass

class APIError(WeatherSDKException):
    """Raised when the API returns an error"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")
