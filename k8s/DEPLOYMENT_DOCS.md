# Todo App Kubernetes Deployment Documentation

## Overview

This document describes the Kubernetes deployment of the Todo Chatbot application. The application consists of three main components:

1. **Frontend**: Next.js application serving the user interface
2. **Backend**: FastAPI application providing REST API endpoints
3. **Database**: PostgreSQL database for storing todo items and user data

## Architecture

```
Internet -> Ingress Controller -> Frontend Service -> Backend Service -> Database
```

### Components

- **Frontend**: Serves the Next.js application on port 3000
- **Backend**: Provides API endpoints on port 8000
- **Database**: PostgreSQL database on port 5432
- **Ingress**: Routes external traffic to the frontend

## Deployment Structure

The deployment uses a Helm chart located at `k8s/helm/todo-app/` with the following structure:

```
todo-app/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── values-prod.yaml    # Production configuration values
├── templates/          # Kubernetes manifest templates
│   ├── _helpers.tpl    # Helper templates
│   ├── configmap.yaml  # Environment variables
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── frontend-ingress.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── database.yaml
│   ├── pvc.yaml
│   ├── monitoring.yaml
│   └── NOTES.txt       # Post-installation notes
└── charts/             # Subcharts (if any)
```

## Configuration

### Values Configuration

The deployment can be customized using the following values:

#### Frontend Configuration
- `frontend.replicaCount`: Number of frontend pods (default: 1)
- `frontend.image.repository`: Frontend image repository (default: "todo-frontend")
- `frontend.image.tag`: Frontend image tag (default: "latest")
- `frontend.service.type`: Service type (default: "ClusterIP")
- `frontend.service.port`: Service port (default: 3000)
- `frontend.ingress.enabled`: Enable ingress (default: false)
- `frontend.resources`: Resource limits and requests

#### Backend Configuration
- `backend.replicaCount`: Number of backend pods (default: 1)
- `backend.image.repository`: Backend image repository (default: "todo-backend")
- `backend.image.tag`: Backend image tag (default: "latest")
- `backend.service.type`: Service type (default: "ClusterIP")
- `backend.service.port`: Service port (default: 8000)
- `backend.resources`: Resource limits and requests

#### Database Configuration
- `database.enabled`: Enable PostgreSQL database (default: true)
- `database.postgresql.auth.database`: Database name (default: "todoapp")
- `database.postgresql.auth.postgresPassword`: Database password
- `database.postgresql.service.port`: Database service port (default: 5432)
- `database.postgresql.persistence.enabled`: Enable persistent storage (default: true)
- `database.postgresql.persistence.size`: Storage size (default: "1Gi")

## Deployment Steps

### Prerequisites

1. Kubernetes cluster (Minikube, Kind, or cloud-based)
2. Helm 3.x
3. kubectl
4. Docker (for building images)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Todo-App
   ```

2. Navigate to the Helm chart:
   ```bash
   cd k8s/helm/todo-app
   ```

3. Install the chart:
   ```bash
   helm install todo-app .
   ```

4. Or install with custom values:
   ```bash
   helm install todo-app . -f values-prod.yaml
   ```

### Using the Deployment Scripts

The repository includes helper scripts for deployment and testing:

1. **Deploy the application**:
   ```bash
   ./k8s/deploy.sh
   ```

2. **Test the services**:
   ```bash
   ./k8s/test-services.sh
   ```

## Accessing the Application

### Via Port Forwarding

```bash
# Access frontend
kubectl port-forward svc/todo-app-frontend 3000:3000

# Access backend
kubectl port-forward svc/todo-app-backend 8000:8000
```

### Via Ingress (if enabled)

If ingress is enabled, the application will be accessible at the configured hostname.

## Scaling

### Horizontal Pod Autoscaling

The deployment supports HPA for automatic scaling:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 70
```

### Manual Scaling

Scale deployments manually:

```bash
# Scale frontend
kubectl scale deployment todo-app-frontend --replicas=3

# Scale backend
kubectl scale deployment todo-app-backend --replicas=3
```

## Monitoring and Health Checks

### Health Endpoints

- Frontend: `/` (returns 200 OK when healthy)
- Backend: `/health` (returns health status)
- Database: Uses `pg_isready` for health checking

### Probes Configuration

Each deployment includes:
- **Liveness Probe**: Determines when to restart a container
- **Readiness Probe**: Determines when a container is ready to serve traffic
- **Startup Probe**: Determines when a container application has started

## Security

### Secrets

Database credentials are stored in Kubernetes secrets:
- `todo-app-postgres-secret`: Contains the PostgreSQL password

### Best Practices

- Use strong passwords for database authentication
- Enable TLS for production deployments
- Limit network access with Network Policies
- Use RBAC to restrict access to necessary resources only

## Persistence

The PostgreSQL database uses persistent storage via PersistentVolumeClaims (PVCs) to ensure data durability across pod restarts and upgrades.

## Backup and Recovery

### Database Backup

Create database backups using:

```bash
kubectl exec -it <postgres-pod-name> -- pg_dump -U postgres -d todoapp > backup.sql
```

### Restoring Data

Restore data using:

```bash
kubectl exec -i <postgres-pod-name> -- psql -U postgres -d todoapp < backup.sql
```

## Troubleshooting

### Common Issues

1. **Pods not starting**: Check resource limits and availability
2. **Service unavailable**: Verify ingress configuration and load balancer
3. **Database connection errors**: Check database credentials and network connectivity
4. **Health check failures**: Review probe configurations and application logs

### Useful Commands

```bash
# Check pod status
kubectl get pods

# View logs
kubectl logs <pod-name>

# Describe resources
kubectl describe <resource-type> <resource-name>

# Check services
kubectl get services

# Check ingress
kubectl get ingress
```

## Updating the Application

### Upgrade the Release

```bash
# Update with new values
helm upgrade todo-app . -f values-prod.yaml

# Rollback to previous version
helm rollback todo-app
```

### Image Updates

Update images by specifying new tags:

```bash
helm upgrade todo-app . \
  --set frontend.image.tag=new-tag \
  --set backend.image.tag=new-tag
```

## Cleanup

To remove the application:

```bash
helm uninstall todo-app
```

This will remove all resources associated with the release.

## Development and Local Testing

### Using Minikube

For local development:

1. Start Minikube:
   ```bash
   minikube start
   ```

2. Enable ingress:
   ```bash
   minikube addons enable ingress
   ```

3. Build images in Minikube's registry:
   ```bash
   eval $(minikube docker-env)
   docker build -t todo-frontend:latest ../frontend
   docker build -t todo-backend:latest ../backend
   ```

4. Deploy:
   ```bash
   helm install todo-app .
   ```

## Production Considerations

For production deployments, consider:

1. **Security**: Enable TLS, use strong passwords, implement network policies
2. **Monitoring**: Set up Prometheus and Grafana for metrics
3. **Logging**: Centralize logs with ELK stack or similar
4. **Backup**: Implement automated backup solutions
5. **Scalability**: Configure HPA and resource limits appropriately
6. **High Availability**: Use multiple replicas and distribute across zones
7. **Disaster Recovery**: Plan for backup and recovery procedures

## Conclusion

This Kubernetes deployment provides a scalable, resilient infrastructure for the Todo Chatbot application. The Helm chart simplifies deployment and management while allowing for customization through values files. The architecture supports horizontal scaling, health monitoring, and persistent storage for production workloads.