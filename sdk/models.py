from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class Location(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    """Location information"""
    name: str
    region: str
    country: str
    lat: float
    lon: float
    localtime: str  # Changed from datetime to str to match API response

class WeatherCondition(BaseModel):
    """Weather condition information"""
    model_config = ConfigDict(populate_by_name=True)
    text: str
    icon: str
    code: int = 1000  # Default value for dummy data

class CurrentWeather(BaseModel):
    """Current weather information"""
    model_config = ConfigDict(populate_by_name=True)
    temp_c: float
    temp_f: float
    condition: WeatherCondition
    wind_mph: float
    wind_kph: float
    wind_degree: int = 0  # Default values for optional fields
    wind_dir: str = "N"
    pressure_mb: float = 1013.0
    pressure_in: float = 29.92
    precip_mm: float = 0.0
    precip_in: float = 0.0
    humidity: int = 50
    cloud: int = 0
    feelslike_c: float = Field(default=None)  # Optional fields
    feelslike_f: float = Field(default=None)
    vis_km: float = 10.0
    vis_miles: float = 6.2
    uv: float = 1.0
    gust_mph: float = Field(default=None)
    gust_kph: float = Field(default=None)

class DayForecast(BaseModel):
    """Daily forecast information"""
    model_config = ConfigDict(populate_by_name=True)
    maxtemp_c: float
    maxtemp_f: float
    mintemp_c: float
    mintemp_f: float
    condition: WeatherCondition

class ForecastDay(BaseModel):
    """Forecast for a specific day"""
    model_config = ConfigDict(populate_by_name=True)
    date: str  # Changed from datetime to str to match API response
    day: DayForecast

class Forecast(BaseModel):
    """Complete forecast response"""
    model_config = ConfigDict(populate_by_name=True)
    location: Location
    current: CurrentWeather
    forecast: List[ForecastDay]

class WeatherResponse(BaseModel):
    """Current weather response"""
    model_config = ConfigDict(populate_by_name=True)
    location: Location
    current: CurrentWeather
