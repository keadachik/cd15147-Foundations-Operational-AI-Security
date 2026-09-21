# Exercise: Right-Size the ResearchBot IAM Roles

**Estimated Time:** 50 minutes
**Deliverables:** See below

---

## Overview

ResearchBot runs on an Amazon Bedrock AgentCore harness. The harness calls a knowledge base Retrieve tool through an AgentCore Gateway, and the gateway searches a Managed Knowledge Base. Three of its IAM roles were written under deadline pressure, and all three have least-privilege violations. Your job: identify the violations, write corrected policies, and describe how much you reduced the blast radius.

| Role (file) | What It Does |
|---|---|
| `agent_execution_role`: the harness execution role | The harness's identity: invokes the model and calls the gateway |
| `kb_sync_role`: the knowledge base service role | Bedrock assumes it during the nightly sync to read documents from S3 and create embeddings |
| `streamlit_app_role` | Attached to the ECS task running the Streamlit app: calls the harness |

The gateway service role, which runs `bedrock:Retrieve` on the knowledge base, isn't part of this exercise. The lesson demo scopes it.

---

## Scenario

**GenCore Pharma** is a pharmaceutical company in a regulated environment. FDA 21 CFR Part 11 applies to electronic records, and overly permissive IAM roles are a compliance finding. ResearchBot must be remediated before production.

Resource ARNs (you'll need these for your fixed policies):

| Resource | ARN / Name |
|---|---|
| Claude Sonnet 4.5 inference profile | `arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Claude Sonnet 4.5 foundation model (the profile routes to us-east-1, us-east-2, us-west-2) | `arn:aws:bedrock:<region>::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Titan Text Embeddings V2 | `arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0` |
| Knowledge Base | `arn:aws:bedrock:us-east-1:123456789012:knowledge-base/researchbot-kb-XXXXXXXX` |
| Guardrail | `arn:aws:bedrock:us-east-1:123456789012:guardrail/researchbot-guardrail-XXXXXXXX` |
| AgentCore Gateway | `arn:aws:bedrock-agentcore:us-east-1:123456789012:gateway/researchbot-gateway-XXXXXXXXXX` |
| AgentCore Harness | `arn:aws:bedrock-agentcore:us-east-1:123456789012:harness/ResearchBot-XXXXXXXXXX` |
| S3 Bucket | `arn:aws:s3:::gencore-research-kb` |
| CloudWatch Log Group | `/aws/researchbot/app-logs` |

---

## Tasks

### Task 1: Review all three roles and identify violations

Open each file in `starter/iam_roles/`. For each role, list every violation. Record what's over-permissive, what an attacker could do with it at GenCore (think about clinical trial data and regulatory submissions), and what it should be scoped to instead.

Write your findings in `starter/LEAST_PRIVILEGE_WORKSHEET.md`.

### Task 2: Write the three corrected policies

Create these files in `starter/iam_roles/`:

**`agent_execution_role_fixed.json`** needs:
- `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on the inference profile ARN and the three foundation model ARNs
- A **Deny** on the same two actions, on `*`, when `bedrock:GuardrailIdentifier` isn't the ResearchBot guardrail ARN (or `ARN:*`). Use the ARN condition operator `ArnNotLike`. `bedrock:GuardrailIdentifier` holds an ARN, and IAM Access Analyzer flags a string operator such as `StringNotLike` on it as a security warning.
- `bedrock:ApplyGuardrail` on the guardrail ARN
- `bedrock-agentcore:InvokeGateway` on the gateway ARN

This exercise covers only the request path. A deployed harness execution role also needs runtime statements for its own logs, ECR image pulls, X-Ray, and workload identity tokens. `DEMO.md` Step 3 shows them. A real harness with only these four statements can stop working.

**`kb_sync_role_fixed.json`** needs only:
- `bedrock:InvokeModel` on the Titan Text Embeddings V2 ARN
- `s3:ListBucket` on the bucket and `s3:GetObject` on the bucket's objects

**`streamlit_app_role_fixed.json`** needs only:
- `bedrock-agentcore:InvokeHarness` and `bedrock-agentcore:InvokeAgentRuntime` on the harness ARN
- `logs:CreateLogStream`, `logs:PutLogEvents`, and `logs:DescribeLogStreams` on the specific log group ARN

### Task 3: Fill in the blast radius comparison

In the worksheet's **Blast Radius Analysis** section, describe for each role what an attacker could do with the original policy and what they could do with the fixed policy. Then write a one-sentence reduction summary for the role.

After you finish all three roles, answer the worksheet's six **Reflection Questions**. The worksheet also has a **Console Notes** table, where you record your own AWS resource names and ARNs for the capstone project.

---

## Deliverables

```
starter/iam_roles/
  agent_execution_role_fixed.json
  kb_sync_role_fixed.json
  streamlit_app_role_fixed.json
starter/
  LEAST_PRIVILEGE_WORKSHEET.md   (violations, blast radius analysis, reflection answers)
```

After you finish all three tasks, compare your policies with the files in `solutions/iam_roles/`.

---

## Key Takeaway

In a regulated research environment, least privilege is a compliance requirement, not just a security recommendation. A role with `bedrock:*` can change guardrails, delete knowledge bases, and call any model directly. A role with `bedrock-agentcore:*` can reconfigure the harness itself. Scope each role to exactly what its hop needs, and the pivot paths a stolen credential would give an attacker are gone.

---

## Connection to the Capstone

Project Task 4 applies least-privilege access controls to your deployed Northstar Assist instance. You'll review your actual harness execution role and gateway service role, identify violations, scope the policies, and document a before/after comparison. This exercise is that skill practiced in isolation, with known inputs and known correct outputs to check against.
