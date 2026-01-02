---

name: kubernetes
description: Guides the deployment, scaling, and management of containerized applications using Kubernetes
---

# Kubernetes

--Instructions:

1. Define the desired architecture for the application including services, pods, and deployments.
2. Create Kubernetes manifests (YAML) for deployments, services, config maps, and secrets.
3. Set up namespaces, resource limits, and labels for efficient management.
4. Deploy applications to a Kubernetes cluster and monitor their status.
5. Scale deployments as needed and implement rolling updates or rollbacks.
6. Ensure high availability and fault tolerance through proper configuration.
7. Document cluster configuration and deployment steps clearly.

-- Examples:

- Deploying a simple web application:

 ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: web-app
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: web-app
    template:
      metadata:
        labels:
          app: web-app
      spec:
        containers:
        - name: web-app
          image: my-web-app:latest
          ports:
          - containerPort: 80
Exposing the deployment with a service:

apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
