import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from entsoe import EntsoePandasClient

# Ngarkojmë variablat e mjedisit nga skedari .env
load_dotenv()
token = os.getenv('ENTSOE_API_TOKEN')

if not token:
    raise ValueError("Token-i nuk u gjet! Sigurohu që skedari .env ekziston dhe emri i variablit është i saktë.")

# Inicializojmë klientin e API-t
client = EntsoePandasClient(api_key=token)

def fetch_power_prices(country_code, start_date, end_date):
    print(f"Duke kërkuar çmimet Day-Ahead për {country_code}...")
    try:
        # entsoe-py kërkon datat me timezone specifik
        start = pd.Timestamp(start_date, tz='Europe/Tirane')
        end = pd.Timestamp(end_date, tz='Europe/Tirane')
        
        # Tërheqim çmimet
        df = client.query_day_ahead_prices(country_code, start=start, end=end)
        
        # API kthen një format 'Series', e kthejmë në DataFrame tabelar
        df = df.reset_index()
        df.columns = ['time', 'price_eur_mwh']
        df['country'] = country_code
        
        print(f"Sukses! U gjetën {len(df)} rreshta.")
        return df
        
    except Exception as e:
        print(f"Gabim nga API i ENTSO-E: {e}")
        return None

if __name__ == "__main__":
    # Marrim të dhënat e djeshme dhe të sotme
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    start_str = yesterday.strftime('%Y%m%d')
    end_str = (today + timedelta(days=1)).strftime('%Y%m%d')
    
    # Kodi për Shqipërinë është 'AL'. 
    # (Nëse do vende të tjera të Ballkanit mund të shtosh 'GR', 'RS', 'ME', 'MK')
    target_country = 'AL' 
    
    prices_df = fetch_power_prices(target_country, start_str, end_str)
    
    if prices_df is not None and not prices_df.empty:
        os.makedirs("raw_data", exist_ok=True)
        file_path = f"raw_data/prices_{target_country}_{today.strftime('%Y%m%d')}.parquet"
        
        prices_df.to_parquet(file_path, index=False)
        print(f"Skedari u ruajt: {file_path}")
    else:
        print("Nuk u ruajt asnjë e dhënë.")