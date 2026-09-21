# Exercise: Audit the CaseAssist API Configuration

**Estimated Time:** 50 minutes
**Deliverables:** See below

---

## Overview

A paralegal-turned-developer wrote the initial CaseAssist configuration. It works, but "works" and "secure" are different things. Your job: read three files, find the security issues, and fill in the checklist.

---

## Scenario

**Apex Legal** is promoting CaseAssist, a RAG assistant on an Amazon Bedrock AgentCore harness for querying case law summaries, internal memos, and client matter notes, from dev to staging. Before that happens, you need to sign off on the security configuration. The team has confirmed that model invocation logging isn't turned on in the account's Bedrock settings.

You have:
- `starter/app_config_review.py`: the harness client code
- `starter/bedrock_invocation.py`: an alternative credential pattern
- `starter/iam_policy_overpermissive.json`: the IAM policy attached to the CaseAssist application's role, which calls the harness
- `starter/API_SECURITY_CHECKLIST.md`: a checklist to complete

---

## Tasks

### Task 1 — Audit the code and IAM policy

Read `app_config_review.py` and `iam_policy_overpermissive.json`. Identify the security issues. For each issue, write:
1. What the problem is
2. Why it matters in a legal context (client matter data, attorney-client privilege)
3. What the correct approach is

Then do the same for `bedrock_invocation.py`. It uses a different credential pattern that's also wrong. Answer: what is the correct way for a client running on AWS compute (EC2/ECS/Lambda) to obtain credentials, and why?

Write your findings in `my_answers/task1_security_review.md`.

**What to look for:**
- Hardcoded credentials
- Configuration that should come from environment variables (the harness ARN and Region)
- IAM wildcard permissions (`bedrock:*`, `s3:*` on `*`). Name three specific Bedrock actions these expose that the app doesn't need, and name the actions the app does need to call the harness.
- No input length limit or validation

### Task 2 — Complete the checklist

Open `starter/API_SECURITY_CHECKLIST.md`. Mark each item **Pass** or **Fail** based on the current configuration. Add one sentence for any Fail. Mark an item **N/A** if it doesn't apply to this configuration, and say why.

Save as `my_answers/task2_checklist_completed.md`.

---

## Deliverables

```
my_answers/
  task1_security_review.md
  task2_checklist_completed.md
```

---

## Key Takeaway

`bedrock:*` on `*` isn't just a theoretical risk. It permits invoking any model at the firm's expense, deleting knowledge bases, turning off invocation logging, and editing guardrails. In a legal context, a weakened guardrail could let CaseAssist return privileged client matter content it was set up to withhold. Scope matters.

---

## Connection to the Capstone

In Project Task 1 you'll configure Northstar Assist on an AgentCore harness with a knowledge base behind an AgentCore Gateway, and in Project Task 4 you'll scope the harness execution role and gateway service role. Those IAM roles control what your deployed application can actually do in AWS. Use the checklist from this exercise to verify the configuration you deploy in Task 1 and the IAM scoping you do in Task 4 before you submit.
