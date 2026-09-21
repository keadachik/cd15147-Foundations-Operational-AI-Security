# AI Threat Modeling and Operational Defense: Exercises

This repository contains the demos and hands-on exercises for the course **AI Threat Modeling and Operational Defense**. Each skill-pair folder goes with one implementation lesson and practices one security skill.

---

## Prerequisites

Before starting any exercise:

1. Complete the setup walkthrough in `skill-pair-00-bedrock-setup/WALKTHROUGH.md` (the same steps are on the **Build Aria: Set Up the Demo Environment** page in Lesson 1). It builds **Aria**, the demo assistant used by every `DEMO.md`, in `us-east-1`: an Amazon Bedrock AgentCore harness, an AgentCore Gateway, and a Managed Knowledge Base. There's no model access step; models are available on first use. Plan about 2 hours for your first run.
2. Have Python 3.10+ with the packages in `requirements.txt` (`pip install -r requirements.txt`). The harness API needs `boto3>=1.43.52`.
3. Install the AWS CLI. Some demos give AWS CLI commands.
4. Connect to your AWS account. Paste your Udacity Cloud Lab credentials from the **Cloud Resources** tab into `aws-credentials.txt`, save the file, and run `python setup_aws.py` from the repository root. Do this again each time your lab session restarts. `WALKTHROUGH.md` Step 8 has the details. If you use your own AWS credentials instead, they need access to Amazon Bedrock, Amazon Bedrock AgentCore (`bedrock-agentcore:*` actions aren't covered by `bedrock:*`), S3, CloudWatch Logs, and basic IAM read access.

---

## Exercise Order

Work through the skill-pairs in lesson order. Later exercises build on concepts introduced earlier. The folder numbers follow the lesson order except for `skill-pair-09`, which goes with Lesson 12.

| Lesson | Directory | Concept | Scenario |
|--------|-----------|---------|----------|
| 1 | `skill-pair-00-bedrock-setup` | Demo environment setup (harness, gateway, knowledge base) | Aria — Vantage Technologies (demo system) |
| 3 | `skill-pair-01-stride-ml` | STRIDE-ML threat modeling | FinQuery — Meridian Analytics |
| 5 | `skill-pair-02-ml-bom` | ML Bill of Materials | ClinicalCompanion — Cascadia Health |
| 7 | `skill-pair-03-secure-model-serving` | Secure model serving & IAM | CaseAssist — Apex Legal |
| 9 | `skill-pair-04-monitoring-ir` | Monitoring & incident response | OpsGuide — NovaTech |
| 11 | `skill-pair-05-input-sanitization` | Input sanitization & Guardrails | BankBot — FirstLight Bank |
| 12 | `skill-pair-09-differential-privacy` | PII detection & data classification | MyHealth Assistant — Westfield Health |
| 13 and 15 | `skill-pair-06-least-privilege` | IAM policies, SCPs & least privilege (Lesson 13 demo: `DEMO_ACCESS_ANALYZER.md`; Lesson 15 demo: `DEMO.md`) | ResearchBot — GenCore Pharma |
| 17 | `skill-pair-07-data-provenance` | Data provenance & KB validation | KnowledgeHub — Vertex Consulting |
| 19 | `skill-pair-08-rate-limiting` | Rate limiting & cost controls | Orion API — Orion AI |

---

## How to Use Each Exercise

Each skill-pair directory contains:

- **`EXERCISE.md`** — Your starting point. Read this first. It lists tasks, deliverables, and learning objectives.
- **`starter/`** — Starter files, worksheets, and any data files you need.
- **`solutions/`** — The answer key. Attempt every task before you open it.
- **`DEMO.md`** (some exercises) — A console or code walkthrough demonstrating the concept on Aria, the Vantage Technologies demo system from skill-pair-00, before you apply it to the exercise scenario.

### Recommended workflow

1. Read `EXERCISE.md` fully before starting.
2. If a `DEMO.md` exists, follow it to observe the concept on Aria.
3. Complete the tasks using the files in `starter/`.
4. Save your answers in the files and folder that `EXERCISE.md` names.
5. Compare your work to `solutions/` after you have attempted all tasks.

---

## Capstone Connection

Skill-pair-00 sets up **Aria**, the internal employee assistant of the fictional Vantage Technologies. Aria is the demonstration system for the course videos and every `DEMO.md`, so you can observe each security concept in a working environment. Each numbered exercise then has you apply the same concept to a different industry scenario, reinforcing transfer of the skill.

The capstone project has you build **Northstar Assist** on the same architecture (harness → AgentCore Gateway → Managed Knowledge Base, with a Bedrock guardrail and invocation logging), so the setup you practice with Aria carries directly into the project.
