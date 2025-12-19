from process_data import process_weather_data


def test_process_weather_data_valid():
    raw_data = [
        {
            "name": "Stockholm",
            "main": {
                "temp": 6.5,
                "humidity": 80
            }
        }
    ]

    result = process_weather_data(raw_data)

    assert len(result) == 1
    assert result[0]["city"] == "Stockholm"
    assert result[0]["temperature"] == 6.5
    assert result[0]["humidity"] == 80


def test_process_weather_data_ignores_none():
    raw_data = [None]

    result = process_weather_data(raw_data)

    assert result == []
