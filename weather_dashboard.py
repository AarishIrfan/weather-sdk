import streamlit as st
import pandas as pd
import plotly.express as px
from sdk.weather_sdk import WeatherSDK
from datetime import datetime

class WeatherDashboard:
    def __init__(self):
        try:
            self.sdk = WeatherSDK(use_dummy=True)  # Use dummy data for testing
            st.set_page_config(
                page_title="Weather Dashboard 2025",
                page_icon="🌤️",
                layout="wide"
            )
        except Exception as e:
            st.error(f"Initialization error: {str(e)}")

    def create_weather_df(self, forecast_data):
        """Convert forecast data to DataFrame"""
        data = []
        for day in forecast_data.forecast:
            data.append({
                'date': day.date,
                'max_temp': day.day.maxtemp_c,
                'min_temp': day.day.mintemp_c,
                'condition': day.day.condition.text
            })
        return pd.DataFrame(data)

    def run(self):
        # Page config
        st.set_page_config(
            page_title="Weather Report Dashboard 2025",
            page_icon="🌤️",
            layout="wide"
        )

        # Header
        st.title("🌤️ Weather Report Dashboard 2025")
        st.markdown("---")

        # City selection
        cities = ["London", "New York", "Tokyo", "Mumbai", "Sydney"]
        city = st.selectbox("Choose a City", cities)

        try:
            # Get current weather
            current = self.sdk.get_current_weather(city)
            forecast = self.sdk.get_forecast(city, days=7)

            # Current Weather Section
            st.subheader(f"Current Weather in {city}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Temperature", f"{current.current.temp_c}°C", 
                         f"{current.current.feelslike_c - current.current.temp_c:+.1f}°C feels like")
            
            with col2:
                st.metric("Humidity", f"{current.current.humidity}%")
            
            with col3:
                st.metric("Wind", f"{current.current.wind_kph} km/h")
            
            with col4:
                st.metric("Pressure", f"{current.current.pressure_mb} mb")

            st.markdown("---")

            # Forecast Section
            st.subheader("7-Day Forecast")
            
            # Convert forecast data to DataFrame
            df = self.create_weather_df(forecast)
            
            # Create temperature trend chart
            fig = px.line(df, x='date', y=['max_temp', 'min_temp'],
                         labels={'value': 'Temperature (°C)', 'date': 'Date'},
                         title='Temperature Trend')
            st.plotly_chart(fig, use_container_width=True)

            # Daily forecast cards
            st.markdown("### Daily Details")
            for i in range(0, len(df), 3):
                cols = st.columns(min(3, len(df) - i))
                for j, col in enumerate(cols):
                    if i + j < len(df):
                        with col:
                            st.markdown(f"""
                            **{df.iloc[i+j]['date']}**
                            - Max: {df.iloc[i+j]['max_temp']}°C
                            - Min: {df.iloc[i+j]['min_temp']}°C
                            - {df.iloc[i+j]['condition']}
                            """)

            # Additional Info
            st.markdown("---")
            st.markdown("### Location Details")
            st.json({
                "Region": current.location.region,
                "Country": current.location.country,
                "Local Time": current.location.localtime,
                "Coordinates": f"({current.location.lat}, {current.location.lon})"
            })

        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")

if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.run()
