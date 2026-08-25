# Advanced Module 3 — Reranking

Add a second-stage relevance model that scores the query and each retrieved recipe together before selecting context for generation.

- **Effort:** High
- **Estimated guided time:** 2.5–3.5 hours
- **Status:** Planned
- **Prerequisite:** Evaluated hybrid retriever

## Learning Outcomes

- Distinguish fast candidate retrieval from more expensive pairwise relevance scoring.
- Select candidate-set and final-context sizes using measured quality and latency.
- Run a local cross-encoder-style reranker behind a replaceable interface.
- Add thresholds and fallbacks for low-confidence or unavailable-model cases.
- Decide whether caching is safe and useful for normalized queries and recipe revisions.

## Planned Implementation

1. Define a reranker protocol so the model can be replaced or mocked.
2. Retrieve a wider hybrid candidate set, then score query–recipe pairs.
3. Select the top context recipes using reranker scores and a configurable threshold.
4. Preserve retrieval and reranking scores for debugging and evaluation.
5. Add graceful fallback to hybrid order when the reranker is unavailable.
6. Benchmark candidate sizes and optionally cache reranking results with versioned keys.
7. Compare hybrid-only and reranked pipelines using the frozen evaluation dataset.

## Deliverables

- Reranker abstraction and local implementation
- Configurable candidate and final-context limits
- Fallback and timeout behavior
- Score-aware API/source response updates
- Quality-versus-latency experiment report
- Tests for ordering, thresholds, ties, timeout, fallback, and cache invalidation

## Verification Gate

- Reranking improves the chosen primary ranking metric on the frozen dataset.
- Added latency stays within the documented local budget.
- Reranker failure does not make search or recommendations unavailable.
- Recipe updates cannot reuse stale cached scores.
- Prompt context contains only the configured final number of sources.

## Interview Focus

Explain bi-encoder retrieval versus cross-encoder reranking, why only a limited candidate set is reranked, and how you balance relevance gains against latency, compute, and operational complexity.
