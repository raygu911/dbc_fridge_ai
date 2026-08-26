# FridgeAI Base Training

The Base Track contains four cumulative sessions covering the complete project journey from local application development through AWS deployment and operations.

| Session | Outcome | Guided time | Status |
| --- | --- | ---: | --- |
| [Session 1](session-1-application-and-search/) | Containerized recipe application with semantic search | 3–4 hours | Complete |
| [Session 2](session-2-rag-and-production/) | Grounded RAG application with background processing and production safeguards | 3–4 hours | Complete |
| [Session 3](session-3-aws-and-terraform/) | Reproducible AWS environment defined with Terraform | 4–6 hours | Planned |
| [Session 4](session-4-deployment-and-operations/) | Verified CI/CD deployment with monitoring, rollback, recovery, and cost controls | 4–6 hours | Planned |

## Learning Sequence

Complete the sessions in order. Each implemented directory is a standalone cumulative snapshot, allowing trainees to run, test, compare, and explain the architecture at that stage.

Sessions 1 and 2 consolidate the former four local milestones. Sessions 3 and 4 split cloud engineering into infrastructure and delivery concerns so trainees can distinguish provisioning from deployment and operation.

## Running a Local Milestone

```bash
cd base/session-1-application-and-search
cp .env.example .env
python -m pip install -e ".[dev]"
docker compose up --build -d
ruff check .
pytest -v
```

Run only one local milestone environment at a time because the snapshots use the same ports.

## Completion Standard

A session is complete only when it includes runnable artifacts, automated verification, architecture and trade-off notes, repeatable operating commands, a completion checklist, and interview talking points. A planned README alone does not count as an implemented capability.
