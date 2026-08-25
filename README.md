# FridgeAI Training Program

> Build a resume-worthy AI engineering project from application foundations through Retrieval-Augmented Generation and production engineering.

FridgeAI is a curriculum-first repository. Application code is organized into standalone session milestones so trainees can run, test, compare, and explain the system at each stage instead of seeing only the final implementation.

> **Current status:** All four base sessions are complete. Advanced modules are planned follow-up training.

## Training Tracks

| Track | Purpose | Status |
| --- | --- | --- |
| [Base training](base/) | Build the complete FridgeAI MVP across four sequential sessions | Complete |
| [Advanced training](advanced/) | Extend the MVP with retrieval, evaluation, observability, and deployment techniques | Planned |

## Repository Structure

```text
dbc_fridge_ai/
├── README.md
├── LICENSE
├── base/
│   ├── README.md
│   ├── session-1-foundation/
│   ├── session-2-semantic-search/
│   ├── session-3-rag/
│   └── session-4-production/
└── advanced/
    ├── README.md
    ├── module-1-evaluation/
    ├── module-2-hybrid-retrieval/
    ├── module-3-reranking/
    ├── module-4-observability/
    └── module-5-cloud-deployment/
```

The root contains curriculum navigation only. Run application, Docker, Ruff, and pytest commands from an individual session directory.

## Base Training Roadmap

| Session | Focus | Effort | Estimated guided time | Status |
| --- | --- | --- | --- | --- |
| [Session 1 — Application Foundation](base/session-1-foundation/) | FastAPI, PostgreSQL, Streamlit, Docker, and tests | Moderate | 1.5–2 hours | Complete |
| [Session 2 — Semantic Retrieval](base/session-2-semantic-search/) | FastEmbed, Qdrant, and semantic search | Moderate–high | 1.5–2 hours | Complete |
| [Session 3 — RAG and Background Processing](base/session-3-rag/) | Ollama, grounded generation, Redis, and Celery | High | 2–2.5 hours | Complete |
| [Session 4 — Production Engineering](base/session-4-production/) | CI, resilience, logging, UX, and project presentation | High | 1.5–2 hours | Complete |

Estimated guided implementation time for all four base sessions is **6.5–8.5 hours**. These estimates exclude environment setup, downloads, breaks, and optional experimentation.

## How to Run a Session

Each completed session is an independent Python project containing its own source code, tests, environment template, Dockerfile, Compose configuration, and README.

For example, to run Session 2:

```bash
cd base/session-2-semantic-search
cp .env.example .env
docker compose up --build -d
docker compose ps
```

To run its quality checks:

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -v
```

Stop the milestone when finished:

```bash
docker compose down
```

Run only one milestone Docker environment at a time because the standalone projects intentionally use the same local ports.

## Milestone Progression

### Session 1

```text
User → Streamlit → FastAPI → PostgreSQL
```

Trainees build the application foundation, structured recipe API, persistence layer, frontend integration, container environment, validation, and automated tests.

### Session 2

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    └── FastEmbed → Qdrant
```

Trainees add recipe embeddings, persistent vector storage, natural-language semantic search, similarity scores, and vector-to-relational result mapping.

### Session 3

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    ├── Qdrant retrieval → Ollama / Gemma 3
                    └── Redis → Celery → FastEmbed → Qdrant indexing
```

Trainees build grounded AI recommendations, return retrieved sources, integrate a local language model, and move embedding work into retryable background tasks.

### Session 4

Trainees productionize the completed application with correlated structured logging, liveness and dependency readiness probes, resilient UI errors, continuous integration, expanded failure-path tests, operational documentation, and an interview-ready project narrative.

## Advanced Training Goals

The [advanced track](advanced/) will build on the completed base MVP through standalone modules in a measurement-first sequence:

- Retrieval and generation evaluation
- Hybrid semantic and lexical retrieval
- Cross-encoder reranking
- Tracing, metrics, logging, and operational dashboards
- Managed cloud deployment and infrastructure as code

Advanced modules may introduce additional model downloads, infrastructure, datasets, and operating costs.

## Prerequisites

Base training requires:

- Git
- Docker Desktop
- Python 3.12 or later
- Basic Python and command-line familiarity

Session 3 additionally requires native [Ollama](https://ollama.com/download/mac) and the `gemma3:4b` model. See the Session 3 README for platform-specific setup.

## Data and Disk Usage

Milestone directories duplicate source code only. They do not contain Python environments, Docker images, databases, vector data, model caches, Ollama models, or secrets.

Avoid `docker compose down --volumes` unless you intentionally want to delete a milestone's local PostgreSQL, Qdrant, Redis, and model-cache volumes.

## Educational Safety Notice

FridgeAI is an educational project. Dietary tags, allergy-related filtering, retrieved content, and AI-generated recommendations must not be treated as medical or food-safety advice.

## License

This project is licensed under the MIT License.
