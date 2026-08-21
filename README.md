# FridgeAI

> Build a Resume-Worthy AI Engineering Project from Scratch

> **Project status:** Sessions 1–3 are complete. FridgeAI now provides grounded AI meal recommendations with Qdrant retrieval, a local Gemma 3 model through Ollama, and asynchronous recipe indexing with Celery and Redis.

FridgeAI is an evolving meal recommendation system designed to demonstrate how modern AI applications are built using Retrieval-Augmented Generation (RAG), vector databases, backend APIs, asynchronous processing, containerization, and production-oriented engineering practices.

Sessions 1–3 provide the application foundation, semantic retrieval pipeline, Retrieval-Augmented Generation, and background embedding workflow. Session 4 will focus on production engineering and project polish.

Unlike many AI demonstration projects that focus only on model inference, FridgeAI emphasizes the complete AI engineering lifecycle—from data ingestion and semantic retrieval to testing, deployment, and system architecture.

This repository serves two purposes:

- A resume-worthy AI engineering portfolio project
- The official project for the FridgeAI Intensive Training Program

---

# Training Paths

FridgeAI is organized into two top-level training tracks:

- [Base training](base/) contains four sequential sessions. Every completed session is a standalone, runnable copy of the project at that milestone, including its application code, tests, Docker configuration, and guided README.
- [Advanced training](advanced/) extends the completed MVP with hybrid retrieval, reranking, evaluation, observability, and cloud deployment techniques.

To inspect or test a completed milestone without changing the current application, enter its directory directly:

```bash
cd base/session-2-semantic-search
cp .env.example .env
docker compose up --build -d
```

Only run one milestone environment at a time because the standalone projects use the same local service ports. Session snapshots contain source files only; dependencies, Docker images, databases, vector data, models, caches, and secrets are not duplicated in Git.

---

# Project Overview

FridgeAI helps developers learn how to build complete AI applications rather than isolated AI demonstrations.

The project demonstrates how traditional software engineering integrates with modern generative AI technologies through an end-to-end architecture that is practical, testable, and extensible.

By the end of the complete project, learners will understand:

- Retrieval-Augmented Generation (RAG)
- Embedding generation
- Semantic search
- Vector databases
- Backend API development
- Asynchronous task processing
- Containerization
- CI/CD
- Local deployment
- AI engineering practices
- System design
- Technical communication for interviews

---

# Current Implementation Status

Sessions 1–3 are complete.

The time ranges below are implementation estimates based on the completed scope. They exclude model downloads, Docker image downloads, environment setup, breaks, and optional experimentation.

| Session | Focus | Effort | Estimated time spent |
| --- | --- | --- | --- |
| Session 1 | Application foundation | Moderate | 1.5–2 hours |
| Session 2 | Semantic retrieval | Moderate–high | 1.5–2 hours |
| Session 3 | RAG and background processing | High | 2–2.5 hours |
| **Completed total** | **Sessions 1–3** |  | **5–6.5 hours** |

## Session 1 — Application Foundation

Completed capabilities:

- FastAPI backend
- PostgreSQL database
- Recipe creation, listing, and retrieval
- Pydantic request validation
- Initial Streamlit browse and recipe-creation interfaces
- Docker Compose local environment
- Persistent PostgreSQL storage
- Automated API tests
- PostgreSQL and FastAPI health checks

## Session 2 — Semantic Retrieval

Completed capabilities:

- Recipe text generation for embedding
- FastEmbed embedding generation with `BAAI/bge-small-en-v1.5`
- Qdrant vector storage with persistent local data
- Recipe vector indexing
- Natural-language semantic recipe search with similarity scores
- Semantic search API with configurable result limits
- Streamlit semantic-search interface
- Embedding validation and semantic-search tests

## Session 3 — RAG and Background Processing

Completed capabilities:

- Retrieval-Augmented Generation grounded in retrieved recipes
- Local AI recommendation generation with Ollama and `gemma3:4b`
- Recommendation responses with source recipes and similarity scores
- Streamlit AI-recommendation interface
- Celery background tasks with retry behavior
- Redis task brokering and result storage
- Asynchronous vector indexing when recipes are created
- Persistent PostgreSQL, Qdrant, Redis, and model-cache storage
- Prompt-grounding, recommendation API, and Celery task tests
- Redis health checks and Celery worker integration

## Shared Engineering Practices

- Ruff code-quality checks
- Automated pytest coverage across completed sessions
- Health checks for PostgreSQL, Qdrant, Redis, and FastAPI
- End-to-end API and UI smoke testing

The following technologies will be added in later sessions:

- GitHub Actions

---

# Planned Core Features

Across the four-session roadmap, FridgeAI will include:

- Ingredient-based meal recommendations
- Natural-language recipe search
- Semantic recipe retrieval
- Dietary preference filtering
- Allergy-related filtering
- Retrieval-Augmented Generation
- AI-generated recommendation explanations
- Recipe ingestion and indexing
- Background processing for long-running tasks
- Containerized local deployment
- Automated testing and continuous integration
- Modular and extensible architecture

See **Current Implementation Status** for the capabilities available today.

> FridgeAI is an educational project. Allergy-related filtering and AI-generated recommendations must not be treated as medical or food-safety advice.

---

# Technology Stack

## Core Implementation

| Category | Technology |
| --- | --- |
| Programming language | Python |
| Backend API | FastAPI |
| Relational database | PostgreSQL |
| Vector database | Qdrant |
| Embedding generation | FastEmbed (`BAAI/bge-small-en-v1.5`) |
| Local LLM runtime | Ollama |
| Background processing | Celery and Redis |
| Frontend | Streamlit |
| Containerization | Docker Compose |
| Testing | pytest |
| Linting | Ruff |
| CI/CD | GitHub Actions |
| Deployment | Local development with Docker Compose |

All core application technologies are open source or free for local development.

---

# Architecture

## Current Session 3 Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
FastAPI API
  ├── PostgreSQL (structured recipe data)
  ├── Qdrant retrieval ──► Ollama / Gemma 3 (grounded generation)
  └── Redis ──► Celery Worker ──► FastEmbed ──► Qdrant indexing
```

The Streamlit interface communicates with FastAPI over HTTP. Recommendation requests retrieve semantically similar recipes from Qdrant, join them to the authoritative PostgreSQL records, and provide only that grounded context to a local Gemma 3 model through Ollama. Recipe creation queues a Celery task through Redis so the worker can generate embeddings and update Qdrant without blocking the API response.

## Target Architecture

The following architecture represents the target system after all four core sessions. Components are introduced incrementally.

```text
                          User
                            │
                            ▼
                   Streamlit Frontend
                            │
                            ▼
                     FastAPI Backend
                            │
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
      ▼                     ▼                     ▼
 PostgreSQL             Qdrant                  Ollama
Structured Data      Vector Search        Response Generation
                            ▲
                            │
                     Celery Worker
                      ├── Recipe ingestion
                      └── Embedding generation
                            ▲
                            │
                          Redis
                     Task Message Broker
```

---

# Repository Structure

```text
dbc_fridge_ai/
├── base/
│   ├── README.md
│   ├── session-1-foundation/       # Standalone completed milestone
│   ├── session-2-semantic-search/  # Standalone completed milestone
│   ├── session-3-rag/              # Standalone completed milestone
│   └── session-4-production/       # Planned; code added after Session 4
├── advanced/
│   ├── README.md
│   ├── hybrid-retrieval/
│   ├── reranking/
│   ├── evaluation/
│   ├── observability/
│   └── cloud-deployment/
├── apps/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── recipes.py
│   │   └── recommendations.py
│   └── web/
│       ├── __init__.py
│       └── app.py
├── src/
│   └── fridge_ai/
│       ├── __init__.py
│       ├── celery_app.py
│       ├── config.py
│       ├── database.py
│       ├── embeddings.py
│       ├── models.py
│       ├── rag.py
│       ├── schemas.py
│       ├── services.py
│       ├── tasks.py
│       └── vector_store.py
├── tests/
│   ├── __init__.py
│   ├── test_embeddings.py
│   ├── test_health.py
│   ├── test_recipes.py
│   └── test_tasks.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# FridgeAI Intensive Training Program

## Overview

**Build a Resume-Worthy AI Engineering Project from Scratch**

**4 Live Sessions • 6–8 Hours Total • Guided and Beginner-Friendly**

Build a focused, working MVP of an AI-powered meal recommendation system using real-world engineering practices.

The course concentrates on the essential end-to-end path:

- Data modeling
- Backend APIs
- Semantic retrieval
- Retrieval-Augmented Generation
- Background processing
- A simple user interface
- Automated testing
- Local containerized execution

To keep this scope achievable, learners work from prepared starter infrastructure and follow guided implementation steps.

Basic Python, Git, and command-line familiarity are recommended. Cloud deployment, infrastructure as code, production observability, orchestration, and scaling are reserved for future development or advanced courses.

---

# Technologies and Concepts Covered

## Artificial Intelligence

- Retrieval-Augmented Generation
- Embeddings
- Semantic search
- Prompt engineering

## Backend Development

- Python
- FastAPI
- REST APIs
- Request validation
- Asynchronous programming

## Data Storage

- PostgreSQL
- Qdrant vector database

## AI Models

- FastEmbed and BGE embedding models
- Ollama
- Open-weight language models

## Background Processing

- Celery
- Redis

## Infrastructure

- Docker
- Docker Compose

## DevOps

- GitHub Actions
- Continuous integration
- Continuous deployment concepts

## Software Engineering

- Production-oriented AI engineering
- System design
- Modular architecture
- Testing
- Technical interview communication

---

# Training Roadmap

## Session 1 — Application Foundation

Topics:

- Project architecture
- Development environment setup
- Python project structure
- FastAPI
- REST APIs
- Request validation
- PostgreSQL
- SQLAlchemy
- Docker and Docker Compose
- Recipe data model
- Automated tests
- Basic Streamlit interface
- Frontend-to-backend integration

Deliverables:

- Running FastAPI backend
- PostgreSQL database connection
- Recipe creation and retrieval API
- Request validation
- Automated API tests
- Streamlit UI connected to FastAPI
- Containerized local application
- One-command startup with Docker Compose

## Session 2 — Semantic Retrieval

**Status: complete**

Topics:

- Embeddings
- FastEmbed and the BGE small English embedding model
- Qdrant
- Vector search
- Semantic recipe search

Deliverables:

- Recipe embedding pipeline
- Qdrant recipe collection
- Semantic search API
- Search interface in Streamlit

## Session 3 — Retrieval-Augmented Generation

**Status: complete**

Topics:

- Ollama
- Prompt engineering
- Retrieval-Augmented Generation
- Celery
- Redis
- Recipe ingestion
- Background embedding generation

Deliverables:

- Complete RAG pipeline
- AI-generated meal recommendations
- Background indexing workflow
- Recommendation explanations with retrieved context

## Session 4 — Production Engineering

Topics:

- Streamlit UI refinement
- GitHub Actions
- Automated testing improvements
- Error handling
- Logging
- Docker Compose refinement
- Local deployment
- Future deployment directions
- Resume presentation
- Technical interview storytelling

Deliverables:

- Polished end-to-end application
- Refined user experience
- Continuous integration workflow
- Improved test coverage
- Interview-ready project documentation

---

# Learning Outcomes

After completing the project, learners will be able to:

- Design an end-to-end AI application
- Explain Retrieval-Augmented Generation
- Build REST APIs using FastAPI
- Validate API requests with Pydantic
- Design relational and vector data storage
- Generate and manage embeddings
- Build semantic search applications
- Implement asynchronous processing
- Containerize multi-service applications
- Build CI/CD pipelines
- Explain architectural decisions during technical interviews

---

# Who Should Join

This project is intended for:

- Software engineering internship candidates
- Computer science students
- Junior software engineers
- Developers transitioning into AI engineering
- Learners building their first substantial portfolio project

---

# Prerequisites

Recommended background:

- Basic Python programming
- Familiarity with Git
- Basic command-line experience

No previous AI or machine-learning experience is required.

---

# Getting Started

## Prerequisites

Install:

- Git
- Docker Desktop
- [Ollama](https://ollama.com/download/mac) on macOS 14 or later

Python 3.12 or later is also required for development outside Docker.

Download the local recommendation model and ensure Ollama is running:

```bash
ollama pull gemma3:4b
curl http://localhost:11434/api/tags
```

## Clone the Repository

```bash
git clone https://github.com/raygu911/dbc_fridge_ai.git
cd dbc_fridge_ai
git switch dev
```

## Configure the Environment

Create your local configuration:

```bash
cp .env.example .env
```

The example values are suitable for local development. Do not use them for a public deployment.

The `.env` file contains local configuration and is intentionally excluded from Git.

## Start FridgeAI with Docker

Build and start PostgreSQL, Qdrant, Redis, the Celery worker, FastAPI, and Streamlit. Ollama runs natively on macOS so it can use Apple hardware acceleration.

```bash
docker compose up --build -d
```

Check the services:

```bash
docker compose ps
```

The PostgreSQL, Qdrant, Redis, and FastAPI services should report a healthy status. The worker should report `ready` in its logs.

Open:

- Streamlit UI: http://localhost:8501
- FastAPI documentation: http://localhost:8000/docs
- FastAPI health endpoint: http://localhost:8000/health

## Stop FridgeAI

Stop the containers while preserving recipe data:

```bash
docker compose down
```

To stop the containers and permanently remove local PostgreSQL data, Qdrant vectors, Redis data, and the downloaded embedding-model cache:

```bash
docker compose down --volumes
```

> Warning: `--volumes` permanently removes all locally stored recipes, recipe vectors, task data, and cached embedding models. It does not remove the native Ollama model.

---

# Local Development

## Create the Python Environment

Using Conda:

```bash
conda create --name fridge-ai python=3.12
conda activate fridge-ai
```

Install the application and development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Start PostgreSQL, Qdrant, and Redis

```bash
docker compose up -d database qdrant redis
```

Check its status:

```bash
docker compose ps
```

## Start FastAPI

In one terminal:

```bash
conda activate fridge-ai
uvicorn apps.api.main:app --reload
```

FastAPI will be available at:

- http://localhost:8000
- http://localhost:8000/docs

## Start the Celery Worker

In another terminal:

```bash
conda activate fridge-ai
celery --app=fridge_ai.celery_app:celery_app worker --loglevel=info
```

For local processes, `.env` points Celery to Redis at `localhost:6379`. Docker Compose uses the internal `redis` service hostname instead.

## Start Streamlit

In another terminal:

```bash
conda activate fridge-ai
streamlit run apps/web/app.py
```

Streamlit will be available at:

- http://localhost:8501

---

# API Endpoints

## General

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Application welcome response |
| GET | `/health` | API health check |

## Recipes

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/v1/recipes` | Create a recipe |
| GET | `/api/v1/recipes` | List recipes |
| GET | `/api/v1/recipes/search?query={text}&limit={1-20}` | Search recipes by semantic similarity |
| GET | `/api/v1/recipes/{recipe_id}` | Retrieve one recipe |

## Recommendations

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/v1/recommendations` | Retrieve recipes and generate a grounded recommendation |

Interactive API documentation is available at:

- http://localhost:8000/docs

---

# Quality Checks

Ensure PostgreSQL is running (Qdrant is not required by the isolated test suite):

```bash
docker compose up -d database
```

Run linting:

```bash
ruff check .
```

Run tests:

```bash
pytest -v
```

The current test suite verifies:

- Root endpoint
- Health endpoint
- Recipe creation
- Recipe retrieval
- Recipe listing
- Missing-recipe behavior
- Invalid-request validation
- Semantic-search result mapping and scores
- Grounded recommendation prompt construction
- RAG recommendation response and source mapping
- Empty embedding-input validation
- Celery recipe-indexing task behavior
- Database transaction rollback during tests

---

# Useful Docker Commands

Start the complete application:

```bash
docker compose up --build -d
```

View service status:

```bash
docker compose ps
```

Follow all logs:

```bash
docker compose logs --follow
```

Follow one service:

```bash
docker compose logs --follow api
docker compose logs --follow web
docker compose logs --follow database
docker compose logs --follow qdrant
docker compose logs --follow redis
docker compose logs --follow worker
```

Stop the application:

```bash
docker compose down
```

Rebuild after dependency changes:

```bash
docker compose up --build -d
```

---

# Roadmap

## Version 1.0

- FastAPI backend
- PostgreSQL
- Streamlit
- Docker Compose
- Automated testing
- Qdrant
- FastEmbed and BGE embedding models
- Semantic recipe search
- Ollama
- Retrieval-Augmented Generation
- Celery
- Redis
- GitHub Actions

## Version 2.0

- Hybrid retrieval
- Cross-encoder reranking
- Improved prompt templates
- AI evaluation metrics
- Improved recommendation quality

## Version 3.0

- User authentication
- Personalized recommendations
- Nutrition tracking
- Meal planning
- Grocery-list generation

---

# Future Directions and Advanced Courses

The core implementation is intentionally limited to a guided MVP that can be completed within the 6–8 hour training program.

The capabilities below are not part of the core course. They are future project directions or material for dedicated advanced courses.

## Workflow Orchestration

- Temporal

## Observability

- OpenTelemetry
- Prometheus
- Grafana

## Infrastructure as Code

- OpenTofu
- Terraform

## Cloud Deployment

- AWS ECS
- AWS RDS
- AWS Secrets Manager
- AWS CloudWatch

## AI Enhancements

- Hybrid retrieval
- Cross-encoder reranking
- Multi-agent workflows
- Evaluation pipelines

## Security

- Authentication
- Authorization
- User accounts
- Secret management

## Scalability

- Kubernetes
- Horizontal scaling
- Load balancing

---

# Contributing

Contributions, suggestions, and feature requests are welcome.

If you find a bug or would like to propose an improvement:

1. Open an issue describing the change.
2. Create a feature branch.
3. Add or update tests.
4. Run Ruff and pytest.
5. Submit a pull request.

Beginner-friendly issues should be labeled `good first issue`.

---

# Project Philosophy

FridgeAI emphasizes engineering over experimentation.

Instead of building another chatbot demonstration, this project teaches how modern AI systems are designed—from backend APIs and structured data to vector search, RAG, deployment, and production-oriented software engineering.

The goal is not only to build a working application, but also to understand the architectural decisions behind every component. Learners should be able to explain their design, technology choices, implementation process, and tradeoffs during technical interviews.

---

# License

This project is licensed under the MIT License.
