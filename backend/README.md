# Antar Backend

Spring Boot modular-monolith backend for Antar, a contemplative Bhagavad Gita reading and study platform.

## Purpose

Provide the HTTP API and domain services that power the Antar mobile client. Business capabilities are organized as package-level modules inside one deployable application.

## Technology

- Java 21
- Spring Boot 4
- Maven Wrapper
- Spring Data JPA
- Spring Data Redis
- Flyway
- PostgreSQL + pgvector
- Redis
- Testcontainers
- JUnit 5
- ArchUnit

## Package structure

```text
com.antar
├── identity
├── scripture
├── reading
├── reflection
├── journey
├── guidance
├── understanding
├── saar
├── search
├── platform
└── shared
```

Each module currently contains only a marker class and a README, plus one platform-owned temporary foundation status endpoint gated to local/test profiles.
Layer packages (`api`, `application`, `domain`, `infrastructure`) will be introduced as product slices are implemented.

## Local dependency startup

From the repository root:

```bash
docker compose up -d
```

This starts PostgreSQL (pgvector) and Redis with development-only defaults from `.env.example`.

## Local profile

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

Local profile configuration lives in `src/main/resources/application-local.yml` and expects:

- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`

Hibernate uses `ddl-auto: validate`. Schema changes happen only through Flyway.

## Migration behavior

Flyway migrations live in:

```text
src/main/resources/db/migration/
```

Current migration:

- `V001__initialize_database_extensions.sql`

It creates the `vector` extension and domain schemas only. It does not create product tables.
There is no `journey` schema because the current data model does not define one.

## Foundation endpoint

```text
GET /api/internal/foundation/status
```

Response:

```json
{"status":"UP","service":"antar-backend"}
```

This is a **temporary** operational connectivity probe under the Platform boundary.

- Enabled only for Spring profiles `local` and `test`
- Not a product API
- Not registered in default/production profiles
- Exists only to prove mobile-to-backend connectivity during repository foundation

## Test and verify commands

```bash
./mvnw test
./mvnw verify
./mvnw --batch-mode clean test
./mvnw --batch-mode clean verify
```

Infrastructure tests (`PersistenceFoundationTest`, context load, foundation endpoint) use JVM-scoped Testcontainers for PostgreSQL and Redis. Docker is required by default.

Local opt-out when Docker is unavailable:

```bash
./mvnw test -Dantar.skipInfrastructureTests=true
```

CI must not set that property. Backend CI also greps Surefire reports to prove `PersistenceFoundationTest` executed.

Architecture-test notes live in `src/test/java/com/antar/architecture/README.md`.

## Explicit status

No product APIs or product tables exist yet. There are no business entities, repositories, Scripture data, authentication flows, or AI functionality in this milestone.
