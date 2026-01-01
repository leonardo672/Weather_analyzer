import json
import csv
from pathlib import Path
from datetime import datetime
from weather_analyzer.logger import get_logger

logger = get_logger(__name__)

# ---------------- JSON ----------------
def save_json(data, filepath: str) -> None:
    """
    Save Python data to a JSON file (overwrite mode).
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON data saved to {filepath}")


def save_json_history(data, folder: str = "data/history/raw") -> Path:
    """
    Save Python data to a JSON file with a timestamp to keep history.
    Each run generates a new file.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = Path(folder) / f"raw_weather_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON history saved to {file_path}")
    return file_path


# ---------------- CSV ----------------
def save_csv(data: list, filepath: str) -> None:
    """
    Save list of dictionaries to a CSV file (overwrite mode).
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


def append_csv_history(data: list, file_path: str = "data/history/weather_summary.csv") -> None:
    """
    Append processed data to a CSV file with a timestamp column.
    Keeps all historical records.
    """
    if not data:
        logger.warning("No data to append to CSV")
        return

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    file_exists = Path(file_path).exists()

    fieldnames = list(data[0].keys()) + ["fetched_at"]

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in data:
            row["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(row)

    logger.info(f"CSV data appended to {file_path}")
