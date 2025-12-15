import logging
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


def setup_logger(level=logging.DEBUG):
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s'
    ))
    
    logging.basicConfig(
        level=level,
        handlers=[
            console_handler, 
        ],
        force=True
    )
    
    # Silence noisy third-party libraries
    logging.getLogger('botocore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('boto3').setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("pydub.converter").setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    print(f"✅ Logging enabled (level={level}) - Console")    