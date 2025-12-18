import requests

API_KEY = "66822a805f6c28b287931c9b5cb0febb"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str) -> dict | None:
    """
    Fetch weather data for a single city.
    Returns JSON dict if successful, otherwise None.
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None
