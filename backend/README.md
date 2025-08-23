# Anesth AI Backend

Local dev quickstart:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Auth:
- Seeded user: anesth@example.com / changeme
- Obtain token: POST /auth/login { email, password }
- Use Authorization: Bearer <token>

Key endpoints:
- GET /health
- GET /patients
- POST /patients
- GET /patients/{id}/risk
- POST /consultations/preop/{id}
- POST /consultations/postop/{id}
- WS /teleconsult/ws/{room}

Compliance considerations (France/EU):
- GDPR: explicit consent tracking on `Patient.consent` and `gdpr_consent_at`
- Hosting: ensure data residency in EU; for production replace in-memory stores with encrypted DB
- Audit trail: `audit.log` middleware writes action logs with timestamp and actor
- Security: replace default JWT secret, rotate keys, enforce TLS, configure CORS
- Medical device: assess MDR classification if decision-support influences care; add disclaimers