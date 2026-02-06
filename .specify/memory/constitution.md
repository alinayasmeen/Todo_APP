<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- Principle 1: Console-First → Web-First
- Principle 2: Single-User → Multi-User with Authentication
- Principle 3: In-Memory Storage → Persistent Storage with Neon PostgreSQL
- Principle 4: No Security → Security-First with Better Auth and JWT
- Principle 5: No Observability → Observability-First with Structured Logging
Added sections: AI-Ready Architecture
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Todo App Constitution

## Core Principles

### I. Web-First Architecture
Modern web application development approach with Next.js 14 frontend and FastAPI backend. Applications start with responsive, accessible web interfaces; console applications are secondary if needed. Clear separation between frontend and backend concerns with well-defined API contracts.

### II. Multi-User with Authentication
Every feature must support multi-user scenarios with proper data isolation. Authentication via Better Auth with JWT tokens; user data must be isolated at both application and database levels. No shared data between users without explicit sharing mechanisms.

### III. Persistent Storage with Neon PostgreSQL
All data must persist using Neon Serverless PostgreSQL with SQLModel ORM. In-memory storage is prohibited for production features; all state must survive application restarts. Database migrations must be handled safely with rollback capabilities.

### IV. Security-First with Better Auth and JWT
All API endpoints must require authentication via JWT tokens. User data isolation enforced through user_id validation on all queries. Security considerations must be addressed before feature completion; never add security as an afterthought.

### V. Observability-First with Structured Logging
All API requests must be logged with structured logging for debugging and monitoring. Performance metrics must be collected for all endpoints. Error handling must provide appropriate responses without leaking sensitive information.

### VI. AI-Ready Architecture
System architecture must provide clear integration points for AI capabilities. APIs should be designed to accommodate future AI features like natural language processing, smart suggestions, and analytics. Extensible architecture to support AI service integration.

## Additional Security Requirements

### Data Isolation
- All queries must filter by user_id for proper data isolation
- API endpoints must validate user ownership before allowing access
- Error responses must not reveal information about other users' data existence

### Authentication Standards
- JWT tokens must be validated on all protected endpoints
- Session management must follow industry best practices
- Password requirements and account security policies must be enforced

## Development Workflow

### API Design Standards
- RESTful endpoints with consistent naming conventions
- Proper HTTP status codes for all responses
- Comprehensive API documentation with OpenAPI
- Versioning strategy for API evolution

### Testing Requirements
- Unit tests for all authentication and authorization logic
- Integration tests for API endpoints with valid/invalid tokens
- Security tests for data isolation between users
- Performance tests for authenticated endpoints

### Quality Gates
- All code changes must pass authentication flow tests
- Security scanning must be performed before deployment
- Database migration scripts must be tested in staging
- Performance benchmarks must be met for authenticated requests

## Governance

All development must comply with these principles. Deviations require explicit approval and documentation. Changes to this constitution require architectural review and team consensus. New features must align with multi-user, authenticated architecture patterns.

Code reviews must verify compliance with authentication, data isolation, and security requirements. Complexity must be justified with clear benefits to user experience or system performance.

**Version**: 1.1.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2026-01-25