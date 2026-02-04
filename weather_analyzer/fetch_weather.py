import time
import requests

from weather_analyzer.logger import get_logger
from weather_analyzer.config.settings import settings

logger = get_logger(__name__)


def fetch_weather(city: str) -> dict | None:
    """
    Fetch weather data for a city with robust retry logic.

    - Uses centralized settings (timeouts, retries, API config)
    - Retries failed requests with exponential backoff
    - Returns parsed JSON on success
    - Returns None after all retries fail
    """

    params = {
        "q": city,
        "appid": settings.WEATHER_API_KEY,
        "units": settings.UNITS,
    }

    for attempt in range(1, settings.API_RETRIES + 1):
        try:
            response = requests.get(
                settings.WEATHER_API_URL,
                params=params,
                timeout=settings.REQUEST_TIMEOUT,
            )

            # HTTP-level failure
            if response.status_code != 200:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text}"
                )

            data = response.json()

            # Data integrity check
            if "main" not in data or "temp" not in data["main"]:
                raise ValueError("Malformed API response")

            logger.info(f"Weather data fetched for {city}")
            return data

        except Exception as exc:
            logger.warning(
                f"API attempt {attempt}/{settings.API_RETRIES} failed for {city}: {exc}"
            )

            # Retry if attempts remain
            if attempt < settings.API_RETRIES:
                backoff_seconds = 2 ** attempt
                time.sleep(backoff_seconds)
            else:
                logger.error(f"API permanently failed for {city}")

    return None
