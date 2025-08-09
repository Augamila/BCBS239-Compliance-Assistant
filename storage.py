import os, json
from typing import Dict, Any

DATA_DIR = ".local_data"

def save_project(project_name: str, blob: Dict[str, Any]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, f"{project_name}.json"), "w", encoding="utf-8") as f:
        json.dump(blob, f, indent=2)

def load_project(project_name: str):
    path = os.path.join(DATA_DIR, f"{project_name}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
