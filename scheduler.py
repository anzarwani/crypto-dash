from http.server import HTTPServer, BaseHTTPRequestHandler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

from etl.extract import fetch_top_coins
from etl.transform import transform
from etl.load import load

# --- Configure logging ---
logging.basicConfig(level=logging.INFO)

# --- ETL Job ---
def etl_job():
    logging.info(f"ETL job started at {datetime.utcnow()}")
    try:
        data = fetch_top_coins()
        transformed_data = transform(data)
        load(transformed_data)
        logging.info("ETL job completed successfully.")
    except Exception as e:
        logging.error(f"ETL job failed: {e}")

# --- Start APScheduler ---
scheduler = BackgroundScheduler()
scheduler.add_job(etl_job, 'interval', minutes=60, id="etl_job")
scheduler.start()
logging.info("Scheduler started. ETL will run every 60 minutes.")

# Minimal HTTP server to fake a port on render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ETL Worker Running!")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 10000), Handler)  # port 10000
    print("Listening on port 10000.")
    server.serve_forever()
