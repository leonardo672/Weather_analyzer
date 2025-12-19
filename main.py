import argparse
from fetch_weather import fetch_weather
from process_data import process_weather_data
from utils import save_json, save_csv
from logger import get_logger

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Weather data pipeline using OpenWeatherMap API"
    )

    parser.add_argument(
        "--cities",
        nargs="+",
        required=True,
        help="List of cities to fetch weather for"
    )

    parser.add_argument(
        "--output",
        default="data/weather_summary.csv",
        help="Path to output CSV file"
    )

    parser.add_argument(
        "--raw-output",
        default="data/raw_weather.json",
        help="Path to raw JSON output file"
    )

    return parser.parse_args()


def main(cities=None, output=None, raw_output=None):
    """
    Main weather data pipeline.
    Can be called from CLI or programmatically (scheduler).
    """
    if cities is None:
        args = parse_args()
        cities = args.cities
        output = args.output
        raw_output = args.raw_output
    else:
        output = output or "data/weather_summary.csv"
        raw_output = raw_output or "data/raw_weather.json"

    logger.info("Weather pipeline started")

    raw_weather_data = []

    for city in cities:
        logger.info(f"Fetching weather for {city}")
        data = fetch_weather(city)
        if data:
            raw_weather_data.append(data)
        else:
            logger.warning(f"No data received for {city}")

    save_json(raw_weather_data, raw_output)

    processed_data = process_weather_data(raw_weather_data)
    save_csv(processed_data, output)

    logger.info("Weather data pipeline completed successfully")


if __name__ == "__main__":
    main()
