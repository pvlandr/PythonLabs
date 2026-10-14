from streamstats.parsers import *

def analyze_files(files: list[str], format: str, output: str, skip_invalid: bool):
    parsed_files = []

    for fname in files:
        with open(fname) as file:
            parsed_files.append(parse_file_with_format(file, format, skip_invalid))

        