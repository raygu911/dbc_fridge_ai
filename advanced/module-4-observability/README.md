# Advanced Module 4 — Observability

Extend Session 4 diagnostics into end-to-end traces, metrics, dashboards, and actionable operational signals.

- **Effort:** High
- **Estimated guided time:** 3–4 hours
- **Status:** Planned
- **Prerequisite:** Final evaluated retrieval and reranking pipeline

## Learning Outcomes

- Propagate trace context across Streamlit, FastAPI, Celery, Redis, database, vector search, and model calls.
- Define service-level indicators for availability, latency, retrieval, generation, and indexing.
- Separate logs, metrics, and traces by the questions each answers.
- Design privacy-aware telemetry that avoids storing secrets and raw user content by default.
- Turn failure symptoms into dashboards, alerts, and a repeatable incident runbook.

## Planned Implementation

1. Preserve Session 4 JSON logs and request IDs as the logging baseline.
2. Add OpenTelemetry spans for API requests, retrieval stages, reranking, Ollama calls, and Celery tasks.
3. Propagate trace context through queued indexing tasks.
4. Export local metrics for request rates, errors, latency, queue depth, task outcomes, and model duration.
5. Add a local collector and dashboard stack to Docker Compose.
6. Define redaction, sampling, and retention rules for prompts, recipes, and identifiers.
7. Simulate database, Qdrant, Redis, worker, and Ollama failures and document diagnosis.

## Deliverables

- Instrumented API, retrieval pipeline, model client, and worker
- Local trace and metrics backend with dashboards
- Service-level indicator and objective definitions
- Privacy and telemetry policy
- Alert examples and failure-injection script
- Incident diagnosis and recovery runbook

## Verification Gate

- One recommendation can be followed from incoming request through retrieval, reranking, and model generation.
- One recipe creation trace links the API request to its Celery indexing task.
- Dashboards show request latency, error rate, dependency health, task failures, and model duration.
- Telemetry tests confirm secrets and raw prompts are not recorded by default.
- Each simulated dependency failure is diagnosable using the documented runbook.

## Interview Focus

Explain correlation versus distributed tracing, RED and queue/worker metrics, trace sampling, cardinality risks, privacy-aware AI telemetry, and how an SLO connects dashboards to user impact.
