---
name: deployment-tools
description: Guides the use of Docker, Kubernetes, and DigitalOcean for containerization, orchestration, and cloud deployment.
---

# Docker, Kubernetes & DigitalOcean

## Instructions
1. Containerize applications using Docker with proper Dockerfiles.
2. Build and manage images, and run containers locally for testing.
3. Deploy containers using Kubernetes with deployments, services, and ingress rules.
4. Configure cloud infrastructure on DigitalOcean, including droplets, databases, and networking.
5. Monitor deployments, scaling, and resource usage.
6. Collaborate with other agents to ensure deployment aligns with architecture.
7. Implement CI/CD pipelines for automated testing and deployment.
8. Document deployment processes, configurations, and troubleshooting steps.

## Examples
- Dockerfile for a Python app:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

- Kubernetes deployment manifest:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: my-app
    template:
      metadata:
        labels:
        app: my-app
      spec:
        containers:
        - name: my-app
          image: my-app:latest
  ```

- Deploying to DigitalOcean using CLI:
  ```bash
  doctl apps create --spec app-spec.yaml
  ```