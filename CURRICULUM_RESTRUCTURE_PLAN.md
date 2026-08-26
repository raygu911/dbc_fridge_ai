# FridgeAI Curriculum Restructure Plan

## Decision Summary

FridgeAI will use two curriculum layers:

1. **Base Track:** four required sessions covering every capability promised in the program listing, from local application development through AWS deployment.
2. **Advanced Track:** four optional extensions for trainees who want deeper AI engineering knowledge after completing the base project.

The existing local application work remains the foundation. The curriculum will be consolidated and expanded rather than discarding the completed implementation.

## Program Promise

After completing the four-session Base Track, a trainee should have a project that demonstrates:

- FastAPI backend development
- PostgreSQL persistence
- Streamlit frontend integration
- Embedding generation
- Vector storage and semantic retrieval with Qdrant
- Retrieval-Augmented Generation (RAG)
- Local or replaceable model integration
- Redis and Celery background processing
- Docker containerization
- Automated testing and continuous integration
- AWS architecture and deployment
- Terraform infrastructure as code
- GitHub Actions-based CI/CD
- Health checks, logging, monitoring, rollback, and cost-aware operations
- An architecture explanation, project narrative, and resume-ready bullet

The Advanced Track is not required to satisfy the listing. It adds evaluation, retrieval optimization, reranking, and deeper observability.

## Target Repository Structure

```text
dbc_fridge_ai/
├── README.md
├── base/
│   ├── README.md
│   ├── session-1-application-and-search/
│   ├── session-2-rag-and-production/
│   ├── session-3-aws-and-terraform/
│   └── session-4-deployment-and-operations/
└── advanced/
    ├── README.md
    ├── module-1-evaluation/
    ├── module-2-hybrid-retrieval/
    ├── module-3-reranking/
    └── module-4-advanced-observability/
```

Each base session should remain a standalone, cumulative project milestone. A trainee should be able to enter a session directory, configure the environment, run the system, execute the tests, and understand what changed from the previous milestone.

## Current-to-New Mapping

| New curriculum item | Current source material | Required action |
| --- | --- | --- |
| Base Session 1 | Current Base Sessions 1 and 2 | Consolidate application foundation and semantic retrieval into one milestone |
| Base Session 2 | Current Base Sessions 3 and 4 | Consolidate RAG, asynchronous processing, and production readiness |
| Base Session 3 | Former Advanced Modules 1 and 2 from the proposed cloud track | Implement AWS adaptation and Terraform infrastructure |
| Base Session 4 | Former Advanced Modules 3 and 4 from the proposed cloud track | Implement CI/CD, deployment, operations, and portfolio delivery |
| Advanced Module 1 | Current planned Evaluation module | Retain as optional advanced work |
| Advanced Module 2 | Current planned Hybrid Retrieval module | Retain as optional advanced work |
| Advanced Module 3 | Current planned Reranking module | Retain as optional advanced work |
| Advanced Module 4 | Current planned Observability module | Retain and clarify that it goes beyond the base CloudWatch coverage |
| Current planned Cloud Deployment module | Cloud plan and requirements | Split its content across new Base Sessions 3 and 4 |

## Base Track

### Session 1 — Application Foundation and Semantic Search

**Purpose:** Build the usable application foundation and add semantic recipe discovery.

**Combines:** Current Base Sessions 1 and 2.

**Topics:**

- Repository and application structure
- FastAPI endpoints and request/response schemas
- PostgreSQL models, persistence, and service layer
- Streamlit frontend and API integration
- Dockerfile and Docker Compose fundamentals
- Input validation and API error handling
- Automated API and service tests
- Embedding concepts and generation with FastEmbed
- Qdrant vector collections and persistence
- Recipe indexing and vector-to-relational ID mapping
- Natural-language semantic search
- Similarity scores and basic retrieval limitations

**Expected deliverable:**

A containerized recipe application in which users can create recipes and find relevant recipes through natural-language semantic search.

**Completion checks:**

- PostgreSQL, Qdrant, API, and Streamlit services start successfully.
- A recipe can be created through the application.
- The recipe is represented in the vector store.
- Semantic search returns the expected relational recipe data.
- Automated tests and lint checks pass.
- The trainee can explain why PostgreSQL remains the source of truth while Qdrant supports retrieval.

### Session 2 — RAG and Production Readiness

**Purpose:** Turn semantic retrieval into a grounded AI workflow and make the local system reliable enough to present as a portfolio project.

**Combines:** Current Base Sessions 3 and 4.

**Topics:**

- Retrieval-Augmented Generation workflow
- Grounded prompt construction
- Ollama/Gemma integration for local development
- Returning retrieved sources with generated recommendations
- Redis as the task broker
- Celery workers and asynchronous indexing
- Retry and failure behavior for background jobs
- Liveness and dependency-readiness endpoints
- Structured JSON logging and request IDs
- Safe API errors and resilient Streamlit states
- Unit, integration, and failure-path tests
- GitHub Actions continuous integration
- Local operating and troubleshooting procedures
- Architecture explanation and interview narrative

**Expected deliverable:**

A complete local RAG recipe application with grounded answers, asynchronous embedding work, dependency diagnostics, controlled failure handling, and continuously verified code.

**Completion checks:**

- Recipe creation queues background vector indexing.
- Semantic retrieval supplies sources to the model.
- Generated recommendations return source information.
- Model and infrastructure failures produce controlled responses.
- Liveness and readiness checks behave independently.
- Request IDs connect user-visible failures with structured logs.
- Ruff, pytest, Docker Compose validation, and GitHub Actions pass.
- The trainee can explain the architecture and major design trade-offs.

### Session 3 — AWS Architecture and Terraform

**Purpose:** Adapt the local application for AWS and provision reproducible cloud infrastructure with Terraform.

**Topics:**

- Mapping local Compose services to AWS components
- Separating the web, API, and Celery worker containers
- Introducing a replaceable model-provider interface
- Selecting and documenting the cloud inference approach
- Database schema migrations
- Runtime configuration and secrets management
- AWS account, region, environment, and cost decisions
- VPC, subnets, route tables, and security groups
- Application Load Balancer
- Amazon ECR image repositories
- Amazon ECS with Fargate services and task definitions
- Amazon RDS for PostgreSQL
- Redis deployment, such as Amazon ElastiCache
- AWS Secrets Manager
- IAM execution and task roles with least privilege
- CloudWatch log groups
- Terraform providers, variables, outputs, modules, and version constraints
- Remote Terraform state and locking
- Development environment configuration
- Terraform formatting, validation, planning, application, and teardown

**Expected deliverable:**

A version-controlled Terraform project that can provision the documented FridgeAI AWS environment without manually recreating resources in the AWS Console.

**Suggested infrastructure layout:**

```text
Users → Application Load Balancer
          ├── Streamlit service on ECS/Fargate
          └── FastAPI service on ECS/Fargate
                    ├── RDS PostgreSQL
                    ├── Qdrant or documented managed vector service
                    ├── Redis → Celery worker on ECS/Fargate
                    ├── Hosted model endpoint
                    └── CloudWatch logs

Container images → Amazon ECR
Secrets          → AWS Secrets Manager
Infrastructure   → Terraform
```

**Completion checks:**

- `terraform fmt`, `terraform validate`, and static infrastructure checks pass.
- A reviewed Terraform plan describes the expected environment.
- Infrastructure can be provisioned from documented commands.
- Containers can access only the dependencies they require.
- Secrets are not committed or embedded in images.
- Public access is limited to intended entry points.
- Infrastructure outputs provide the information needed by deployment automation.
- A complete teardown procedure is documented and tested.

### Session 4 — CI/CD, Deployment, and Cloud Operations

**Purpose:** Deploy the application repeatably, verify releases, operate the environment, and present the result professionally.

**Topics:**

- GitHub Actions for application and infrastructure workflows
- GitHub OIDC authentication to AWS
- Pull-request linting, testing, image building, and Terraform planning
- Immutable container tags based on the Git revision
- Publishing web, API, and worker images to ECR
- Controlled Terraform application
- ECS service deployment
- Database migration stage
- Post-deployment smoke tests
- Liveness and readiness verification
- Failed-deployment stopping or rollback
- HTTPS and certificate configuration
- CloudWatch logs, metrics, dashboards, and alarms
- Backup and restore procedures
- Failure-injection and recovery exercises
- Basic load testing and capacity observations
- Cost estimation, budget alerts, and teardown
- Cloud architecture diagram and decision records
- Final project walkthrough, interview narrative, and resume bullet

**Expected deliverable:**

A deployed and observable FridgeAI environment with a repeatable CI/CD workflow, release verification, recovery documentation, and portfolio-ready evidence.

**Recommended workflow:**

```text
Pull request
    → Ruff and pytest
    → Build containers
    → Validate Terraform
    → Publish Terraform plan for review

Approved merge or release
    → Authenticate to AWS through OIDC
    → Build and tag immutable images
    → Push images to ECR
    → Apply approved infrastructure changes
    → Run database migrations
    → Deploy ECS services
    → Run smoke tests
    → Complete release or initiate rollback
```

**Completion checks:**

- No long-lived AWS credentials are stored in the repository.
- Pull requests run application and infrastructure checks.
- The deployment uses immutable, traceable container versions.
- Smoke tests cover health, readiness, recipe creation, indexing, retrieval, and generation.
- A failed release does not silently replace a working deployment.
- Logs and dashboards make common failures diagnosable.
- PostgreSQL and vector data have a documented recovery strategy.
- The environment has a measured cost and working teardown process.
- The trainee can demonstrate the application and explain deployment trade-offs.

## Advanced Track — Optional Extensions

The Advanced Track is outside the required four-session program. It is intended for trainees who want to go deeper after they can run and explain the deployed base project.

### Module 1 — RAG Evaluation

- Versioned evaluation queries and relevance judgments
- Recall@k, Precision@k, MRR, and nDCG
- Generation faithfulness and relevance rubrics
- Deterministic regression checks versus optional model judging
- Reproducible baseline and comparison reports

### Module 2 — Hybrid Retrieval

- PostgreSQL lexical search alongside Qdrant semantic search
- Reciprocal Rank Fusion
- Consistent filtering across retrievers
- Query-level wins, losses, and failure analysis
- Quality and latency comparison against the evaluation baseline

### Module 3 — Cross-Encoder Reranking

- Candidate retrieval versus second-stage scoring
- Replaceable reranker interface
- Candidate and final-context limits
- Thresholds, timeouts, fallback, and caching decisions
- Measured quality-versus-latency trade-offs

### Module 4 — Advanced Observability

- OpenTelemetry instrumentation
- Distributed traces across API, retrieval, generation, and Celery
- Model, retrieval, queue, and worker metrics
- Trace propagation through asynchronous work
- Privacy-aware telemetry, redaction, sampling, and retention
- Advanced dashboards, service objectives, and incident response

Base Session 4 should still include sufficient CloudWatch logging, metrics, and alerts to operate a deployed system. This optional module goes deeper into distributed tracing and AI-specific telemetry.

## Scope Boundaries

### Included in the required Base Track

- A working local AI application
- Semantic retrieval and grounded generation
- Asynchronous processing
- Containers and automated tests
- AWS infrastructure defined with Terraform
- CI/CD and a verified cloud deployment
- Basic monitoring, recovery, cost control, and teardown
- Project and architecture presentation

### Optional Advanced Track

- Formal RAG evaluation datasets and metrics
- Hybrid lexical and semantic retrieval
- Cross-encoder reranking
- Full distributed tracing and AI-specific observability

### Not implied without implementation evidence

The curriculum should not claim that a capability is complete merely because a README describes it. AWS, Terraform, CI/CD, rollback, backup, and monitoring claims require runnable configuration, automated workflows, verification results, and documented operating procedures.

## Delivery-Time Guidance

Combining modules reduces the number of sessions but not the amount of technical work.

| Session | Realistic guided hands-on estimate |
| --- | ---: |
| Session 1 — Application and Search | 3–4 hours |
| Session 2 — RAG and Production | 3–4 hours |
| Session 3 — AWS and Terraform | 4–6 hours |
| Session 4 — Deployment and Operations | 4–6 hours |

The full hands-on base program is therefore more realistically **14–20 hours**, excluding account setup, downloads, cloud provisioning delays, optional experiments, and breaks.

A shorter 6–8-hour version is possible only as an accelerated guided workshop with:

- Prepared milestone code
- Prebuilt container images
- A prepared AWS account or sandbox
- Preconfigured permissions and remote state
- Carefully selected code changes rather than building every component from scratch
- Deployment demonstrations where long provisioning steps are started in advance
- Take-home exercises for deeper implementation

Marketing material should distinguish between guided class time and independent implementation time.

## Migration Checklist

### Phase 1 — Documentation and structure

- [ ] Update the root README with the new two-layer curriculum.
- [ ] Update the Base README with four required sessions and revised estimates.
- [ ] Update the Advanced README to describe optional extensions.
- [ ] Add new Session 1–4 outcome and verification checklists.
- [ ] Move the cloud deployment plan into the Base Session 3 and 4 plans.
- [ ] Remove references to an incomplete fifth advanced cloud module.
- [ ] Clearly distinguish completed, in-progress, and planned work.

### Phase 2 — Consolidate the local milestones

- [ ] Create the new cumulative Session 1 snapshot from current Sessions 1 and 2.
- [ ] Create the new cumulative Session 2 snapshot from current Sessions 3 and 4.
- [ ] Rewrite exercises so trainees understand what they build rather than only run completed code.
- [ ] Preserve automated tests and final verification checks.
- [ ] Confirm each milestone starts independently.

### Phase 3 — Implement AWS and Terraform

- [ ] Decide on AWS region, environments, inference provider, vector deployment, and cost ceiling.
- [ ] Add the model-provider abstraction and cloud configuration.
- [ ] Add database migration support.
- [ ] Implement Terraform networking, compute, data, identity, secrets, logging, and state.
- [ ] Add infrastructure validation and security checks.
- [ ] Provision a clean development environment and document observed cost.
- [ ] Test complete teardown.

### Phase 4 — Implement deployment and operations

- [ ] Extend GitHub Actions from CI to CI/CD.
- [ ] Configure GitHub OIDC and least-privilege AWS roles.
- [ ] Build and publish immutable images to ECR.
- [ ] Deploy ECS services and run migrations.
- [ ] Add smoke tests and rollback behavior.
- [ ] Configure HTTPS, dashboards, and alerts.
- [ ] Exercise backup, recovery, failure diagnosis, and teardown.
- [ ] Capture portfolio evidence and finalize the interview narrative.

### Phase 5 — Preserve the optional extensions

- [ ] Keep evaluation as the first optional module.
- [ ] Keep hybrid retrieval dependent on the evaluation baseline.
- [ ] Keep reranking dependent on the evaluated hybrid retriever.
- [ ] Keep advanced observability after the final retrieval pipeline is selected.
- [ ] Mark all unimplemented extension modules as planned.

## Final Positioning

Suggested program description:

> Build and deploy a production-oriented AI recipe recommendation system across four cumulative sessions. Start with FastAPI, PostgreSQL, Streamlit, embeddings, Qdrant, and semantic search; add grounded RAG, Celery, Redis, testing, and resilience; then provision AWS infrastructure with Terraform and deliver the system through secure CI/CD, monitoring, rollback, and cost-aware operations. Optional advanced modules explore RAG evaluation, hybrid retrieval, reranking, and distributed observability.

Suggested short distinction:

- **Base:** Build it, productionize it, deploy it, and explain it.
- **Advanced:** Measure it, improve retrieval, rerank results, and observe it deeply.
