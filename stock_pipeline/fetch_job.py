from dagster import job, op, In
from typing import Tuple
from stock_pipeline.email_utils import send_email
from data_fetching.fetch_to_bigquery import run_fetch_to_bigquery
from stock_pipeline.validate import validate_data
from stock_pipeline.summary_utils import generate_both_summaries
from stock_pipeline.dbt_ops import dbt_run_op

@op
def run_fetch_script_op():
    run_fetch_to_bigquery()
    return True

@op(ins={"upstream": In()})
def validate_data_op(upstream) -> bool:
    return validate_data()

@op(ins={"upstream": In()})
def generate_summary_op(upstream) -> Tuple[str, str]:
    return generate_both_summaries()

@op
def notify_success_op(validation_passed: bool, excel_paths: Tuple[str, str] = None):
    if validation_passed and excel_paths:
        body = "The daily fetch_to_bigquery job has completed successfully. Summaries attached."
        send_email(
            subject="✅ BigQuery Upload Success",
            body=body,
            attachment_path=excel_paths
        )
    else:
        body = "The job completed but failed the data quality check. Please review the logs."
        send_email(
            subject="⚠️ BigQuery Job Completed with Validation Issues",
            body=body
        )

@job
def fetch_job():
    fetch_result = run_fetch_script_op()
    dbt_result = dbt_run_op(fetch_result)
    validation_passed = validate_data_op(dbt_result)
    excel_paths = generate_summary_op(validation_passed)
    notify_success_op(validation_passed, excel_paths)

