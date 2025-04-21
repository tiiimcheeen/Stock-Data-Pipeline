from dagster_dbt import dbt_cli_resource
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env variables (so dbt knows the BQ key path, etc.)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

dbt_resource = dbt_cli_resource.configured({
    "project_dir": str(Path(__file__).resolve().parent.parent.parent / "stock_dbt"),
    "profiles_dir": str(Path(os.getenv("USERPROFILE", "")) / ".dbt"),
})
