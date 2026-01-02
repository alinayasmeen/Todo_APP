---
name: dapr
description: Guides the use of DAPR (Distributed Application Runtime) to build resilient, event-driven, and microservice-based applications.
---

# DAPR

## Instructions

1. Identify the services or microservices that need DAPR integration.
2. Configure DAPR components such as state stores, pub/sub brokers, and bindings.
3. Implement service-to-service communication using DAPR sidecars or HTTP/gRPC APIs.
4. Handle state management, event publishing, and subscription reliably.
5. Monitor DAPR applications and troubleshoot communication or state issues.
6. Ensure security by configuring secret stores, authentication, and encryption.
7. Document DAPR configurations, endpoints, and workflows for maintainers.

## Examples

- Publishing an event from a service:

  ```bash
  curl -X POST http://localhost:3500/v1.0/publish/pubsub-topic my-event.json

Subscribing to a topic in another service:

apiVersion: dapr.io/v1alpha1
kind: Subscription
metadata:
  name: order-subscription
spec:
  topic: orders
  route: /orders
  pubsubname: pubsub-topic

Saving state using DAPR state store:
curl -X POST <http://localhost:3500/v1.0/state/statestore> -H "Content-Type: application/json" -d '[{"key":"order123","value":{"status":"processed"}}]'
