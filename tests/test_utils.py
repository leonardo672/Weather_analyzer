import json
from pathlib import Path
from weather_analyzer.utils import save_json_history


def test_save_json_creates_file(tmp_path):
    data = {"city": "London"}

    # pass a FOLDER, not a file
    folder = tmp_path / "history"

    file_path = save_json_history(data, folder)

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data
