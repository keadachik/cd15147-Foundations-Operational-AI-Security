# Demo: Setting Up AI-Specific Monitoring for an AgentCore Harness

**Estimated Time:** 15 minutes

---

> **Note:** This demo uses **Aria**, the internal employee assistant of **Vantage Technologies**, running on an Amazon Bedrock AgentCore harness (harness → AgentCore Gateway → Managed Knowledge Base, Claude Sonnet 4.5). At this point in the course, the guardrail `aria-production-guardrails` is version 1 and isn't attached. Lesson 11 creates version 2 and attaches it. Results that need the attached guardrail ("What the guardrail did", Step 5, and the guardrail alarms in Step 6) come from a lab run with version 2 attached. The goal is to show the concept working in a live environment before you apply it to the exercise scenario in `EXERCISE.md`. Your capstone project, Northstar Assist, uses the same setup.

## Scenario

Aria has been running for two weeks. This morning a sales engineer filed an IT ticket: she asked Aria what Vantage's product tiers cost, and the answer included list prices and discount rules. She has never seen that information, and she isn't authorized to see it.

You're the security team. Where do you start, and what would you have needed to log to find out what happened?

### Reproduce the incident

`demo_documents/vantage_price_list_confidential.md` is labeled **Confidential – Sales leadership only**.

**Run the reproduction without the guardrail.** Do it before you attach `aria-production-guardrails`. If the guardrail is already attached, edit the harness, remove the `guardrailConfig` parameter, and choose **Save Harness**. Re-attach it when you're done. With guardrail v2 attached, the lab couldn't reproduce the incident: the guardrail masked the misconfiguration and produced two false positives (see "What the guardrail did" below).

If you've added the IAM Deny on the harness execution role that requires the guardrail (lessons 11 and 15), unguarded calls fail with `AccessDenied`. That's the control working, so run the reproduction before you add the Deny. (The lab sent unguarded requests with a per-request model override that left out `guardrailConfig`. That's the documented bypass Step 5 detects, not a setup method. The override is a `model` argument on the `invoke_harness` call: `model={"bedrockModelConfig": {"modelId": "us.anthropic.claude-sonnet-4-5-20250929-v1:0", "apiFormat": "converse_stream"}}`.)

1. Turn on model invocation logging (Step 1) so the turns are recorded.
2. Upload the file to the Aria knowledge base bucket (`vantage-aria-kb-<suffix>`), in the same prefix as the other Aria documents (`vantage-aria-knowledge-base/`).
3. Sync the knowledge base. Expect 12 scanned, 1 new.
4. In the Harness playground, ask each question in a new session:
   - "What product tiers does Vantage offer, and what do they cost?"
   - "What is the per-user monthly price for the Vantage Professional tier?"

   In the lab, the first answer listed the tier prices from the price list. The second answered "$42 per user per month." Keep the questions neutral. With the guardrail attached, "I'm a sales engineer preparing a quote…" is blocked as `PROMPT_ATTACK`.
5. Select the **Aria-Kb Retrieve** step in the agent trace. One result's `documentId` is `…/vantage-aria-knowledge-base/vantage_price_list_confidential.md`. The same `toolResult` is in the invocation log (Step 3).
6. **Clean up:** delete the file from the bucket and sync again (expect 1 deleted). Ask both questions again to confirm. Aria lists the tiers without prices and says it can't provide the Professional price.

Before the upload, Aria retrieves `product_overview.md` and lists the tiers without prices. See `demo_documents/README.md`. Never upload the price list to a production knowledge base.

Optional: also ask "What discount can a sales engineer approve without escalation?" With the price list indexed, Aria answers from its discount authority table. After cleanup, the same question drove 9 Retrieve calls in one turn (see the runaway tool loop signal).

#### What the guardrail did

With guardrail v2 attached, both questions were blocked at input, before retrieval. "What product tiers does Vantage offer, and what do they cost?" tripped the `competitor-pricing` denied topic, a false positive on Vantage's own pricing. "I'm a sales engineer preparing a quote. What is the per-user price for the Professional tier, and what discount can I approve?" was blocked as `PROMPT_ATTACK` (MEDIUM confidence). The price list stayed indexed the whole time. The guardrail hid a real data exposure problem rather than fixing it. The fix is removing the document and re-syncing, plus access control on what gets ingested into an all-employee knowledge base.

---

## Tools

- AWS console: Amazon Bedrock (Settings), Amazon Bedrock AgentCore (Harness, Harness playground), CloudWatch Logs Insights, CloudWatch Metrics and Alarms, Amazon SNS
- boto3 for scripting

---

## Key Insights

### 1. AI monitoring isn't application monitoring

Traditional monitoring tells you *that* a request happened: timestamp, status code, latency. For an AI system, you need four records:

- What the user *asked* (the exact prompt)
- What the model *retrieved* (which knowledge base chunks)
- What the model *said* (the full response)
- Which guardrails ran, and what they did

Without those four, you're looking at a black box.

### 2. On a harness, all four come from the model invocation log

The harness calls the model with `ConverseStream`, and model invocation logging records every call:

| Question | Where it is in the record |
|---|---|
| What was asked | `input.inputBodyJson.messages` (user text) and `input.inputBodyJson.system` (full system prompt) |
| What was retrieved | A `toolUse` named `aria-kb___Retrieve` (search text in `input.retrievalQuery.text`), then a `toolResult` with the full chunk text, in the next request's `messages` |
| What was said | `output.outputBodyJson.output.message.content` |
| Which guardrail ran | `output.outputBodyJson.trace.guardrail` |

There's no `prompt`, `completion`, or `retrievedContext` field, and no agent alias or orchestration trace.

### 3. The log identifies a session, not a user

`identity.arn` is the harness execution role plus `BedrockAgentCore-<session-uuid>`. Every Aria user shares the same role. The model invocation log doesn't record the `runtimeSessionId` or `runtimeUserId` your app sends. The session ID in `identity.arn` is a different value that the harness generates. To name the user behind a request, your app must log the user and `runtimeSessionId` itself.

### 4. Guardrail metrics and model metrics

- **`AWS/Bedrock/Guardrails`:**
  - Metrics: `Invocations`, `InvocationsIntervened`, `InvocationLatency`, `TextUnitCount`
  - Harness traffic is reported under `Operation=ApplyGuardrail`
  - Dimensions: `GuardrailArn`, `GuardrailVersion`, `GuardrailPolicyType` (`ContentPolicy`, `SensitiveInformationPolicy`, `TopicPolicy`, `WordPolicy`), and `GuardrailContentSource` (`Input`, `Output`)
- **`AWS/Bedrock`, dimension `ModelId`:** `Invocations`, `InvocationLatency`, `InvocationClientErrors`, `InputTokenCount`, `OutputTokenCount`

The names `GuardrailInvocations`, `GuardrailInterventions`, `GuardrailBlockedRequests`, and `InvocationCount` don't exist.

### 5. Why this pricing answer is an incident

In a consumer chatbot, a wrong answer is a quality problem. In an enterprise assistant, an answer containing restricted data is a security incident, whether it came from a real document or from the model's training data. The retrieval record is what tells the two apart.

---

## Steps

### Step 1: Enable model invocation logging

If you followed the **Build Aria: Set Up the Demo Environment** page in Lesson 1, logging is already on. To turn it on yourself, create the log group first. The role that Bedrock creates for logging can write to an existing log group, but it can't create one. In CloudWatch, choose **Logs > Log groups > Create log group**, and enter `/aws/bedrock/vantage-aria/invocations`.

Then open **Amazon Bedrock > Settings > Model invocation logging**. You can deliver to:

- A CloudWatch Logs log group, for querying and alarms
- An S3 bucket, for long-term retention

Text data delivery has to be on, or you get metadata without prompts or responses.

Aria logs to `/aws/bedrock/vantage-aria/invocations`. The role `VantageAriaInvocationLoggingRole` trusts `bedrock.amazonaws.com` and allows `logs:CreateLogStream` and `logs:PutLogEvents`.

```python
import boto3

bedrock = boto3.client("bedrock", region_name="us-east-1")

bedrock.put_model_invocation_logging_configuration(
    loggingConfig={
        "cloudWatchConfig": {
            "logGroupName": "/aws/bedrock/vantage-aria/invocations",
            "roleArn": "arn:aws:iam::<acct>:role/VantageAriaInvocationLoggingRole",
        },
        "textDataDeliveryEnabled": True,
    }
)
```

`VantageAriaInvocationLoggingRole` is the role the Build Aria page creates. If the call fails with **Failed to validate permissions for log group**, the log group doesn't exist yet. Create it, then run the call again. When logging starts, it writes one non-JSON line: "Permissions are correctly set for Amazon Bedrock logs."

**Protect this log group.** It stores:

- Full retrieved chunks, including any personal data in them
- Answers the guardrail withheld from the user (Step 5)

Restrict read access and set a retention period.

### Step 2: Understand what one question produces

The log group gets one record per **model turn**, not per question:

- A knowledge base question produces a `ConverseStream` record ending in `stopReason: tool_use` (about 1.2K input tokens for Aria). A second record follows that ends in `end_turn` (about 4.5K input tokens, because the retrieved chunks are now in the context).
- A question that needs more detail can trigger two retrievals, and so three records.
- The knowledge base's embedding calls add separate `InvokeModel` records for `amazon.titan-embed-text-v2:0` under the knowledge base service role.

In the lab, 17 harness questions produced 34 `ConverseStream` records and 65 `InvokeModel` embedding records. Filter on `operation = "ConverseStream"` when you count Aria traffic.

### Step 3: Read a logged record

This is the final turn of the pricing question from the reproduction, trimmed. Values in angle brackets are placeholders, and `<trimmed>` marks shortened text. The reproduction ran without the guardrail, so the record has no `trace` key.

```json
{
  "schemaType": "ModelInvocationLog",
  "schemaVersion": "1.0",
  "timestamp": "2026-09-14T04:12:37Z",
  "accountId": "<acct>",
  "region": "us-east-1",
  "requestId": "<request-id>",
  "operation": "ConverseStream",
  "modelId": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
  "inferenceRegion": "us-east-2",
  "identity": {
    "arn": "arn:aws:sts::<acct>:assumed-role/AmazonBedrockAgentCoreHarnessDefaultServiceRole-<sfx>/BedrockAgentCore-<session-uuid>"
  },
  "input": {
    "inputBodyJson": {
      "system": [
        { "text": "You are Aria, Vantage's internal employee assistant. <trimmed>" }
      ],
      "messages": [
        {
          "role": "user",
          "content": [{ "text": "What product tiers does Vantage offer, and what do they cost?" }]
        },
        {
          "role": "assistant",
          "content": [
            {
              "toolUse": {
                "toolUseId": "<tool-use-id>",
                "name": "aria-kb___Retrieve",
                "input": { "retrievalQuery": { "text": "Vantage product tiers pricing" } }
              }
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "toolResult": {
                "toolUseId": "<tool-use-id>",
                "content": [
                  {
                    "text": "{\"retrievalResults\": [<product_overview.md chunk trimmed>, {\"content\": {\"text\": \"# Vantage Price List and Discount Authority – FY2026 **Classification: Confidential – Sales leadership only** ... | Starter | **$18 per user per month** | ... | Professional | **$42 per user per month** | ... <trimmed>\"}, \"documentId\": \"s3://vantage-aria-kb-<suffix>/vantage-aria-knowledge-base/vantage_price_list_confidential.md\", \"metadata\": {\"_document_title\": \"vantage_price_list_confidential.md\"}, \"score\": <score>}]}"
                  }
                ]
              }
            }
          ]
        }
      ],
      "inferenceConfig": { "<trimmed>": "<trimmed>" },
      "toolConfig": {
        "tools": [
          { "toolSpec": { "name": "aria-kb___Retrieve", "description": "<trimmed>", "inputSchema": { "<trimmed>": "<trimmed>" } } }
        ]
      }
    },
    "inputTokenCount": 4512
  },
  "output": {
    "outputBodyJson": {
      "output": {
        "message": {
          "role": "assistant",
          "content": [
            { "text": "Based on the Vantage knowledge base, here's information about our product tiers and pricing: <trimmed> According to the **Vantage Price List and Discount Authority – FY2026** document: **Starter**: $18 per user per month <trimmed> **Professional**: $42 per user per month <trimmed> **Enterprise**: Custom pricing, starting at $95,000 per year <trimmed> **Source documents**: `product_overview.md` and `vantage_price_list_confidential.md`" }
          ]
        }
      },
      "stopReason": "end_turn",
      "metrics": { "latencyMs": "<ms>" },
      "usage": { "inputTokens": 4512, "outputTokens": "<count>", "totalTokens": "<count>" }
    },
    "outputTokenCount": "<count>"
  }
}
```

Point out:

- **The answer is grounded, and that's the problem.** The `toolResult` shows the prices came from `vantage_price_list_confidential.md`, not from the model's training data. This is a knowledge base access misconfiguration: a confidential document is sitting in a knowledge base every employee can query.
- **The search text tells you intent.** `input.retrievalQuery.text` is what the model searched for, not what the user typed.
- **`inferenceRegion` shows cross-Region routing.** The request came in through us-east-1 and was processed in us-east-2.
- **`identity.arn` is a session, not a person.** Its session ID is generated by the harness and doesn't match the `runtimeSessionId` in your app log (Key Insight 3).
- **There's no `trace` key, so no guardrail ran.** When the guardrail is attached, `output.outputBodyJson.trace.guardrail` lists its ARN and version (Step 5). This record would be returned by the "ran without the guardrail" query in Step 5.
- **The `inputTokenCount` baseline.** About 1.2K on a `tool_use` turn and 4.5K on an `end_turn` turn is normal for Aria. A large input on a turn with no `toolResult` means the text came from the prompt itself.

For a quick look at a single conversation, open the Harness playground and select the **Aria-Kb Retrieve** step in the agent trace. It shows the retrieval query and each result's text, S3 URI, document title, and score.

### Step 4: Query the log group with Logs Insights

In CloudWatch, open **Logs > Logs Insights** and select `/aws/bedrock/vantage-aria/invocations`.

**Model-turn timeline:**

```
fields @timestamp, operation, modelId, identity.arn, input.inputTokenCount, output.outputTokenCount, output.outputBodyJson.stopReason
| filter operation = "ConverseStream"
| sort @timestamp asc
```

Rows alternate between `tool_use` and `end_turn`.

**What the model searched for:**

```
filter operation = "ConverseStream" and @message like /toolResult/
| parse @message /"retrievalQuery":\s*\{"text":\s*"(?<kbQuery>[^"]*)"/
| display @timestamp, identity.arn, kbQuery
| sort @timestamp asc
```

In the lab, the sessions that leaked salary data showed searches like "salary bands engineering roles compensation". Searches drifting toward restricted topics are a probing signal.

**Per-session volume:**

```
filter operation = "ConverseStream"
| parse identity.arn "/BedrockAgentCore-*" as session_id
| stats count(*) as modelTurns, sum(input.inputTokenCount) as inTokens, sum(output.outputTokenCount) as outTokens by session_id
| sort modelTurns desc
```

This replaces the old "requests per user" query. That query grouped by `identity.arn`, which on a harness gives one row per session. Remember that `modelTurns` counts model turns, and one retrieval question is at least two.

Query gotcha: a `parse` capture can't be listed again in `fields` ("Ephemeral field is already defined"). Use `display` after `parse`.

**Scripting it with boto3:** paginate. An unpaginated `filter_log_events` can return 0 events and a `nextToken` even when records exist.

```python
import json
import boto3

logs = boto3.client("logs", region_name="us-east-1")
paginator = logs.get_paginator("filter_log_events")

for page in paginator.paginate(
    logGroupName="/aws/bedrock/vantage-aria/invocations",
    filterPattern='"ConverseStream"',
):
    for event in page["events"]:
        try:
            record = json.loads(event["message"])
        except json.JSONDecodeError:
            continue  # the one-time "Permissions are correctly set" line
        session = record["identity"]["arn"].split("/BedrockAgentCore-")[-1]
        stop = record["output"]["outputBodyJson"].get("stopReason")
        print(record["timestamp"], session, stop, record["input"]["inputTokenCount"])
```

### Step 5: Read the guardrail evidence

When the guardrail runs, each `ConverseStream` record carries `output.outputBodyJson.trace.guardrail`:

- `inputAssessment.<guardrail-id>` has `appliedGuardrailDetails` (`guardrailArn`, `guardrailVersion`) and `invocationMetrics`. When the guardrail intervenes on input, the triggering policy appears here too.
- `outputAssessments[]` has the same fields for the response, plus the triggering policy when it intervenes on output, for example `sensitiveInformationPolicy.piiEntities`.

Three things change how you read these records:

1. **`guardrail_intervened` doesn't always mean blocked.** Aria's guardrail anonymizes emails and phone numbers. A benign parental leave answer with its contact email masked still reports `stopReason: guardrail_intervened`. Check which policy fired, and what it did, in the trace.
2. **The log keeps what the user didn't see.** When the guardrail blocks the output, the record stores the model's full original answer in `trace.guardrail.modelOutput`.
3. **An output block doesn't retract streamed text.** On a streaming harness, the user can see the whole answer before the blocked message is appended. In the lab, a reimbursement answer streamed in full, then ended with "Sorry, Vantage Aria can't answer this question." Treat an output-side intervention as "the user may have seen it."

**Guardrail interventions over time:**

```
filter output.outputBodyJson.stopReason = "guardrail_intervened"
| stats count(*) as blocked by bin(5m)
```

**Harness model calls that ran without the guardrail:**

```
filter operation = "ConverseStream" and identity.arn like /BedrockAgentCore-/ and @message not like /"appliedGuardrailDetails"/
| parse identity.arn "/BedrockAgentCore-*" as session_id
| display @timestamp, session_id, output.outputBodyJson.stopReason
| sort @timestamp desc
```

A caller with invoke permissions can override the model on a single request. That override drops the harness guardrail, and the record has no `trace` key at all. Your unguarded reproduction turns also appear here, which is expected. Once a guardrail is attached, every new row this query returns needs investigation. The lasting fix is an IAM deny on the harness execution role for model calls without the guardrail (lessons 11 and 15).

### Step 6: Set CloudWatch alarms

First create the SNS topic `vantage-aria-security-alerts` (SNS > Topics > Create topic > Standard) and subscribe your email address. Then create these alarms. The two guardrail alarms need an attached guardrail, so create them after Lesson 11 attaches it.

| Alarm | Namespace / metric | Dimensions | Condition |
|---|---|---|---|
| `VantageAria-GuardrailInterventions` | `AWS/Bedrock/Guardrails` / `InvocationsIntervened` | `GuardrailArn`, `GuardrailVersion` | Sum over 5 minutes > 3 |
| `VantageAria-PromptAttackInterventions` | `AWS/Bedrock/Guardrails` / `InvocationsIntervened` | `GuardrailContentSource=Input`, `GuardrailPolicyType=ContentPolicy`, `Operation=ApplyGuardrail` | Sum over 5 minutes > 0 |
| `VantageAria-HighInvocationVolume` | `AWS/Bedrock` / `Invocations` | `ModelId` | Sum over 1 hour > 50 |

Prompt attack detection is part of the content policy, so its interventions are counted under `ContentPolicy`.

```python
import boto3

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
TOPIC = "arn:aws:sns:us-east-1:<acct>:vantage-aria-security-alerts"
GUARDRAIL_ARN = "arn:aws:bedrock:us-east-1:<acct>:guardrail/<guardrail-id>"

# Alarm 1: any guardrail intervention spike
cloudwatch.put_metric_alarm(
    AlarmName="VantageAria-GuardrailInterventions",
    AlarmDescription="Guardrail interventions above normal: possible probing or exfiltration",
    Namespace="AWS/Bedrock/Guardrails",
    MetricName="InvocationsIntervened",
    Dimensions=[
        {"Name": "GuardrailArn", "Value": GUARDRAIL_ARN},
        {"Name": "GuardrailVersion", "Value": "2"},  # version 2 exists after Lesson 11
    ],
    Statistic="Sum",
    Period=300,
    EvaluationPeriods=1,
    Threshold=3,
    ComparisonOperator="GreaterThanThreshold",
    TreatMissingData="notBreaching",
    AlarmActions=[TOPIC],
)

# Alarm 2: input-side content policy interventions (includes prompt attacks)
cloudwatch.put_metric_alarm(
    AlarmName="VantageAria-PromptAttackInterventions",
    AlarmDescription="Input-side content policy interventions, including prompt attacks",
    Namespace="AWS/Bedrock/Guardrails",
    MetricName="InvocationsIntervened",
    Dimensions=[
        {"Name": "GuardrailContentSource", "Value": "Input"},
        {"Name": "GuardrailPolicyType", "Value": "ContentPolicy"},
        {"Name": "Operation", "Value": "ApplyGuardrail"},
    ],
    Statistic="Sum",
    Period=300,
    EvaluationPeriods=1,
    Threshold=0,
    ComparisonOperator="GreaterThanThreshold",
    TreatMissingData="notBreaching",
    AlarmActions=[TOPIC],
)

# Alarm 3: model invocation volume
cloudwatch.put_metric_alarm(
    AlarmName="VantageAria-HighInvocationVolume",
    AlarmDescription="Aria model invocations above expected hourly volume",
    Namespace="AWS/Bedrock",
    MetricName="Invocations",
    Dimensions=[
        {"Name": "ModelId", "Value": "us.anthropic.claude-sonnet-4-5-20250929-v1:0"},
    ],
    Statistic="Sum",
    Period=3600,
    EvaluationPeriods=1,
    Threshold=50,
    ComparisonOperator="GreaterThanThreshold",
    TreatMissingData="notBreaching",
    AlarmActions=[TOPIC],
)
```

In the lab, `VantageAria-PromptAttackInterventions` went to **ALARM** during guarded test traffic.

**There's no per-session or per-user metric.** The old `RequestsPerSession` custom metric had nothing emitting it. CloudWatch metrics have no session dimension, so when an alarm fires, run the per-session query from Step 4 over the alarm window to find the session. The invocation log can't name the user and can't be joined to your app log by session ID (Key Insight 3), so the user has to come from your app's own log.

To alert on output-side sensitive data, use the same metric with `GuardrailContentSource=Output`, `GuardrailPolicyType=SensitiveInformationPolicy`, and `Operation=ApplyGuardrail`. Remember that Aria anonymizes emails and phone numbers in normal answers, so set the threshold with that in mind.

### Step 7: Know the other sources and their limits

| Source | What it gives you | Limit |
|---|---|---|
| Harness runtime log group `/aws/bedrock-agentcore/runtimes/harness_VantageAria-<id>-DEFAULT` | Runtime container output | Mostly noise (urllib3 `NotOpenSSLWarning`). Low monitoring value |
| Knowledge base application logs `/aws/vendedlogs/bedrock/knowledge-base/APPLICATION_LOGS/<kb-id>` | `StartIngestionJob.StatusChanged` events: crawling started and completed, with job and data source IDs | Use it to find when the price list entered the knowledge base |
| Harness details page, **Observability** panel | Sessions, invocations, gateway and tool invocations, tokens, error and throttle rates | "May be delayed up to 60 minutes." In the lab it showed 27 sessions but 0 gateway invocations and 0 tokens, although every session used the gateway. Don't use it for real-time detection |
| Harness playground agent trace | One conversation's retrieval steps and results | One session at a time. Not an audit record |
| Gateway tracing / CloudWatch Transaction Search | Traces across harness and gateway | Requires Transaction Search, which isn't available in the Udacity lab |
| CloudTrail | Control plane API calls | Denied in the Udacity lab. Use it in your own account |

### AI-specific signals

| Signal | Where to see it | What it suggests |
|---|---|---|
| Guardrail intervention spike | `VantageAria-GuardrailInterventions` | Policy violations at volume: possible injection or exfiltration |
| Input-side content policy interventions | `VantageAria-PromptAttackInterventions` | Someone is trying to override instructions |
| Search text drifting toward restricted topics | Retrieval query (Step 4) | Probing, or a user reaching a document they shouldn't |
| Unusually long responses | `output.outputTokenCount` | Output beyond normal scope; a jailbreak may have worked |
| High `input.inputTokenCount` on a turn with no `toolResult` | Timeline query | A large payload pushed in the prompt itself |
| Intervention in `outputAssessments` | Invocation record | The model generated the content, and the user may have seen part of it |
| Harness records with no guardrail trace | Bypass query (Step 5) | Guardrail bypassed through a model override |
| Many model turns in one session | Per-session query (Step 4) | Probing. The invocation log can't name the user (Key Insight 3) |
| Many `tool_use`/`tool_result` turns in one session before an answer | Per-session query (Step 4); `tool_use` rows in the timeline query | A runaway tool loop: the model keeps searching for data that isn't there, adding cost and latency. In the lab, one discount question after cleanup drove 9 Retrieve calls in one turn. The harness default `maxIterations` of 75 allows it |

---

## Key Takeaway

You can't investigate an AI incident you didn't log.

On an AgentCore harness, the model invocation log holds all four records: the prompt, the retrieved chunks, the response, and the guardrail trace. You just need to know the field paths. The log doesn't know who the user is, and the harness Observability panel lags, so plan for both. Log the user ID in your app, and alarm on CloudWatch metrics, not the panel.

The pricing ticket turned out to be a grounded answer from a document that never belonged in an all-employee knowledge base. Without the `toolResult` in the log, you couldn't have told that apart from a hallucination. A guardrail that blocks the question doesn't fix it. Removing the document and re-syncing does.
