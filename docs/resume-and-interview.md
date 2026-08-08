# IncidentPilot — Resume & Interview Notes

Three resume bullets:

- Developed "IncidentPilot", an end-to-end AI-assisted incident response demo using FastAPI, React/TypeScript, and SQLAlchemy; implemented alert ingestion, commit correlation, runbook retrieval, and deterministic AI reasoning for reproducible demos.
- Architected a provider abstraction enabling OpenAI integration or a safe local deterministic fallback; validated structured JSON outputs and recorded evidence vs inference in an append-only audit log.
- Built an interactive operations console with a demo scenario that simulates a faulty `checkout-service` deployment, enabling live investigation, human-approved simulated remediation, and automated postmortem generation.

30-second explanation:

IncidentPilot is a demo platform that ingests production-style alerts, correlates them with recent deployments and commits, ranks likely suspects, retrieves runbooks, estimates impact, drafts incident briefs, and generates a postmortem — all while protecting secrets and requiring human approval for remediation.

Two-minute technical walkthrough:

1. The FastAPI backend exposes webhook endpoints for alerts, deployments, metrics, and resolution. Alerts create incidents persisted in SQLite via SQLAlchemy.
2. An AI provider abstraction calls OpenAI when configured, otherwise uses a deterministic local reasoning engine that produces structured JSON outputs (summary, suspected_cause, impact estimate, evidence, confidence).
3. The frontend (React + Vite) shows incidents in real time with an in-app Slack simulator and a human approval panel for simulated rollback/flag disablement.

Interview Qs & concise answers:

- Q: How do you avoid AI hallucinations affecting incident decisions?
  A: We separate observed evidence (alerts, metrics, deployments) from AI inference; outputs are structured JSON validated against schemas and accompanied by confidence scores and citations. Remediation requires explicit human approval.
- Q: Is remediation automated?
  A: No. Actions are simulated and gated by human approval. The system provides safe rollback/flag toggles as simulated options.
- Q: What would you change for production?
  A: Replace SQLite with Postgres, add strict auth, rate-limiting, secure secrets management, robust observability, and integrate with real CI/CD and Slack via credentials.

Note: All integrations and remediation are explicitly simulated unless configured with real credentials.
