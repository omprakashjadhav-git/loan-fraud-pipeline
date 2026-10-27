
# import json
# import time

# from event_generator import generate_loan_event
# from fraud_detector import detect_fraud_risk


# def run_pipeline():
#     print("Loan Fraud Detection Pipeline started.")
#     print("Press Ctrl+C to stop.\n")

#     try:
#         while True:
#             # Generate a loan application event
#             event = generate_loan_event()

#             # Check the event for risk indicators
#             result = detect_fraud_risk(event)

#             # Display the event and its screening result
#             print(json.dumps({
#                 "event": event,
#                 "screening_result": result,
#             }, indent=2))

#             print("-" * 60)
#             time.sleep(2)

#     except KeyboardInterrupt:
#         print("\nPipeline stopped.")


# if __name__ == "__main__":
#     run_pipeline()


# import json
# import time

# from event_generator import generate_loan_event
# from fraud_detector import detect_fraud_risk, validate_loan_event


# def run_pipeline():
#     print("Loan Fraud Detection Pipeline started.")
#     print("Saving results to data/processed/screening_results.jsonl")
#     print("Press Ctrl+C to stop.\n")

#     try:
#         while True:
#             event = generate_loan_event()

# # Validate the event before processing
# is_valid, error = validate_loan_event(event)

# if not is_valid:
#     print(f"Invalid event rejected: {error}")
#     time.sleep(2)
#     continue

# # Screen only valid events
# result = detect_fraud_risk(event)

# record = {
#     "event": event,
#     "screening_result": result,
# }

#             # Save each event and screening result to a file
#             with open(
#                 "data/processed/screening_results.jsonl",
#                 "a",
#                 encoding="utf-8",
#             ) as output_file:
#                 output_file.write(json.dumps(record) + "\n")

#             # Display the result in the terminal
#             print(json.dumps(record, indent=2))
#             print("-" * 60)

#             time.sleep(2)

#     except KeyboardInterrupt:
#         print("\nPipeline stopped.")


# if __name__ == "__main__":
#     run_pipeline()


import json
import time
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_FILE = DATA_DIR / "screening_results.jsonl"
PROCESSED_IDS_FILE = DATA_DIR / "processed_event_ids.jsonl"

sys.path.insert(0, str(PROJECT_ROOT))

from src.event_generator import generate_loan_event
from src.fraud_detector import detect_fraud_risk, validate_loan_event


def load_processed_event_ids():
    """Load tracked IDs and recover missing IDs from saved results."""
    processed_ids = set()

    # Load IDs from the tracking file.
    if PROCESSED_IDS_FILE.exists():
        with PROCESSED_IDS_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                try:
                    record = json.loads(line)
                    event_id = record.get("event_id")

                    if isinstance(event_id, str) and event_id:
                        processed_ids.add(event_id)

                except (json.JSONDecodeError, AttributeError):
                    continue

    # Recover IDs from results only when using the real project files.
    # This prevents tests using temporary files from reading real project data.
    if PROCESSED_IDS_FILE == DATA_DIR / "processed_event_ids.jsonl":
        if RESULTS_FILE.exists():
            with RESULTS_FILE.open("r", encoding="utf-8") as file:
                for line in file:
                    try:
                        record = json.loads(line)
                        event = record.get("event", {})

                        event_id = (
                            event.get("event_id")
                            if isinstance(event, dict)
                            else None
                        )

                        if isinstance(event_id, str) and event_id:
                            processed_ids.add(event_id)

                    except (json.JSONDecodeError, AttributeError):
                        continue

        # Find IDs missing from the tracking file.
        existing_ids = set()

        if PROCESSED_IDS_FILE.exists():
            with PROCESSED_IDS_FILE.open("r", encoding="utf-8") as file:
                for line in file:
                    try:
                        record = json.loads(line)
                        event_id = record.get("event_id")

                        if isinstance(event_id, str) and event_id:
                            existing_ids.add(event_id)

                    except (json.JSONDecodeError, AttributeError):
                        continue

        # Backfill recovered IDs without deleting existing data.
        missing_ids = processed_ids - existing_ids

        if missing_ids:
            DATA_DIR.mkdir(parents=True, exist_ok=True)

            with PROCESSED_IDS_FILE.open("a", encoding="utf-8") as file:
                for event_id in sorted(missing_ids):
                    file.write(json.dumps({"event_id": event_id}) + "\n")

    return processed_ids


def is_duplicate_event(event_id, processed_event_ids):
    """Check whether an event ID has already been processed."""
    if event_id in processed_event_ids:
        return True

    processed_event_ids.add(event_id)
    return False


def run_pipeline():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Loan Application Risk Screening Pipeline started.")
    print(f"Saving results to: {RESULTS_FILE}")
    print(f"Tracking processed IDs in: {PROCESSED_IDS_FILE}")
    print("Press Ctrl+C to stop.\n")

    processed_event_ids = load_processed_event_ids()

    duplicate_events = 0
    total_processed = 0
    invalid_events = 0

    print(
        f"Loaded {len(processed_event_ids)} "
        "previously processed event IDs."
    )

    try:
        while True:
            event = generate_loan_event()

            is_valid, error = validate_loan_event(event)

            if not is_valid:
                invalid_events += 1
                print(f"Invalid event rejected: {error}")
                time.sleep(2)
                continue

            event_id = event["event_id"]

            if is_duplicate_event(event_id, processed_event_ids):
                duplicate_events += 1
                print(f"Duplicate event rejected: {event_id}")
                time.sleep(2)
                continue

            result = detect_fraud_risk(event)

            record = {
                "event": event,
                "screening_result": result,
            }

            # Save the screening result first.
            # Startup recovery handles an ID missing from the tracking file.
            with RESULTS_FILE.open("a", encoding="utf-8") as output_file:
                output_file.write(json.dumps(record) + "\n")

            # Save the processed event ID.
            with PROCESSED_IDS_FILE.open("a", encoding="utf-8") as id_file:
                id_file.write(json.dumps({"event_id": event_id}) + "\n")

            total_processed += 1

            print(json.dumps(record, indent=2))
            print("-" * 60)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nPipeline stopped.")
        print(f"New applications processed: {total_processed}")
        print(f"Invalid events rejected: {invalid_events}")
        print(f"Duplicate events rejected: {duplicate_events}")
        print(
            f"Total event IDs remembered: {len(processed_event_ids)}"
        )


if __name__ == "__main__":
    run_pipeline()












