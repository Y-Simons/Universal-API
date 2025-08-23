# Anesth AI
AI-assisted workflow for French anesthetists: risk stratification, pre/post-op automation, and teleconsultation.

## Run (Docker recommended)
```bash
docker compose build
docker compose up
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

Seeded credentials:
- anesth@example.com / changeme

## Run locally (no Docker)
Backend:
```bash
cd backend
pip install --break-system-packages -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Compliance and privacy
- GDPR: explicit consent tracking, audit logging, data minimization
- Hosting: EU/HDS-compliant provider for PHI in production
- Security: JWT auth, CORS config, TLS, secret rotation
- Clinical: decision-support only; clinician review required
