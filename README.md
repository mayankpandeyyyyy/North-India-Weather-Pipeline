# North India Weather Intelligence Pipeline 

### The Project Goal
I built this project to move beyond simple "weather fetching." My goal was to take live API data from 30+ cities across North India (UP, Punjab, Uttarakhand, etc.) and translate those raw numbers into something useful for local businesses—like predicting when fog will hit logistics or when the power grid in the hills will face high demand.

## How it works (Medallion Architecture)
I followed the Medallion framework to keep the data clean and reliable:
- **Bronze (The Raw Stuff):** I fetch JSON data from OpenWeatherMap and store it exactly as it is. No changes, just a backup of the truth.
- **Silver (The Clean-up):** I use PySpark to enforce a strict schema. This is where I convert Kelvin to Celsius and drop any "junk" data that might break the app.
- **Gold (The Logic):** This is the final layer where I run my business logic. I aggregate the data into Parquet files that are fast enough for the dashboard to read instantly.

## What makes this "Intelligence" and not just "Data"?
Instead of just showing "Temperature: 6°C," I added a feature engineering layer that calculates:
- **Logistics Risk:** If humidity is high and temps are low, the dashboard flags a Fog Warning. This is critical for transport companies in the plains.
- **Grid Load Alerts:** Based on extreme temps, I categorize cities into "High Heating" or "High Cooling" zones to simulate how a power utility company would monitor the grid.

## Tech I Used
- **Big Data:** PySpark (for the heavy lifting in transformations)
- **Engine:** Python 3.12 & Pandas
- **UI:** Streamlit & Plotly (for the interactive bits)
- **Infrastructure:** Ubuntu on WSL

## To get it running
1. Throw your OpenWeatherMap API key into `01_ingest.py`.
2. Run `python3 orchestrator.py` to trigger the whole flow.
3. Launch the UI: `streamlit run 04_dashboard.py`.
