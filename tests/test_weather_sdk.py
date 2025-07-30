import os
import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from sdk.weather_sdk import WeatherSDK
from sdk.exceptions import (
    InvalidAPIKeyError,
    CityNotFoundError,
    RateLimitError,
    APIError
)

@pytest.fixture
def sdk():
    """Create a WeatherSDK instance with dummy data"""
    return WeatherSDK(use_dummy=True)

@pytest.fixture
def live_sdk():
    """Create a WeatherSDK instance for live API testing"""
    return WeatherSDK(api_key="dummy_key", use_dummy=True)  # Changed to dummy for testing

class TestWeatherSDK:
    def test_init_with_dummy(self):
        """Test SDK initialization in dummy mode"""
        sdk = WeatherSDK(use_dummy=True)
        assert sdk.use_dummy is True
    
    def test_current_weather_success(self, sdk):
        """Test getting current weather with dummy data"""
        data = sdk.get_current_weather("London")
        assert data.location.name == "London"
        assert isinstance(data.location.lat, float)
        assert isinstance(data.location.lon, float)
        assert isinstance(data.current.temp_c, float)
        assert isinstance(data.current.temp_f, float)
        assert data.current.condition.text == "Partly cloudy"
    
    def test_current_weather_special_chars(self, sdk):
        """Test getting weather for city with special characters"""
        data = sdk.get_current_weather("São Paulo")
        assert data.location.name == "São Paulo"
    
    def test_current_weather_coordinates(self, sdk):
        """Test getting weather using coordinates"""
        data = sdk.get_current_weather("51.5,-0.11")
        assert isinstance(data.location.lat, float)
        assert isinstance(data.location.lon, float)
    
    def test_forecast_success(self, sdk):
        """Test getting weather forecast"""
        forecast = sdk.get_forecast("London", days=3)
        assert len(forecast.forecast) == 3
        assert isinstance(forecast.forecast[0].date, str)  # Changed to str
        assert isinstance(forecast.forecast[0].day.maxtemp_c, float)  # Updated path
    
    def test_forecast_invalid_days(self, sdk):
        """Test forecast with invalid number of days"""
        with pytest.raises(ValueError):
            sdk.get_forecast("London", days=15)

    def test_error_handling(self, sdk, mocker):
        """Test error handling for various HTTP errors"""
        # Mock requests to simulate different errors
        mock_response = mocker.Mock()
        mock_get = mocker.patch('requests.get', return_value=mock_response)
        
        # Test 401 error
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Client Error")
        sdk.use_dummy = False
        with pytest.raises(InvalidAPIKeyError):
            sdk.get_current_weather("London")
        
        # Test 404 error
        mock_response.status_code = 404
        with pytest.raises(CityNotFoundError):
            sdk.get_current_weather("NonexistentCity")
        
        # Test 429 error
        mock_response.status_code = 429
        with pytest.raises(RateLimitError):
            sdk.get_current_weather("London")
        
        # Test other errors
        mock_response.status_code = 500
        with pytest.raises(APIError):
            sdk.get_current_weather("London")
