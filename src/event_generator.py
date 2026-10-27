
# import json
# import uuid
# from datetime import datetime, timezone

# def generate_loan_event():
#     """Generate one synthetic loan application event."""
#     return {
#         "event_id": str(uuid.uuid4()),
#         "event_timestamp": datetime.now(timezone.utc).isoformat(),
#         "application_id": str(uuid.uuid4()),
#         "source": "mobile_app",
#         "applicant_age": 32,
#         "loan_amount": 150000,
#         "annual_income": 600000,
#         "credit_score": 720,
#     }


# if __name__ == "__main__":
#     event = generate_loan_event()
#     print(json.dumps(event, indent=2))


import json
import uuid
import random
from datetime import datetime, timezone


def generate_loan_event():
    """Generate one synthetic loan application event."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "application_id": str(uuid.uuid4()),
        "source": random.choice(
            ["mobile_app", "website", "bank_branch"]
        ),
        "applicant_age": random.randint(18, 75),
        "loan_amount": random.randint(10000, 1000000),
        "annual_income": random.randint(100000, 2000000),
        "credit_score": random.randint(300, 850),
    }


if __name__ == "__main__":
    import time

    try:
        while True:
            event = generate_loan_event()
            print(json.dumps(event), flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nEvent generation stopped.")
