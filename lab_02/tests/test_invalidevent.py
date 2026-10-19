import pytest

from streamstats.errors import *
from streamstats.report import *


# csv
def test_csv_missingfield():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../csv_missingfield.csv"], "csv", False)

def test_csv_emptysource():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../csv_emptysource.csv"], "csv", False)

def test_csv_invalidtimestamp():
    with pytest.raises(InvalidTimestampError):
        report_from_files([f"{__file__}/../csv_invalidtimestamp.csv"], "csv", False)

def test_csv_invalidlevel():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../csv_invalidlevel.csv"], "csv", False)

# jsonl
def test_jsonl_invalidline():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../jsonl_invalidline.jsonl"], "jsonl", False)
        
def test_jsonl_wrongtype():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../jsonl_wrongtype.jsonl"], "jsonl", False)
        
def test_jsonl_missingfield():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../jsonl_missingfield.jsonl"], "jsonl", False)

def test_jsonl_emptysource():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../jsonl_emptysource.jsonl"], "jsonl", False)

def test_jsonl_invalidtimestamp():
    with pytest.raises(InvalidTimestampError):
        report_from_files([f"{__file__}/../jsonl_invalidtimestamp.jsonl"], "jsonl", False)

def test_jsonl_invalidlevel():
    with pytest.raises(InvalidEventError):
        report_from_files([f"{__file__}/../jsonl_invalidlevel.jsonl"], "jsonl", False)