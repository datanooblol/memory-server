from pathlib import Path
import duckdb
import pandas as pd

def init_project():
    project_dataset = Path("./project_dataset")
    data = Path("./data")
    for path in [project_dataset, data]:
        path.mkdir(parents=True, exist_ok=True)

def query_csv_in_duckdb(files:list[str], query)->pd.DataFrame:
    conn = duckdb.connect()
    for file in files:
        table_name = Path(file).stem  # Gets "tips" from "tips.csv"
        conn.execute(f"CREATE VIEW {table_name} AS SELECT * FROM '{file}'")
    data = conn.execute(query).df()
    conn.close()
    return data
    