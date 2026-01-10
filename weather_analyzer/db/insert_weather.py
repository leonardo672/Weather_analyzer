import time
import psycopg2
from psycopg2.extras import execute_batch
from weather_analyzer.logger import get_logger
from weather_analyzer.config.settings import settings

logger = get_logger(__name__)


def insert_weather_records(records: list[dict]) -> int:
    """
    Insert processed weather records into PostgreSQL with
    retries, transaction safety, and partial failure tolerance.
    Ensures the logger reports the **actual inserted rows**,
    ignoring duplicates handled by ON CONFLICT DO NOTHING.
    """

    if not records:
        logger.warning("No records to insert into DB")
        return 0

    db_config = {
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "dbname": settings.DB_NAME,
        "user": settings.DB_USER,
        "password": settings.DB_PASSWORD,
        "connect_timeout": 10,
    }

    sql = """
        INSERT INTO weather_summary (city, temperature, humidity, fetched_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (city, fetched_at) DO NOTHING
    """

    values = [
        (
            row["city"],
            row["temperature"],
            row["humidity"],
            row["fetched_at"],
        )
        for row in records
    ]

    for attempt in range(1, settings.DB_RETRIES + 1):
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as cur:
                    # Capture row count **before insertion**
                    cur.execute("SELECT COUNT(*) FROM weather_summary;")
                    before_count = cur.fetchone()[0]

                    execute_batch(cur, sql, values, page_size=50)

                    # Capture row count **after insertion**
                    cur.execute("SELECT COUNT(*) FROM weather_summary;")
                    after_count = cur.fetchone()[0]

                    inserted = after_count - before_count

                    logger.info(f"{inserted} records inserted into PostgreSQL")
                    return inserted

        except psycopg2.OperationalError as e:
            logger.warning(
                f"DB connection attempt {attempt}/{settings.DB_RETRIES} failed: {e}"
            )

        except psycopg2.DatabaseError as e:
            logger.error(f"Database error: {e}")
            break  # Do NOT retry on corrupted SQL or schema errors

        # Exponential backoff
        time.sleep(2 ** attempt)

    logger.critical("Database permanently unavailable — records not inserted")
    return 0
