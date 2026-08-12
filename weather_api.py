import requests


def get_rainfall_data(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,relative_humidity_2m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        hourly = data["hourly"]

        rainfall = hourly["precipitation"]

        humidity = hourly["relative_humidity_2m"]

        # Last 3 hours
        rainfall_3h = sum(rainfall[-3:])

        # Last 24 hours
        rainfall_24h = sum(rainfall[-24:])

        # Most recent humidity value
        current_humidity = humidity[-1]

        return {
            "rainfall_3h": rainfall_3h,
            "rainfall_24h": rainfall_24h,
            "humidity": current_humidity
        }

    except Exception as error:

        print("Weather API error:", error)

        return None