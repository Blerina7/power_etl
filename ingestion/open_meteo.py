import os
from datetime import datetime

import pandas as pd
import requests


def fetch_weather_data(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "Europe/Tirane"
    }

    print(f"Fetching weather for coordinates {lat}, {lon}...")
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        df = pd.DataFrame({
            "time": data["hourly"]["time"],
            "temperature_2m": data["hourly"]["temperature_2m"]
        })

        df["time"] = pd.to_datetime(df["time"])
        print(f"Data retrieved successfully. {len(df)} rows found.")

        return df
    else:
        print(f"API error: {response.status_code}")
        return None


if __name__ == "__main__":
    TIRANA_LAT = 41.3275
    TIRANA_LON = 19.8189

    weather_df = fetch_weather_data(TIRANA_LAT, TIRANA_LON)

    if weather_df is not None:
        os.makedirs("raw_data", exist_ok=True)

        today = datetime.now().strftime("%Y%m%d")
        file_path = f"raw_data/weather_tirana_{today}.parquet"

        weather_df.to_parquet(file_path, index=False)
        print(f"Data saved to: {file_path}")