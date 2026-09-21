# Demo Documents: PII Minimization and Data Classification

These files support the PII and data classification demo. All people and values are fictional.

## Ingested into the knowledge base

| File | Purpose |
|---|---|
| `employee_directory_minimized.csv` | Minimized directory (employee ID, department, office only). Replaces the full `employee_directory.csv` to show data minimization. |

## Classification only (never ingest)

| File | Suggested Classification | Why |
|---|---|---|
| `hr_roster.csv` | Restricted | SSNs, home addresses, bank details, salaries |
| `employee_performance_data.md` | Confidential | Performance ratings by department; small groups can identify individuals |
| `client_contracts_summary.md` | Confidential | Customer contract values and negotiated terms |

Use the classification-only files to practice labeling and to decide what should be kept out of the Aria knowledge base. Do not upload them to S3 or sync them into a knowledge base.
