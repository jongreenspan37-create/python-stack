# Reads csv/fruits.csv. The leading _ in the names means "internal helper".
import os
import csv

# Full path to fruits.csv, built from this file's own folder so it works
# whatever directory the server was started from.
def _fruits_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "csv", "fruits.csv")


# DictReader uses the header row as keys, so each row is {"id": "1", "fruit": "melon"}.
# Values are always strings (CSV has no types). `with` closes the file automatically.
def _read_fruits():
    with open(_fruits_csv_path(), mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))
