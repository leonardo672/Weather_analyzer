import os
import csv
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from weather_analyzer.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "history" / "weather_summary.csv"


def load_csv():
    logger.info("Connecting to PostgreSQL")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    logger.info(f"Loading {len(rows)} rows into database")

    for row in rows:
        cur.execute(
            """
            INSERT INTO weather_summary (city, temperature, humidity, fetched_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                row["city"],
                row["temperature"],
                row["humidity"],
                row["fetched_at"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

    logger.info("CSV successfully loaded into PostgreSQL")


if __name__ == "__main__":
    load_csv()
