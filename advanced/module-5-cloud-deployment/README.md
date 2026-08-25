# Advanced Module 5 — Cloud Deployment

Deploy the evaluated and observable FridgeAI system using managed infrastructure while preserving security, reproducibility, rollback, and cost control.

- **Effort:** Very high
- **Estimated guided time:** 4–6 hours
- **Status:** Planned
- **Prerequisite:** Completed observability module and incident runbook
- **Cost:** Provider resources may incur charges; define a budget and teardown plan before provisioning

## Learning Outcomes

- Translate local Compose services into explicit managed or containerized cloud components.
- Build immutable images and promote the same artifact through environments.
- Manage secrets, network access, migrations, health checks, and least-privilege identities.
- Choose between managed vector storage and self-hosted Qdrant using operational criteria.
- Choose a hosted inference endpoint or GPU-backed model service instead of assuming local Ollama.
- Validate rollback, backup/restore, scaling, observability, and teardown.

## Planned Implementation

1. Write an architecture decision record for provider, region, inference, vector storage, and cost ceiling.
2. Build versioned API, worker, and web images in a container registry.
3. Provision networking, compute, PostgreSQL, Redis, secrets, and observability with infrastructure as code.
4. Configure Qdrant or a managed vector alternative and document data migration.
5. Add a cloud-compatible model-provider interface and select an inference deployment.
6. Add schema migration, deployment, smoke-test, and rollback stages to CI/CD.
7. Configure TLS, restricted ingress, service identities, backups, resource limits, and autoscaling.
8. Run failure recovery, backup/restore, load, cost, and teardown exercises.

## Deliverables

- Cloud architecture diagram and decision records
- Infrastructure-as-code project with separate environment configuration
- Image build and deployment pipeline
- Secrets and identity design
- Database/vector migration and backup/restore procedure
- Smoke, rollback, load, and disaster-recovery checks
- Monthly cost estimate, budget alerts, and complete teardown instructions

## Verification Gate

- A clean environment can be provisioned from documented commands without manual secret copying.
- Public traffic uses TLS and only intended services are reachable.
- Deployment smoke tests cover liveness, readiness, recipe creation, indexing, retrieval, and generation.
- A failed release automatically stops or rolls back without corrupting data.
- PostgreSQL and vector data can be restored in a recovery exercise.
- Dashboards and alerts work in the deployed environment.
- The measured cost is within the documented budget, and teardown removes billable resources.

## Interview Focus

Explain service mapping from local Compose to cloud infrastructure, build-once/promote-many delivery, migration and rollback safety, secrets and identity boundaries, inference deployment trade-offs, recovery objectives, autoscaling signals, and cost governance.
