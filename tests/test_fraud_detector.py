
# from src.fraud_detector import detect_fraud_risk


# def test_low_credit_score_is_flagged():
#     event = {
#         "application_id": "APP001",
#         "applicant_age": 30,
#         "loan_amount": 100000,
#         "annual_income": 500000,
#         "credit_score": 450,
#     }

#     result = detect_fraud_risk(event)

#     assert result["risk_flag"] is True
#     assert "Low credit score" in result["risk_reasons"]


# def test_normal_application_is_not_flagged():
#     event = {
#         "application_id": "APP002",
#         "applicant_age": 30,
#         "loan_amount": 100000,
#         "annual_income": 500000,
#         "credit_score": 750,
#     }

#     result = detect_fraud_risk(event)

#     assert result["risk_flag"] is False
#     assert result["risk_reasons"] == []

# from src.fraud_detector import detect_fraud_risk


# def test_low_credit_score_is_flagged():
#     event = {
#         "application_id": "APP001",
#         "applicant_age": 30,
#         "loan_amount": 100000,
#         "annual_income": 500000,
#         "credit_score": 450,
#     }

#     result = detect_fraud_risk(event)

#     assert result["risk_flag"] is True
#     assert "Low credit score" in result["risk_reasons"]


# def test_normal_application_is_not_flagged():
#     event = {
#         "application_id": "APP002",
#         "applicant_age": 30,
#         "loan_amount": 100000,
#         "annual_income": 500000,
#         "credit_score": 750,
#     }

#     result = detect_fraud_risk(event)

#     assert result["risk_flag"] is False
#     assert result["risk_reasons"] == []

from src.pipeline import load_processed_event_ids
from src.pipeline import is_duplicate_event
from src.fraud_detector import detect_fraud_risk, validate_loan_event


def make_valid_event():
    return {
        "event_id": "EVT001",
        "event_timestamp": "2026-10-24T12:00:00+00:00",
        "application_id": "APP001",
        "source": "website",
        "applicant_age": 30,
        "loan_amount": 100000,
        "annual_income": 500000,
        "credit_score": 750,
    }


def test_low_credit_score_is_flagged():
    event = make_valid_event()
    event["credit_score"] = 450

    result = detect_fraud_risk(event)

    assert result["risk_flag"] is True
    assert "Low credit score" in result["risk_reasons"]


def test_normal_application_is_not_flagged():
    event = make_valid_event()

    result = detect_fraud_risk(event)

    assert result["risk_flag"] is False
    assert result["risk_reasons"] == []


def test_valid_event_passes_validation():
    event = make_valid_event()

    is_valid, error = validate_loan_event(event)

    assert is_valid is True
    assert error is None


def test_missing_field_fails_validation():
    event = make_valid_event()
    del event["credit_score"]

    is_valid, error = validate_loan_event(event)

    assert is_valid is False
    assert "Missing required field" in error


def test_invalid_credit_score_fails_validation():
    event = make_valid_event()
    event["credit_score"] = 900

    is_valid, error = validate_loan_event(event)

    assert is_valid is False
    assert "Credit score" in error


def test_zero_loan_amount_fails_validation():
    event = make_valid_event()
    event["loan_amount"] = 0

    is_valid, error = validate_loan_event(event)

    assert is_valid is False
    assert "Loan amount" in error


def test_negative_annual_income_fails_validation():
    event = make_valid_event()
    event["annual_income"] = -1000

    is_valid, error = validate_loan_event(event)

    assert is_valid is False
    assert "Annual income" in error

from src.pipeline import is_duplicate_event


def test_duplicate_event_is_detected():
    processed_event_ids = set()

    assert is_duplicate_event("EVT001", processed_event_ids) is False
    assert is_duplicate_event("EVT001", processed_event_ids) is True

def test_non_dictionary_event_fails_validation():
    is_valid, error = validate_loan_event(None)

    assert is_valid is False
    assert error == "Event must be a dictionary"
def test_applicant_age_below_18_fails_validation():
    event = make_valid_event()
    event["applicant_age"] = 17

    is_valid, error = validate_loan_event(event)

    assert is_valid is False
    assert error == "Applicant age must be between 18 and 100"

def test_load_processed_event_ids(tmp_path, monkeypatch):
    ids_file = tmp_path / "processed_event_ids.jsonl"
    ids_file.write_text(
        '{"event_id": "EVT001"}\n'
        '{"event_id": "EVT002"}\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "src.pipeline.PROCESSED_IDS_FILE",
        ids_file,
    )

    processed_ids = load_processed_event_ids()

    assert processed_ids == {"EVT001", "EVT002"}

def test_load_processed_event_ids_skips_malformed_records(tmp_path, monkeypatch):
    ids_file = tmp_path / "processed_event_ids.jsonl"
    ids_file.write_text(
        '{"event_id": "EVT001"}\n'
        'this is not valid JSON\n'
        '{"event_id": "EVT002"}\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "src.pipeline.PROCESSED_IDS_FILE",
        ids_file,
    )

    processed_ids = load_processed_event_ids()

    assert processed_ids == {"EVT001", "EVT002"}