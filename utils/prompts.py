# utils/prompts.py
# All AI prompts live here. Good prompts = good AI output.

def risk_explanation_prompt(category, probability, impact, severity, description):
    return f"""
You are a senior financial risk analyst writing for business stakeholders.

Given this risk data:
- Risk Category: {category}
- Probability: {probability}/10
- Impact: {impact}/10
- Severity: {severity}
- Description: {description}

Write a clear, plain-English explanation of this risk (3-4 sentences).
Avoid jargon. Make it suitable for a non-technical executive audience.
"""

def mitigation_prompt(category, probability, impact, severity, description):
    return f"""
You are a risk management expert.

For this financial risk:
- Category: {category}
- Probability: {probability}/10
- Impact: {impact}/10
- Severity: {severity}
- Description: {description}

Provide exactly 4 specific mitigation strategies. Number each one.
Each strategy should be actionable and concrete.
"""

def summary_prompt(category, probability, impact, severity, description):
    return f"""
You are a risk reporting specialist.

Create a structured risk summary report for:
- Category: {category}
- Probability: {probability}/10
- Impact: {impact}/10
- Severity: {severity}
- Description: {description}

Format your response EXACTLY like this:
Risk Title: [title]
Risk Level: [Low/Medium/High/Critical]
Probability Score: {probability}/10
Impact Score: {impact}/10
Risk Explanation: [2 sentences]
Recommended Actions: [3 bullet points]
Priority Level: [Immediate/Short-term/Long-term]
"""

def compliance_prompt(category, probability, impact, severity, description):
    return f"""
You are a compliance officer drafting regulatory documentation.

Write a professional compliance commentary for the following risk:
- Category: {category}
- Probability: {probability}/10
- Impact: {impact}/10
- Severity: {severity}
- Description: {description}

The commentary should:
1. Reference relevant regulatory frameworks (Basel III, COSO, ISO 31000 where appropriate)
2. Be suitable for inclusion in an audit report
3. Use formal, professional language
4. Be 3-4 paragraphs long
"""

def web_search_prompt(query, fetched_content):
    return f"""
You are a financial risk researcher.

The user asked: "{query}"

Here is relevant content retrieved from the web:
{fetched_content[:3000]}

Based on this content, provide a helpful, accurate summary relevant to financial risk management.
Keep your response to 3-4 paragraphs.
"""