import json
from datetime import datetime

from streamstats.analysis import *
from streamstats.errors import *


class Report:
    '''Отчет для лог-файлов'''
    num_events: int
    num_events_by_level: dict[str, int]
    num_events_by_source: dict[str, int]
    top_5_error_critical_sources: dict[str, int]
    first_timestamp: str
    last_timestamp: str
    skipped_events: int

    def __init__(self, events: list[LogEntry], skipped_events: int):
        if(len(events) == 0):
            raise ReportError("В файлах нет правильных событий")

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

        error_critical_sources_count_list: list[tuple[str, int]] = []
        for key, value in error_critical_sources_count.items():
            error_critical_sources_count_list.append((key, value))
        error_critical_sources_count_list.sort(reverse=True, key=(lambda t : t[1]))

        self.top_5_error_critical_sources = {}
        for t in error_critical_sources_count_list[:5]:
            self.top_5_error_critical_sources[t[0]] =  t[1]

        self.first_timestamp = first_datetime.isoformat()
        self.last_timestamp = last_datetime.isoformat()

        self.skipped_events = skipped_events

    def to_json(self):
        d = {}
        d["num_events"] = self.num_events
        d["num_events_by_level"] = self.num_events_by_level
        d["num_events_by_source"] = self.num_events_by_source
        d["top_5_error_critical_sources"] = self.top_5_error_critical_sources
        d["first_timestamp"] = self.first_timestamp
        d["last_timestamp"] = self.last_timestamp
        if(self.skipped_events > 0):
            d["skipped_events"] = self.skipped_events
        
        return json.dumps(d, indent=4)

def write_report_from_files(files: list[str], format: str, output: str, skip_invalid: bool):
    '''Создает отчет из списка файлов и записывает его в файл output'''
    report = report_from_files(files, format, skip_invalid)

    with open(output, "w") as output_file:
        output_file.write(report.to_json())

def report_from_files(files: list[str], format: str, skip_invalid: bool) -> Report:
    '''Создает отчет из списка файлов'''
    events, skipped_events = read_events_from_files(files, format, skip_invalid)
    return Report(events, skipped_events)