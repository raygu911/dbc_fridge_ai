# FridgeAI Base Training

The base track contains four standalone project milestones. Each session directory is an independent FridgeAI project with its own application code, tests, configuration, Docker Compose environment, and session guide.

| Session | Focus | Effort | Estimated guided time | Status |
| --- | --- | --- | --- | --- |
| [Session 1](session-1-foundation/) | Application foundation | Moderate | 1.5–2 hours | Complete |
| [Session 2](session-2-semantic-search/) | Embeddings and semantic retrieval | Moderate–high | 1.5–2 hours | Complete |
| [Session 3](session-3-rag/) | RAG and background processing | High | 2–2.5 hours | Complete |
| [Session 4](session-4-production/) | Production engineering | High | 1.5–2 hours | Complete |

## How to Use a Milestone

Enter one session directory and follow its README. For example:

```bash
cd base/session-2-semantic-search
cp .env.example .env
python -m pip install -e ".[dev]"
docker compose up --build -d
pytest -v
```

Run only one milestone's Docker Compose environment at a time because the sessions intentionally use the same local ports.

## Learning Sequence

Start with Session 1 and progress in order. Each milestone includes everything delivered in earlier sessions, allowing trainees to inspect, run, test, and explain the completed architecture at that point in the course.

The milestone directories contain source code only. Docker images, databases, vector data, model caches, Python environments, and secrets are not stored in Git.
