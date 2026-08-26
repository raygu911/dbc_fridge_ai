# Session 1 — Application Foundation and Semantic Search

Session 1 builds the FastAPI, PostgreSQL, Streamlit, and Docker application foundation, then adds embeddings and vector search so users can find recipes by meaning rather than exact keywords.

- **Effort:** High
- **Estimated guided time:** 3–4 hours
- **Status:** Complete

## Learning Goals

- Structure a FastAPI service with validated recipe schemas and PostgreSQL persistence.
- Connect a Streamlit interface to the API and run the stack with Docker Compose.
- Convert recipe content into embedding-friendly text.
- Generate BGE embeddings with FastEmbed.
- Store and query vectors in Qdrant.
- Join vector matches back to authoritative PostgreSQL records.
- Expose semantic retrieval through FastAPI and Streamlit.

## Completed Architecture

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    └── FastEmbed → Qdrant
```

## Milestone Capabilities

- FastAPI recipe endpoints backed by PostgreSQL
- Streamlit recipe creation and browsing interface
- Reproducible Docker Compose environment
- `BAAI/bge-small-en-v1.5` embedding generation
- Persistent Qdrant recipe collection
- Recipe indexing during creation
- Semantic search endpoint with result limits
- Similarity scores and PostgreSQL recipe responses
- Streamlit semantic-search interface
- Embedding and semantic-search tests

## Run the Milestone

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

The first embedding request may download the model and take longer than later requests.

## Test Semantic Search

Create a recipe through http://localhost:8000/docs or the Streamlit UI, then run:

```bash
curl --get http://localhost:8000/api/v1/recipes/search \
  --data-urlencode "query=a quick plant-based meal with grains" \
  --data-urlencode "limit=5"
```

## Verify the Milestone

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -v
```

## Completion Checklist

- [ ] PostgreSQL, Qdrant, API, and web services start.
- [ ] Recipes can be created and retrieved through the API and web interface.
- [ ] Creating a recipe adds structured and vector records.
- [ ] A natural-language query returns relevant recipes.
- [ ] Search results include similarity scores.
- [ ] Ruff and pytest pass.

## Interview Talking Points

Explain cosine similarity, why recipe vectors live in Qdrant while complete recipes remain in PostgreSQL, and how semantic search differs from exact keyword matching.
