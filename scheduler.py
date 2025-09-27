from prefect import flow, task
from etl.extract import fetch_top_coins
from etl.transform import transform
from etl.load import load
import logging

# --- Configure logging ---
logging.basicConfig(level=logging.INFO)

# --- Prefect Tasks ---
@task(name="Extract Top Coins", retries=3, retry_delay_seconds=30)
def extract_task():
    logging.info("Starting extraction")
    df = fetch_top_coins()
    if df.empty:
        logging.warning("No data fetched from API.")
    return df

@task(name="Transform Data")
def transform_task(df):
    logging.info("Starting transformation")
    df_transformed, df_anomalies = transform(df)
    logging.info(f"Transformed {len(df_transformed)} rows, found {len(df_anomalies)} anomalies")
    return df_transformed, df_anomalies

@task(name="Load Data")
def load_task(df_transformed, df_anomalies):
    logging.info("Starting load into Supabase")
    load(df_transformed, df_anomalies)
    logging.info("Load complete")

# --- Prefect Flow ---
@flow(name="Crypto ETL Flow")
def crypto_etl_flow():
    df = extract_task()
    df_transformed, df_anomalies = transform_task(df)
    load_task(df_transformed, df_anomalies)

if __name__ == "__main__":
    crypto_etl_flow()
