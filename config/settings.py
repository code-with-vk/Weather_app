import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in environment variables. Please check your .env file.")

APP_TITLE = "Weather Data Visualization Dashboard"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

CHARTS_DIRECTORY = "assets/charts"
CHART_FILENAME = "current_weather_chart.png"

TEMPERATURE_UNIT = "metric"
APP_TITLE = "Weather Data Visualization Dashboard"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

# File Paths
CHARTS_DIRECTORY = "assets/charts"
CHART_FILENAME = "current_weather_chart.png"

# Weather Data Units
TEMPERATURE_UNIT = "metric"  # metric, imperial, or kelvin
