# Exercise: Threat Model FinQuery

**Estimated Time:** 30 minutes
**Deliverable:** `starter/STRIDE_ML_COMPLETED.md`

---

## Overview

You're applying STRIDE-ML to FinQuery, a Bedrock RAG agent at a financial analytics firm. The architecture and current system state are described in the template — you don't need to re-read them here.

Your job: identify the three most important threats, rank them, and pick one mitigation for each.

---

## Scenario

You are an **AI Security Engineer at Meridian Analytics**. FinQuery is functionally complete but not yet hardened. Current state:

- No active Guardrails (passthrough mode)
- S3 bucket with source documents is accessible to any principal in the account
- The AgentCore harness execution role has `bedrock:*` from development
- No per-user rate limiting
- No query-level audit logging
- Source documents include non-public research subject to internal **information barriers** — some analysts are not authorized to see all research

The engineering team wants a threat model before production launch.

---

## Tasks

### Task 1 — Fill in the three threat tables

Open `starter/STRIDE_ML_TEMPLATE.md`. The template covers the three highest-risk STRIDE categories for RAG systems: **Tampering**, **Information Disclosure**, and **Elevation of Privilege**.

For each threat:
- Describe the specific attack in concrete terms (who does what, using which component)
- Rate likelihood and impact (Low / Medium / High) with one sentence of reasoning each
- Identify one mitigation

**Hints:**
- **Tampering:** Who can write to the S3 bucket today? What would a replaced research note do after the next sync?
- **Information Disclosure:** When retrieval finds a relevant document, does anything check whether the analyst asking is cleared to see it? What does that mean in a firm with information barriers?
- **Elevation of Privilege:** What happens when a document in the knowledge base contains text addressed to the model instead of to a human reader?

### Task 2 — Rank your three threats

Fill in the Priority Ranking table. One sentence per threat explaining why it lands where it does.

### Task 3 — Pick your one mitigation

If you could implement only one control before launch, what would it be? Answer the final question in the template.

---

## Deliverable

Save as `starter/STRIDE_ML_COMPLETED.md`. Remove all placeholder text before submitting.

---

## Key Takeaway

Financial RAG systems face a threat that simpler chatbots don't: **information barrier violations via retrieval**. If the vector store returns documents without checking who's authorized to see them, the model synthesizes and presents restricted research to analysts who shouldn't have it. This is both a securities law issue and an architecture issue — and it won't be caught by Guardrails alone.

---

## Connection to the Capstone

Project Task 3 asks you to deliver a STRIDE-ML threat model of your Northstar Assist agent and retrieval flow. The architecture is nearly identical. Students who work through this exercise carefully — especially the indirect injection and information disclosure angles — consistently produce stronger capstone threat models.
