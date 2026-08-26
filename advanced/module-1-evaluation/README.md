# Advanced Module 1 — Evaluation

Build the measurement foundation used to decide whether every later retrieval or generation change is actually better.

- **Effort:** High
- **Estimated guided time:** 3–4 hours
- **Status:** Planned
- **Baseline:** completed Base Session 4; use `base/session-2-rag-and-production` until cloud sessions are implemented

## Learning Outcomes

- Design versioned evaluation cases with queries, relevant recipe IDs, constraints, and expected behavior.
- Measure retrieval with Recall@k, Precision@k, Mean Reciprocal Rank, and nDCG.
- Evaluate grounded generation for faithfulness, relevance, source use, and constraint satisfaction.
- Separate deterministic CI checks from slower optional model-based experiments.
- Compare experiments without silently changing the dataset, prompt, model, or configuration.

## Planned Implementation

1. Create a small human-reviewed recipe corpus and evaluation dataset in version-controlled JSONL.
2. Add a CLI that runs semantic retrieval against the dataset and writes a timestamped JSON report.
3. Implement ranking metrics with unit-tested edge cases.
4. Add deterministic prompt and source-attribution regression tests.
5. Add a human-review rubric for recommendation usefulness and faithfulness.
6. Optionally add model-assisted judging, clearly separated from ground truth and never required for CI.
7. Record model, prompt, dataset, and configuration versions in every report.

## Deliverables

- Versioned evaluation dataset and schema
- Retrieval metric library and CLI runner
- Baseline Session 4 metrics report
- Generation rubric and sample reviewed outputs
- Fast CI regression subset and optional full evaluation command
- Experiment comparison template

## Verification Gate

- The same configuration produces the same retrieval metrics across repeated runs.
- Metric implementations pass hand-calculated test cases.
- Reports identify the code revision, dataset version, embedding model, prompt version, and configuration.
- CI fails on a deliberately introduced retrieval regression.
- Human and optional model-assisted judgments are reported separately.

## Interview Focus

Explain why offline metrics need curated relevance judgments, why retrieval and generation require different measures, how model judges can introduce bias, and how evaluation prevents “demo-driven development.”
