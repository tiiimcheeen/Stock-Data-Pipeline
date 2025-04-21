import os
from dagster import Definitions
from dagster_dbt import DbtCliResource
from .fetch_job import fetch_job
from .schedules import fetch_schedule

dbt_cli_resource = DbtCliResource(
    project_dir=os.path.join(os.getcwd(), "stock_dbt"),
    profiles_dir=os.path.expanduser("~/.dbt"),
)

defs = Definitions(
    jobs=[fetch_job],
    schedules=[fetch_schedule],
    resources={"dbt": dbt_cli_resource}
)
