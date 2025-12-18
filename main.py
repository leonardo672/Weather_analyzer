from fetch_weather import fetch_weather
from process_data import process_weather_data
from utils import save_json, save_csv


def main():
    cities = [
        "Stockholm",
        "London",
        "New York"
    ]

    raw_weather_data = []

    for city in cities:
        data = fetch_weather(city)
        if data:
            raw_weather_data.append(data)

    save_json(raw_weather_data, "data/raw_weather.json")

    processed_data = process_weather_data(raw_weather_data)

    save_csv(processed_data, "data/weather_summary.csv")

    print("Weather data pipeline completed successfully.")


if __name__ == "__main__":
    main()
