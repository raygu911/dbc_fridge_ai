# FridgeAI

> Build a Resume-Worthy AI Engineering Project from Scratch

> **Project status:** FridgeAI is currently in early development. The 6–8 hour core course described below focuses on a guided, working MVP. Production-scale infrastructure and advanced AI features are documented as future directions and advanced-course material.

FridgeAI is an end-to-end AI-powered meal recommendation system designed to demonstrate how modern AI applications are built using Retrieval-Augmented Generation (RAG), vector databases, backend APIs, asynchronous processing, containerization, and production-oriented engineering practices.

Unlike many AI demo projects that focus only on model inference, FridgeAI emphasizes the complete AI engineering lifecycle—from data ingestion and semantic retrieval to deployment, testing, and system architecture.

This repository serves two purposes:

- A resume-worthy AI engineering portfolio project
- The official project for the FridgeAI Intensive Training Program

---

# Project Overview

FridgeAI helps developers learn how to build complete AI applications rather than isolated AI demos.

The project demonstrates how traditional software engineering integrates with modern generative AI technologies through an end-to-end architecture that is both practical and extensible.

By the end of this project, you will understand:

- Retrieval-Augmented Generation (RAG)
- Embedding generation
- Semantic search
- Vector databases
- Backend API development
- Asynchronous task processing
- Containerization
- CI/CD
- Local deployment fundamentals
- AI engineering best practices
- System design
- Technical communication for interviews

---

# Features

FridgeAI includes the following capabilities:

- Ingredient-based meal recommendations
- Natural language recipe search
- Semantic recipe retrieval
- Personalized meal recommendations
- Dietary preference filtering
- Allergy filtering
- Retrieval-Augmented Generation (RAG)
- AI-generated recommendation explanations
- Recipe ingestion and indexing
- Background processing for long-running tasks
- Containerized deployment
- Modular and extensible architecture

---

# Technology Stack

## Core Implementation (Main Course)

The core implementation focuses on building a complete AI application using mature, open-source technologies.

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Backend API | FastAPI |
| Relational Database | PostgreSQL |
| Vector Database | Qdrant |
| Embedding Models | Sentence Transformers |
| Local LLM Runtime | Ollama |
| Background Processing | Celery + Redis |
| Frontend | Streamlit |
| Containerization | Docker Compose |
| Testing | pytest |
| Linting | Ruff |
| CI/CD | GitHub Actions |
| Deployment | Local development with Docker Compose |

---

# High-Level Architecture

```text
                          User
                            │
                            ▼
                   Streamlit Frontend
                            │
                            ▼
                     FastAPI Backend
                            │
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
      ▼                     ▼                     ▼
 PostgreSQL             Qdrant                  Ollama
Structured Data      Vector Search        Response Generation
                            ▲
                            │
                     Celery Worker
                      ├── Recipe ingestion
                      └── Embedding generation
                            ▲
                            │
                          Redis
                     Task Message Broker
```

---

# Repository Structure

```text
fridge-ai/
│
├── apps/
│   ├── api/
│   └── web/
│
├── src/
│   ├── api/
│   ├── database/
│   ├── embeddings/
│   ├── ingestion/
│   ├── llm/
│   ├── prompts/
│   ├── rag/
│   ├── retrieval/
│   ├── services/
│   └── tasks/
│
├── data/
│
├── infrastructure/
│
├── scripts/
│
├── tests/
│
├── docs/
│
├── .github/
│
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# FridgeAI Intensive Training Program

## Overview

**Build a Resume-Worthy AI Engineering Project from Scratch**

**4 Live Sessions • 6–8 Hours Total • Guided and Beginner-Friendly**

Build a focused, working MVP of an AI-powered meal recommendation system using real-world engineering practices. The 6–8 hour core course concentrates on the essential end-to-end path: data modeling, semantic retrieval, RAG, backend APIs, background processing, a simple interface, testing, and local containerized execution.

To keep this scope achievable, learners work from prepared starter infrastructure and follow guided implementation steps. Basic Python, Git, and command-line familiarity are recommended. Cloud deployment, infrastructure as code, production observability, orchestration, and scaling are intentionally reserved for future development or advanced courses.

---

## Technologies & Concepts Covered

### Artificial Intelligence

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Semantic Search
- Prompt Engineering

### Backend Development

- Python
- FastAPI
- REST APIs
- Asynchronous Programming

### Data Storage

- PostgreSQL
- Qdrant Vector Database

### AI Models

- Sentence Transformers
- Ollama
- Open-source Large Language Models

### Background Processing

- Celery
- Redis

### Infrastructure

- Docker
- Docker Compose

### DevOps

- GitHub Actions
- Continuous Integration / Continuous Deployment (CI/CD)

### Software Engineering

- Production-oriented AI engineering
- System design
- Clean architecture
- Testing
- Technical interview communication

---

# Training Roadmap

## Session 1 — Application Foundation

Topics include:

- Project architecture
- Development environment setup
- FastAPI
- PostgreSQL
- Docker
- Recipe data model

Deliverables:

- Running backend API
- Database connection
- Initial project structure

---

## Session 2 — Semantic Retrieval

Topics include:

- Embeddings
- Sentence Transformers
- Qdrant
- Vector search
- Metadata filtering

Deliverables:

- Recipe embedding pipeline
- Semantic search API

---

## Session 3 — Retrieval-Augmented Generation

Topics include:

- Ollama
- Prompt engineering
- Retrieval-Augmented Generation
- Celery
- Redis
- Recipe ingestion
- Embedding generation

Deliverables:

- Complete RAG pipeline
- Background indexing workflow

---

## Session 4 — Production Engineering

Topics include:

- Streamlit
- Docker Compose
- GitHub Actions
- Automated testing
- Local deployment with Docker Compose
- Future deployment directions
- Resume presentation
- Technical interview storytelling

Deliverables:

- Complete end-to-end application
- Interview-ready project

---

# Learning Outcomes

After completing this project, you will be able to:

- Design an end-to-end AI application
- Explain Retrieval-Augmented Generation (RAG)
- Build REST APIs using FastAPI
- Design relational and vector data storage
- Generate and manage embeddings
- Build semantic search applications
- Implement asynchronous processing
- Containerize multi-service applications
- Build CI/CD pipelines
- Explain architectural decisions during technical interviews

---

# Who Should Join

This project is intended for:

- Software engineering internship candidates
- Computer science students
- Junior software engineers
- Developers transitioning into AI engineering
- Anyone looking to build a high-impact portfolio project

---

# Prerequisites

Recommended background:

- Basic Python programming
- Familiarity with Git
- Basic command-line experience

No prior AI or machine learning experience is required.

---

# Getting Started

## Prerequisites

Install the following software:

- Python 3.12+
- Git
- Docker Desktop
- Ollama

Clone the repository:

```bash
git clone https://github.com/raygu911/dbc_fridge_ai.git

cd dbc_fridge_ai
```

Create the environment configuration:

```bash
cp .env.example .env
```

Start the local services:

```bash
docker compose up --build
```

Download a local language model:

```bash
ollama pull qwen2.5
```

Open the application:

```
FastAPI:
http://localhost:8000/docs

Streamlit:
http://localhost:8501
```

---

# Roadmap

## Version 1.0

- FastAPI backend
- PostgreSQL
- Qdrant
- Ollama
- Sentence Transformers
- Celery
- Redis
- Streamlit
- Docker Compose
- GitHub Actions

## Version 2.0

- Hybrid retrieval
- Cross-encoder reranking
- Improved prompt templates
- Better evaluation metrics

## Version 3.0

- User authentication
- Personalized recommendations
- Nutrition tracking
- Meal planning
- Grocery list generation

---

# Future Directions and Advanced Courses

The core implementation is intentionally limited to a guided MVP that can be completed within the 6–8 hour training program.

The capabilities below are **not part of the core course**. They are future project directions or material for dedicated advanced courses after learners are comfortable with the foundational architecture.

## Workflow Orchestration

- Temporal

## Observability

- OpenTelemetry
- Prometheus
- Grafana

## Infrastructure as Code

- OpenTofu
- Terraform

## Cloud Deployment

- AWS ECS
- AWS RDS
- AWS Secrets Manager
- AWS CloudWatch

## AI Enhancements

- Hybrid retrieval
- Cross-encoder reranking
- Multi-agent workflows
- Evaluation pipelines

## Security

- Authentication
- Authorization
- User accounts

## Scalability

- Kubernetes
- Horizontal scaling
- Load balancing

---

# Contributing

Contributions, suggestions, and feature requests are welcome.

If you find a bug or would like to propose an improvement, please open an issue or submit a pull request.

---

# Project Philosophy

FridgeAI emphasizes engineering over experimentation.

Instead of building another chatbot demonstration, this project teaches how modern AI systems are designed—from backend APIs and vector search to deployment and production-oriented software engineering.

The goal is not only to build a working application, but also to understand the architectural decisions behind every component so that you can confidently explain your design, technology choices, and implementation during technical interviews.

---

# License

This project is licensed under the MIT License.