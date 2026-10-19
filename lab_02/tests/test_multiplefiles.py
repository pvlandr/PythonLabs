from streamstats.report import *


# csv
def test_csv_success():
    report = report_from_files([f"{__file__}/../csv_multifile_1.csv", f"{__file__}/../csv_multifile_2.csv"], "csv", False)
    assert report.num_events == 10
    assert report.num_events_by_level["INFO"] == 1
    assert report.num_events_by_level["DEBUG"] == 5
    assert report.num_events_by_level["WARNING"] == 2
    assert report.num_events_by_level["ERROR"] == 1
    assert report.num_events_by_level["CRITICAL"] == 1
    assert report.num_events_by_source["test1"] == 1
    assert report.num_events_by_source["test2"] == 3
    assert report.num_events_by_source["test3"] == 6

# jsonl
def test_jsonl_success():
    report = report_from_files([f"{__file__}/../jsonl_multifile_1.jsonl", f"{__file__}/../jsonl_multifile_2.jsonl"], "jsonl", False)
    assert report.num_events == 11
    assert report.num_events_by_level["INFO"] == 1
    assert report.num_events_by_level["DEBUG"] == 3
    assert report.num_events_by_level["WARNING"] == 3
    assert report.num_events_by_level["ERROR"] == 3
    assert report.num_events_by_level["CRITICAL"] == 1
    assert report.num_events_by_source["test1"] == 5
    assert report.num_events_by_source["test2"] == 2
    assert report.num_events_by_source["test3"] == 4