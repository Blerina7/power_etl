from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'blerina',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'balkan_energy_etl_pipeline',
    default_args=default_args,
    description='Automated ELT pipeline for power prices and weather data',
    schedule_interval='@daily',
    start_date=datetime(2026, 11, 1),
    catchup=False,
) as dag:

    # Hapi 1: Ekzekutimi i skripteve të Ingestion (Entsoe & Open-Meteo) dhe pastaj Load te DuckDB
    run_etl_scripts = BashOperator(
        task_id='run_python_extraction_and_load',
        bash_command=(
            'python /opt/airflow/project/ingestion/entsoe_prices.py && '
            'python /opt/airflow/project/ingestion/open_meteo.py && '
            'python /opt/airflow/project/load/to_duckdb.py'
        ),
    )

    # Hapi 2: Ekzekutimi i dbt transformations brenda dosjes transform
    run_dbt_models = BashOperator(
        task_id='run_dbt_transformation',
        bash_command='cd /opt/airflow/project/transform && dbt run --profiles-dir .',
    )

    # Rregulli: Së pari ekzekutohet Python-i (Extract & Load), pastaj dbt (Transform)
    run_etl_scripts >> run_dbt_models