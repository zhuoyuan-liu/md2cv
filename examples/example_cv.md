# Alex Chen

**Software / Platform Engineer**

- **Phone:** +1-555-0142
- **Email:** alex.chen@example.com
- **LinkedIn:** [linkedin.com/in/alexchen](https://www.linkedin.com/in/alexchen/)
- **GitHub:** [github.com/alex-chen](https://github.com/alex-chen)
- **Address:** 123 Maple Street, Apt 4B, San Francisco, CA 94102

---

## About Me

Platform engineer with 5+ years of experience, including 3+ years building and operating a centralized observability platform serving 3,000+ active users. Primary author of the telemetry ingestion gateway and multi-tenant authorization service in Go; designed and led multi-tenancy end-to-end; drove significant infrastructure cost savings and led a cloud migration. Full production ownership and on-call responsibility.

---

## Skills

- Go, Python, Bash; Linux/Unix systems; DevOps and GitOps practices
- Kubernetes (AKS, GKE, EKS), Docker, Helm, Kustomize, Flux CD, Karpenter
- GitHub Actions, Terraform
- Networking: Envoy, ingress-nginx, TLS/cert-manager, DNS
- Kafka, PostgreSQL, Redis
- Grafana LGTM stack, OpenTelemetry, Prometheus

---

## Experience

### Software / Platform Engineer | Nov 2022 --- Now
**Acme Corp** | San Francisco

Core member of the Observability Platform team: a centralized platform serving 3,000+ active users and ingesting millions of metrics, logs, and spans per second.

- Led the endpoint device management platform: deployed an agent to 50K+ devices, enabling remote software inventory, device health monitoring, and distributed ad-hoc queries across the fleet
- Developed the telemetry ingestion gateway (Go) processing all metrics, logs, and traces at scale: label validation, sensitive data masking, multi-tenancy routing, and label enrichment
- Designed and delivered the multi-tenancy platform end-to-end: built the authorization service (Go) from scratch as a JWT-based Kubernetes ingress backend, enforcing data isolation for 3,000+ users at low latency
- Migrated platform across cloud providers with zero data loss; designed hierarchical GitOps structure for multiple clusters using Kustomize
- Drove infrastructure cost optimization: improved cluster utilization from 15% to 75% via resource right-sizing and spot instances

### DevOps Engineer | Jun 2021 --- Oct 2022
**TechStart Solutions** | New York

- Designed and delivered CI/CD pipelines and ArgoCD GitOps workflows for enterprise clients, enabling automated multi-environment promotion with full audit trails
- Built on-premise Kubernetes platform: container registry, ArgoCD, Sealed Secrets
- Set up cloud infrastructure with full Terraform IaC, audit logging, and least-privilege automation

### ML Research Assistant | Nov 2020 --- May 2021
**City General Hospital** | New York

- Built deep learning model for medical image classification (~95% accuracy); deployed model and web application used by the clinical team for ongoing research

---

## Education

**MSc in Computer Science** | 2018 --- 2020
State University | GPA: 3.8/4.0
