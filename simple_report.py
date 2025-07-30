from sdk.weather_sdk import WeatherSDK
import time
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

# Only initialize colorama if this is the main script
if __name__ == "__main__":
    colorama.init()

def generate_simple_report(city: str):
    """Generate a simple weather report for a city"""
    sdk = WeatherSDK(use_dummy=True)
    
    print(f"\n{Fore.CYAN}" + "="*60 + Style.RESET_ALL)
    print(f"{Fore.GREEN}Weather Report for {Fore.YELLOW}{city}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}" + "="*60 + Style.RESET_ALL)
    
    # Get current weather
    current = sdk.get_current_weather(city)
    
    # Current conditions
    print(f"\n{Fore.MAGENTA}CURRENT CONDITIONS at {current.location.localtime}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}" + "-"*40 + Style.RESET_ALL)
    
    # Temperature with color coding
    temp_color = Fore.RED if current.current.temp_c > 30 else (Fore.BLUE if current.current.temp_c < 10 else Fore.GREEN)
    print(f"{Fore.WHITE}Temperature: {temp_color}{current.current.temp_c}°C ({current.current.temp_f}°F){Style.RESET_ALL}")
    print(f"{Fore.WHITE}Feels Like: {temp_color}{current.current.feelslike_c}°C{Style.RESET_ALL}")
    
    # Weather condition
    print(f"{Fore.WHITE}Condition: {Fore.YELLOW}{current.current.condition.text}{Style.RESET_ALL}")
    
    # Humidity with color coding
    humidity_color = Fore.RED if current.current.humidity > 70 else (Fore.GREEN if current.current.humidity < 30 else Fore.YELLOW)
    print(f"{Fore.WHITE}Humidity: {humidity_color}{current.current.humidity}%{Style.RESET_ALL}")
    
    # Wind
    wind_color = Fore.RED if current.current.wind_kph > 30 else (Fore.GREEN if current.current.wind_kph < 10 else Fore.YELLOW)
    print(f"{Fore.WHITE}Wind: {wind_color}{current.current.wind_kph} km/h {current.current.wind_dir}{Style.RESET_ALL}")
    
    # Get forecast
    forecast = sdk.get_forecast(city, days=5)
    
    # 5-day forecast
    print(f"\n{Fore.MAGENTA}5-DAY FORECAST{Style.RESET_ALL}")
    print(f"{Fore.CYAN}" + "-"*40 + Style.RESET_ALL)
    
    for day in forecast.forecast:
        print(f"\n{Fore.YELLOW}Date: {day.date}{Style.RESET_ALL}")
        
        # Max temperature with color coding
        max_temp_color = Fore.RED if day.day.maxtemp_c > 30 else (Fore.BLUE if day.day.maxtemp_c < 10 else Fore.GREEN)
        print(f"Max Temperature: {max_temp_color}{day.day.maxtemp_c}°C{Style.RESET_ALL}")
        
        # Min temperature with color coding
        min_temp_color = Fore.RED if day.day.mintemp_c > 25 else (Fore.BLUE if day.day.mintemp_c < 5 else Fore.GREEN)
        print(f"Min Temperature: {min_temp_color}{day.day.mintemp_c}°C{Style.RESET_ALL}")
        
        # Condition
        print(f"Condition: {Fore.CYAN}{day.day.condition.text}{Style.RESET_ALL}")
    
    print("\n" + "="*50 + "\n")

def main():
    cities = [
        "London", "New York", "Tokyo", "Mumbai", "Sydney", 
        "Dubai", "Singapore", "Paris", "Berlin", "Toronto"
    ]
    
    while True:
        print(f"\n{Fore.GREEN}Weather Reporting System 2025{Style.RESET_ALL}")
        print(f"{Fore.CYAN}=" * 40 + Style.RESET_ALL)
        print(f"{Fore.YELLOW}1. View Single City Report")
        print("2. View All Cities Report")
        print("3. Monitor Live Updates (30s interval)")
        print(f"4. Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}Enter your choice (1-4): {Style.RESET_ALL}")
    
    if choice == "1":
        while True:
            print(f"\n{Fore.CYAN}Available cities:{Style.RESET_ALL}")
            for i, city in enumerate(cities, 1):
                print(f"{Fore.YELLOW}{i}. {city}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}0. Back to main menu{Style.RESET_ALL}")
            
            try:
                city_idx = int(input(f"\n{Fore.GREEN}Enter city number (0 to go back): {Style.RESET_ALL}"))
                if city_idx == 0:
                    break
                if 1 <= city_idx <= len(cities):
                    generate_simple_report(cities[city_idx - 1])
                else:
                    print(f"{Fore.RED}Invalid city number! Choose 0-{len(cities)}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
    
    elif choice == "2":
        print(f"{Fore.CYAN}Generating reports for all cities...{Style.RESET_ALL}")
        for city in cities:
            generate_simple_report(city)
            print(f"{Fore.CYAN}Press Enter for next city...{Style.RESET_ALL}")
            input()
            
    elif choice == "3":
        try:
            print(f"\n{Fore.YELLOW}Starting live monitoring (Press Ctrl+C to stop){Style.RESET_ALL}")
            update_count = 1
            while True:
                print(f"\n{Fore.CYAN}Update #{update_count}{Style.RESET_ALL}")
                for city in cities:
                    generate_simple_report(city)
                    time.sleep(1)  # Small delay between cities
                print(f"\n{Fore.YELLOW}Updating in 30 seconds...{Style.RESET_ALL}")
                time.sleep(30)
                update_count += 1
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Monitoring stopped{Style.RESET_ALL}")
    
    elif choice == "4":
        print(f"\n{Fore.GREEN}Thank you for using Weather Reporting System 2025!{Style.RESET_ALL}")
        return False
    
    else:
        print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
    
    return True

if __name__ == "__main__":
    print(f"{Fore.CYAN}" + "="*60)
    print(f"{Fore.GREEN}Welcome to Weather Reporting System 2025!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}" + "="*60 + f"{Style.RESET_ALL}\n")
    
    while main():
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
