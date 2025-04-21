from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from google.cloud import bigquery

project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / ".env")

client = bigquery.Client()

def _fetch_bq_dataframe(query: str) -> pd.DataFrame:
    return client.query(query).to_dataframe()

def _generate_excel(df: pd.DataFrame, file_path: Path):
    with pd.ExcelWriter(file_path) as writer:
        for ticker in df['ticker'].unique():
            sheet_df = df[df['ticker'] == ticker].copy()
            sheet_df.to_excel(writer, index=False, sheet_name=ticker[:31])  # Excel sheet names max 31 chars

def generate_both_summaries():
    # 1. Standard summary
    standard_query = """
        SELECT date, ticker, open, high, low, close, volume
        FROM stock_data.raw_stock_prices
        ORDER BY date
    """
    standard_df = _fetch_bq_dataframe(standard_query)
    standard_path = project_root / "outputs" / "stock_summary.xlsx"
    _generate_excel(standard_df, standard_path)

    # 2. Super summary (from dbt model)
    super_query = """
        SELECT *
        FROM stock_data.final_summary_table
    """
    super_df = _fetch_bq_dataframe(super_query)
    super_path = project_root / "outputs" / "stock_super_summary.xlsx"
    _generate_excel(super_df, super_path)

    return str(standard_path), str(super_path)

