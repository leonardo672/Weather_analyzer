import json
import csv
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)


def save_json(data, filepath: str) -> None:
    """
    Save Python data to a JSON file.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON data saved to {filepath}")


def save_csv(data: list, filepath: str) -> None:
    """
    Save list of dictionaries to a CSV file.
    """
    if not data:
        logger.warning("No data to save to CSV")
        return

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"CSV data saved to {filepath}")
