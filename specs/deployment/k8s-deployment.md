# Phase IV: Local Kubernetes Deployment (Minikube, Helm Charts, kubectl-ai, Kagent, Docker Desktop, and Gordon)

Cloud Native Todo Chatbot with Basic Level Functionality

## Objective: Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube, Helm Charts

### 💡Development Approach: Use the Agentic Dev Stack workflow

Write spec → Generate
plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will
review the process, prompts, and iterations to judge each phase and project.

### Requirements

• Containerize frontend and backend applications (Use Gordon)
• Use Docker AI Agent (Gordon) for AI-assisted Docker operations
• Create Helm charts for deployment (Use kubectl-ai and/or kagent to generate)
• Use kubectl-ai and kagent for AI-assisted Kubernetes operations
• Deploy on Minikube locally

### Note

If Docker AI (Gordon) is unavailable in your region or tier, use standard Docker CLI
commands or ask Claude Code to generate the docker run commands for you.
Technology Stack
Component Technology
Containerization Docker (Docker Desktop)
Docker AI Docker AI Agent (Gordon)
Orchestration Kubernetes (Minikube)
Package Manager Helm Charts
AI DevOps kubectl-ai, and Kagent
Application Phase III Todo Chatbot
AIOps
Use Docker AI Agent (Gordon) for intelligent Docker operations:

#### To know its capabilities

docker ai "What can you do?"
Enable Gordon: Install latest Docker Desktop 4.53+, go to Settings > Beta features, and
toggle it on.
Use kubectl-ai, and Kagent for intelligent Kubernetes operations:

#### Using kubectl-ai

kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"

#### Using kagent

kagent "analyze the cluster health"
kagent "optimize resource allocation"
Starting with kubectl-ai will make you feel empowered from day one. Layer in Kagent for
advanced use cases. Pair them with Minikube for zero-cost learning and work

## Phase 4: Deployment and Testing

1. Deploy the application using Helm
2. Verify all services are running
3. Test the application functionality
4. Troubleshoot any issues

## Phase 5: Optimization

1. Set proper resource limits
2. Configure health checks
3. Set up persistent storage for database
4. Document the deployment process
