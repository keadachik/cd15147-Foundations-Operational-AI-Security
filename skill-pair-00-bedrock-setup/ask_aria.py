"""Ask Aria questions from the terminal.

Before you run it, finish WALKTHROUGH.md Step 4 (create the harness), paste your
credentials and harness ARN into aws-credentials.txt, and run `python setup_aws.py`
from the repository root. Then, from the repository root:

    python skill-pair-00-bedrock-setup/ask_aria.py
    python skill-pair-00-bedrock-setup/ask_aria.py "What is Vantage's remote work policy?"

With no question, it starts a conversation. Follow-up questions share one harness
session. Type /new to start a new session and /quit to stop. Every question is billed.
"""
import os
import sys
import uuid
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

# setup_aws.py writes the harness ARN and region to .env in the repository root.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

CREDENTIAL_ERROR_CODES = {
    "ExpiredToken",
    "ExpiredTokenException",
    "InvalidClientTokenId",
    "InvalidSignatureException",
    "SignatureDoesNotMatch",
    "UnrecognizedClientException",
}


def is_credential_error(error):
    """True when AWS credentials are missing, expired, or not recognized."""
    if isinstance(error, (NoCredentialsError, PartialCredentialsError)):
        return True
    if not isinstance(error, ClientError):
        return False
    details = error.response.get("Error", {})
    # The harness API reports a bad or expired token as AccessDeniedException, so check the message too.
    return (details.get("Code") in CREDENTIAL_ERROR_CODES
            or "security token included in the request" in details.get("Message", ""))


def ask(harness_arn, region, session_id, question):
    """Send one question to the harness and print the answer as it streams in."""
    # A new Session reads ~/.aws/credentials again, so rerunning setup_aws.py takes effect
    # right away. Bounded timeouts and no automatic retries: a retry sends the question
    # into the same session again and adds model calls (lesson 19).
    client = boto3.session.Session().client(
        "bedrock-agentcore",
        region_name=region,
        config=Config(connect_timeout=10, read_timeout=120, retries={"total_max_attempts": 1}),
    )
    response = client.invoke_harness(
        harnessArn=harness_arn,
        runtimeSessionId=session_id,
        messages=[{"role": "user", "content": [{"text": question}]}],
    )

    # The harness streams every model turn, including text before and after a tool call.
    stop_reason = None
    for event in response["stream"]:
        if "contentBlockStart" in event:
            tool_use = event["contentBlockStart"]["start"].get("toolUse")
            if tool_use:
                print(f"\n[tool call: {tool_use['name']}]", flush=True)
        elif "contentBlockDelta" in event:
            text = event["contentBlockDelta"]["delta"].get("text")
            if text:
                print(text, end="", flush=True)
        elif "messageStop" in event:
            stop_reason = event["messageStop"]["stopReason"]
        elif "runtimeClientError" in event:
            raise RuntimeError(event["runtimeClientError"].get("message", "Runtime error"))
    print(f"\n[stop reason: {stop_reason}]")


def ask_and_report(harness_arn, region, session_id, question):
    """Ask one question and explain any error. Returns True when Aria answered."""
    print("Aria: ", end="", flush=True)
    try:
        ask(harness_arn, region, session_id, question)
        return True
    except Exception as error:
        if is_credential_error(error):
            print("\nYour AWS credentials are missing or expired. Paste fresh credentials from the "
                  "Cloud Resources tab into aws-credentials.txt in the repository root, run "
                  "`python setup_aws.py`, and ask again.")
        else:
            print(f"\nError: {error}")
        return False


def main():
    harness_arn = os.environ.get("AGENTCORE_HARNESS_ARN", "")
    region = os.environ.get("AWS_REGION", "us-east-1")
    if not harness_arn:
        print("AGENTCORE_HARNESS_ARN isn't set. Paste your harness ARN into aws-credentials.txt "
              "in the repository root, then run `python setup_aws.py`.")
        return 1

    session_id = str(uuid.uuid4())  # a harness session ID must be at least 33 characters; a UUID is 36
    if len(sys.argv) > 1:
        return 0 if ask_and_report(harness_arn, region, session_id, " ".join(sys.argv[1:])) else 1

    print("Ask Aria a question. Type /new to start a new session or /quit to stop.")
    while True:
        try:
            question = input("\nYou: ").strip()
        except EOFError:
            print()
            return 0
        if question == "/quit":
            return 0
        if question == "/new":
            session_id = str(uuid.uuid4())
            print("Started a new session.")
        elif question:
            ask_and_report(harness_arn, region, session_id, question)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(130)
