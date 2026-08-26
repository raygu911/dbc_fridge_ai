# Session 4 — CI/CD, Deployment, and Cloud Operations

Session 4 deploys the AWS-ready application through controlled CI/CD and verifies that it can be monitored, recovered, rolled back, and removed safely.

- **Estimated guided time:** 4–6 hours
- **Status:** Planned
- **Prerequisite:** Completed Session 3 infrastructure

## Learning Outcomes

- Authenticate GitHub Actions to AWS through OIDC without long-lived keys.
- Build, tag, and publish immutable application images to Amazon ECR.
- Separate pull-request verification from approved deployment.
- Run migrations, deploy ECS services, smoke test, and stop or roll back failures.
- Configure HTTPS, dashboards, alerts, backups, recovery, and cost controls.
- Present the deployed architecture and its trade-offs clearly.

## Planned Delivery Flow

```text
Pull request
    → Ruff + pytest
    → Build containers
    → Validate Terraform
    → Publish Terraform plan for review

Approved merge or release
    → GitHub OIDC authentication
    → Push revision-tagged images to ECR
    → Apply approved infrastructure changes
    → Run database migrations
    → Deploy ECS services
    → Run smoke tests
    → Complete release or initiate rollback
```

## Planned Implementation

1. Configure GitHub environments, OIDC trust, and least-privilege deployment roles.
2. Add application and infrastructure pull-request checks.
3. Build and publish web, API, and worker images with immutable tags.
4. Deploy ECS task revisions and run database migrations.
5. Add liveness, readiness, indexing, retrieval, and generation smoke tests.
6. Define release failure and rollback behavior.
7. Configure TLS, CloudWatch dashboards, alarms, and budget alerts.
8. Exercise backup/restore, dependency failure, load, recovery, and teardown.
9. Produce architecture decisions, a walkthrough, and a resume narrative.

## Completion Gate

- Pull requests verify application and Terraform changes.
- Deployment uses OIDC rather than stored long-lived AWS keys.
- Every release maps to immutable source and image revisions.
- Smoke tests cover the critical RAG workflow.
- Failed releases preserve or restore the last working version.
- Dashboards and runbooks diagnose common failures.
- Backup/restore and teardown exercises succeed.
- Costs, limitations, decisions, and interview talking points are documented.

This session remains **planned** until its workflows, deployed snapshot, operational artifacts, and verification evidence exist.
