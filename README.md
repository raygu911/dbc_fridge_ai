# FridgeAI Training Program

> Build, productionize, and deploy a resume-worthy AI engineering project, then optionally deepen its retrieval quality and observability.

FridgeAI is organized as cumulative project milestones. The required Base Track covers the complete journey from application development through AWS deployment. The Advanced Track contains optional AI engineering extensions.

> **Current status:** Base Sessions 1 and 2 are implemented. Base Sessions 3 and 4 and all Advanced modules are planned.

## Training Tracks

| Track | Purpose | Status |
| --- | --- | --- |
| [Base training](base/) | Build the local RAG application, provision AWS with Terraform, and deploy through CI/CD | Sessions 1–2 complete; Sessions 3–4 planned |
| [Advanced training](advanced/) | Evaluate and improve retrieval, reranking, and distributed observability | Planned and optional |

## Repository Structure

```text
dbc_fridge_ai/
├── CURRICULUM_RESTRUCTURE_PLAN.md
├── base/
│   ├── session-1-application-and-search/
│   ├── session-2-rag-and-production/
│   ├── session-3-aws-and-terraform/
│   └── session-4-deployment-and-operations/
└── advanced/
    ├── module-1-evaluation/
    ├── module-2-hybrid-retrieval/
    ├── module-3-reranking/
    └── module-4-advanced-observability/
```

## Base Training Roadmap

| Session | Focus | Guided hands-on estimate | Status |
| --- | --- | ---: | --- |
| [Session 1 — Application and Search](base/session-1-application-and-search/) | FastAPI, PostgreSQL, Streamlit, Docker, FastEmbed, Qdrant, and semantic search | 3–4 hours | Complete |
| [Session 2 — RAG and Production](base/session-2-rag-and-production/) | Ollama, grounded generation, Redis, Celery, tests, logging, resilience, and CI | 3–4 hours | Complete |
| [Session 3 — AWS and Terraform](base/session-3-aws-and-terraform/) | AWS architecture, ECS/Fargate, data services, IAM, and Terraform | 4–6 hours | Planned |
| [Session 4 — Deployment and Operations](base/session-4-deployment-and-operations/) | OIDC, ECR, CI/CD, rollback, monitoring, recovery, and cost control | 4–6 hours | Planned |

The complete hands-on Base Track is expected to require **14–20 guided hours**. A 6–8-hour accelerated workshop requires prepared code, infrastructure, and selected exercises rather than building every component from scratch.

## Milestone Progression

### Session 1

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    └── FastEmbed → Qdrant
```

Trainees build the application foundation, persistence layer, frontend integration, container environment, embeddings, vector storage, semantic search, validation, and tests.

### Session 2

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    ├── Qdrant retrieval → Ollama / Gemma
                    └── Redis → Celery → FastEmbed → Qdrant indexing
```

Trainees add grounded recommendations, source attribution, background indexing, structured logs, request correlation, readiness checks, resilient UI behavior, failure-path tests, and CI.

### Session 3

Trainees adapt the application for cloud configuration, map local services to AWS, and provision networking, compute, data, identity, secrets, and logging with Terraform.

### Session 4

Trainees build immutable images, authenticate GitHub Actions through OIDC, deploy through CI/CD, run migrations and smoke tests, verify rollback and recovery, monitor the system, and document cost-aware teardown.

## Running an Implemented Session

```bash
cd base/session-2-rag-and-production
cp .env.example .env
docker compose up --build -d --wait
python -m pip install -e ".[dev]"
ruff check .
pytest
```

Run only one local milestone at a time because the standalone projects use the same ports.

## Advanced Extensions

After completing the Base Track, trainees may continue with retrieval and generation evaluation, hybrid retrieval, cross-encoder reranking, and advanced distributed observability. These extensions are optional and are not required to satisfy the four-session program promise.

## Prerequisites and Cost

Sessions 1 and 2 require Git, Docker Desktop, Python 3.12 or later, basic Python and command-line familiarity, and native Ollama with the configured model. Sessions 3 and 4 additionally require an AWS account and may incur charges. Set a budget and verify teardown before provisioning resources.

## Educational Safety Notice

FridgeAI is educational. Dietary tags, retrieved content, and AI-generated recommendations must not be treated as medical or food-safety advice.

## License

This project is licensed under the MIT License.
