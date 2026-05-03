# services/ai_service.py
# Uses OpenRouter (free AI)

import requests

from utils.config import OPENROUTER_API_KEY
from utils.prompts import (
    risk_explanation_prompt,
    mitigation_prompt,
    summary_prompt,
    compliance_prompt,
    web_search_prompt
)

MODEL_NAME = "openai/gpt-3.5-turbo"

def call_ai(prompt_text):
    """Send prompt to OpenRouter and return response."""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ]
            },
            timeout=30
        )

        data = response.json()

        # Debug print (optional but useful)
        print("OpenRouter response:", data)

        if response.status_code == 200:
            return data["choices"][0]["message"]["content"]

        return f"API Error: {data}"

    except Exception as e:
        print("OpenRouter Error:", e)

        return (
            "Risk Analysis: Unable to generate AI response at the moment. "
            "Please review the risk and apply appropriate mitigation."
        )

def generate_risk_explanation(category, probability, impact, severity, description):
    prompt = risk_explanation_prompt(category, probability, impact, severity, description)
    return call_ai(prompt)


def generate_mitigation(category, probability, impact, severity, description):
    prompt = mitigation_prompt(category, probability, impact, severity, description)
    return call_ai(prompt)


def generate_summary(category, probability, impact, severity, description):
    prompt = summary_prompt(category, probability, impact, severity, description)
    return call_ai(prompt)


def generate_compliance(category, probability, impact, severity, description):
    prompt = compliance_prompt(category, probability, impact, severity, description)
    return call_ai(prompt)


def generate_from_web_content(query, fetched_content):
    prompt = web_search_prompt(query, fetched_content)
    return call_ai(prompt)