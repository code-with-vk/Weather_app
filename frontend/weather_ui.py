import flet as ft
import os
from typing import Optional
from backend.weather_service import WeatherDataService
from backend.chart_generator import WeatherChartGenerator
from config.settings import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class WeatherDashboardUI:
    """Main UI class for the weather dashboard"""
    
    def __init__(self):
        self.weather_service = WeatherDataService()
        self.chart_generator = WeatherChartGenerator()
        self.current_weather_data = None
        
        # UI Components
        self.city_input_field = None
        self.search_button = None
        self.weather_info_display = None
        self.weather_chart_image = None
        self.loading_indicator = None
        self.error_message_display = None
        self.page_reference = None
    
    def initialize_ui_components(self):
        """Initialize all UI components"""
        # City input field
        self.city_input_field = ft.TextField(
            label="Enter City Name",
            hint_text="e.g., London, Tokyo, New York",
            width=300,
            autofocus=True,
            on_submit=self.handle_weather_search
        )
        
        # Search button
        self.search_button = ft.ElevatedButton(
            text="Get Weather Data",
            icon=ft.icons.SEARCH,
            on_click=self.handle_weather_search,
            width=200
        )
        
        # Loading indicator
        self.loading_indicator = ft.ProgressRing(visible=False)
        
        # Weather information display
        self.weather_info_display = ft.Text(
            value="Enter a city name to get weather information",
            size=16,
            text_align=ft.TextAlign.CENTER
        )
        
        # Error message display
        self.error_message_display = ft.Text(
            value="",
            color=ft.colors.RED,
            size=14,
            visible=False
        )
        
        # Weather chart image
        self.weather_chart_image = ft.Image(
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN,
            visible=False
        )
    
    def handle_weather_search(self, event):
        """Handle weather search button click or enter key press"""
        city_name = self.city_input_field.value.strip()
        
        if not city_name:
            self.show_error_message("Please enter a city name")
            return
        
        self.start_loading()
        self.clear_error_message()
        
        # Fetch weather data
        weather_data = self.weather_service.get_complete_weather_info(city_name)
        
        if weather_data:
            self.current_weather_data = weather_data
            self.display_weather_information(weather_data)
            self.generate_and_display_chart(weather_data)
        else:
            self.show_error_message(f"Could not find weather data for '{city_name}'. Please check the city name.")
        
        self.stop_loading()
    
    def display_weather_information(self, weather_data):
        """Display weather information in text format"""
        city_name = weather_data['city_name']
        country = weather_data['country_code']
        temperature = weather_data['current_temperature']
        feels_like = weather_data['feels_like_temperature']
        humidity = weather_data['humidity_percentage']
        pressure = weather_data['atmospheric_pressure']
        wind_speed = weather_data['wind_speed']
        description = weather_data['weather_description']
        
        weather_text = f"""
🌍 {city_name}, {country}
🌡️ Temperature: {temperature}°C (feels like {feels_like}°C)
💧 Humidity: {humidity}%
📊 Pressure: {pressure} hPa
💨 Wind Speed: {wind_speed} m/s
☁️ Conditions: {description.title()}
        """
        
        self.weather_info_display.value = weather_text
        self.page_reference.update()
    
    def generate_and_display_chart(self, weather_data):
        """Generate weather chart and display it"""
        try:
            chart_file_path = self.chart_generator.create_weather_overview_chart(weather_data)
            
            if os.path.exists(chart_file_path):
                self.weather_chart_image.src = chart_file_path
                self.weather_chart_image.visible = True
                self.page_reference.update()
        except Exception as chart_error:
            self.show_error_message(f"Error generating chart: {str(chart_error)}")
    
    def start_loading(self):
        """Show loading indicator"""
        self.loading_indicator.visible = True
        self.search_button.disabled = True
        self.page_reference.update()
    
    def stop_loading(self):
        """Hide loading indicator"""
        self.loading_indicator.visible = False
        self.search_button.disabled = False
        self.page_reference.update()
    
    def show_error_message(self, message: str):
        """Display error message"""
        self.error_message_display.value = message
        self.error_message_display.visible = True
        self.page_reference.update()
    
    def clear_error_message(self):
        """Clear error message"""
        self.error_message_display.visible = False
        self.page_reference.update()
    
    def build_main_layout(self) -> ft.Column:
        """Build the main layout of the application"""
        return ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Text(
                        APP_TITLE,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center
                ),
                
                # Search section
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self.city_input_field,
                            self.search_button,
                            self.loading_indicator
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(10)
                ),
                
                # Error message
                ft.Container(
                    content=self.error_message_display,
                    alignment=ft.alignment.center
                ),
                
                # Weather information
                ft.Container(
                    content=self.weather_info_display,
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center
                ),
                
                # Weather chart
                ft.Container(
                    content=self.weather_chart_image,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10)
                )
            ],
            scroll=ft.ScrollMode.ALWAYS,
            auto_scroll=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    
    def setup_main_page(self, page: ft.Page):
        """Setup the main page configuration"""
        self.page_reference = page
        
        # Page configuration
        page.title = APP_TITLE
        page.window_width = WINDOW_WIDTH
        page.window_height = WINDOW_HEIGHT
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = ft.ScrollMode.ALWAYS
        page.auto_scroll = True
        
        # Initialize components and add to page
        self.initialize_ui_components()
        
        # Wrap main layout in a scrollable container
        scrollable_content = ft.Container(
            content=self.build_main_layout(),
            expand=True,
            padding=ft.padding.all(10)
        )
        
        page.add(scrollable_content)
        page.update()

# Create global dashboard instance
weather_dashboard = WeatherDashboardUI()

def create_weather_app(page: ft.Page):
    """Main function to create the weather app"""
    weather_dashboard.setup_main_page(page)
