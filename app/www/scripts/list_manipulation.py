import csv
import os


def _fruits_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "csv", "fruits.csv")


def _read_fruits():
    with open(_fruits_csv_path(), mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def upload_fruits(body=None):
    return _read_fruits()


def count_fruit(body):
    target = body
    count = sum(1 for row in _read_fruits() if row["fruit"] == target)
    return {"fruit": target, "count": count}
