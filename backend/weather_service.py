import requests
import logging
from typing import Dict, Optional

# Setup project path for imports
from utils.path_helper import setup_project_path
setup_project_path()

from config.settings import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, TEMPERATURE_UNIT

# Set up logging
logging.basicConfig(level=logging.INFO)
weather_logger = logging.getLogger(__name__)

class WeatherDataService:
    """Service class to handle weather data operations"""
    
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = OPENWEATHER_BASE_URL
        self.units = TEMPERATURE_UNIT
        
        # Validate API key is available
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key is not configured. Please check your .env file.")
        
        weather_logger.info("Weather service initialized successfully")
    
    def fetch_weather_data(self, city_name: str) -> Optional[Dict]:
        """
        Fetch weather data from OpenWeatherMap API
        
        Args:
            city_name (str): Name of the city to get weather for
            
        Returns:
            Dict: Weather data or None if request fails
        """
        try:
            request_url = f"{self.base_url}?q={city_name}&appid={self.api_key}&units={self.units}"
            
            weather_logger.info(f"Fetching weather data for: {city_name}")
            api_response = requests.get(request_url, timeout=10)
            api_response.raise_for_status()
            
            return api_response.json()
            
        except requests.exceptions.RequestException as request_error:
            weather_logger.error(f"Error fetching weather data: {request_error}")
            return None
        except Exception as general_error:
            weather_logger.error(f"Unexpected error: {general_error}")
            return None
    
    def process_weather_information(self, raw_weather_data: Dict) -> Dict:
        """
        Process raw weather data into a clean format
        
        Args:
            raw_weather_data (Dict): Raw API response data
            
        Returns:
            Dict: Processed weather information
        """
        try:
            processed_data = {
                "city_name": raw_weather_data.get("name", "Unknown"),
                "country_code": raw_weather_data.get("sys", {}).get("country", ""),
                "current_temperature": round(raw_weather_data.get("main", {}).get("temp", 0), 1),
                "feels_like_temperature": round(raw_weather_data.get("main", {}).get("feels_like", 0), 1),
                "humidity_percentage": raw_weather_data.get("main", {}).get("humidity", 0),
                "atmospheric_pressure": raw_weather_data.get("main", {}).get("pressure", 0),
                "wind_speed": raw_weather_data.get("wind", {}).get("speed", 0),
                "weather_description": raw_weather_data.get("weather", [{}])[0].get("description", ""),
                "weather_main": raw_weather_data.get("weather", [{}])[0].get("main", ""),
                "visibility_meters": raw_weather_data.get("visibility", 0),
                "cloudiness_percentage": raw_weather_data.get("clouds", {}).get("all", 0)
            }
            
            weather_logger.info(f"Successfully processed weather data for {processed_data['city_name']}")
            return processed_data
            
        except Exception as processing_error:
            weather_logger.error(f"Error processing weather data: {processing_error}")
            return {}
    
    def get_complete_weather_info(self, city_name: str) -> Optional[Dict]:
        """
        Get complete weather information for a city
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            Dict: Complete processed weather information or None
        """
        raw_data = self.fetch_weather_data(city_name)
        if raw_data:
            return self.process_weather_information(raw_data)
        return None
