# Todo App Kubernetes Deployment Guide

This guide explains how to deploy the Todo Chatbot application to Kubernetes using Helm charts.

## Prerequisites

- Kubernetes cluster (Minikube, Kind, or cloud-based)
- Helm 3.x
- kubectl
- Docker (for building images)

## Quick Start

### Using Minikube

1. Start Minikube:
```bash
minikube start
```

2. Enable ingress addon (optional):
```bash
minikube addons enable ingress
```

3. Point Docker CLI to Minikube's Docker daemon:
```bash
eval $(minikube docker-env)
```

4. Build container images:
```bash
cd backend
docker build -t todo-backend .
cd ../frontend
docker build -t todo-frontend .
```

5. Install the Helm chart:
```bash
cd k8s/helm/todo-app
helm install todo-app .
```

### Using Pre-built Images

If you're using pre-built images from a registry:

```bash
helm install todo-app . \
  --set frontend.image.repository=<your-registry>/todo-frontend \
  --set frontend.image.tag=<tag> \
  --set backend.image.repository=<your-registry>/todo-backend \
  --set backend.image.tag=<tag>
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend pods | `1` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.service.type` | Frontend service type | `ClusterIP` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.ingress.enabled` | Enable ingress for frontend | `false` |
| `backend.replicaCount` | Number of backend pods | `1` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.service.type` | Backend service type | `ClusterIP` |
| `backend.service.port` | Backend service port | `8000` |
| `database.enabled` | Enable PostgreSQL database | `true` |
| `database.postgresql.auth.database` | PostgreSQL database name | `todoapp` |
| `database.postgresql.auth.postgresPassword` | PostgreSQL password | `postgrespassword` |
| `database.postgresql.service.port` | PostgreSQL service port | `5432` |
| `env.NEXT_PUBLIC_API_BASE_URL` | API base URL for frontend | `http://todo-backend-service:8000` |

## Accessing the Application

After installation, you can access the application using port forwarding:

```bash
# Forward frontend port
kubectl port-forward svc/todo-app-frontend 3000:3000

# Forward backend port
kubectl port-forward svc/todo-app-backend 8000:8000
```

Then access the frontend at http://localhost:3000

## Uninstalling the Chart

To uninstall/delete the `todo-app` release:

```bash
helm delete todo-app
```

## Development Notes

### Building Custom Images

To build custom images for your environment:

```bash
# Build backend
cd backend
docker build -t <your-registry>/todo-backend:<tag> .
docker push <your-registry>/todo-backend:<tag>

# Build frontend
cd frontend
docker build -t <your-registry>/todo-frontend:<tag> .
docker push <your-registry>/todo-frontend:<tag>
```

### Local Development with Skaffold

For local development, you can use Skaffold to automate the build and deployment process:

```bash
skaffold dev
```

## Architecture Overview

The application consists of three main components:

1. **Frontend**: Next.js application serving the user interface
2. **Backend**: FastAPI application providing REST API endpoints
3. **Database**: PostgreSQL database for storing todo items and user data

The components communicate as follows:
- Frontend connects to Backend via HTTP API calls
- Backend connects to Database via PostgreSQL protocol
- External users access the Frontend via HTTP

## Security Considerations

- Database passwords should be stored in Kubernetes secrets
- TLS should be enabled for production deployments
- Network policies should restrict traffic between components
- RBAC should limit access to necessary resources only

## Scaling

The application supports horizontal scaling:

- Frontend: Scale based on web traffic
- Backend: Scale based on API request load
- Database: Scale vertically (more resources) or use read replicas

## Monitoring and Logging

- Application logs are available via `kubectl logs`
- Metrics can be collected using Prometheus
- Health checks are available at `/health` endpoints