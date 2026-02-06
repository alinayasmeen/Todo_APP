# ADR-0002: Backend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-25
- **Feature:** Todo App Authentication and RBAC
- **Context:** Need to select a modern backend stack that provides type safety, async performance, and good integration with authentication services for a multi-user todo application with persistent storage.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Selected an integrated backend stack consisting of:
- **Framework**: FastAPI for async Python web framework with automatic API documentation
- **ORM**: SQLModel for type-safe database interactions with SQLAlchemy and Pydantic compatibility
- **Language**: Python 3.12 for type hints and modern language features
- **Authentication**: Better Auth with JWT tokens for secure user management
- **Type Safety**: Pydantic models for request/response validation
- **Testing**: pytest for comprehensive testing framework

## Consequences

### Positive

- FastAPI provides automatic OpenAPI documentation and excellent developer experience
- SQLModel offers type safety with seamless integration of SQLAlchemy and Pydantic
- Python 3.12 provides modern language features and performance improvements
- Async capabilities enable better performance under load
- Strong type safety reduces runtime errors and improves maintainability
- Built-in validation and serialization with Pydantic
- Rich ecosystem of Python packages for various functionality
- Excellent integration with authentication services

### Negative

- Python's Global Interpreter Lock (GIL) may limit CPU-bound performance
- Async programming complexity for team members unfamiliar with async patterns
- Runtime type checking only (no compile-time like compiled languages)
- Potential memory consumption under high load
- Dependency on third-party libraries for certain functionality

## Alternatives Considered

- **Alternative Stack A**: Flask + SQLAlchemy + Marshmallow + Authlib
  - Why rejected: Less modern, no automatic documentation, more boilerplate code
- **Alternative Stack B**: Django + DRF + Django REST Framework JWT
  - Why rejected: Heavier framework, more opinionated, overkill for this application
- **Alternative Stack C**: Node.js + Express + Prisma + Passport.js
  - Why rejected: Different language ecosystem, less type safety without TypeScript
- **Alternative Stack D**: Go + Gin + GORM + JWT
  - Why rejected: Different language ecosystem, steeper learning curve for team
- **Alternative Stack E**: Java + Spring Boot + Hibernate + Spring Security
  - Why rejected: More verbose, heavier framework, different ecosystem

## References

- Feature Spec: specs/001-arch-spec-integration/spec.md
- Implementation Plan: specs/001-arch-spec-integration/plan.md
- Related ADRs: ADR-0001 (Frontend Technology Stack)
- Evaluator Evidence: specs/001-arch-spec-integration/research.md
