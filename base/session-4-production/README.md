# Session 4 — Production Engineering

Session 4 turns the working RAG application into a resilient, observable, continuously verified portfolio project.

- **Effort:** High
- **Estimated guided time:** 1.5–2 hours
- **Status:** Complete

## Learning Goals

- Separate liveness from dependency readiness.
- Correlate user-visible failures with structured application logs.
- Handle infrastructure and model failures without exposing internals.
- Refine the Streamlit experience for loading, success, and failure states.
- Continuously verify code with GitHub Actions.
- Document repeatable local operations and incident diagnosis.

## Production Architecture

```text
User → Streamlit → FastAPI request-ID middleware
                    ├── PostgreSQL
                    ├── Qdrant retrieval → Ollama / Gemma 3
                    ├── Redis → Celery → FastEmbed → Qdrant indexing
                    └── JSON logs + liveness/readiness probes

Git push / pull request → GitHub Actions → Ruff + PostgreSQL-backed pytest
```

## Production Improvements

- JSON logs include timestamp, severity, logger, message, request ID, HTTP method, path, status, and duration.
- Every API response includes `X-Request-ID`; client-provided IDs are preserved for end-to-end correlation.
- Unexpected exceptions return a safe HTTP 500 response with a reference ID.
- `/health` is a lightweight process liveness endpoint.
- `/ready` verifies PostgreSQL, Qdrant, and Redis and returns HTTP 503 when a dependency is unavailable.
- Streamlit displays dependency status and user-friendly errors with request references.
- Tests cover readiness degradation, model outages, empty retrieval, request IDs, and structured logs.
- Root-level GitHub Actions CI runs Ruff and pytest against PostgreSQL for Session 4 changes.

## Prerequisites

- Docker Desktop
- Python 3.12 or later
- Ollama running natively with `gemma3:4b`

```bash
ollama pull gemma3:4b
ollama list
```

## Run the Application

From this directory:

```bash
cp .env.example .env
docker compose up --build -d --wait
docker compose ps
```

Open:

- Streamlit: <http://localhost:8501>
- FastAPI documentation: <http://localhost:8000/docs>
- Qdrant dashboard: <http://localhost:6333/dashboard>

## Operational Checks

Liveness checks whether the API process can respond:

```bash
curl http://localhost:8000/health
```

Readiness checks required infrastructure:

```bash
curl -i \
  -H "X-Request-ID: manual-readiness-check" \
  http://localhost:8000/ready
```

A ready system returns HTTP 200:

```json
{
  "status": "ready",
  "checks": {
    "database": "healthy",
    "qdrant": "healthy",
    "redis": "healthy"
  }
}
```

Correlate the request with API logs:

```bash
docker compose logs --tail=50 api
docker compose logs --tail=50 worker
```

## Quality Checks

Keep PostgreSQL running, then execute:

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
git diff --check
docker compose config --quiet
```

The CI workflow at `../../.github/workflows/session-4-ci.yml` runs Ruff and the PostgreSQL-backed test suite for relevant pushes and pull requests.

## Troubleshooting

### API request fails immediately after a rebuild

Use `docker compose up --build -d --wait`. The `--wait` option prevents requests from racing the API startup health check.

### Readiness returns HTTP 503

Inspect the `checks` object to identify the unavailable dependency, then run:

```bash
docker compose ps
docker compose logs --tail=50 database qdrant redis api
```

### Recommendations report that the model is unavailable

Confirm the native Ollama service and model:

```bash
curl http://localhost:11434/api/tags
ollama list
```

### Recipe indexing does not complete

Confirm that Redis and the worker are healthy, then inspect the task log:

```bash
docker compose logs --tail=50 worker
```

## Shutdown and Cleanup

Stop containers while preserving data:

```bash
docker compose down
```

Delete test databases, vectors, Redis data, and the Compose model cache only when intentionally resetting the milestone:

```bash
docker compose down --volumes
```

The Ollama model is managed outside Docker and is not removed by either command.

## Final Verification Checklist

- [x] All six Compose services start successfully.
- [x] `/health` returns HTTP 200.
- [x] `/ready` reports PostgreSQL, Qdrant, and Redis as healthy.
- [x] Request IDs match between API responses and JSON logs.
- [x] Recipe creation completes and the Celery worker indexes it.
- [x] Semantic search retrieves the expected recipe.
- [x] Gemma produces a grounded recommendation with sources.
- [x] The Streamlit status panel and all four tabs work.
- [x] Ruff, pytest, `git diff --check`, and Compose validation pass.
- [x] GitHub Actions passes on the pull request.

## Interview Narrative

**Problem:** FridgeAI needed semantic discovery and locally generated recommendations without returning ungrounded answers or blocking recipe creation.

**Design:** PostgreSQL remains the source of truth, Qdrant supports semantic retrieval, Ollama generates from retrieved recipe context, and Celery with Redis moves embedding work outside the request path.

**Production engineering:** Liveness and readiness are separated, dependencies are diagnosed individually, request IDs correlate UI errors with structured JSON logs, failure paths return controlled status codes, and GitHub Actions continuously runs lint and PostgreSQL-backed tests.

**Trade-off:** Local models improve privacy and avoid hosted inference costs, but require explicit model lifecycle management and may produce less consistent prose than larger managed models. Returning retrieved sources keeps recommendations inspectable.

### Resume Bullet

Built and productionized a containerized RAG recipe platform using FastAPI, PostgreSQL, Qdrant, FastEmbed, Ollama, Redis, Celery, and Streamlit; added asynchronous indexing, grounded source attribution, dependency readiness probes, correlated JSON logging, resilient failure handling, and PostgreSQL-backed CI.

## Educational Safety Notice

Dietary tags and AI-generated recommendations are educational features, not medical, allergy, or food-safety advice.
