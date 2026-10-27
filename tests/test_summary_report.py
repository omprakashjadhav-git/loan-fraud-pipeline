
import csv
import json

from src import summary_report


def test_generate_summary_creates_correct_csv(tmp_path, monkeypatch, capsys):
    results_file = tmp_path / "screening_results.jsonl"
    report_file = tmp_path / "summary_report.csv"

    records = [
        {
            "screening_result": {
                "application_id": "APP001",
                "risk_flag": True,
            }
        },
        {
            "screening_result": {
                "application_id": "APP002",
                "risk_flag": False,
            }
        },
        {
            "screening_result": {
                "application_id": "APP003",
                "risk_flag": True,
            }
        },
    ]

    with results_file.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

    monkeypatch.setattr(summary_report, "RESULTS_FILE", results_file)
    monkeypatch.setattr(summary_report, "REPORT_FILE", report_file)

    summary_report.generate_summary()

    with report_file.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    assert rows[0] == ["Metric", "Count"]
    assert rows[1] == ["Total applications processed", "3"]
    assert rows[2] == ["Applications flagged for risk", "2"]
    assert rows[3] == ["Applications not flagged", "1"]
    assert rows[4] == ["Malformed records skipped", "0"]

    output = capsys.readouterr().out
    assert "Total applications processed: 3" in output

def test_generate_summary_skips_malformed_records(
    tmp_path, monkeypatch, capsys
):
    results_file = tmp_path / "screening_results.jsonl"
    report_file = tmp_path / "summary_report.csv"

    results_file.write_text(
        '{"screening_result": {"risk_flag": true}}\n'
        'this is not valid JSON\n'
        '{"screening_result": {"risk_flag": false}}\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(summary_report, "RESULTS_FILE", results_file)
    monkeypatch.setattr(summary_report, "REPORT_FILE", report_file)

    summary_report.generate_summary()

    output = capsys.readouterr().out

    assert "Total applications processed: 2" in output
    assert "Applications flagged for risk: 1" in output
    assert "Applications not flagged: 1" in output
    assert "Malformed records skipped: 1" in output

def test_generate_summary_handles_missing_input_file(
    tmp_path, monkeypatch, capsys
):
    results_file = tmp_path / "missing_screening_results.jsonl"
    report_file = tmp_path / "summary_report.csv"

    monkeypatch.setattr(summary_report, "RESULTS_FILE", results_file)
    monkeypatch.setattr(summary_report, "REPORT_FILE", report_file)

    summary_report.generate_summary()

    output = capsys.readouterr().out

    assert "Error: Screening results file not found:" in output
    assert not report_file.exists()