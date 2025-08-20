import flet as ft
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from frontend.weather_ui import create_weather_app

def main():
    """Main function to launch the weather dashboard application"""
    print("🌤️  Starting Weather Data Visualization Dashboard...")
    print("📊 Loading user interface...")
    
    try:
        # Launch the Flet application
        ft.app(
            target=create_weather_app,
            view=ft.AppView.FLET_APP,  # Desktop application
            port=8080
        )
    except Exception as app_error:
        print(f"❌ Error starting the application: {app_error}")
        print("💡 Please check your internet connection and API key configuration")

if __name__ == "__main__":
    main()
