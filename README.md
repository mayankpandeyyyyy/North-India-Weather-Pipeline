# North India Weather Pipeline: Medallion Architecture

An automated data engineering pipeline designed to ingest, process, and visualize real-time weather metrics for Northern Indian states including Uttar Pradesh, Punjab, Haryana, Himachal, and Uttarakhand. This project implements a modular Medallion Architecture to maintain data integrity from raw ingestion to final insights.



## Data Strategy (Medallion Framework)

The pipeline is organized into three distinct layers to ensure scalability and data quality:

- Bronze (Raw): Ingests live JSON payloads from the OpenWeatherMap API. Data is stored in its original form to allow for historical reprocessing.
- Silver (Cleaned): Leverages PySpark to handle schema enforcement, type casting (e.g., converting Kelvin to Celsius), and removing null values or outliers.
- Gold (Curated): Aggregates the cleaned data into optimized Parquet files. This layer is structured specifically for the Streamlit dashboard to ensure sub-second query performance.

## Tech Stack and Environment

- Infrastructure: Ubuntu on WSL (Windows Subsystem for Linux)
- Processing: Apache Spark (PySpark) for ETL operations
- Language: Python 3.12
- Frontend: Streamlit for the interactive data portal
- Storage: Parquet (Columnar storage for efficient read operations)

## System Components

1. 01_ingest.py: Handles API communication and raw storage in the Bronze layer.
2. 02_transform.py: The Spark engine that converts Raw to Silver to Gold.
3. 04_dashboard.py: A lightweight UI providing state-specific meteorological reports.
4. orchestrator.py: A central script to trigger the entire pipeline end-to-end.

## Dashboard Access

The dashboard allows users to select specific states to view a sequential, cleaned table of local weather data, including Temperature, Humidity, and Wind Speeds.

---

Note: To run this project locally, you will need an OpenWeatherMap API key and a configured Spark environment on WSL.
