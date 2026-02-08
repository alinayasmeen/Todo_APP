#!/bin/bash

# Todo App Kubernetes Deployment Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Todo App Kubernetes Deployment Script${NC}"
echo "========================================"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed${NC}"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo -e "${RED}helm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"

# Check if we're connected to a cluster
echo -e "\n${YELLOW}Checking cluster connection...${NC}"
if kubectl cluster-info &> /dev/null; then
    echo -e "${GREEN}✓ Connected to cluster${NC}"
else
    echo -e "${RED}✗ Cannot connect to cluster${NC}"
    exit 1
fi

# Build and push images if needed
read -p "Do you want to build and push new images? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Building Docker images...${NC}"
    
    # Build backend
    echo "Building backend image..."
    cd ../backend
    docker build -t todo-backend:latest .
    
    # Build frontend
    echo "Building frontend image..."
    cd ../frontend
    docker build -t todo-frontend:latest .
    
    cd ../k8s/helm
    
    echo -e "${GREEN}✓ Images built successfully${NC}"
fi

# Install the application
echo -e "\n${YELLOW}Installing Todo App using Helm...${NC}"

HELM_RELEASE_NAME="todo-app"
HELM_CHART_PATH="./todo-app"

# Check if release already exists
if helm status "$HELM_RELEASE_NAME" &> /dev/null; then
    echo "Release $HELM_RELEASE_NAME already exists. Upgrading..."
    helm upgrade "$HELM_RELEASE_NAME" "$HELM_CHART_PATH"
else
    helm install "$HELM_RELEASE_NAME" "$HELM_CHART_PATH"
fi

echo -e "${GREEN}✓ Application deployed successfully${NC}"

# Wait for deployments to be ready
echo -e "\n${YELLOW}Waiting for deployments to be ready...${NC}"

kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app-frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

echo -e "${GREEN}✓ All deployments are ready${NC}"

# Show deployment status
echo -e "\n${YELLOW}Deployment status:${NC}"
kubectl get pods,services,ingress

# Show application access information
echo -e "\n${GREEN}Application is now running!${NC}"
echo "Frontend service: $(kubectl get svc todo-app-frontend -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')"
echo "Backend service: $(kubectl get svc todo-app-backend -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')"
echo "Database service: $(kubectl get svc todo-app-postgres -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')"

echo -e "\nTo access the application locally, use port forwarding:"
echo "kubectl port-forward svc/todo-app-frontend 3000:3000"
echo "kubectl port-forward svc/todo-app-backend 8000:8000"

echo -e "\n${GREEN}Deployment completed successfully!${NC}"