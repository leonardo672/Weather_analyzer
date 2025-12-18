def process_weather_data(weather_data: list) -> list:
    """
    Convert raw OpenWeatherMap JSON data into a clean summary.
    """
    processed = []

    for item in weather_data:
        if item is None:
            continue

        city = item.get("name")
        main = item.get("main", {})

        temperature = main.get("temp")
        humidity = main.get("humidity")

        processed.append({
            "city": city,
            "temperature": temperature,
            "humidity": humidity
        })

    return processed
