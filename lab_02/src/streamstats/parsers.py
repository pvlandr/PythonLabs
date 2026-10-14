import csv
import json
from datetime import datetime
from io import TextIOWrapper

def parse_file_with_format(file: TextIOWrapper, format: str, skip_invalid: bool | None = False):
    match format:
        case "jsonl":
            return parse_jsonl_file(file)
        case "csv":
            return parse_csv_file(file)

    raise Exception(f"Unsupported file format: {format}")

def parse_jsonl_file(file: TextIOWrapper, skip_invalid: bool | None = False):
    entries: list[dict] = []
    for line in file:
        j: dict = json.loads(line)
        entries.append(j)

    return entries

def parse_csv_file(file: TextIOWrapper, skip_invalid: bool | None = False):
    entries: list[dict] = []
    for row in csv.DictReader(file):
        entries.append()

    return entries