import time
import requests
import os
from dotenv import load_dotenv
from weather_analyzer.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str, retries: int = 3, delay: int = 2) -> dict | None:
    """
    Fetch weather data for a city with retry logic.
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)

            if response.status_code == 200:
                logger.info(f"Weather data fetched for {city}")
                return response.json()

            logger.warning(
                f"Attempt {attempt}/{retries} failed for {city} "
                f"(status {response.status_code})"
            )

        except requests.RequestException as e:
            logger.error(
                f"Attempt {attempt}/{retries} error for {city}: {e}"
            )

        if attempt < retries:
            time.sleep(delay)

    logger.error(f"All retry attempts failed for {city}")
    return None
