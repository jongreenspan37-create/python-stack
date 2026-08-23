import os
import csv

def _fruits_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "csv", "fruits.csv")


def _read_fruits():
    with open(_fruits_csv_path(), mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))
