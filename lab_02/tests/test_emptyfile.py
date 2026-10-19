import pytest

from streamstats.errors import *
from streamstats.report import *


# csv
def test_csv_empty():
    with pytest.raises(ReportError):
        report_from_files([f"{__file__}/../csv_empty.csv"], "csv", False)
        
def test_csv_onlyheader():
    with pytest.raises(ReportError):
        report_from_files([f"{__file__}/../csv_onlyheader.csv"], "csv", False)

# jsonl
def test_jsonl_empty():
    with pytest.raises(ReportError):
        report_from_files([f"{__file__}/../jsonl_empty.jsonl"], "jsonl", False)