# FridgeAI Advanced Training

The Advanced Track contains optional extensions for trainees who have completed the four-session Base Track and want deeper AI engineering experience. These modules are not required to satisfy the core program listing.

## Recommended Sequence

| Order | Module | Primary outcome | Guided time | Status |
| --- | --- | --- | ---: | --- |
| 1 | [Evaluation](module-1-evaluation/) | Establish reproducible retrieval and generation baselines | 3–4 hours | Planned |
| 2 | [Hybrid retrieval](module-2-hybrid-retrieval/) | Combine semantic and lexical retrieval and measure the change | 3–4 hours | Planned |
| 3 | [Reranking](module-3-reranking/) | Improve ordering with a second-stage relevance model | 2.5–3.5 hours | Planned |
| 4 | [Advanced observability](module-4-advanced-observability/) | Add distributed tracing and privacy-aware AI telemetry | 3–4 hours | Planned |

The estimated guided time for all optional extensions is **11.5–15 hours**, excluding model downloads and experiments.

## Entry Requirements

Trainees should be able to explain the completed Base Track: application services, semantic retrieval, grounded generation, asynchronous indexing, failure handling, AWS architecture, Terraform, CI/CD, monitoring, rollback, recovery, and teardown.

Until Base Sessions 3 and 4 are implemented, use [`base/session-2-rag-and-production`](../base/session-2-rag-and-production/) as the runnable baseline and defer cloud-dependent extension work.

## Shared Module Standard

Each module is complete only when it contains a runnable cumulative snapshot, tests, reproducible experiments or operational checks, a before/after result against an explicit baseline, architecture and trade-off notes, a completion checklist, and interview talking points.

## Progression

1. Evaluation freezes the dataset, metrics, configuration, and report format.
2. Hybrid retrieval demonstrates measured improvement against that baseline.
3. Reranking compares quality and latency against the evaluated hybrid pipeline.
4. Advanced observability traces and measures the final selected pipeline.

Base Session 4 will include the CloudWatch monitoring needed to operate the deployment. Advanced Module 4 goes further with OpenTelemetry, cross-component trace propagation, AI-specific metrics, and telemetry privacy controls.
