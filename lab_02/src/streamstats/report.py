import json
from datetime import datetime

from streamstats.errors import *

log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class LogEntry:
    def __init__(self, timestamp: datetime, level: str, source: str, message: str):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message

        if(self.level not in log_levels):
            raise InvalidEventError(f"Неправильный уровень события: {self.level}")

class Report:
    num_events: int
    num_events_by_level: dict[str, int]
    num_events_by_source: dict[str, int]
    top_5_error_critical_sources: list[str]
    first_timestamp: str
    last_timestamp: str

    def __init__(self, events: list[LogEntry]):
        self.num_events = len(events)

        self.num_events_by_level = {}
        self.num_events_by_source = {}

        first_datetime: datetime = None
        last_datetime: datetime = None

        error_critical_sources_count: dict[str, int] = {}

        for e in events:
            if(e.level not in self.num_events_by_level):
                self.num_events_by_level[e.level] = 0
            self.num_events_by_level[e.level] += 1

            if(e.source not in self.num_events_by_source):
                self.num_events_by_source[e.source] = 0
            self.num_events_by_source[e.source] += 1

            if(e.level == "ERROR") or (e.level == "CRITICAL"):
                if(e.source not in error_critical_sources_count):
                    error_critical_sources_count[e.source] = 0
                error_critical_sources_count[e.source] += 1

            if(first_datetime == None) or (e.timestamp < first_datetime):
                first_datetime = e.timestamp

            if(last_datetime == None) or (e.timestamp > last_datetime):
                last_datetime = e.timestamp

        self.first_timestamp = first_datetime.isoformat()
        self.last_timestamp = last_datetime.isoformat()

        error_critical_sources_count_list: list[tuple[str, int]] = []
        for key, value in error_critical_sources_count.items():
            error_critical_sources_count_list.append((key, value))
        error_critical_sources_count_list.sort(key=(lambda t : t[1]))

        self.top_5_error_critical_sources = []
        for t in error_critical_sources_count_list[:5]:
            self.top_5_error_critical_sources.append(t[0])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)