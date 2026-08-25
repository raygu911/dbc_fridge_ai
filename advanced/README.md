# FridgeAI Advanced Training

The advanced track extends the completed production milestone with measurable retrieval improvements, deeper observability, and a deployable cloud architecture. Every module will be a standalone project snapshot, just like the base sessions.

## Recommended Sequence

| Order | Module | Primary outcome | Effort | Guided time | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | [Evaluation](module-1-evaluation/) | Establish a repeatable quality baseline and regression gates | High | 3–4 hours | Planned |
| 2 | [Hybrid retrieval](module-2-hybrid-retrieval/) | Combine semantic and lexical signals and prove the improvement | High | 3–4 hours | Planned |
| 3 | [Reranking](module-3-reranking/) | Reorder retrieved candidates with a second-stage model | High | 2.5–3.5 hours | Planned |
| 4 | [Observability](module-4-observability/) | Trace and monitor API, retrieval, generation, and worker behavior | High | 3–4 hours | Planned |
| 5 | [Cloud deployment](module-5-cloud-deployment/) | Deploy, secure, operate, and cost-control the complete system | Very high | 4–6 hours | Planned |

Estimated guided time for the complete advanced track is **15.5–21.5 hours**, excluding cloud account setup, model downloads, optional experiments, and provider costs.

Evaluation comes first because later retrieval changes need a stable dataset and metrics. Observability follows the model-quality work so traces and dashboards capture the final pipeline. Cloud deployment is last because it integrates every earlier concern.

## Entry Requirements

Before starting, trainees should be able to run and explain Session 4, including:

- FastAPI, PostgreSQL, Qdrant, Redis, Celery, Streamlit, and Ollama responsibilities
- Semantic retrieval and grounded prompt construction
- Background indexing and failure handling
- Liveness, readiness, request IDs, structured logs, tests, and CI

Start each module from the latest completed advanced snapshot. Until Module 1 exists, use [`base/session-4-production`](../base/session-4-production/) as the baseline.

## Shared Module Standard

Each module is complete only when it contains:

- A standalone runnable code snapshot and environment template
- An architecture note explaining the new data flow and trade-offs
- Automated unit and integration tests
- Reproducible commands for the experiment or operational check
- A before/after result against an explicit baseline
- A completion checklist and interview talking points
- Updated disk, model, infrastructure, and cost notes where relevant

## Progression Gates

1. **Evaluation → Hybrid retrieval:** freeze a versioned query set, relevance judgments, baseline metrics, and report format.
2. **Hybrid retrieval → Reranking:** demonstrate that fusion is reproducible and does not regress the agreed baseline.
3. **Reranking → Observability:** select the final retrieval pipeline and record its latency and quality budget.
4. **Observability → Cloud:** define service-level indicators, privacy rules, dashboards, and an incident runbook.
5. **Cloud completion:** pass deployment, rollback, backup/restore, security, cost, and smoke-test checks.

## Cost and Safety Boundaries

Evaluation and model experiments may consume significant CPU, memory, disk, and time. Cloud deployment may incur ongoing charges. Every module should offer a local path where practical, document optional paid services before use, avoid committing secrets or evaluation prompts containing personal data, and include explicit teardown instructions.
