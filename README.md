# IncidentPilot

IncidentPilot is an autonomous AI-assisted incident response demo. It ingests alerts, correlates deployments and commits, ranks suspect commits, retrieves relevant runbooks, estimates impact, produces a Slack-style brief, and generates a postmortem after resolution. The demo uses a deterministic local AI fallback when no OpenAI key is provided.

**Architecture**

```mermaid
flowchart LR
  A[Alerts webhook] --> B[FastAPI backend]
  B --> C[(SQLite/SQLAlchemy)]
  B --> D[AI Provider (OpenAI or local deterministic)]
  B --> E[Frontend (React + Vite)]
  E -->|API| B
```

## Local setup

Requirements: Python 3.12, Node 20, npm

Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend

```bash
cd frontend
npm install
npm run dev
```

Or using Docker Compose:

```bash
docker compose up --build
```

## Demo scenario
Open the frontend and click "Run demo" to generate a seeded incident for `checkout-service` that demonstrates detection, analysis, and evidence.

## Environment
See `.env.example` for variables. Do not commit secrets.

## Tests
Backend tests:

```bash
cd backend
pytest
```

## Design notes
- Uses SQLAlchemy with SQLite for local development
- AI provider abstraction. When `OPENAI_API_KEY` is set, OpenAI is used; otherwise a deterministic local provider produces structured output.
- All AI outputs are validated and stored as incident events. Evidence is kept separate from inference.
# IncidentPilot
