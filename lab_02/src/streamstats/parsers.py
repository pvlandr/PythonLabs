import csv
import json
from datetime import datetime
from io import TextIOWrapper

log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class LogEntry:
    def __init__(self, timestamp: datetime, level: str, source: str, message: str):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message

        if(self.level not in log_levels):
            raise Exception(f"Invalid log level: {self.level}")

def parse_file_with_format(file: TextIOWrapper, format: str, skip_invalid: bool | None = False) -> list[LogEntry]:
    match format:
        case "jsonl":
            return parse_jsonl_file(file)
        case "csv":
            return parse_csv_file(file)

    raise Exception(f"Unsupported file format: {format}")

def parse_jsonl_file(file: TextIOWrapper, skip_invalid: bool | None = False) -> list[LogEntry]:
    entries: list[LogEntry] = []
    for line in file:
        j: dict = json.loads(line)
        entry = parse_entry(j)
        entries.append(entry)

    return entries

def parse_csv_file(file: TextIOWrapper, skip_invalid: bool | None = False) -> list[LogEntry]:
    entries: list[LogEntry] = []
    for row in csv.DictReader(file):
        entry = parse_entry(row)
        entries.append(entry)

    return entries

def read_entry_property(d: dict, prop: str, needed_type: type):
    if(prop not in d):
        raise Exception(f"Log entry is missing the \"{prop}\" property")
    p = d[prop]
    if(type(p) != needed_type):
        raise Exception(f"Log entry property \"{prop}\" is {type(p)} instead of {needed_type}")

    return p

def parse_entry(entry: dict) -> LogEntry:
    timestamp_str = read_entry_property(entry, "timestamp", str)
    level = read_entry_property(entry, "level", str)
    source = read_entry_property(entry, "source", str)
    message = read_entry_property(entry, "message", str)

    timestamp = datetime.fromisoformat(timestamp_str)

    return LogEntry(timestamp, level, source, message)