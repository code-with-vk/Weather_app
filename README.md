# Weather Data Visualization Dashboard

A simple desktop weather dashboard built with:
- Python (requests for API calls)
- OpenWeatherMap API (current weather data)
- Matplotlib + Seaborn (charts)
- Flet (UI)
- python-dotenv (env config)

## What it does
- Fetches current weather for any city
- Shows key metrics: temperature, feels-like, humidity, pressure, wind, visibility, cloudiness
- Renders a chart image and displays it in the UI

## Requirements
- Python 3.9+
- OpenWeatherMap API key

## Quick start
1) Install dependencies
```
pip install -r requirements.txt
```

2) Create a .env file in the project root with your API key
```
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

3) Run the app
```
python main.py
```

## How to use
- Enter a city name (e.g., London, Tokyo, New York)
- Click “Get Weather Data”
- See details and a chart in the window

## Project structure
```
weather app/
├─ backend/
│  └─ weather_service.py      # Fetch + process weather data
├─ backend/
│  └─ chart_generator.py      # Build charts with matplotlib/seaborn
├─ frontend/
│  └─ weather_ui.py           # Flet UI
├─ config/
│  └─ settings.py             # Loads .env and app settings
├─ assets/
│  └─ charts/                 # Generated images saved here
├─ utils/
│  └─ path_helper.py          # Ensures imports work across modules
├─ main.py                    # App entry point
├─ requirements.txt           # Dependencies
└─ README.md                  # This file
```

## Configuration
- settings.py reads environment variables via python-dotenv
- Units default to metric
- Chart images are saved to assets/charts

Key env variable:
- OPENWEATHER_API_KEY

## Troubleshooting
- ModuleNotFoundError: No module named 'config'
  - Ensure you run from the project root: `python main.py`
  - utils/path_helper.py should be present and imported before settings
- OPENWEATHER_API_KEY not found
  - Make sure `.env` exists in the project root and contains `OPENWEATHER_API_KEY=...`
  - Restart the app after updating `.env`
- Chart not visible
  - Check that `assets/charts` exists and is writable
  - The app saves images like `current_weather_chart.png`
- No data for city
  - Try another city spelling; OpenWeatherMap expects valid names

## Notes
- Free OpenWeatherMap keys may take a few minutes to activate
- Network errors or rate limits can temporarily fail requests
- You can switch units in `config/settings.py` (metric/imperial)

Enjoy exploring the weather.
#
