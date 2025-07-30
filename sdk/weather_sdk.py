import requests
import os
from datetime import datetime, timedelta
from typing import Optional, Union, List
from dateutil.parser import parse
from dotenv import load_dotenv

from .models import WeatherResponse, Forecast, Location, CurrentWeather, ForecastDay
from .exceptions import (
    WeatherSDKException, 
    InvalidAPIKeyError, 
    CityNotFoundError, 
    RateLimitError, 
    APIError
)

class WeatherSDK:
    """
    A Python SDK for accessing weather data.
    
    Args:
        api_key (str, optional): API key for WeatherAPI.com. If not provided, will look for WEATHER_API_KEY env var
        use_dummy (bool, optional): Whether to use dummy data for testing. Defaults to False
    
    Raises:
        InvalidAPIKeyError: If no API key is provided and WEATHER_API_KEY env var is not set
    """
    
    def __init__(self, api_key: Optional[str] = None, use_dummy: bool = False):
        self.use_dummy = use_dummy
        load_dotenv()  # Always load env in case we switch modes
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        if not self.use_dummy and not self.api_key:
            raise InvalidAPIKeyError("No API key provided")
        self.base_url = "https://api.weatherapi.com/v1"
        
    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make a request to the WeatherAPI.com API"""
        if self.use_dummy:
            return self._get_dummy_data(endpoint, params)
            
        url = f"{self.base_url}/{endpoint}"
        params["key"] = self.api_key
        
        headers = {
            "User-Agent": "WeatherSDK/2.0",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise InvalidAPIKeyError("Invalid API key")
            elif response.status_code == 404:
                raise CityNotFoundError(f"City not found: {params.get('q')}")
            elif response.status_code == 429:
                raise RateLimitError("API rate limit exceeded")
            else:
                raise APIError(response.status_code, str(e))
                
    def _get_dummy_data(self, endpoint: str, params: dict) -> dict:
        """Get dummy data for testing"""
        city = params.get("q", "London")
        base_data = {
            "location": {
                "name": city,
                "region": "Test Region",
                "country": "Test Country",
                "lat": 51.52,
                "lon": -0.11,
                "localtime": datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            "current": {
                "temp_c": 22.0,
                "temp_f": 71.6,
                "condition": {
                    "text": "Partly cloudy",
                    "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
                    "code": 1003
                },
                "wind_mph": 8.1,
                "wind_kph": 13.0,
                "wind_degree": 220,
                "wind_dir": "SW",
                "pressure_mb": 1013.0,
                "pressure_in": 29.91,
                "precip_mm": 0.0,
                "precip_in": 0.0,
                "humidity": 65,
                "cloud": 40,
                "feelslike_c": 22.0,
                "feelslike_f": 71.6,
                "vis_km": 10.0,
                "vis_miles": 6.2,
                "uv": 4.0,
                "gust_mph": 10.5,
                "gust_kph": 16.9
            }
        }
        
        if endpoint == "forecast.json":
            days = params.get("days", 1)
            base_data["forecast"] = {
                "forecastday": [
                    {
                        "date": (datetime.now() + timedelta(days=i)).isoformat(),
                        "day": {
                            "maxtemp_c": 25.0,
                            "maxtemp_f": 77.0,
                            "mintemp_c": 15.0,
                            "mintemp_f": 59.0,
                            "condition": {
                                "text": "Sunny",
                                "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                                "code": 1000
                            }
                        }
                    } for i in range(days)
                ]
            }
        
        return base_data
    
    def get_current_weather(self, city: str) -> WeatherResponse:
        """
        Get current weather for a city
        
        Args:
            city (str): City name or coordinates (e.g., "London" or "51.5,-0.11")
            
        Returns:
            WeatherResponse: Current weather data
            
        Raises:
            CityNotFoundError: If the city is not found
            InvalidAPIKeyError: If the API key is invalid
            RateLimitError: If the API rate limit is exceeded
            APIError: If any other API error occurs
        """
        data = self._make_request("current.json", {"q": city})
        return WeatherResponse(**data)
    
    def get_forecast(self, city: str, days: int = 3) -> Forecast:
        """
        Get weather forecast for a city
        
        Args:
            city (str): City name or coordinates
            days (int, optional): Number of days to forecast (1-14). Defaults to 3
            
        Returns:
            Forecast: Forecast data
        """
        if not 1 <= days <= 14:
            raise ValueError("Days must be between 1 and 14")
            
        data = self._make_request("forecast.json", {
            "q": city,
            "days": days
        })
        return Forecast(**data)
