import argparse
from weather_analyzer.fetch_weather import fetch_weather
from weather_analyzer.process_data import process_weather_data
from weather_analyzer.utils import save_json_history
from weather_analyzer.db.insert_weather import insert_weather_records
from weather_analyzer.logger import get_logger
from weather_analyzer.config.settings import settings

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Weather data pipeline (API → PostgreSQL)"
    )

    parser.add_argument(
        "--cities",
        nargs="+",
        help="List of cities to fetch weather for (overrides default)"
    )

    parser.add_argument(
        "--raw-output",
        default=None,
        help="Folder path to raw JSON output files"
    )

    return parser.parse_args()


def main(cities=None, raw_output=None):
    """
    Main weather data pipeline.
    Safe, fault-tolerant, production-ready.
    """

    # If called via CLI (python -m), parse arguments
    if cities is None:
        args = parse_args()
        cities = args.cities
        raw_output = args.raw_output

    # Apply config defaults
    cities = cities or settings.CITIES
    raw_output = raw_output or "data/history/raw"

    logger.info(f"Weather pipeline started for cities: {cities}")

    raw_weather_data = []

    for city in cities:
        try:
            logger.info(f"Fetching weather for {city}")
            data = fetch_weather(city)

            if data:
                raw_weather_data.append(data)
            else:
                logger.warning(f"No data returned for {city}")

        except Exception as e:
            logger.error(f"Fatal error while processing {city}: {e}")

    if not raw_weather_data:
        logger.critical("All cities failed — pipeline aborted")
        return

    try:
        raw_file = save_json_history(raw_weather_data, raw_output)
        logger.info(f"Raw JSON snapshot saved: {raw_file}")
    except Exception as e:
        logger.warning(f"Failed to save raw JSON history: {e}")

    try:
        processed_data = process_weather_data(raw_weather_data)
    except Exception as e:
        logger.critical(f"Data processing failed: {e}")
        return

    try:
        inserted = insert_weather_records(processed_data)
        logger.info(f"{inserted} records inserted into PostgreSQL")
    except Exception as e:
        logger.critical(f"Database insertion failed: {e}")

    logger.info("Weather pipeline completed")


if __name__ == "__main__":
    main()

