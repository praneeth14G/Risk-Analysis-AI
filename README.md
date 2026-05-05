# RiskExplain AI

**RiskExplain AI** is an intelligent financial risk analysis platform powered by AI. It allows risk officers and analysts to input risk scenarios and instantly receive AI-generated explanations, mitigation strategies, structured summaries, and compliance commentary — all in plain English.

---

##  Features

- Role-based Authentication — Secure login system with `admin` and `user` roles
- AI-Powered Risk Reports — Generate four types of AI analysis per risk:
  - Explanation — Plain-English breakdown for executive audiences
  - Mitigation Strategies — 4 actionable steps to reduce the risk
  - Structured Summary — Formatted risk report with scores and priorities
  - Compliance Commentary — Audit-ready notes referencing Basel III, COSO, ISO 31000
- Live Web Search — Firecrawl-powered search to pull real-time risk intelligence from the web
- Risk History — User sessions persist risk records using Momento serverless cache (24-hour TTL)
- Sample Dataset — HuggingFace `financial_phrasebank` dataset loaded on the dashboard for quick testing
- Admin Panel — Admin users can view all registered user accounts

---

## Project Structure

```
riskexplain-ai/
│
├── app.py                        # Main Flask app — all routes
│
├── models/
│   ├── user_model.py             # User credentials and role definitions
│   └── risk_model.py             # Risk data model
│
├── services/
│   ├── ai_service.py             # OpenRouter (GPT-3.5-turbo) AI calls
│   ├── auth_service.py           # Login logic and session helpers
│   ├── dataset_loader.py         # HuggingFace dataset integration
│   ├── memory_service.py         # Momento cache for risk history
│   └── websearch_service.py      # Firecrawl web search integration
│
├── utils/
│   ├── config.py                 # Loads API keys from .env
│   └── prompts.py                # All AI prompt templates
│
├── templates/
│   ├── login.html                # Login page
│   ├── dashboard.html            # Main dashboard
│   ├── risk_form.html            # Risk input form
│   └── report.html               # AI-generated report view
│
├── static/                       # CSS / JS / assets
├── requirements.txt
└── .env                          # API keys (not committed to git)
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/riskexplain-ai.git
cd riskexplain-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
MOMENTO_API_KEY=your_momento_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
SECRET_KEY=your_flask_secret_key
```

> **Where to get keys:**
> - **OpenRouter** — [https://openrouter.ai](https://openrouter.ai) (free tier available)
> - **Momento** — [https://www.gomomento.com](https://www.gomomento.com) (free serverless cache)
> - **Firecrawl** — [https://www.firecrawl.dev](https://www.firecrawl.dev) (web scraping API)

### 5. Run the Application

```bash
python app.py
```

Open your browser and navigate to: **[http://localhost:5000](http://localhost:5000)**

---

##  Default Login Credentials

| Username   | Password   | Role   |
|------------|------------|--------|
| `admin`    | `admin123` | Admin  |
| `officer1` | `risk2024` | User   |

>  **These are demo credentials.** Replace them with a proper database and hashed passwords before deploying to production.

---

##  Application Routes

| Route              | Method     | Description                                  |
|--------------------|------------|----------------------------------------------|
| `/`                | GET        | Redirects to dashboard or login              |
| `/login`           | GET, POST  | User login page                              |
| `/logout`          | GET        | Clears session and redirects to login        |
| `/dashboard`       | GET        | Main dashboard with history & sample data    |
| `/risk-form`       | GET        | Risk input form                              |
| `/generate-report` | POST       | Runs AI analysis and renders report          |
| `/web-search`      | POST       | Live web search with AI summarization (JSON) |
| `/admin/users`     | GET        | Admin-only: view all users                   |

---

## AI Analysis Pipeline

When a user submits a risk via the form, four parallel AI prompts are sent to **OpenRouter (GPT-3.5-turbo)**:

```
Risk Input (category, probability, impact, severity, description)
         │
         ├──▶ generate_risk_explanation()   →  Plain-English Explanation
         ├──▶ generate_mitigation()         →  4 Mitigation Strategies
         ├──▶ generate_summary()            →  Structured Summary Report
         └──▶ generate_compliance()         →  Regulatory Compliance Commentary
```

Results are saved to **Momento cache** (keyed per user + timestamp) and displayed on the report page.

---

## Memory & Persistence

Risk records are stored using **Momento Serverless Cache**:

- Each record is saved with key format: `risk:{username}:{timestamp}`
- A user's key list is tracked under: `keys:{username}`
- All records expire automatically after **24 hours**

---

## Dependencies

| Package              | Purpose                                      |
|----------------------|----------------------------------------------|
| `flask`              | Web framework                                |
| `google-generativeai`| Gemini AI SDK (optional/future use)          |
| `momento`            | Serverless cache for risk history            |
| `datasets`           | HuggingFace dataset loader                   |
| `python-dotenv`      | Load environment variables from `.env`       |
| `requests`           | HTTP calls to OpenRouter & Firecrawl         |
| `firecrawl-py`       | Web scraping and search API client           |

---

## Security Notes

- Sessions are secured with a Flask `SECRET_KEY`
- All routes check for authenticated sessions before rendering
- Admin routes verify the `role == "admin"` condition
- **For production:** use hashed passwords (e.g., `bcrypt`), a real database, and HTTPS

---

## Future Improvements

- [ ] Database integration (PostgreSQL / MongoDB) for persistent user management
- [ ] Password hashing with `bcrypt`
- [ ] PDF export of risk reports
- [ ] Role-based access control (RBAC) for more granular permissions
- [ ] Risk trend analytics and dashboard charts
- [ ] Email notifications for high-severity risks

---

