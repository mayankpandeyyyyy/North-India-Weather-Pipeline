import subprocess
import time
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_pipeline():
    logging.info("PIPELINE EXECUTION STARTED")
    
    try:
        logging.info("Executing Ingestion: 01_ingest.py")
        subprocess.run([sys.executable, "01_ingest.py"], check=True)
        
        logging.info("Executing Transformation: 02_transform.py")
        subprocess.run([sys.executable, "02_transform.py"], check=True)
        
        logging.info("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Pipeline failed at step: {e}")

if __name__ == "__main__":
    INTERVAL_SECONDS = 900
    
    while True:
        execute_pipeline()
        logging.info(f"System standby. Next execution in {INTERVAL_SECONDS // 60} minutes.")
        time.sleep(INTERVAL_SECONDS)