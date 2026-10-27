
# Real-Time Loan Fraud Detection Data Pipeline

## Project Overview

A data engineering portfolio project that simulates loan application events, validates incoming records, applies rule-based risk screening, and stores structured results for reporting.

The project currently runs locally and focuses on data quality, persistent event tracking, duplicate detection, automated testing, and reporting.

## Current Features

- Generates synthetic loan application events.
- Simulates application sources such as mobile apps, websites, and bank branches.
- Validates required fields and acceptable data ranges.
- Flags potentially risky applications using configurable rules.
- Stores screening results in JSONL format.
- Persists processed event IDs to support duplicate detection across restarts.
- Recovers tracked IDs from saved results when necessary.
- Generates a CSV summary of processed applications and risk flags.
- Includes automated tests for validation, duplicate detection, ID loading, and reporting.

## Technology Stack

- **Python** — event generation, validation, screening, and reporting
- **JSONL** — event and screening-result storage
- **CSV** — summary reporting
- **pytest** — automated testing
- **Git** — version control

## Architecture

1. **Event generation:** Creates synthetic loan application events.
2. **Validation:** Checks required fields, data types, and acceptable value ranges.
3. **Risk screening:** Applies rule-based checks, including low credit scores.
4. **Persistence:** Appends screening results and processed event IDs to local files.
5. **Reporting:** Generates a CSV summary of processed applications, risk flags, and malformed records.

## Current Project Status

**Local prototype implemented; development in progress.**

The current implementation passes **15 automated tests**.

Latest verified local screening report:

| Metric | Result |
|---|---:|
| Applications processed | 98 |
| Applications flagged for risk | 34 |
| Applications not flagged | 64 |
| Malformed records skipped | 0 |

These figures describe the current synthetic dataset and may change as more events are generated.

The results and processed-ID tracking files each contain 98 records. All 98 tracked IDs are unique, and the result IDs match the tracked IDs.

## Planned Improvements

- Strengthen end-to-end duplicate-event testing.
- Add automated tests for pipeline failure scenarios.
- Introduce Apache Kafka for event streaming.
- Organize data into Bronze, Silver, and Gold layers.
- Add SQL-based analysis of processed records.
- Measure pipeline reliability and performance.
- Explore cloud deployment after reviewing free-tier eligibility, costs, and safeguards.

## Data and Evaluation

The current pipeline uses synthetic application events. Risk flags are produced by rules, not by a trained machine-learning model, and are not verified fraud labels.

Future evaluation will use documented test cases and measured pipeline behavior. Any public dataset will be identified and documented before being incorporated.

## Disclaimer

This is an educational portfolio project. It does not connect to real banking systems, verify real-world fraud, or make actual lending decisions. Risk flags are illustrative and should not be used to assess real applicants.

