
# import json
# from pathlib import Path


# def generate_summary():
#     file_path = Path("data/processed/screening_results.jsonl")

#     total_applications = 0
#     flagged_applications = 0
#     rejected_records = 0

#     with file_path.open("r", encoding="utf-8") as input_file:
#         for line in input_file:
#             if not line.strip():
#                 continue

#             try:
#                 record = json.loads(line)
#                 result = record["screening_result"]

#                 total_applications += 1

#                 if result["risk_flag"]:
#                     flagged_applications += 1

#             except (json.JSONDecodeError, KeyError, TypeError):
#                 rejected_records += 1

#     print("\n=== Loan Application Screening Summary ===")
#     print(f"Total applications processed: {total_applications}")
#     print(f"Applications flagged for risk: {flagged_applications}")
#     print(f"Applications not flagged: {total_applications - flagged_applications}")
#     print(f"Malformed records skipped: {rejected_records}")


# if __name__ == "__main__":
#     generate_summary()


# import csv
# import json
# from pathlib import Path


# def generate_summary():
#     file_path = Path("data/processed/screening_results.jsonl")
#     report_path = Path("data/processed/summary_report.csv")

#     total_applications = 0
#     flagged_applications = 0
#     rejected_records = 0

#     with file_path.open("r", encoding="utf-8") as input_file:
#         for line in input_file:
#             if not line.strip():
#                 continue

#             try:
#                 record = json.loads(line)
#                 result = record["screening_result"]

#                 total_applications += 1

#                 if result["risk_flag"]:
#                     flagged_applications += 1

#             except (json.JSONDecodeError, KeyError, TypeError):
#                 rejected_records += 1

#     not_flagged = total_applications - flagged_applications

#     print("\n=== Loan Application Screening Summary ===")
#     print(f"Total applications processed: {total_applications}")
#     print(f"Applications flagged for risk: {flagged_applications}")
#     print(f"Applications not flagged: {not_flagged}")
#     print(f"Malformed records skipped: {rejected_records}")

#     with report_path.open("w", newline="", encoding="utf-8") as output_file:
#         writer = csv.writer(output_file)

#         writer.writerow(["Metric", "Count"])
#         writer.writerow(["Total applications processed", total_applications])
#         writer.writerow(["Applications flagged for risk", flagged_applications])
#         writer.writerow(["Applications not flagged", not_flagged])
#         writer.writerow(["Malformed records skipped", rejected_records])

#     print(f"\nCSV report saved to: {report_path}")


# if __name__ == "__main__":
#     generate_summary()


import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

RESULTS_FILE = DATA_DIR / "screening_results.jsonl"
REPORT_FILE = DATA_DIR / "summary_report.csv"


def generate_summary():
    if not RESULTS_FILE.exists():
        print(f"Error: Screening results file not found: {RESULTS_FILE}")
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    total_applications = 0
    flagged_applications = 0
    rejected_records = 0

    with RESULTS_FILE.open("r", encoding="utf-8") as input_file:
        for line in input_file:
            if not line.strip():
                continue

            try:
                record = json.loads(line)
                result = record["screening_result"]
                risk_flag = result["risk_flag"]

                if not isinstance(risk_flag, bool):
                    raise ValueError("risk_flag must be a boolean")

                total_applications += 1

                if risk_flag:
                    flagged_applications += 1

            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                rejected_records += 1

    not_flagged = total_applications - flagged_applications

    print("\n=== Loan Application Screening Summary ===")
    print(f"Total applications processed: {total_applications}")
    print(f"Applications flagged for risk: {flagged_applications}")
    print(f"Applications not flagged: {not_flagged}")
    print(f"Malformed records skipped: {rejected_records}")

    with REPORT_FILE.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Metric", "Count"])
        writer.writerow(["Total applications processed", total_applications])
        writer.writerow(["Applications flagged for risk", flagged_applications])
        writer.writerow(["Applications not flagged", not_flagged])
        writer.writerow(["Malformed records skipped", rejected_records])

    print(f"\nCSV report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    generate_summary()

