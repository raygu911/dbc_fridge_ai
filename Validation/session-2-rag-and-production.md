# Session 2 Validation Guide — RAG and Production Readiness

Use this guide to validate Session 2 through Streamlit, FastAPI, Qdrant, Redis, PostgreSQL, Ollama, Celery, and the terminal.

## Learning Objectives

Trainees will learn to:

- Run and inspect all six containerized services.
- Verify liveness separately from dependency readiness.
- Create recipes and observe asynchronous Celery indexing.
- Test semantic retrieval and grounded AI recommendations.
- Confirm that recommendations include retrieved sources.
- Correlate API responses with structured logs using request IDs.
- Observe controlled behavior when a dependency is unavailable.
- Run the automated production-readiness checks.

## Architecture

```text
User → Streamlit → FastAPI request-ID middleware
                    ├── PostgreSQL
                    ├── Qdrant retrieval → Ollama / Gemma 3
                    ├── Redis → Celery → FastEmbed → Qdrant indexing
                    └── JSON logs + liveness/readiness probes

Git push / pull request → GitHub Actions → Ruff + PostgreSQL-backed pytest
```

## 1. Prepare Ollama

Session 2 expects Ollama to run natively on the host, outside Docker.

```bash
ollama pull gemma3:4b
ollama list
```

Confirm that Ollama responds:

```bash
curl http://localhost:11434/api/tags
```

If another Ollama model is configured in `.env`, use that model instead.

## 2. Start Session 2

Session 1 and Session 2 use the same local ports. Stop Session 1 before continuing:

```bash
cd base/session-1-application-and-search
docker compose down
```

Start Session 2 from the repository root:

```bash
cd ../session-2-rag-and-production
cp .env.example .env
docker compose up --build -d --wait
docker compose ps
```

Confirm that these services are running:

- `database`
- `qdrant`
- `redis`
- `api`
- `worker`
- `web`

Open:

- Streamlit: <http://localhost:8501>
- FastAPI documentation: <http://localhost:8000/docs>
- Qdrant dashboard: <http://localhost:6333/dashboard>

Redis, PostgreSQL, Celery, and logs are inspected through the terminal.

## 3. Verify Liveness and Readiness

Liveness proves that the API process can respond:

```bash
curl -i http://localhost:8000/health
```

Expected body:

```json
{
  "status": "healthy",
  "service": "fridge-ai-api",
  "environment": "development"
}
```

Readiness checks PostgreSQL, Qdrant, and Redis:

```bash
curl -i http://localhost:8000/ready
```

Expected body:

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

In Streamlit, confirm that the sidebar displays **All services ready** with healthy database, Qdrant, and Redis indicators.

### Teaching Point

- `/health` answers: “Is the API process alive?”
- `/ready` answers: “Can the application serve requests using its dependencies?”

## 4. Create Recipes and Observe Asynchronous Indexing

Select **Add a recipe** in Streamlit and add at least two recipes. You may reuse the Session 1 examples or add the following recipe.

### Fresh Chickpea Grain Bowl

| Field | Value |
| --- | --- |
| Recipe name | Fresh Chickpea Grain Bowl |
| Description | A quick vegan bowl with grains, chickpeas, and fresh vegetables. |
| Cooking time | 20 |
| Dietary tags | vegan, quick, high-protein |

Ingredients:

```text
cooked quinoa
chickpeas
cucumber
tomato
lemon juice
olive oil
```

Instructions:

```text
Add quinoa and chickpeas to a bowl
Chop the cucumber and tomato
Add the vegetables to the bowl
Dress with lemon juice and olive oil
```

Click **Add recipe**. The API writes the recipe to PostgreSQL and queues the recipe ID in Redis. Celery then loads the record, generates its embedding, and writes it to Qdrant.

Follow the worker logs:

```bash
docker compose logs -f worker
```

Look for the `fridge_ai.index_recipe` task and a successful completion. Press `Ctrl+C` after observing it.

Inspect Redis:

```bash
docker compose exec redis redis-cli ping
docker compose exec redis redis-cli llen celery
```

Expected `ping` result:

```text
PONG
```

The queue length is commonly `0` after the worker finishes the task.

## 5. Validate Browse and Semantic Search

In Streamlit:

1. Select **Browse recipes** and click **Load recipes**.
2. Confirm that the new recipe appears.
3. Select **Semantic search**.
4. Search for `a fast plant-based meal with grains and fresh vegetables`.
5. Confirm that the chickpea grain bowl ranks highly.

If a newly added recipe does not appear in semantic search immediately, wait for the Celery task to complete and try again.

Test the search endpoint from the terminal:

```bash
curl --get http://localhost:8000/api/v1/recipes/search \
  --data-urlencode "query=a fast plant-based meal with grains" \
  --data-urlencode "limit=3"
```

## 6. Generate a Grounded AI Recommendation

In Streamlit:

1. Select **AI recommendations**.
2. Enter `I want a quick vegan dinner with grains and fresh vegetables`.
3. Find the slider labeled **Recipes to use as context** directly below the meal-description text box.
4. Set the slider to `3`. Its allowed UI range is `1` to `5`, and its default is `3`.
5. Click **Generate recommendation**.

The slider controls the `limit` sent to FastAPI:

```json
{
  "query": "I want a quick vegan dinner with grains and fresh vegetables",
  "limit": 3
}
```

The limit tells Qdrant to retrieve up to three recipes for grounding context. It does not ask Ollama to produce three recommendations.

Confirm that the result contains:

- A generated recommendation
- The configured Ollama model name
- A **Retrieved sources** section
- Source recipes with semantic similarity scores

The first request may take longer while the model and embedding components initialize.

### Teaching Point

The language model does not search the database directly:

```text
User request
    ↓
FastEmbed query vector
    ↓
Qdrant retrieves recipe IDs
    ↓
PostgreSQL supplies authoritative recipe context
    ↓
FridgeAI builds a grounded prompt
    ↓
Ollama generates an answer from the retrieved context
    ↓
API returns the answer and its sources
```

## 7. Test the Recommendation API

Open <http://localhost:8000/docs>.

1. Expand `POST /api/v1/recommendations`.
2. Click **Try it out**.
3. Submit:

```json
{
  "query": "I want a quick vegan dinner with grains and fresh vegetables",
  "limit": 3
}
```

4. Click **Execute**.

Confirm HTTP `200` and these response fields:

```json
{
  "query": "...",
  "recommendation": "...",
  "model": "gemma3:4b",
  "sources": []
}
```

For a successful request, `sources` should contain one or more retrieved recipe records and scores.

Run the same request in the terminal:

```bash
curl http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I want a quick vegan dinner with grains and fresh vegetables",
    "limit": 3
  }'
```

## 8. Inspect Qdrant and PostgreSQL

Open Qdrant at <http://localhost:6333/dashboard>:

1. Select **Collections**.
2. Open `recipes`.
3. Inspect the stored points.
4. Compare point IDs with recipe IDs.

Count exact Qdrant points:

```bash
curl http://localhost:6333/collections/recipes/points/count \
  -H "Content-Type: application/json" \
  -d '{"exact":true}'
```

Inspect PostgreSQL records:

```bash
docker compose exec database \
  psql -U fridge_ai -d fridge_ai -c \
  "SELECT id, name, cooking_time_minutes FROM recipes ORDER BY id;"
```

The point count should eventually match the number of successfully indexed recipes.

## 9. Correlate Requests with Structured Logs

Send a request with a known request ID:

```bash
curl -i \
  -H "X-Request-ID: lecture-session-2-check" \
  http://localhost:8000/ready
```

Confirm that the response contains:

```text
X-Request-ID: lecture-session-2-check
```

Search the API logs:

```bash
docker compose logs api | grep lecture-session-2-check
```

The matching JSON log should include the request ID, method, path, status code, and duration.

Generate an automatic request ID:

```bash
curl -i http://localhost:8000/health
```

Copy the returned `X-Request-ID` and search for it in the logs.

## 10. Validate Controlled Dependency Failure

This exercise demonstrates the difference between liveness and readiness.

Stop Redis:

```bash
docker compose stop redis
```

Check liveness:

```bash
curl -i http://localhost:8000/health
```

The API should remain alive and return HTTP `200`.

Check readiness:

```bash
curl -i http://localhost:8000/ready
```

Readiness should return HTTP `503`, with Redis marked unhealthy. Streamlit should warn that some services are unavailable.

Restore Redis and the worker:

```bash
docker compose start redis
docker compose restart worker
```

Wait briefly and confirm readiness again:

```bash
curl -i http://localhost:8000/ready
```

Do not create recipes while Redis is intentionally stopped because their indexing tasks cannot be queued normally.

## 11. Validate Model Failure Handling

Use a deliberately invalid model name to test the failure path without modifying `.env` or stopping a shared Ollama service.

### Confirm the Normal Configuration

First, confirm that Ollama and the valid model are available:

```bash
ollama list
curl http://localhost:11434/api/tags
```

Generate one successful recommendation before introducing the failure.

### Recreate the API with an Invalid Model

From `base/session-2-rag-and-production`:

```bash
OLLAMA_MODEL=missing-training-model \
docker compose up -d --force-recreate api web
```

This shell override does not edit `.env`. It temporarily configures the recreated API container with a model name that should not exist.

Wait for the services and check readiness:

```bash
docker compose ps
curl -i http://localhost:8000/ready
```

Readiness may still return HTTP `200` because `/ready` currently checks PostgreSQL, Qdrant, and Redis, not whether the configured Ollama model exists.

### Test the Failure Through the Terminal

Make sure at least one recipe is indexed, then send a recommendation request with a known request ID:

```bash
curl -i http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: model-failure-test" \
  -d '{
    "query": "I want a quick vegan dinner with grains and fresh vegetables",
    "limit": 3
  }'
```

Expected status:

```text
HTTP/1.1 503 Service Unavailable
```

Expected body:

```json
{
  "detail": "Recommendation model is unavailable"
}
```

The response should also preserve:

```text
X-Request-ID: model-failure-test
```

Find the corresponding structured log:

```bash
docker compose logs api | grep model-failure-test
```

### Test the Failure Through Streamlit

While the invalid model configuration is active:

1. Refresh Streamlit.
2. Open **AI recommendations**.
3. Enter the recommendation request.
4. Click **Generate recommendation**.

Streamlit should display `Recommendation model is unavailable` and a request reference rather than exposing an internal traceback or Ollama error.

### Restore the Valid Model

Recreate the services without the temporary shell override so Compose uses the normal value from `.env`:

```bash
docker compose up -d --force-recreate api web
docker compose ps
```

Generate another recommendation and confirm that the valid configured model works again.

## 12. Run Automated Verification

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -v
git diff --check
docker compose config --quiet
```

Expected test result:

```text
20 passed
```

## Completion Checklist

- [ ] All six services start successfully.
- [ ] `/health` returns HTTP `200`.
- [ ] `/ready` reports PostgreSQL, Qdrant, and Redis as healthy.
- [ ] Streamlit displays all four tabs and healthy service indicators.
- [ ] Recipe creation queues a Celery indexing task.
- [ ] The worker indexes the recipe into Qdrant.
- [ ] Semantic search retrieves the expected recipe.
- [ ] Ollama returns a grounded recommendation.
- [ ] The recommendation includes retrieved sources and scores.
- [ ] PostgreSQL recipe IDs correspond to Qdrant point IDs.
- [ ] A supplied request ID appears in the response and JSON logs.
- [ ] Stopping Redis keeps liveness healthy but makes readiness fail.
- [ ] Restarting Redis and the worker restores readiness.
- [ ] An invalid model returns HTTP `503` with a safe message and request ID.
- [ ] Streamlit shows the controlled model error without an internal traceback.
- [ ] Recreating the services without the override restores valid recommendations.
- [ ] Ruff, pytest, Git whitespace checks, and Compose validation pass.
- [ ] The trainee can explain retrieval, generation, asynchronous indexing, and failure handling.

## Shut Down

Stop the environment while preserving data:

```bash
docker compose down
```

Do not use `docker compose down --volumes` unless you intentionally want to delete PostgreSQL records, Qdrant vectors, Redis data, and the model cache.

## Troubleshooting

### A recipe exists in PostgreSQL but not in semantic search

```bash
docker compose ps redis worker qdrant
docker compose logs --tail=100 worker
```

Confirm that the Celery indexing task completed.

### Recommendation requests return HTTP 503

```bash
curl http://localhost:11434/api/tags
ollama list
docker compose logs --tail=100 api
```

Confirm that Ollama is running and the configured model is installed.

### Readiness returns HTTP 503

```bash
docker compose ps
docker compose logs --tail=100 database qdrant redis api
```

Use the `/ready` response to identify the unhealthy dependency.

### Streamlit cannot reach the API

```bash
docker compose ps api web
docker compose logs --tail=100 api web
```
