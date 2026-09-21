# Exercise: Apply Privacy-Preserving Design to the MyHealth Assistant Knowledge Base

**Estimated Time:** 45 minutes
**Deliverables:** See below

---

## Overview

The content team has handed you 6 documents and asked you to review them before uploading to the MyHealth Assistant knowledge base. Your job: classify each document, decide what belongs (and what doesn't), minimize PII before upload, and configure the PII guardrail as a safety net.

---

## Scenario

**Westfield Health** is a large integrated health system. MyHealth Assistant is a **patient-facing** AI chatbot. Any authenticated patient can query it. The KB is meant to help patients navigate appointments, understand discharge instructions, and find information about covered medications.

The system has no access to individual patient medical records. It is strictly a knowledge base chatbot. However, patients may volunteer PHI in their queries — HIPAA applies.

The 6 documents to review are in `starter/documents_to_classify_myhealth/`.

---

## Tasks

### Task 1 — Classify all six documents

Open `starter/DATA_CLASSIFICATION_WORKSHEET.md` and complete the table.

For each document:
- **Classification:** Public / Internal / Confidential / Restricted
- **Include in KB?:** Yes / No / Modified (with specific changes)
- **Reason:** 1–2 sentences — be specific about the risk to patients if this data were accessible

**The key question for each document:** This system is accessible to authenticated patients, not employees. Which documents are appropriate for patients to query? Which expose internal Westfield Health information to people with no business need for it?

### Task 2 — Staff directory: decide what to remove

The staff directory, `starter/documents_to_classify_myhealth/staff_directory.csv`, has 8 columns:

```
employee_id, full_name, email, phone_extension, department, manager_name, office_location, salary_band
```

If you decided to include a minimized version of the directory (so patients can find which department handles a service), answer in the worksheet:

1. Which columns must be removed before uploading? For each, explain the specific privacy or safety risk in a patient-facing context.
2. Write the minimized CSV header.

### Task 3 — Configure the PII guardrail

Open `starter/GUARDRAIL_PII_CONFIG.md` and complete the configuration table.

Choose BLOCK / ANONYMIZE / ALLOW for each PII type. Remember: a Bedrock guardrail checks both the patient's **input** and the model's **output**. In the output, the most likely PII is the model echoing back what the patient included in their query.

Then answer the written question: why is data minimization (not putting PHI in the KB in the first place) a stronger control than output filtering?

---

## Deliverables

- `starter/DATA_CLASSIFICATION_WORKSHEET.md` — completed table + Task 2 answers
- `starter/GUARDRAIL_PII_CONFIG.md` — completed PII table + written response

---

## Key Takeaway

"Who can query this system" completely changes the data classification calculus. A staff directory that's Internal (appropriate for employees) becomes Restricted when it's accessible to patients. Privacy-preserving AI starts by asking not "is this data sensitive?" but "is this data appropriate for this specific user population?"

---

## Connection to the Capstone

Project Task 5 requires output PII detection and filtering on your Northstar Assist guardrail, and Project Task 7 requires a test prompt that tries to elicit sensitive knowledge base information. The PII guardrail configuration and classification reasoning you practice here are the foundation for both.
