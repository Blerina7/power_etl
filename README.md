# Balkan Power Prices - End-to-End ELT Pipeline

**Project Bio:** An automated ELT pipeline that ingests hourly electricity prices, load, generation mix, and weather data for Albania and neighbouring SEE countries, transforms it with dbt, and serves it through an analytics dashboard.


---

## Architecture

```text
ENTSO-E API ──┐
              ├─> Python Ingestion -> Raw Parquet (data/raw)
Open-Meteo ───┘                              |
                                             v
                          Airflow (daily schedule, retries, alerts)
                                             |
                                             v
                    dbt: staging -> intermediate -> marts
                                             |
                                             v
                                    DuckDB Warehouse
                                             |
                                             v
                                  Streamlit Dashboard
```

---

## Tech Stack

* **Ingestion:** Python, `entsoe-py`, `requests`, `pandas`, `pyarrow`
* **Orchestration:** Apache Airflow
* **Transformation:** dbt (`dbt-duckdb`)
* **Warehouse:** DuckDB
* **Dashboard:** Streamlit
* **Infrastructure:** Docker, Docker Compose, GitHub Actions

---

## Data Sources

| Source | Data | Access |
|--------|------|--------|
| **ENTSO-E Transparency Platform** | Day-ahead prices, load, generation by source | Free API token required |
| **Open-Meteo** | Temperature, wind, solar radiation | Free, no token |

**Countries covered:** Albania, Greece, Italy, Montenegro, North Macedonia (configurable).

---

## Project Structure

```text
balkan-power-prices/
├── ingestion/              # Python scripts to fetch and store raw data
│   ├── entsoe_client.py
│   └── weather_client.py
├── orchestration/
│   └── dags/               # Airflow DAGs
├── dbt/
│   ├── models/
│   │   ├── staging/        # Cleaned, typed raw data
│   │   ├── intermediate/   # Joins and business logic
│   │   └── marts/          # Fact and dimension tables
│   └── tests/              # Data quality tests
├── dashboard/
│   └── app.py              # Streamlit app
├── docker/                 # Dockerfiles
├── docs/                   # Architecture diagram, design decisions
├── data/                   # Raw Parquet files (git-ignored)
├── .github/workflows/      # CI/CD
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Data Model

### Fact Tables

* **`fact_price_hourly`** - hourly day-ahead price per country
* **`fact_generation_hourly`** - hourly generation by source type
* **`fact_load_hourly`** - hourly electricity load

### Dimension Tables

* **`dim_country`** - country codes, names, bidding zones
* **`dim_time`** - date, hour, weekday, season
* **`dim_source`** - generation source (hydro, solar, wind, gas, etc.)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/balkan-power-prices.git
cd balkan-power-prices
```

### 2. Get an ENTSO-E API Token

Register at the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/), then request **Restful API access** via their support to receive your token.

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your token:

```text
ENTSOE_API_KEY=your_token_here
```

### 4. Start the Stack

```bash
docker compose up -d
```

---

## Usage

### Run the Pipeline via Airflow

Open the Airflow UI at `http://localhost:8080` and trigger the `power_prices_daily` DAG.

### Run Ingestion Manually

```bash
python -m ingestion.entsoe_client --start 2024-01-01 --end 2024-01-31
```

### Run dbt Transformations and Tests

```bash
cd dbt
dbt run
dbt test
dbt docs generate && dbt docs serve
```

### Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Data Quality

Automated checks run on every pipeline execution:

* **Not null:** no missing timestamps or country codes
* **Range checks:** prices and load within realistic bounds
* **Uniqueness:** one record per country per hour
* **Freshness:** alert if new data stops arriving

If a test fails, the pipeline stops and an alert is raised.

---

## CI/CD

GitHub Actions runs on every push:

1. **Lint:** code style checks
2. **dbt tests:** validate models on sample data
3. **Build:** verify Docker images build successfully

---

## Roadmap

* [ ] Ingestion for ENTSO-E and Open-Meteo
* [ ] Airflow DAG with retries and alerts
* [ ] dbt staging and marts with tests
* [ ] Streamlit dashboard
* [ ] CI/CD with GitHub Actions
* [ ] Real-time streaming with Kafka
* [ ] Price forecasting model
* [ ] Cloud deployment with Terraform

---

## Common Issues

* **"401 Unauthorized" from ENTSO-E:** Check that your token is correct and that Restful API access was activated.
* **"No data returned":** Some countries or time ranges have gaps in ENTSO-E. Try another range or country.
* **"Port already in use":** Change the port mapping in `docker-compose.yml`.
* **"Airflow DAG not showing":** Wait a minute for the scheduler to refresh, then check `docker compose logs airflow`.

---

## License

MIT
