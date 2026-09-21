# Exercise: Build a Monitoring Plan and IR Playbook for OpsGuide

**Estimated Time:** 75 minutes
**Deliverables:** See below

---

## Overview

OpsGuide is a RAG assistant on an Amazon Bedrock AgentCore harness at NovaTech (industrial manufacturing) used by plant operators to query equipment manuals, maintenance procedures, safety data sheets, and OSHA compliance docs. An incorrect answer isn't just an annoyance — it can cause equipment damage or a safety incident.

Your job: design a monitoring plan for OpsGuide and write an incident response playbook for the most likely AI-specific attack.

---

## Scenario

**OpsGuide architecture:**

```
Plant operator terminal → Streamlit app → AgentCore harness (Claude Sonnet 4.5) → AgentCore Gateway → Managed Knowledge Base
```

Source documents are stored in S3 and synced to the KB nightly. Model invocation logging is on. The Streamlit app logs the operator's user ID, the terminal ID, and the `runtimeSessionId` it sends with each request. The model invocation log doesn't record the `runtimeSessionId` or `runtimeUserId` your app sends. The session ID in `identity.arn` is a different value that the harness generates. That's why the app keeps its own log. Guardrails are active with prompt attack detection, a sensitive information filter, and a topic policy. A contextual grounding check is also enabled, but in testing on harness traffic the guardrail recorded no grounding assessment, so don't rely on it.

**Threat context:** Plant operators work rotating shifts (day/night). "Normal" usage looks like bursts of activity at shift start/end. A sustained stream of queries at 3 AM from a single terminal is not normal. An unauthorized document appearing in the KB about a maintenance procedure is extremely high-risk.

---

## Tasks

### Task 1 — Fill in the Monitoring Plan

Copy `starter/MONITORING_PLAN_TEMPLATE.md` to `my_answers/task1_monitoring_plan.md` and fill it in.

Complete the four rows. For each log source:
- **What to Log:** Name the specific fields or event types — not just "API calls"
- **Alert Condition:** Give a concrete threshold (e.g., "InvocationsIntervened for input-side ContentPolicy > 5 in 10 minutes") rather than "suspicious activity"

Then answer the two questions at the bottom of the template.

### Task 2 — Analyze the Mock Incident Log

Open `starter/MOCK_INCIDENT_LOG.md`.

Read **Event A** only. Answer:
1. What is happening?
2. Which detection signal(s) from your monitoring plan would catch this?
3. What information is missing from this log that you'd want to have?

Write your answers in `my_answers/task2_incident_analysis.md`.

### Task 3 — Write the IR Playbook

Copy `starter/IR_PLAYBOOK_TEMPLATE.md` to `my_answers/task3_ir_playbook.md` and fill it in.

Complete the playbook for **Incident Type: Suspected Prompt Injection**. Write at the level of detail that an on-call IT analyst with no prior AI incident experience could follow. Name the AWS console path or CLI command for each action — "check the logs" is not actionable at 2 AM.

---

## Deliverables

```
my_answers/
  task1_monitoring_plan.md       (copy of starter/MONITORING_PLAN_TEMPLATE.md: all 4 rows + 2 questions)
  task2_incident_analysis.md     (3 questions on Event A)
  task3_ir_playbook.md           (copy of starter/IR_PLAYBOOK_TEMPLATE.md: the prompt injection playbook)
```

---

## Key Takeaway

The monitoring sources unique to AI systems — Bedrock Model Invocation Logs and Guardrails Metrics — are the most important ones to get right before launch. A traditional application monitoring plan won't include them, but they are the primary signal for the attack types most likely to target an AI system.

---

## Connection to the Capstone

Project Task 6 is this exercise at full scale, applied to Northstar Assist. You'll turn on Bedrock model invocation logging (it's off by default) and deliver a monitoring plan built on AI-specific signals (guardrail intervention counts, retrieval anomalies, token count anomalies), name its log sources, set at least one concrete alert threshold, and write a prompt-injection IR playbook with console paths or CLI commands. The templates you're working with today are the same ones you'll use there.
