from pathlib import Path

def init_project():
    project_dataset = Path("./project_dataset")
    data = Path("./data")
    for path in [project_dataset, data]:
        path.mkdir(parents=True, exist_ok=True)
