from streamstats.report import *


# csv
def test_csv_success():
    report_3e = report_from_files([f"{__file__}/../csv_success_3e.csv"], "csv", False)
    assert report_3e.num_events == 3
    assert report_3e.num_events_by_level["INFO"] == 1
    assert report_3e.num_events_by_level["DEBUG"] == 2
    assert report_3e.num_events_by_source["test1"] == 1
    assert report_3e.num_events_by_source["test2"] == 1
    assert report_3e.num_events_by_source["test3"] == 1

# jsonl
def test_jsonl_success():
    report_3e = report_from_files([f"{__file__}/../jsonl_success_3e.jsonl"], "jsonl", False)
    assert report_3e.num_events == 3
    assert report_3e.num_events_by_level["INFO"] == 1
    assert report_3e.num_events_by_level["DEBUG"] == 2
    assert report_3e.num_events_by_source["test1"] == 1
    assert report_3e.num_events_by_source["test2"] == 1
    assert report_3e.num_events_by_source["test3"] == 1