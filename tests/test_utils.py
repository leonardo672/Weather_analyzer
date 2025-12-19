import json
from pathlib import Path
from utils import save_json


def test_save_json_creates_file(tmp_path):
    data = {"city": "London"}
    file_path = tmp_path / "test.json"

    save_json(data, file_path)

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data
