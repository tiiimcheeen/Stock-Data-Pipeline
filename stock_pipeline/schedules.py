from dagster import ScheduleDefinition
from .fetch_job import fetch_job

fetch_schedule = ScheduleDefinition(
    job=fetch_job,
    cron_schedule="0 8 * * *",  # 8am EST
    execution_timezone="US/Eastern"
)
