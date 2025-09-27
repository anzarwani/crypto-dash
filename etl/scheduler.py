from apscheduler.schedulers.blocking import BlockingScheduler
from etl.extract import fetch_top_coins
from etl.transform import transform
from etl.load import load
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def etl_job():
    logging.info("Starting ETL job...")
    try:
        df = fetch_top_coins()
        df_transformed, df_anomalies = transform(df)
        load(df_transformed, df_anomalies)
        logging.info("ETL job completed successfully.")
    except Exception as e:
        logging.error(f"ETL job failed: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Run every 1 hour
    scheduler.add_job(etl_job, 'interval', minutes=60)
    logging.info("Scheduler started. ETL will run every 60 minutes.")
    scheduler.start()
