import logging
from datetime import datetime

import streamstats.parsers
from streamstats.errors import *

log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
streamstats_logger = logging.getLogger("streamstats")

class LogEntry:
    '''Событие, записанное в лог'''
    line: int
    file: str
    timestamp: datetime
    level: str
    source: str
    message: str

    def __init__(self, line: int, file_name: str, entry: dict):
        self.line = line
        self.file = file_name

        timestamp_str = self.read_entry_property(entry, "timestamp", str)
        self.level = self.read_entry_property(entry, "level", str)
        self.source = self.read_entry_property(entry, "source", str)
        self.message = self.read_entry_property(entry, "message", str)
        
        try:
            self.timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError:
            raise InvalidTimestampError(f"Неправильное событие на строке {self.line} файла {self.file}: Неверная временная метка: {timestamp_str}")

        if(self.level not in log_levels):
            raise InvalidEventError(f"Неправильное событие на строке {self.line} файла {self.file}: Неправильный уровень события: {self.level}")

        if(len(self.source) == 0):
            raise InvalidEventError(f"Неправильное событие на строке {self.line} файла {self.file}: Пустой источник события")

    def read_entry_property(self, d: dict, prop: str, needed_type: type):
        '''Считывает поле события'''
        if(prop not in d):
            raise InvalidEventError(f"Неправильное событие на строке {self.line} файла {self.file}: У события отсутствует обязательное поле {prop}")
        p = d[prop]
        if(type(p) != needed_type):
            raise InvalidEventError(f"Неправильное событие на строке {self.line} файла {self.file}: Значение {p} поля {prop} неправильного типа (нужно {needed_type})")

        return p

def read_events_from_files(files: list[str], format: str, skip_invalid: bool) -> tuple[list[LogEntry], int]:
    '''Считывает события из списка файлов'''
    events: list[LogEntry] = []
    skipped_events = 0

    for fname in files:
        with open(fname) as file:
            events_here, skipped_here = streamstats.parsers.parse_file_with_format(file, fname, format, skip_invalid)
            events.extend(events_here)
            skipped_events += skipped_here

    return events, skipped_events