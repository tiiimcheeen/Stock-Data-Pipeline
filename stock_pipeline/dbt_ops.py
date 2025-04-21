import os
import subprocess
from dagster import op, OpExecutionContext, In


@op(ins={"upstream": In()})
def dbt_run_op(context: OpExecutionContext, upstream):
    project_dir = os.path.join(os.getcwd(), "stock_dbt")
    profiles_dir = os.path.expanduser("~/.dbt")

    context.log.info(f"📁 Using project_dir: {project_dir}")
    context.log.info(f"📁 Using profiles_dir: {profiles_dir}")

    try:
        result = subprocess.run(
            ["dbt", "run", "--project-dir", project_dir, "--profiles-dir", profiles_dir],
            check=True,
            capture_output=True,
            text=True
        )
        context.log.info(f"✅ dbt run completed successfully:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        context.log.error(f"❌ dbt run failed:\n{e.stderr}")
        raise
