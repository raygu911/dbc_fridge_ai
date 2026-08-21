# Session 1 — Application Foundation

Session 1 establishes a conventional, testable web application before AI capabilities are introduced.

- **Effort:** Moderate
- **Estimated guided time:** 1.5–2 hours
- **Milestone commit:** `52871b1`

## Learning Goals

- Organize a Python application into API, frontend, domain, and test modules.
- Build REST endpoints with FastAPI and validate input with Pydantic.
- Persist structured recipes with PostgreSQL and SQLAlchemy.
- Connect a Streamlit interface to an HTTP API.
- Run the application locally with Docker Compose.
- Verify behavior with pytest and Ruff.

## Completed Architecture

```text
User → Streamlit → FastAPI → PostgreSQL
```

## Milestone Capabilities

- API health endpoint
- Recipe creation, listing, and retrieval
- Request validation and missing-recipe handling
- PostgreSQL persistence
- Streamlit recipe browsing and creation
- Docker Compose services and health checks
- Automated API tests

## Run the Milestone

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

Open:

- Streamlit: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health

## Verify the Milestone

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -v
```

## Completion Checklist

- [ ] All services start successfully.
- [ ] A recipe can be created through the API or UI.
- [ ] The recipe persists in PostgreSQL.
- [ ] Invalid recipe requests return HTTP 422.
- [ ] Ruff and pytest pass.

## Interview Talking Points

Explain why PostgreSQL remains the source of truth, how FastAPI dependency injection supplies database sessions, and why building a reliable non-AI foundation makes later AI features easier to test.
