# Exercise: Implement Rate Limiting for the Orion API

**Estimated Time:** 20 minutes
**Deliverables:** See below

---

## Overview

Orion AI is a B2B SaaS startup. Their product gives enterprise customers programmatic access to an AI assistant running on an Amazon Bedrock AgentCore harness. Each customer is billed per query at ~$0.024/call. Before enforcing rate limits, the team needs to understand the current usage pattern — and which customers are already operating outside expected bounds.

---

## Scenario

Orion AI has sold access to 40 enterprise customers. Monthly budget: $2,000 (~83,000 queries). Standard contract: 3,000 queries/month per customer.

A usage log has been pulled from CloudWatch into `starter/usage_log.csv`. It covers 9 of the 40 customers over about nine days.

---

## Tasks

### Task 1: Read and run the rate limiter

Open `starter/rate_limiter.py`. The implementation is complete — do not modify it. Read it, then answer in `my_answers/task1_rate_limiter_analysis.md`:

1. In plain English, what's the difference between a sliding window and a fixed clock window? Why is a sliding window harder to game?
2. Walk through what happens step-by-step when a user at 19 requests makes their 20th request (limit is 20). What does `check_rate_limit` return?
3. Why must `get_user_stats` never call `record_request`?

Then run the script and paste the output:
```bash
python starter/rate_limiter.py
```

### Task 2: Analyze the usage log

Open `starter/usage_log.csv`.

**Tip:** Open it in a spreadsheet, or run: `python -c "import csv; rows=list(csv.DictReader(open('starter/usage_log.csv'))); print(len(rows))"` to start exploring.

The columns: `timestamp`, `customer_id`, `session_id`, `query_length_chars`, `response_length_chars`, `estimated_cost_usd`, `guardrail_triggered`

Answer in `my_answers/task2_usage_analysis.md`:

1. Which customer(s) appear to be abusing the system? For each: what's the specific pattern (volume, timing, query length)?
2. What is the total cost in the log? Which customer accounts for the largest share and what percentage?
3. Which customer has a notably elevated `guardrail_triggered` rate? What are two explanations — one benign, one malicious?

### Task 3: Design one CloudWatch alarm

Describe one alarm — the most important one for Orion AI to have — in `my_answers/task3_alarm.md`:

- Which metric does it use?
- What is the threshold and evaluation period?
- Why is this the highest-priority alarm for this specific business?

Hint: the provider-side metric is `Invocations` in the `AWS/Bedrock` namespace, with dimension `ModelId`. It counts model turns, not customer queries: a harness query that uses a tool takes at least two turns. It has no customer dimension.

Two steps if your alarm needs per-customer tracking: (1) what the application must log to CloudWatch Logs, and (2) how a Logs Metric Filter turns those entries into a per-customer metric.

### Task 4: Rate limit calculation

Show your math in `my_answers/task4_rate_limit_math.md`:

1. At ~$0.024/query and a $2,000/month budget, how many total queries/month can the system afford?
2. If a customer scripts their integration at 1 query/second for an hour, how much does that cost? How does an hourly limit prevent this?
3. What per-hour limit would you recommend, and why?

### Task 5: Blast radius

One paragraph in `my_answers/task5_blast_radius.md`:

If an enterprise customer's API credentials are stolen and used to flood the Orion API, how does the rate limiter reduce the damage compared to no limits? Cover: Orion AI's cost exposure and time to detection.

---

## Deliverables

```
my_answers/
  task1_rate_limiter_analysis.md
  task2_usage_analysis.md
  task3_alarm.md
  task4_rate_limit_math.md
  task5_blast_radius.md
```

---

## Key Takeaway

For a B2B AI API, rate limiting is simultaneously a security control, a cost control, and a contractual obligation. When presenting this to leadership, lead with cost governance and SLA fairness — those are the frames that move organizations to act. The security benefit (limiting what a compromised credential can extract) is real but secondary.

---

## Connection to the Capstone

The project doesn't have a dedicated rate-limiting task, but the cost and abuse reasoning you practice here carries into it. In Project Task 6, your monitoring plan for Northstar Assist tracks token count anomalies and sets at least one concrete alert threshold — the same thinking behind the alarm you design here. In Project Task 7, a per-user rate limiter is a hardening you can recommend in your launch-readiness report.
