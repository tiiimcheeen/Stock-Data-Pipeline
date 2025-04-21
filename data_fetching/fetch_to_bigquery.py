import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def run_fetch_to_bigquery():
    """
    This function handles the full ETL pipeline:
    - Delete old data in BigQuery
    - Download latest data from Yahoo Finance
    - Upload to BigQuery
    """
    # Step 1: Load environment and credentials
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(dotenv_path=project_root / ".env")

    key_path = project_root / os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(key_path.resolve())

    PROJECT_ID = os.getenv("BQ_PROJECT_ID")
    DATASET = os.getenv("BQ_DATASET")
    TABLE = os.getenv("BQ_TABLE")
    DAYS_BACK = int(os.getenv("LOOKBACK_DAYS", "30"))

    tickers_file = project_root / "tickers" / "tickers.csv"
    TICKERS = pd.read_csv(tickers_file, header=None)[0].tolist()

    start_date = datetime.today() - timedelta(days=DAYS_BACK)
    end_date = datetime.today()

    client = bigquery.Client()
    table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    # Step 2: Delete old data (if table exists)
    try:
        client.get_table(table_ref)
        print("🔁 Deleting old records in BigQuery...")

        delete_query = f"""
        DELETE FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE DATE(date) BETWEEN DATE("{start_date.date()}") AND DATE("{end_date.date()}")
          AND ticker IN UNNEST(@tickers)
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("tickers", "STRING", list(TICKERS))
            ]
        )

        client.query(delete_query, job_config=job_config).result()
        print("✅ Old records deleted.\n")

    except NotFound:
        print(f"⚠️ Table {TABLE} not found. Skipping deletion (first run?).\n")

    # Step 3: Download and format data
    all_data = []

    for symbol in TICKERS:
        print(f"📈 Fetching: {symbol}")
        df = yf.download(
            symbol,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval="1d",
            progress=False
        )

        if df.empty:
            print(f"⚠️ No data for {symbol}, skipping.\n")
            continue

        df.reset_index(inplace=True)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns.values]

        df.rename(columns=lambda x: x.strip().lower().replace(" ", "_").replace(".", ""), inplace=True)

        df["ticker"] = symbol
        df["load_timestamp"] = datetime.now(timezone.utc)

        all_data.append(df)

    # Step 4: Upload to BigQuery
    if not all_data:
        print("❌ No valid data to upload. Exiting.")
        return

    final_df = pd.concat(all_data)

    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True,
    )

    print(f"\n🚀 Uploading {len(final_df)} rows to {table_id}...")
    job = client.load_table_from_dataframe(final_df, table_id, job_config=job_config)
    job.result()
    print("✅ Upload complete.")
