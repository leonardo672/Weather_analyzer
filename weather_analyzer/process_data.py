from weather_analyzer.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


def process_weather_data(weather_data: list) -> list:
    """
    Convert raw OpenWeatherMap JSON data into a clean summary.
    """
    processed = []
    fetched_at = datetime.utcnow()

    for item in weather_data:
        if item is None:
            logger.warning("Received None weather item")
            continue

        city = item.get("name")
        main = item.get("main", {})

        if not city or not main:
            logger.warning("Incomplete weather data received")
            continue

        temperature = main.get("temp")
        humidity = main.get("humidity")

        processed.append({
            "city": item["name"],
            "temperature": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "fetched_at": fetched_at,
        })

    return processed
