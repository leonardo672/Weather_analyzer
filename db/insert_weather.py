import os
import psycopg2
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()
logger = get_logger(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def insert_weather_records(records: list[dict]) -> int:
    """
    Insert processed weather records into PostgreSQL.
    Uses ON CONFLICT DO NOTHING to prevent duplicates.
    """
    if not records:
        logger.warning("No records to insert into DB")
        return 0

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0

    for row in records:
        cur.execute(
            """
            INSERT INTO weather_summary (city, temperature, humidity, fetched_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city, fetched_at) DO NOTHING
            """,
            (
                row["city"],
                row["temperature"],
                row["humidity"],
                row["fetched_at"],
            ),
        )

        if cur.rowcount > 0:
            inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    logger.info(f"{inserted} new records inserted into PostgreSQL")
    return inserted
