from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime, timedelta

# Load environment variables
project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / ".env")

PROJECT_ID = os.getenv("BQ_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")
TABLE = os.getenv("BQ_TABLE")

client = bigquery.Client()
table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"

# Define a basic validation function
def validate_data():
    """
    Fetches data from the BigQuery table within the last LOOKBACK_DAYS,
    and checks for common data issues. Returns True if clean, False if issues found.
    """

    start_date = (datetime.utcnow() - timedelta(days=int(os.getenv("LOOKBACK_DAYS", "30")))).date()

    query = f"""
        SELECT * FROM `{table_ref}`
        WHERE DATE(date) >= '{start_date}'
    """
    df = client.query(query).to_dataframe()

    issues = []

    # 1. Missing values in critical columns
    for col in ["date", "open", "close", "high", "low", "ticker"]:
        if df[col].isnull().any():
            issues.append(f"Missing values in column: {col}")

    # 2. Negative or zero prices
    for col in ["open", "close", "high", "low"]:
        if (df[col] <= 0).any():
            issues.append(f"Non-positive values in column: {col}")

    # 3. Duplicate rows
    if df.duplicated(subset=["date", "ticker"]).any():
        issues.append("Duplicate (date, ticker) rows found")

    # 4. Suspicious high-low spreads
    df["spread"] = df["high"] - df["low"]
    if (df["spread"] > df["close"] * 0.2).any():
        issues.append("Unusually large high-low spreads found")

    if issues:
        print("\n".join(issues))
        return False
    else:
        print("✅ Data passed validation.")
        return True
