# Exercise: Audit the KnowledgeHub Knowledge Base for Poisoning Risk

**Estimated Time:** 25 minutes
**Deliverables:** See below

---

## Overview

Eight documents have been staged for upload to the KnowledgeHub S3 bucket. The KB sync is scheduled to run at end of day. Your job: decide what's safe to ingest, identify anomalies in the access log, and understand the bugs in the validation script — before the sync runs.

---

## Scenario

**Vertex Consulting** is a management consulting firm. KnowledgeHub is an internal RAG agent consultants use to query client deliverables, industry research, and analytical frameworks. The S3 bucket (`vertex-kb-staging`) accepts uploads from practice leads, research analysts, and a central knowledge management team. There's no automated validation before ingestion — that's what you're analyzing.

**Files you're working with:**
- `starter/sample_docs/` — 8 documents staged for upload
- `starter/s3_access_log.txt` — 48-hour S3 upload log for the whole bucket (10 entries). Some entries are for files that aren't among the eight staged documents, and some staged documents have no entry in this period.
- `starter/validate_documents.py` — a validation script with 3 bugs

---

## Tasks

### Task 1 — Classify the documents

Read each document in `starter/sample_docs/`. Classify each one:

| Document | Classification | Reason (one line) |
|---|---|---|
| remote_work_policy_v3.txt | | |
| incident_response_runbook_v5.txt | | |
| compensation_review_policy_2026.txt | | |
| vpn_setup_guide_v2.txt | | |
| all_hands_q1_2026_update.txt | | |
| denver_office_opening.txt | | |
| cloud_infrastructure_guide.txt | | |
| employee_expense_policy.txt | | |

**Classifications:**
- **SAFE** — content is appropriate for the KB, no suspicious patterns
- **REVIEW** — something is anomalous but not definitively malicious; needs human review before ingesting
- **REJECT** — contains clear injection content or manipulation attempts; do not ingest

Write your completed table in `my_answers/task1_document_classification.md`.

### Task 2 — Analyze the S3 access log

Open `starter/s3_access_log.txt`. Two of the 10 entries are suspicious.

For each suspicious entry, answer:
1. What is specifically anomalous? (Consider: who's making the request, what time, what prefix, what IP)
2. What is your immediate next step?

Write your answers in `my_answers/task2_access_log_analysis.md`.

### Task 3 — Identify the validation script bugs

Open `starter/validate_documents.py`. The script has **3 intentional bugs**. Read it and for each bug:
1. Where is it (function name + what the logic does)
2. What incorrect behavior it causes — does it let poisoned content through, or report wrong results?
3. What the correct logic should be (plain English — no code required)

**Hint:** The three bugs involve unit conversion, case-sensitivity, and boolean return logic.

Write your answers in `my_answers/task3_bug_analysis.md`.

### Task 4 — Incident response

Write your answer in `my_answers/task4_incident_response.md`:

You've discovered that `compensation_review_policy_2026.txt` was already synced into KnowledgeHub 48 hours ago. Consultants have been querying the system since then. What are your first three steps?

---

## Deliverables

```
my_answers/
  task1_document_classification.md
  task2_access_log_analysis.md
  task3_bug_analysis.md
  task4_incident_response.md
```

---

## Key Takeaway

A poisoned chunk in the vector index is harder to find and reason about than a poisoned HTTP request — it arrived through the legitimate ingest pipeline and looks like every other chunk. Validation at ingestion time is significantly more reliable than catching an attack at query time with a guardrail.

---

## Connection to the Capstone

In Project Task 1, you'll sync the Northstar Assist knowledge base from S3, and in Project Task 3 your threat model covers indirect injection through retrieved content. What you're practicing here — validating documents before sync, reviewing access logs for anomalies — is the security layer that makes that sync safe to run, and the poisoning scenarios give you concrete threats to model.
