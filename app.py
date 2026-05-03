# app.py
# Main Flask application — all routes defined here

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.config import SECRET_KEY
from services.auth_service import login_user, is_logged_in, is_admin
from services.ai_service import (
    generate_risk_explanation,
    generate_mitigation,
    generate_summary,
    generate_compliance,
    generate_from_web_content
)
from services.memory_service import save_risk_record, get_risk_history, save_key_for_user
from services.dataset_loader import load_sample_risks
from services.websearch_service import search_web

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ─── AUTH ROUTES ────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    if is_logged_in(session):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = login_user(username, password)
        if user:
            session["username"] = username
            session["role"]     = user["role"]
            session["name"]     = user["name"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─── DASHBOARD ──────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if not is_logged_in(session):
        return redirect(url_for("login"))
    
    samples = load_sample_risks()  # Load HuggingFace sample data
    history = get_risk_history(session["username"])
    
    return render_template(
        "dashboard.html",
        user=session,
        samples=samples,
        history=history,
        is_admin=is_admin(session)
    )

# ─── RISK FORM & AI GENERATION ──────────────────────────────

@app.route("/risk-form", methods=["GET"])
def risk_form():
    if not is_logged_in(session):
        return redirect(url_for("login"))
    return render_template("risk_form.html", user=session)

@app.route("/generate-report", methods=["POST"])
def generate_report():
    if not is_logged_in(session):
        return redirect(url_for("login"))
    
    # Collect form data
    category    = request.form.get("category")
    probability = request.form.get("probability")
    impact      = request.form.get("impact")
    severity    = request.form.get("severity")
    description = request.form.get("description")
    
    # Call all 4 AI functions
    explanation = generate_risk_explanation(category, probability, impact, severity, description)
    mitigation  = generate_mitigation(category, probability, impact, severity, description)
    summary     = generate_summary(category, probability, impact, severity, description)
    compliance  = generate_compliance(category, probability, impact, severity, description)
    
    # Build the complete record
    record = {
        "category": category, "probability": probability,
        "impact": impact, "severity": severity,
        "description": description,
        "explanation": explanation, "mitigation": mitigation,
        "summary": summary, "compliance": compliance
    }
    
    # Save to Momento memory
    key = save_risk_record(session["username"], record)
    save_key_for_user(session["username"], key)
    
    return render_template("report.html", report=record, user=session)

# ─── WEB SEARCH ROUTE ───────────────────────────────────────

@app.route("/web-search", methods=["POST"])
def web_search():
    if not is_logged_in(session):
        return jsonify({"error": "Not logged in"}), 401
    
    query = request.form.get("query", "")
    raw_content = search_web(query)
    ai_answer = generate_from_web_content(query, raw_content)
    
    return jsonify({"result": ai_answer})

# ─── ADMIN ONLY: VIEW ALL USERS ─────────────────────────────

@app.route("/admin/users")
def admin_users():
    if not is_logged_in(session) or not is_admin(session):
        return redirect(url_for("dashboard"))
    from models.user_model import USERS
    return render_template("dashboard.html", user=session, all_users=USERS, is_admin=True)

# ─── RUN ────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)