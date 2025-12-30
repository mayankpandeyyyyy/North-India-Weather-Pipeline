import time
import subprocess

def run_job():
    print(f"\n🚀 Starting Pipeline at {time.ctime()}")
    
    print("Step 1: Ingesting...")
    subprocess.run(["python3", "01_ingest.py"])
    
    print("Step 2: Transforming...")
    subprocess.run(["python3", "02_transform.py"])
    
    print("✅ Cycle Complete. Waiting 10 minutes...")

while True:
    run_job()
    time.sleep(600) # Wait 10 mins (600 seconds)