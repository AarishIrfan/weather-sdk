from sdk.weather_sdk import WeatherSDK

def main():
    # Create SDK instance with dummy data
    sdk = WeatherSDK(use_dummy=True)
    
    # Test current weather
    weather = sdk.get_current_weather("London")
    print("\nCurrent Weather Test:")
    print("-" * 20)
    print(f"City: {weather.location.name}")
    print(f"Temperature: {weather.current.temp_c}°C")
    print(f"Condition: {weather.current.condition.text}")
    
    # Test forecast
    forecast = sdk.get_forecast("London", days=3)
    print("\nForecast Test:")
    print("-" * 20)
    for day in forecast.forecast:
        print(f"Date: {day.date}")
        print(f"Max: {day.day.maxtemp_c}°C")
        print(f"Min: {day.day.mintemp_c}°C")
        print()

if __name__ == "__main__":
    main()
