# 🌬️ Airflow ETL Pipeline with Postgres & API Integration

This project builds an **ETL (Extract, Transform, Load) data pipeline** using **Apache Airflow** to pull data from an external **REST API**, transform it in Python and load it into a **PostgreSQL** database.

The goal is to demonstrate how to orchestrate a real-world pipeline end-to-end:
- Schedule and monitor workflows with Airflow  
- Extract JSON data from an API (e.g. NASA APOD)  
- Transform the response into a clean tabular format  
- Load it into Postgres for analytics and reporting  

---

## 🎯 Objectives

- Use **Apache Airflow** to orchestrate an ETL workflow.
- Extract data from an external HTTP API on a schedule.
- Transform raw JSON into a structured format using Python.
- Load the cleaned data into a **Postgres** table.
- Run the full stack in **Docker** for easy local development.

---

## 🏗️ High-Level Architecture

1. **Airflow DAG**
   - Defines the ETL workflow and task dependencies.
   - Schedules the pipeline (for example, once per day).

2. **API Extraction**
   - Calls an external REST API endpoint (e.g. NASA APOD).
   - Stores the raw response for downstream processing.

3. **Transformation**
   - Parses the JSON payload.
   - Selects and renames fields.
   - Handles basic type casting and data cleaning.

4. **Load to Postgres**
   - Creates the target table if it does not exist.
   - Inserts or upserts the cleaned records.
   - Data becomes available for BI tools or analytics.

---

## 🧰 Tech Stack

- **Apache Airflow** – Workflow orchestration
- **PostgreSQL** – Target database for the ETL pipeline
- **Python** – Transformation logic and tasks
- **Docker / Docker Compose** – Local containerized environment
- **Airflow Providers** – Hooks & operators for HTTP and Postgres

---

## 📁 Project Structure

> Adjust this section if your folder names differ, but this is a common layout.

```text
Airflow-ETL-Pipeline-with-Postgres-and-API-Integration/
│
├── dags/                     # Airflow DAGs and ETL logic
│   └── etl_api_to_postgres_dag.py
│
├── tests/
│   └── dags/                 # (Optional) DAG tests
│
├── docker-compose.yml        # Airflow + Postgres services
├── Dockerfile                # Image for Airflow worker/webserver
├── requirements.txt          # Python / Airflow dependencies
├── .env                      # Environment variables (API key, DB creds)
└── README.md
⚙️ Getting Started
1. Prerequisites
Docker & Docker Compose installed

Python 3.x (if you want to run anything locally outside Docker)

Optional but useful:

curl or a REST client to test the API

A SQL client (DBeaver, psql, etc.) to inspect Postgres

2. Clone the repository

git clone https://github.com/yaminideconda/Airflow-ETL-Pipeline-with-Postgres-and-API-Integration.git
cd Airflow-ETL-Pipeline-with-Postgres-and-API-Integration
3. Configure environment variables
Create a .env file in the project root (or update the one provided) with values similar to:

# API configuration
API_BASE_URL=https://api.nasa.gov/planetary/apod
API_KEY=<YOUR_API_KEY>

# Postgres configuration (must match docker-compose.yml)
POSTGRES_DB=etl_db
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Airflow basics
AIRFLOW__CORE__LOAD_EXAMPLES=False
Update the keys and DB values as needed for your environment.

4. Start Airflow and Postgres with Docker
From the project root:

docker compose up -d
This will:

Start the Airflow webserver, scheduler and worker

Start the Postgres database

Mount the dags/ folder into the Airflow container

Once the services are up:

Open the Airflow UI at: http://localhost:8080

Default credentials (if using standard config):

Username: airflow

Password: airflow

5. Configure Airflow Connections (if required)
In the Airflow UI:

Go to Admin → Connections.

Create or update:

HTTP connection for the API

Conn ID: api_http_default (or match what your DAG expects)

Host: https://api.nasa.gov (or your API base)

Postgres connection

Conn ID: postgres_default

Host: postgres

Schema: etl_db

Login: airflow

Password: airflow

Port: 5432

Adjust names and values to match your actual DAG code.

6. Trigger the DAG
In the Airflow UI:

Locate the DAG, e.g. etl_api_to_postgres.

Turn the toggle to ON to enable scheduling.

Click Trigger DAG to run it manually.

You can monitor:

Graph view – the ETL tasks (create table, extract, transform, load)

Logs – to debug failures

Postgres DB – to verify rows were loaded correctly

🧩 DAG Overview
A typical DAG in this project includes tasks such as:

create_table

Ensures the target Postgres table exists.

extract_api_data

Calls the external API and stores the response (raw JSON).

transform_data

Cleans and reshapes the JSON into rows/columns.

load_to_postgres

Inserts the transformed data into the Postgres table.

The DAG can be scheduled to run daily to collect new data over time.

💡 Possible Enhancements
Add data quality checks (row counts, null checks).

Implement idempotent loads (upsert logic, deduplication).

Parameterize the date range or API parameters for backfilling.

Add tests under tests/dags/ to validate DAG integrity.

Expose Postgres data to a BI tool (e.g. Power BI, Tableau or Metabase).

🧾 Author
Yamini Deconda
Data Engineer · ETL & Orchestration · Apache Airflow · Postgres
