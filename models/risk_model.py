# models/risk_model.py
# Data structure for a risk entry

def create_risk_record(category, probability, impact, severity, description, explanation, mitigation, summary, compliance):
    """Build a structured dict for one risk record."""
    return {
        "category":    category,
        "probability": probability,
        "impact":      impact,
        "severity":    severity,
        "description": description,
        # AI-generated fields:
        "explanation": explanation,
        "mitigation":  mitigation,
        "summary":     summary,
        "compliance":  compliance
    }