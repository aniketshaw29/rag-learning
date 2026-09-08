# TechNova — Engineering Team Structure

## Engineering Organization

The Engineering department has **120 engineers** across Austin and Toronto,
led by **VP of Engineering: Priya Sharma**.

### Teams

#### Platform Team (25 engineers)
- **Lead:** James O'Brien
- **Responsibilities:** Core infrastructure, CI/CD pipelines, cloud infrastructure
- **Tech Stack:** Go, Kubernetes, Terraform, AWS (EKS, RDS, S3)
- **On-call rotation:** Weekly, shared between Austin and Toronto

#### AI/ML Team (18 engineers)
- **Lead:** Dr. Wei Zhang
- **Responsibilities:** Model training, inference optimization, embeddings, RAG pipelines
- **Tech Stack:** Python, PyTorch, Hugging Face, ONNX, vLLM
- **Note:** This team maintains all internal AI model serving infrastructure

#### NovaCode Team (30 engineers)
- **Lead:** Elena Volkov
- **Responsibilities:** VS Code extension, JetBrains plugin, code completion engine
- **Tech Stack:** TypeScript, Rust (for parser), Python (for ML inference)

#### NovaTest Team (15 engineers)
- **Lead:** David Kim
- **Responsibilities:** Test generation AI, coverage analysis, CI integration
- **Tech Stack:** Python, TypeScript, PostgreSQL

#### NovaDeploy Team (12 engineers)
- **Lead:** Amara Johnson
- **Responsibilities:** Deployment pipeline, infrastructure provisioning, monitoring
- **Tech Stack:** Go, Python, Kubernetes, Prometheus, Grafana

#### QA & DevRel (20 engineers)
- **Lead:** Tom Nguyen
- **Responsibilities:** Automated testing, developer relations, documentation
- **Tech Stack:** Python, Playwright, MkDocs

## Development Practices

- **Git workflow:** trunk-based development with short-lived feature branches
- **Code review:** Every PR requires 2 approvals
- **CI/CD:** GitHub Actions, builds run in under 8 minutes
- **Deployment frequency:** NovaCode ships 2-3 times per week; other products weekly
- **Incident response:** PagerDuty with 15-minute SLA for P1 incidents
- **Architecture decisions:** Recorded as ADRs (Architecture Decision Records) in
  the team's internal wiki

## Tech Stack Summary

| Layer          | Technology                           |
|----------------|--------------------------------------|
| Frontend       | React, TypeScript, TailwindCSS       |
| Backend        | Go, Python (FastAPI), Node.js        |
| AI/ML          | PyTorch, vLLM, ONNX Runtime          |
| Database       | PostgreSQL, Redis, Pinecone (vector) |
| Infrastructure | AWS (EKS), Terraform, Helm           |
| Monitoring     | Prometheus, Grafana, Datadog         |
| CI/CD          | GitHub Actions, ArgoCD               |
