# Exercise: Design Guardrails for BankBot

**Estimated Time:** 50 minutes
**Deliverable:** Your completed worksheet, saved as `starter/GUARDRAIL_DESIGN_WORKSHEET_COMPLETED.md`

---

## Overview

BankBot is a customer-facing AI assistant for FirstLight Bank, accessible to any authenticated retail customer. Your job: design the Guardrails configuration before launch.

Every setting is a tradeoff — higher sensitivity catches more attacks and blocks more legitimate customers. The right configuration requires understanding who's using the system, what data it has access to, and what acceptable error rates look like on both sides.

---

## Scenario

BankBot's knowledge base contains: product information, regulatory disclosures, FAQ content, and general banking procedures. It does **not** have access to any individual customer account data.

A public-facing bank chatbot has a fundamentally different threat model than an internal corporate tool:
- The user population includes everyone: regular customers, curious people, security researchers, and adversarial actors
- False positives affect paying customers — blocking a legitimate query has a direct business cost (lost sales, customer frustration, increased call center volume)
- Regulatory disclosures (fee schedules, APR tables) that the model gets wrong create legal liability

---

## Tasks

### Task 1 — Classify the test prompts

Open `starter/TEST_PROMPTS.md`. For each of the 10 prompts, fill in the Classification column in your worksheet using these codes:

| Code | Meaning |
|---|---|
| L | Legitimate customer query |
| DI | Direct injection (explicit override instructions) |
| II | Indirect injection setup (attempting to process attacker-controlled content) |
| PII | Customer volunteers sensitive personal data |
| DT | Denied topic |
| HA | Harmful action |

### Task 2 — Complete the guardrail worksheet

Copy `starter/GUARDRAIL_DESIGN_WORKSHEET.md` to `starter/GUARDRAIL_DESIGN_WORKSHEET_COMPLETED.md`, and fill in Parts 1–5:

**Part 1 — Content filters:** Set input and output thresholds for all five categories. Write 2–3 sentences explaining your overall approach for a public-facing bank.

**Part 2 — Denied topics:** Define two denied topics with names, definitions, and example phrases. Think about: what topics would create regulatory risk or enable social engineering for a bank?

**Part 3 — PII detection:** Choose BLOCK / ANONYMIZE / ALLOW for each PII type. Note: the KB has no account data — the most likely PII in a response is the model echoing back what the customer included in their query.

**Part 4 — Prompt attack detection:** Choose a sensitivity level and explain the tradeoff for this specific user population. Then name the attack patterns from the test prompts that this setting catches, and what it might miss.

**Part 5 — Setting most likely to block a legitimate customer:** Reread your configuration. Name the one setting most likely to block a legitimate customer, the test prompt that shows it, and whether you accept that cost.

**Console Notes:** If you build the guardrail in the AWS console, record the guardrail name, ID, ARN, the version attached to the harness, and the AWS Region in the Console Notes table at the end of the worksheet.

---

## Key Takeaway

Public-facing AI deployments face a qualitatively different threat model than internal tools. The same guardrail setting that's conservative-but-workable for 150 internal employees becomes a customer satisfaction and regulatory liability issue when applied to hundreds of thousands of bank customers.

---

## Connection to the Capstone

Project Task 5 requires you to create a real Bedrock Guardrail, attach it to your Northstar Assist harness (as the `guardrailConfig` model parameter, with `bedrock:ApplyGuardrail` added to the harness execution role), and document your configuration decisions with justification. The design reasoning you practice here translates directly to Task 5.
