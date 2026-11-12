import os
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient

load_dotenv()
token = os.getenv("ENTSOE_API_TOKEN")

if not token:
    raise ValueError("API token not found. Make sure the .env file exists and the variable name is correct.")

client = EntsoePandasClient(api_key=token)


def fetch_power_prices(country_code, start_date, end_date):
    print(f"Fetching Day-Ahead prices for {country_code}...")
    try:
        start = pd.Timestamp(start_date, tz="Europe/Tirane")
        end = pd.Timestamp(end_date, tz="Europe/Tirane")

        df = client.query_day_ahead_prices(country_code, start=start, end=end)

        df = df.reset_index()
        df.columns = ["time", "price_eur_mwh"]
        df["country"] = country_code

        print(f"Success! {len(df)} rows found.")
        return df

    except Exception as e:
        print(f"ENTSO-E API error: {e}")
        return None


if __name__ == "__main__":
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    start_str = yesterday.strftime("%Y%m%d")
    end_str = (today + timedelta(days=1)).strftime("%Y%m%d")

    target_country = "AL"

    prices_df = fetch_power_prices(target_country, start_str, end_str)

    if prices_df is not None and not prices_df.empty:
        os.makedirs("raw_data", exist_ok=True)
        file_path = f"raw_data/prices_{target_country}_{today.strftime('%Y%m%d')}.parquet"

        prices_df.to_parquet(file_path, index=False)
        print(f"File saved: {file_path}")
    else:
        print("No data was saved.")