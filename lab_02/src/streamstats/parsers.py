import csv
import json
from io import TextIOBase

import streamstats.analysis
from streamstats.errors import *


def parse_file_with_format(file: TextIOBase, file_name: str, format: str, skip_invalid: bool | None = False) -> tuple[list[streamstats.analysis.LogEntry], int]:
    '''Считывает события из файла с форматом format'''
    match format:
        case "jsonl":
            return parse_jsonl_file(file, file_name, skip_invalid)
        case "csv":
            return parse_csv_file(file, file_name, skip_invalid)

    raise UnsupportedFormatError(f"Неподдерживаемый формат: {format}")

def parse_jsonl_file(file: TextIOBase, file_name: str, skip_invalid: bool | None = False) -> tuple[list[streamstats.analysis.LogEntry], int]:
    '''Считывает события из JSONL файла'''
    entries: list[streamstats.analysis.LogEntry] = []
    skipped_events: int = 0

    for line_number,line in enumerate(file, start=1):
        try:
            try:
                j: dict = json.loads(line)
                entry = streamstats.analysis.LogEntry(line_number, file_name, j)
                entries.append(entry)
            except json.JSONDecodeError as e:
                raise InvalidEventError(f"Неправильное событие на строке {line_number} файла {file_name}: {e.msg}")
        except (ValueError, StreamStatsError) as e:
            if(skip_invalid):
                skipped_events += 1
                streamstats.analysis.streamstats_logger.warning(e)
            else:
                raise

    return entries, skipped_events

def parse_csv_file(file: TextIOBase, file_name: str, skip_invalid: bool | None = False) -> tuple[list[streamstats.analysis.LogEntry], int]:
    '''Считывает события из CSV файла'''
    entries: list[streamstats.analysis.LogEntry] = []
    skipped_events: int = 0
    
    for line_number,row in enumerate(csv.DictReader(file),start=2):
        try:
            entry = streamstats.analysis.LogEntry(line_number, file_name, row)
            entries.append(entry)
        except (ValueError, StreamStatsError) as e:
            if(skip_invalid):
                skipped_events += 1
                streamstats.analysis.streamstats_logger.warning(e)
            else:
                raise

    return entries, skipped_events