import json
import csv
from pathlib import Path


def save_json(data, filepath: str) -> None:
    """
    Save Python data to a JSON file.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_csv(data: list, filepath: str) -> None:
    """
    Save list of dictionaries to a CSV file.
    """
    if not data:
        print("No data to save.")
        return

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
