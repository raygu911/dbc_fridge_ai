# Session 3 — Retrieval-Augmented Generation

Session 3 grounds local language-model responses in retrieved recipes and moves embedding work to a background worker.

- **Effort:** High
- **Estimated guided time:** 2–2.5 hours
- **Milestone commit:** `855d8d7`

## Learning Goals

- Build a Retrieval-Augmented Generation pipeline.
- Construct prompts that constrain generation to retrieved context.
- Run a local Gemma 3 model through Ollama.
- Queue background work with Redis and Celery.
- Make recipe creation responsive by indexing asynchronously.
- Test system boundaries without calling live AI services.

## Completed Architecture

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    ├── Qdrant retrieval → Ollama / Gemma 3
                    └── Redis → Celery → FastEmbed → Qdrant indexing
```

## Prerequisites

Install Ollama natively on macOS, then download the model:

```bash
ollama pull gemma3:4b
curl http://localhost:11434/api/tags
```

## Run the Milestone

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
docker compose logs --tail=30 worker
```

The worker log should show that it connected to Redis and is ready.

## Test a Grounded Recommendation

```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{"query":"a quick vegan dinner with grains","limit":3}'
```

The response includes the local model's explanation and the retrieved source recipes with similarity scores.

## Verify the Milestone

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -v
```

## Completion Checklist

- [ ] Ollama responds at `localhost:11434`.
- [ ] Redis and the Celery worker start successfully.
- [ ] Creating a recipe queues and completes an indexing task.
- [ ] The recommendation endpoint cites retrieved recipes.
- [ ] The AI recommendations tab works in Streamlit.
- [ ] Ruff and pytest pass.

## Interview Talking Points

Explain how retrieval reduces hallucination risk, why source recipes are returned with the generated answer, why asynchronous indexing improves API latency, and how retries handle transient worker failures.
