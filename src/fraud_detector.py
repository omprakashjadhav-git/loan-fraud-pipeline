
# def detect_fraud_risk(event):
#     """Flag applications that meet basic risk-screening rules."""
#     reasons = []

#     if event["credit_score"] < 500:
#         reasons.append("Low credit score")

#     if event["loan_amount"] > 5 * event["annual_income"]:
#         reasons.append("Loan amount exceeds 5x annual income")

#     if event["applicant_age"] < 18 or event["applicant_age"] > 100:
#         reasons.append("Applicant age outside expected range")

#     return {
#         "application_id": event["application_id"],
#         "risk_flag": len(reasons) > 0,
#         "risk_reasons": reasons,
#     }



def validate_loan_event(event):
    """Validate required fields and basic loan application values."""
    if not isinstance(event, dict):
        return False, "Event must be a dictionary"

    required_fields = [
        "event_id",
        "event_timestamp",
        "application_id",
        "source",
        "applicant_age",
        "loan_amount",
        "annual_income",
        "credit_score",
    ]

    for field in required_fields:
        if field not in event:
            return False, f"Missing required field: {field}"

    if not isinstance(event["applicant_age"], int) or isinstance(event["applicant_age"], bool):
        return False, "Applicant age must be an integer"

    if not isinstance(event["loan_amount"], (int, float)) or isinstance(event["loan_amount"], bool):
        return False, "Loan amount must be numeric"

    if not isinstance(event["annual_income"], (int, float)) or isinstance(event["annual_income"], bool):
        return False, "Annual income must be numeric"

    if not isinstance(event["credit_score"], int) or isinstance(event["credit_score"], bool):
        return False, "Credit score must be an integer"

    if not 18 <= event["applicant_age"] <= 100:
        return False, "Applicant age must be between 18 and 100"

    if event["loan_amount"] <= 0:
        return False, "Loan amount must be positive"

    if event["annual_income"] <= 0:
        return False, "Annual income must be positive"

    if not 300 <= event["credit_score"] <= 850:
        return False, "Credit score must be between 300 and 850"

    return True, None


def detect_fraud_risk(event):
    """Flag applications that meet basic risk-screening rules."""
    reasons = []

    if event["credit_score"] < 500:
        reasons.append("Low credit score")

    if event["loan_amount"] > 5 * event["annual_income"]:
        reasons.append("Loan amount exceeds 5x annual income")

    if event["applicant_age"] < 18 or event["applicant_age"] > 100:
        reasons.append("Applicant age outside expected range")

    return {
        "application_id": event["application_id"],
        "risk_flag": len(reasons) > 0,
        "risk_reasons": reasons,
    }


