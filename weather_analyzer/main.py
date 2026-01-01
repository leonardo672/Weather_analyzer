import argparse
from weather_analyzer.fetch_weather import fetch_weather
from weather_analyzer.process_data import process_weather_data
from weather_analyzer.utils import save_json_history
from weather_analyzer.db.insert_weather import insert_weather_records
from weather_analyzer.logger import get_logger

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Weather data pipeline (API → PostgreSQL)"
    )

    parser.add_argument(
        "--cities",
        nargs="+",
        required=True,
        help="List of cities to fetch weather for"
    )

    parser.add_argument(
        "--raw-output",
        default="data/history/raw",
        help="Folder path to raw JSON output files (optional archive)"
    )

    return parser.parse_args()


def main(cities=None, raw_output=None):
    """
    Main weather data pipeline.
    Can be called from CLI or programmatically (scheduler).
    """
    if cities is None:
        args = parse_args()
        cities = args.cities
        raw_output = args.raw_output
    else:
        raw_output = raw_output or "data/history/raw"

    logger.info("Weather pipeline started")

    raw_weather_data = []

    for city in cities:
        logger.info(f"Fetching weather for {city}")
        data = fetch_weather(city)
        if data:
            raw_weather_data.append(data)
        else:
            logger.warning(f"No data received for {city}")

    if not raw_weather_data:
        logger.warning("No weather data fetched — pipeline stopped")
        return

    # Optional: save raw JSON snapshot (history / debugging)
    raw_file = save_json_history(raw_weather_data, raw_output)
    logger.info(f"Raw JSON snapshot saved: {raw_file}")

    # Process API data
    processed_data = process_weather_data(raw_weather_data)

    # Insert directly into PostgreSQL
    inserted = insert_weather_records(processed_data)
    logger.info(f"{inserted} records inserted into PostgreSQL")

    logger.info("Weather pipeline completed successfully")


if __name__ == "__main__":
    main()
