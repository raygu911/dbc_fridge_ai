# Advanced Module 2 — Hybrid Retrieval

Combine semantic similarity with lexical search so FridgeAI handles both conceptual requests and exact ingredients, tags, or recipe names.

- **Effort:** High
- **Estimated guided time:** 3–4 hours
- **Status:** Planned
- **Prerequisite:** Completed evaluation module with a frozen baseline

## Learning Outcomes

- Build PostgreSQL full-text retrieval alongside Qdrant semantic search.
- Understand score incompatibility and rank-based fusion.
- Apply dietary, time, and ingredient filters consistently across both retrievers.
- Diagnose which query types benefit from semantic, lexical, or hybrid retrieval.
- Measure quality and latency changes against the evaluation baseline.

## Planned Implementation

1. Add a searchable PostgreSQL text representation and appropriate index.
2. Implement lexical candidate retrieval with normalized query handling.
3. Retrieve semantic and lexical candidates independently.
4. Fuse ranked lists with Reciprocal Rank Fusion using stable recipe IDs.
5. Add configurable semantic, lexical, and hybrid modes for experiments.
6. Apply metadata filters before or during retrieval and document the trade-off.
7. Extend the evaluation report with per-query wins, losses, latency, and failure analysis.

## Deliverables

- Lexical retriever and database migration/index definition
- Hybrid retrieval service with configurable candidate counts and fusion constant
- Filtered search API and Streamlit controls
- Unit tests for fusion, duplicates, empty result sets, and filters
- Before/after evaluation report against semantic-only Session 4

## Verification Gate

- Exact-name and exact-ingredient queries improve without materially regressing semantic queries.
- Fusion produces deterministic ordering and never returns duplicate recipes.
- Dietary and cooking-time filters are enforced in tests.
- The report includes quality metrics plus p50/p95 retrieval latency.
- Any accepted regression is documented with a clear trade-off rationale.

## Interview Focus

Explain why dense retrieval can miss exact tokens, why raw lexical and vector scores should not be naively added, how Reciprocal Rank Fusion works, and when filtering should happen before versus after retrieval.
