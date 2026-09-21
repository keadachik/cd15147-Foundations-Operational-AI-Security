# Demo: Detect Overpermissive Policies with IAM Access Analyzer

> **Note:** This demo goes with Lesson 13, and the classroom demo page has the same steps. `DEMO.md` in this folder goes with Lesson 15.

### Before You Start This Demo

This demo uses Aria, the Vantage Technologies assistant you built on the **Build Aria: Set Up the Demo Environment** page in Lesson 1. If you haven't built Aria yet, do that first. The demo reads Aria's knowledge base bucket and its harness execution role, and it doesn't change Aria. The access preview never applies its bucket policy, and the lab can't attach the SCP.

Aria is the internal assistant at Vantage Technologies. It runs on an Amazon Bedrock AgentCore harness. The harness retrieves information from a knowledge base through an AgentCore Gateway.

This walkthrough answers two questions:

- How do you find permissions that nobody meant to grant?
- How do you stop those permissions from being granted again?

## Key Steps

### Step 1: Know What Access Analyzer Can See

Access Analyzer creates **external-access findings**, which are reports that a principal outside your account can reach a resource. These findings cover resources that have **resource policies**. A resource policy is attached directly to a resource, such as a bucket, and says which principals can use that resource. Supported resources include:

- S3 buckets
- IAM roles
- KMS keys
- Secrets Manager secrets
- Lambda functions
- SQS queues
- A few others

Knowledge bases, harnesses, and gateways aren't on that list. Aria's documents are stored in the S3 bucket `vantage-aria-kb-<suffix>`, so you analyze the bucket.

### Step 2: Preview a Proposed Change Before You Apply It

An **access preview** shows the findings that a policy would create, without applying the policy.

1. Create the analyzer if you don't have one. In IAM, choose **Access Analyzer**, and create an analyzer of type **Account** named `vantage-aria-analyzer`. This type of analyzer is free.
2. Create an **access preview** for a bucket policy on the Aria knowledge base bucket. In S3, open `vantage-aria-kb-<suffix>`, and choose **Permissions** > **Bucket policy** > **Edit**. Paste a bucket policy that grants account `111122223333` `s3:GetObject` and `s3:ListBucket`, and choose **Preview external access**. Don't save the policy.

The preview shows a **new, active** external-access finding. The policy itself is never applied.

In the Udacity Cloud Lab, you'll probably also see two other results. Neither one means your account is compromised:

- An **unchanged, active** finding for a **CanonicalUser** with write actions such as `s3:PutObject`. That canonical ID is your own account, as the owner of the bucket.
- Active findings on the lab's `voclabs` role, which external accounts can assume. That's how the lab signs you in. You can archive these findings.

### Step 3: Read the Finding in Detail

Three details matter:

- **Which resource is exposed:** `AWS::S3::Bucket`, the bucket that holds Aria's knowledge base documents
- **Which external principal can reach it:** account `111122223333`
- **What level of access the principal has:** read and list. The access isn't public.

You can't act on the finding until you can answer all three.

### Step 4: Check the Roles Aria Runs As

The harness calls the model with its **execution role** (`AmazonBedrockAgentCoreHarnessDefaultServiceRole-…`). An execution role is the IAM role that a service uses to act on your behalf. The harness doesn't use your identity.

Open that role in IAM, and check three things:

- **Last Accessed tab:** The role is granted 11 services, but it has used only 5 (`bedrock`, `bedrock-agentcore`, `ecr-public`, `logs`, `xray`).
- **Default execution policy:** It allows `bedrock:InvokeModel*` on `arn:aws:bedrock:*::foundation-model/*` and on `arn:aws:bedrock:us-east-1:<acct>:*`. That covers every model, instead of only the one Aria uses.
- **Policy validation:** Paste a policy into the IAM JSON editor to see its **Security**, **Errors**, **Warnings**, and **Suggestions** counts. Validation checks grammar and best practices. It doesn't tell you whether a policy is too broad, or whether an allow-list matches the Regions your inference profile uses. In the lab, validation reported 0 findings both for the example SCP below and for a policy that grants `bedrock:*` on `*`.

### Step 5: Read an Organization-Level Policy That Restricts Models

The lab is a single account without AWS Organizations access. So you can't create or attach this service control policy (SCP). Instead, read it and reason about what it blocks.

Aria's harness saves the model `us.anthropic.claude-sonnet-4-5-20250929-v1:0`. This ID is a US **cross-Region inference profile**, which sends each request to the model in one of several AWS Regions. So an allow-list has to name the inference profile **and** the foundation model it routes to.

A **condition key** is a value that a policy can check in its `Condition` block, such as the Region a request is sent to. Bedrock has no `bedrock:ModelId` condition key. To restrict models, you can match on either:

- Resource ARNs, as in the policy below
- The `bedrock:ModelArn` and `bedrock:InferenceProfileArn` condition keys

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnapprovedModels",
      "Effect": "Deny",
      "Action": "bedrock:InvokeModel*",
      "NotResource": [
        "arn:aws:bedrock:us-east-1:*:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
        "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
        "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0"
      ]
    },
    {
      "Sid": "DenyUnapprovedRegions",
      "Effect": "Deny",
      "Action": "bedrock:InvokeModel*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-east-2", "us-west-2"]
        }
      }
    }
  ]
}
```

> **Region note:** A cross-Region inference profile can send a request to a Region other than the one you call. So a Region allow-list must include every Region that the inference profile uses. In the lab, Aria's invocation logs showed inference running in `us-east-2`. A scoped harness role that allowed the Claude Sonnet 4.5 foundation model in `us-east-1`, `us-east-2`, and `us-west-2` kept working. That's why this policy names the foundation model in all three Regions and allows all three Regions. It also allows Titan Text Embeddings V2, which the knowledge base uses to create embeddings during sync. If you leave Titan out, knowledge base sync fails. This policy wasn't tested in the lab, because the lab account can't use AWS Organizations.

Ask yourself two questions:

- If a team calls a different model, which statement denies the request?
- Why does the Region list include `us-east-2`? (Hint: The invocation logs showed Aria's inference running in that Region.)

## Why It Works

### An SCP Sets a Permission Ceiling

A service control policy sets a permission ceiling. It doesn't grant any permissions. No IAM policy in any member account can go beyond it, so an SCP is a different kind of control from account-level least privilege. If an account administrator grants a broad permission locally, that permission still can't go past the organization's ceiling.

Because of this, an SCP gives you consistent enforcement. Least privilege applied account by account depends on every team doing the work correctly and continuing to do it. An organization-level ceiling applies no matter how each account is configured. It's the only way to enforce rules consistently across teams you don't control.

### Access Analyzer Finds Unintended Access

Access Analyzer handles the other part of the problem. Over time, policies drift, resources get shared, and trust relationships build up.

- **External-access findings** show when the storage behind an AI resource, such as the bucket that holds knowledge base documents, becomes reachable from outside the account.
- **An access preview** catches that exposure before the policy is applied.
- **Last accessed data and policy validation** show when a role can do far more than its workload needs.

### Restricting by Model

Model restriction deserves special attention. An organization can approve a set of models and enforce that decision everywhere. It doesn't have to trust each team to invoke only the models that were reviewed.

The harness uses inference profiles, so the approved list has to name both the profile and the foundation models behind it.

> **Cost note:** Access Analyzer also offers an **unused access** analyzer, which flags unused roles and permissions. It's billed per IAM role or user per month. If you try it, delete it when you're done.

## Related Resources

- `skill-pair-06-least-privilege/starter/iam_roles/trust_policies/` holds the cross-account trust policy examples used in the exercise.
