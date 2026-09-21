# Exercise: Create the ML-BOM for ClinicalCompanion

**Estimated Time:** 45 minutes

---

## Overview

In this exercise you will document all AI components in the ClinicalCompanion system by completing an ML-BOM using the provided template. You will cover both models that make up the RAG pipeline, characterize their roles, and produce an attestation-ready document that could be submitted to a compliance or security review.

This is a documentation and analysis exercise. There is no code to run. The skill being practiced is systematic AI component inventory — identifying every model in a system, understanding what each one does, and capturing the security-relevant details that a threat model depends on.

---

## Scenario

You work as an **AI Security Engineer at Cascadia Health**, a regional health system. The clinical informatics team has built ClinicalCompanion — a RAG assistant deployed on an Amazon Bedrock AgentCore harness that allows clinical staff (nurses, hospitalists, and pharmacists) to query internal clinical guidelines, formulary data, discharge procedure checklists, and regulatory compliance documentation.

Before the system goes live in a production clinical environment, the Chief Information Security Officer and compliance team require an ML-BOM covering every AI model in the system. The CISO's message to you:

> "I need a complete inventory of every AI model in this pipeline — not just the chatbot. Each model needs full documentation: what it does, what it was trained on to the extent we can determine, what it can be misused for, and who is accountable for it. This is going into our HIPAA risk assessment documentation. Don't leave blanks — if the vendor doesn't disclose something, document that the information is not available and why that matters."

ClinicalCompanion uses two AI models:

- **Amazon Titan Text Embeddings V2** — converts clinical staff queries and knowledge base documents into vector embeddings, which are stored and searched in a Managed Knowledge Base vector store. Accessed via Amazon Bedrock as a managed service.
- **Anthropic Claude Sonnet 4.5** — receives the clinical staff member's original question plus the top retrieved document chunks and generates a grounded natural-language answer with citations.

Both models are accessed as managed API services through AWS Bedrock. Neither runs on Cascadia Health's own infrastructure.

---

## Tools

- `starter/ML_BOM_TEMPLATE.md` — your starting point; save your completed version as `ML_BOM_COMPLETED.md`
- The harness configuration — the **Configs** panel in the Harness playground or the `GetHarness` API — to confirm the saved model ID and inference profile (Amazon Bedrock no longer has a model access page)
- Anthropic model documentation: https://docs.anthropic.com/en/docs/about-claude/models
- Amazon Titan Embeddings documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html

---

## Tasks

### Task 1 — Document Model 1: Amazon Titan Text Embeddings V2

Fill in all fields in the Model 1 section for this model.

Answer these questions as you fill it in:

- **Model type:** Does this model produce text, or something else? What would go wrong in the threat model if you classified it as a generation model?
- **Architecture:** Is it an encoder or a decoder? Given that, does a compromise of this model threaten what gets retrieved, or what text the system outputs?
- **Input and output:** What is the maximum input size, and what exactly does the model output? Check the Amazon Titan Embeddings documentation.
- **Intended use:** What does ClinicalCompanion use this model for?
- **Misuse:** This model can't output text. How could an attacker use it to change which clinical content reaches the generation model? Consider poisoning retrieval and embedding collisions.

---

### Task 2 — Document Model 2: Anthropic Claude Sonnet 4.5

Fill in all fields in the Model 2 section.

Answer these questions as you fill it in:

- **Training data:** Claude Sonnet 4.5 is a managed API, and Anthropic doesn't disclose the composition of its training dataset. What can you record as known, and what must you record as not disclosed? In a HIPAA risk assessment, what can't Cascadia Health verify because of that gap?
- **Architecture:** What architecture does the model use, and which alignment method has Anthropic published? Why does the alignment method matter when someone sends the model an adversarial prompt?
- **Input and output:** What goes into the model's input in this RAG system? What are the maximum input and output sizes? Check the Anthropic model documentation.
- **Misuse:** Cover these three, and describe each one for a clinical setting:
  - Prompt injection that tries to extract the system prompt or non-public formulary data
  - Clinical recommendations that aren't grounded in the retrieved guidelines. Why is this a patient safety issue and not only a quality issue?
  - Indirect injection through poisoned clinical documents in the knowledge base

---

### Task 3 — Document Software Dependencies and Hardware Requirements

For each model, answer these questions:

- **Software dependencies:** Which SDK does the application use, and which AgentCore API does it call instead of calling the model directly?
- **Hardware requirements:** Who manages the hardware each model runs on, and can Cascadia Health access it? What can't Cascadia Health attest to because of that? Which agreement with AWS governs the hardware security posture for the HIPAA risk assessment?

---

### Task 4 — Fill in the Model Lineage Section

For each model, what is publicly known about its parent model, its base model, and any post-training adaptation? Where a detail isn't disclosed, record that it isn't disclosed and who doesn't disclose it. Don't leave a lineage field blank.

---

### Task 5 — Complete the Attestation Table and System Overview

Fill in the attestation table (preparer, date, review date, attestation statement).

Write a 2-sentence system overview explaining how Titan Text Embeddings V2 and Claude Sonnet 4.5 work together in the ClinicalCompanion RAG pipeline. Make clear that these are two distinct models with distinct security failure modes: a failure in the embedding model threatens what clinical content reaches the generation model; a failure in the generation model threatens what clinical information is returned to the clinician.

---

## Key Takeaway

In a RAG system, two models serve completely different roles. In a clinical context, this distinction is patient safety-critical: the embedding model governs which clinical guidelines are retrieved, and the generation model governs how that guidance is presented to the clinician. A threat model that inventories only the generation model misses an entire attack class — retrieval poisoning — that can cause the system to surface contraindicated clinical content without the generation model ever "misbehaving."

---

## Deliverable

Save your completed template as `ML_BOM_COMPLETED.md` in this directory.

---

## Connection to the Capstone

In Project Task 2, you will create an AI asset inventory (ML-BOM) for the live Northstar Assist system you have deployed. That deliverable builds directly on what you practice here — with your actual foundation model and Titan embedding model, your knowledge source, vector store, and gateway, your harness, gateway, and knowledge base service roles, a training-data disclosure, and a system overview.
