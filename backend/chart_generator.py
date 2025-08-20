import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict
from config.settings import CHARTS_DIRECTORY, CHART_FILENAME

class WeatherChartGenerator:
    """Class to generate weather data visualizations"""
    def __init__(self):
        self.charts_folder = CHARTS_DIRECTORY
        self.chart_file_name = CHART_FILENAME
        self._ensure_charts_directory_exists()
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def _ensure_charts_directory_exists(self):
        """Create charts directory if it doesn't exist"""
        if not os.path.exists(self.charts_folder):
            os.makedirs(self.charts_folder)
    
    def create_weather_overview_chart(self, weather_info: Dict) -> str:
        """
        Create a comprehensive weather overview chart
        
        Args:
            weather_info (Dict): Processed weather information
            
        Returns:
            str: Path to the generated chart image
        """
        city_display_name = f"{weather_info['city_name']}, {weather_info['country_code']}"
        
        # Create figure with subplots
        figure, chart_axes = plt.subplots(2, 2, figsize=(12, 10))
        figure.suptitle(f'Weather Dashboard - {city_display_name}', fontsize=16, fontweight='bold')
        
        # Temperature Chart
        temperature_data = [
            weather_info['current_temperature'], 
            weather_info['feels_like_temperature']
        ]
        temperature_labels = ['Current Temp', 'Feels Like']
        
        chart_axes[0, 0].bar(temperature_labels, temperature_data, color=['#ff6b6b', '#feca57'])
        chart_axes[0, 0].set_title('Temperature (°C)', fontweight='bold')
        chart_axes[0, 0].set_ylabel('Temperature (°C)')
        
        # Add value labels on bars
        for i, temp_value in enumerate(temperature_data):
            chart_axes[0, 0].text(i, temp_value + 0.5, f'{temp_value}°C', 
                                ha='center', fontweight='bold')
        
        # Atmospheric Conditions
        atmospheric_metrics = [
            weather_info['humidity_percentage'],
            weather_info['atmospheric_pressure'] / 10,  # Scale down for better visualization
            weather_info['cloudiness_percentage']
        ]
        atmospheric_labels = ['Humidity (%)', 'Pressure (kPa)', 'Cloudiness (%)']
        
        chart_axes[0, 1].bar(atmospheric_labels, atmospheric_metrics, 
                           color=['#48cae4', '#023e8a', '#6c757d'])
        chart_axes[0, 1].set_title('Atmospheric Conditions', fontweight='bold')
        chart_axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Wind and Visibility
        wind_visibility_data = [
            weather_info['wind_speed'],
            weather_info['visibility_meters'] / 1000  # Convert to km
        ]
        wind_visibility_labels = ['Wind Speed (m/s)', 'Visibility (km)']
        
        chart_axes[1, 0].bar(wind_visibility_labels, wind_visibility_data,
                           color=['#90e0ef', '#0077b6'])
        chart_axes[1, 0].set_title('Wind & Visibility', fontweight='bold')
        
        # Weather Summary (Text)
        chart_axes[1, 1].axis('off')
        summary_text = f"""
Weather Summary

Condition: {weather_info['weather_main']}
Description: {weather_info['weather_description'].title()}

Temperature: {weather_info['current_temperature']}°C
Feels Like: {weather_info['feels_like_temperature']}°C
Humidity: {weather_info['humidity_percentage']}%
Pressure: {weather_info['atmospheric_pressure']} hPa
Wind Speed: {weather_info['wind_speed']} m/s
        """
        
        chart_axes[1, 1].text(0.1, 0.9, summary_text, transform=chart_axes[1, 1].transAxes,
                            fontsize=11, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # Adjust layout and save
        plt.tight_layout()
        chart_save_path = os.path.join(self.charts_folder, self.chart_file_name)
        plt.savefig(chart_save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return chart_save_path
    
    def create_simple_temperature_chart(self, weather_info: Dict) -> str:
        """
        Create a simple temperature comparison chart
        
        Args:
            weather_info (Dict): Processed weather information
            
        Returns:
            str: Path to the generated chart image
        """
        plt.figure(figsize=(8, 6))
        
        temperature_values = [
            weather_info['current_temperature'],
            weather_info['feels_like_temperature']
        ]
        temperature_types = ['Actual Temperature', 'Feels Like Temperature']
        
        bars = plt.bar(temperature_types, temperature_values, 
                      color=['#ff6b6b', '#feca57'], alpha=0.8)
        
        plt.title(f"Temperature in {weather_info['city_name']}", 
                 fontsize=14, fontweight='bold')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar, temp_value in zip(bars, temperature_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{temp_value}°C', ha='center', fontweight='bold')
        
        plt.tight_layout()
        simple_chart_path = os.path.join(self.charts_folder, 'simple_' + self.chart_file_name)
        plt.savefig(simple_chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return simple_chart_path
