import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from sympy import content
import json

# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# ENV_FILE = PROJECT_ROOT / ".env"

# load_dotenv(ENV_FILE)
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    # raise SystemExit(f"Missing GROQ_API_KEY in {ENV_FILE}")
    raise SystemExit(f"Missing GROQ_API_KEY in ENV FILE")

groq_client = Groq(api_key=api_key)


def build_messages(prompt):
    return [
        {
            "role": "user",
            "content": prompt,
        },
    ]

def llm_classify_log(log_msg):
    
    prompt = f'''"You are a log classification assistant.\n"
        "You MUST ONLY respond with a JSON object using exactly these keys:"
        " \"label\" (one of: \"Workflow Error\", \"Deprecation Warning\", \"Unclassified\")"
        " and \"confidence\" (a number between 0 and 1)."
        " Do not include any extra text, explanation, or markdown."
        Log Message: {log_msg}'''

    stream = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=build_messages(prompt),
        temperature=0.2,
        max_completion_tokens=64,
        top_p=1,
        # stream=True,
        stop=["\n\n"],
    )

    content = stream.choices[0].message.content
    label = json.loads(content)["label"]
    # confidence = json.loads(content).get("confidence")

    if label is None:
        label = "Unclassified"
    
    # return label.strip()+f" (confidence: {confidence})"
    return label.strip()


if __name__ == "__main__":

    log_messages = [
    
    "Lead conversion failed for prospect ID 7842 due to missing contact information.",
    "API endpoint 'getCustomerDetails' is deprecated and will be removed in version 3.2. Use 'fetchCustomerInfo' instead.",
    "Customer follow-up process for lead ID 5621 failed due to missing next action.",
    "Escalation rule execution failed for ticket ID 9807 - undefined escalation level.",
    "The 'ExportToCSV' feature is outdated. Please migrate to 'ExportToXLSX' by the end of Q3.",
    "Support for legacy authentication methods will be discontinued after 2025-06-01.",
    "Task assignment for TeamID 3425 could not complete due to invalid priority level."

    ]
    for log_message in log_messages:
        print(f"Log Message: {log_message}")
        print(f"Classification: {llm_classify_log(log_message)}")
        print()  # Add a blank line for readability
