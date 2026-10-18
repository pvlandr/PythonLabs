
from streamstats.errors import *
from streamstats.parsers import *
from streamstats.report import *


def analyze_files(files: list[str], format: str, output: str, skip_invalid: bool):
    events: list[LogEntry] = []

    for fname in files:
        with open(fname) as file:
            events_here = parse_file_with_format(file, format, skip_invalid)
            events.extend(events_here)

    report = Report(events)
    with open(output, mode="w") as f:
        f.write(report.to_json())