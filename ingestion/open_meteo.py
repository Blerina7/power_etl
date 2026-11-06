import requests
import pandas as pd
from datetime import datetime
import os

def fetch_weather_data(lat, lon):
    # API i Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Parametrat që na duhen (p.sh. temperatura orare)
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "Europe/Tirane"
    }
    
    print(f"Duke tërhequr motin për koordinatat {lat}, {lon}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Krijojmë një DataFrame nga të dhënat JSON
        df = pd.DataFrame({
            "time": data["hourly"]["time"],
            "temperature_2m": data["hourly"]["temperature_2m"]
        })
        
        # Sigurohemi që formati i kohës është datetime
        df["time"] = pd.to_datetime(df["time"])
        print(f"Tërheqja me sukses! U gjetën {len(df)} rreshta.")
        
        return df
    else:
        print(f"Gabim në API: {response.status_code}")
        return None

if __name__ == "__main__":
    # Koordinatat e Tiranës 
    TIRANA_LAT = 41.3275
    TIRANA_LON = 19.8189
    
    weather_df = fetch_weather_data(TIRANA_LAT, TIRANA_LON)
    
    if weather_df is not None:
        # Krijojmë dosjen raw_data nëse nuk ekziston
        os.makedirs("raw_data", exist_ok=True)
        
        # Gjenerojmë emrin e skedarit me datën e sotme
        today = datetime.now().strftime('%Y%m%d')
        file_path = f"raw_data/weather_tirana_{today}.parquet"
        
        # E ruajmë në formatin columnar Parquet (perfekt për DuckDB/dbt)
        weather_df.to_parquet(file_path, index=False)
        print(f"Të dhënat u ruajtën në: {file_path}")