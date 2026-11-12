import duckdb


def load_data():
    print("Connecting to DuckDB warehouse (warehouse.duckdb)...")

    con = duckdb.connect("warehouse.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    print("Reading Parquet files and loading them into tables...")

    try:
        con.execute("""
            CREATE OR REPLACE TABLE raw.entsoe_prices AS
            SELECT * FROM 'raw_data/prices_AL_*.parquet'
        """)
        print("Table 'entsoe_prices' loaded successfully.")
    except Exception as e:
        print(f"Error loading power prices: {e}")

    try:
        con.execute("""
            CREATE OR REPLACE TABLE raw.open_meteo AS
            SELECT * FROM 'raw_data/weather_tirana_*.parquet'
        """)
        print("Table 'open_meteo' loaded successfully.")
    except Exception as e:
        print(f"Error loading weather data: {e}")

    print("\nPreview of the first 3 rows from the prices table:")
    print(con.sql("SELECT * FROM raw.entsoe_prices LIMIT 3").df())

    con.close()


if __name__ == "__main__":
    load_data()