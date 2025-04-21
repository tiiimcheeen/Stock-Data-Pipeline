# 📊 Stock Data Pipeline

This project showcases a modern data engineering pipeline that automates the daily ingestion, transformation, validation, and reporting of stock price data. It is designed to demonstrate key data engineering concepts such as orchestration, ELT design, data quality checks, and analytics workflow automation.

---

## 🚀 Key Features

- **Daily Scheduling with Dagster**  
  Automatically fetches and uploads stock data to BigQuery every morning at 8am EST.

- **Data Ingestion & Storage**  
  Uses `yfinance` to retrieve historical stock data for multiple tickers. Data is stored in a BigQuery table (`raw_stock_prices`).

- **Data Validation**  
  Runs checks to ensure data freshness and completeness before downstream steps.

- **Transformation with dbt**  
  Models include:
  - `average_price_by_day`
  - `volatility_7d`
  - `weekly_aggregates`
  - `final_summary_table`

- **Automated Email Reporting**  
  Generates and sends an Excel summary with key stats (date range, row counts, averages) to a designated recipient via Gmail API.

---

## 🛠️ Tech Stack

- **Orchestration**: Dagster
- **Data Ingestion**: Python, yfinance
- **Cloud Storage**: Google BigQuery
- **Transformations**: dbt (BigQuery adapter)
- **Validation & Reporting**: Pandas, openpyxl
- **Notification**: Gmail API (token auth)

---

## 📁 Project Structure

```
stock_project/
│
├── stock_pipeline/              # Dagster logic
│   └── resources/
│       ├── __init__.py
│       ├── dbt.py               # dbt resource config
│       ├── dbt_ops.py           # runs dbt models via Dagster
│       ├── fetch_job.py         # orchestrates the full pipeline
│       ├── schedules.py         # schedule config for Dagster
│       ├── email_utils.py       # Gmail API email logic
│       ├── summary_utils.py     # Excel summary generation
│       └── validate.py          # basic data quality check
│
├── stock_dbt/                   # dbt transformation logic
│   ├── models/                  # core dbt models (SQL)
│   ├── macros/                  # reusable SQL macros (optional)
│   ├── seeds/                   # CSV seed files (if any)
│   ├── snapshots/               # dbt snapshots (if used)
│   ├── tests/                   # dbt tests
│   ├── dbt_project.yml          # dbt project config
│   ├── .gitignore
│   └── README.md
│
├── .env                         # Local environment variables
├── pyproject.toml               # Dagster entrypoint
├── requirements.txt             # Python dependencies
└── README.md                    # Project description (this file)
```

---

## 📌 How to Run Locally

1. Create and activate a virtual environment
2. Install dependencies  
   `pip install -r requirements.txt`
3. Set up `.env` with BigQuery & Gmail credentials
4. Run job locally:  
   `dagster job execute -m stock_pipeline -j fetch_job`
5. (Optional) Launch Dagster UI:  
   `dagster dev`

---

## 📬 Example Output

- Stock data uploaded to BigQuery: `stock_data.raw_stock_prices`
- Email received with Excel summary:
  - Sheet 1: Standard Summary
  - Sheet 2: dbt Final Model Summary



