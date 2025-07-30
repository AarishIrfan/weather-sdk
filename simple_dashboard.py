import streamlit as st
from sdk.weather_sdk import WeatherSDK
import time

# Configure the page
st.set_page_config(
    page_title="Weather Dashboard 2025",
    page_icon="🌤️",
    layout="wide"
)

# Initialize SDK with error handling
try:
    sdk = WeatherSDK(use_dummy=True)
    st.title("🌤️ Weather Dashboard 2025")
    
    # City selection
    cities = ["London", "New York", "Tokyo", "Mumbai", "Sydney"]
    city = st.selectbox("Choose a City", cities)
    
    try:
        # Get weather data
        current = sdk.get_current_weather(city)
        
        # Display current weather
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Temperature", f"{current.current.temp_c}°C", 
                     f"{current.current.feelslike_c - current.current.temp_c:+.1f}°C feels like")
        
        with col2:
            st.metric("Humidity", f"{current.current.humidity}%")
        
        with col3:
            st.metric("Wind", f"{current.current.wind_kph} km/h")
        
        # Add location details
        st.subheader("Location Details")
        st.json({
            "City": current.location.name,
            "Region": current.location.region,
            "Country": current.location.country,
            "Local Time": current.location.localtime
        })
        
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        
except Exception as e:
    st.error(f"Failed to initialize Weather SDK: {str(e)}")

# Add a refresh button
if st.button("Refresh Data"):
    st.rerun()
