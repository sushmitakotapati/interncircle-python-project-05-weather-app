
import os
import requests
from datetime import datetime

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    print("API key not found.")
    print("Please set OPENWEATHER_API_KEY.")
    exit()

city = input("Enter city name: ").strip()

current_url = "https://api.openweathermap.org/data/2.5/weather"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}

try:
    response = requests.get(current_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    print("\n--- Current Weather ---")
    print("City:", data["name"])
    print("Temperature:", data["main"]["temp"], "°C")
    print("Humidity:", data["main"]["humidity"], "%")
    print("Weather:", data["weather"][0]["description"])
    print("Wind Speed:", data["wind"]["speed"], "m/s")

    forecast_response = requests.get(
        forecast_url, params=params, timeout=10
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    print("\n--- 5-Day Forecast ---")

    shown_dates = set()

    for item in forecast_data["list"]:
        date = item["dt_txt"].split()[0]

        if date not in shown_dates:
            shown_dates.add(date)
            day = datetime.strptime(date, "%Y-%m-%d")
            print(
                day.strftime("%d %b"),
                "-",
                item["main"]["temp"],
                "°C,",
                item["weather"][0]["description"]
            )

        if len(shown_dates) == 5:
            break

except requests.exceptions.HTTPError as error:
    if response.status_code == 404:
        print("City not found.")
    elif response.status_code == 401:
        print("Invalid or inactive API key.")
    else:
        print("API error:", error)

except requests.exceptions.RequestException:
    print("Network error. Check your internet connection.")

except (KeyError, ValueError):
    print("Unable to read weather data.")
