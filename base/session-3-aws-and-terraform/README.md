# Session 3 — AWS Architecture and Terraform

Session 3 adapts the completed local RAG application for AWS and provisions reproducible cloud infrastructure with Terraform.

- **Estimated guided time:** 4–6 hours
- **Status:** Planned
- **Baseline:** [`../session-2-rag-and-production`](../session-2-rag-and-production/)

## Learning Outcomes

- Map the local Compose architecture to explicit AWS services.
- Separate web, API, and worker container responsibilities.
- Replace the local-only model dependency with a configurable provider interface.
- Manage database migrations, runtime configuration, and secrets safely.
- Define networking, compute, data, identity, secrets, and logging with Terraform.
- Review plans, provision a clean environment, and remove billable resources.

## Planned Architecture

```text
Users → Application Load Balancer
          ├── Streamlit on ECS/Fargate
          └── FastAPI on ECS/Fargate
                    ├── RDS PostgreSQL
                    ├── Qdrant or a documented managed vector service
                    ├── Redis → Celery worker on ECS/Fargate
                    ├── Hosted model endpoint
                    └── CloudWatch logs

Images         → Amazon ECR
Secrets        → AWS Secrets Manager
Infrastructure → Terraform
```

## Planned Implementation

1. Record provider, region, inference, vector storage, environment, and cost decisions.
2. Add a model-provider interface, cloud-safe configuration, and migrations.
3. Define VPC networking, security groups, and load balancing.
4. Define ECR and ECS/Fargate services for web, API, and worker containers.
5. Define RDS PostgreSQL, Redis, secrets, IAM roles, and CloudWatch logs.
6. Configure Terraform constraints, variables, outputs, remote state, and environments.
7. Add formatting, validation, planning, security checks, and teardown instructions.

## Completion Gate

- Terraform formatting, validation, and static checks pass.
- A reviewed plan describes the expected environment.
- Documented commands provision a clean environment.
- Secrets are absent from source, images, state outputs, and logs.
- Network access and IAM permissions follow least privilege.
- Teardown succeeds and measured cost is documented.

This session remains **planned** until its Terraform, cloud-adapted application snapshot, tests, and provisioning evidence exist.
