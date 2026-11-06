import duckdb

def load_data():
    print("Duke u lidhur me databazën DuckDB (warehouse.duckdb)...")
    # Kjo krijon skedarin e databazës nëse nuk ekziston
    con = duckdb.connect('warehouse.duckdb')
    
    # Krijojmë një skemë 'raw' për të mbajtur të dhënat e papërpunuara
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    
    print("Duke lexuar skedarët Parquet dhe duke i kaluar në tabela...")
    
    # DuckDB është aq i zgjuar sa mund të lexojë direkt nga skedarët Parquet!
    # Krijojmë/Zëvendësojmë tabelën e çmimeve
    try:
        con.execute("""
            CREATE OR REPLACE TABLE raw.entsoe_prices AS 
            SELECT * FROM 'raw_data/prices_AL_*.parquet'
        """)
        print("✅ Tabela 'entsoe_prices' u ngarkua me sukses!")
    except Exception as e:
        print(f"❌ Gabim te çmimet: {e}")

    # Krijojmë/Zëvendësojmë tabelën e motit
    try:
        con.execute("""
            CREATE OR REPLACE TABLE raw.open_meteo AS 
            SELECT * FROM 'raw_data/weather_tirana_*.parquet'
        """)
        print("✅ Tabela 'open_meteo' u ngarkua me sukses!")
    except Exception as e:
        print(f"❌ Gabim te moti: {e}")

    # Le të bëjmë një query të thjeshtë SQL për të parë çfarë kemi
    print("\nPreview i 3 rreshtave të parë nga çmimet:")
    print(con.sql("SELECT * FROM raw.entsoe_prices LIMIT 3").df())
    
    con.close()

if __name__ == "__main__":
    load_data()