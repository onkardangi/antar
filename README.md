# Antar

Antar is a contemplative Bhagavad Gita reading and study platform.

This repository currently contains only the initial engineering foundation.
No product features have been implemented yet.

## Current status

Repository foundation only:

- Spring Boot modular-monolith backend boots
- PostgreSQL with pgvector and Redis start locally
- Expo mobile application boots
- Mobile can call a non-product foundation status endpoint
- CI validates backend and mobile
- No Scripture, Reading, Reflection, Journey, Guidance, Understanding, Search, Saar, or authentication features exist yet

## Architecture summary

Antar V1 is a mobile-first modular monolith:

- Backend: Java 21, Spring Boot 4
- Mobile: React Native, TypeScript, Expo
- Data: PostgreSQL + pgvector
- Cache / temporary state: Redis
- Migrations: Flyway

Product domains are package modules inside one deployable backend. Detailed design lives under `docs/architecture/`.

## Repository map

```text
antar/
├── README.md
├── compose.yaml
├── .env.example
├── docs/
├── design/
├── specs/
├── ai/
├── backend/
├── mobile/
└── .github/workflows/
```

## Prerequisites

- Java 21
- Docker and Docker Compose
- Node.js 22.13+ (Expo SDK 57 / React Native 0.86 engine requirement; CI uses Node 22.13.1)
- npm
- Xcode and/or Android Studio for simulator or emulator runs
- Docker is required for backend infrastructure tests unless you explicitly opt out locally

## Quick start (one command)

From the repository root:

```bash
make start
```

This starts:

- PostgreSQL (pgvector) + Redis via Docker Compose
- Spring Boot backend (`local` profile)
- Expo iOS Simulator

It resolves common host port conflicts (for example Postgres `5432` → `5435`, API `8080` → `8082`) and syncs `mobile/.env` to the backend port.

Useful variants:

```bash
make start-backend   # infra + API only
make start-android   # infra + API + Android
make stop            # stop backend + mobile (leave Docker up)
make stop-all        # also docker compose down
```

Equivalent script entrypoint: `./scripts/development/start-local.sh`.

## Local infrastructure

```bash
cp .env.example .env   # optional overrides; do not commit .env
docker compose up -d
docker compose ps
```

This starts:

- PostgreSQL with pgvector on port `5432` (or `POSTGRES_PORT` from `.env`)
- Redis on port `6379`

Stop with:

```bash
docker compose down
```

## Backend startup

```bash
cd backend
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

If Postgres is published on a non-default host port:

```bash
POSTGRES_PORT=5435 ./mvnw spring-boot:run \
  -Dspring-boot.run.profiles=local \
  -Dspring-boot.run.arguments=--server.port=8082
```

Foundation connectivity endpoint (temporary, **local and test profiles only**):

```bash
curl http://localhost:8080/api/internal/foundation/status
```

Expected response:

```json
{"status":"UP","service":"antar-backend"}
```

This endpoint is not a product API and is not registered outside `local`/`test` profiles.

## Mobile startup

```bash
cd mobile
cp .env.example .env   # optional; adjust API base URL for your runtime
npm ci
npm start
```

Then press `i` for iOS simulator or `a` for Android emulator, or run:

```bash
npm run ios
npm run android
```

### Mobile API base URL notes

Set `EXPO_PUBLIC_API_BASE_URL`:

| Runtime | Typical value |
| --- | --- |
| iOS simulator | `http://localhost:8080` |
| Android emulator | `http://10.0.2.2:8080` |
| Physical device | `http://<your-lan-ip>:8080` |

Do not assume `localhost` works on every platform. `make start` writes the matching URL into `mobile/.env` automatically.

## Test commands

Backend:

```bash
cd backend
./mvnw --batch-mode test
./mvnw --batch-mode verify
```

Mobile:

```bash
cd mobile
npm run typecheck
npm run lint
npm test
npm run expo:config
```

## CI summary

- `.github/workflows/backend-ci.yml` runs `./mvnw --batch-mode verify` and confirms `PersistenceFoundationTest` executed
- `.github/workflows/mobile-ci.yml` uses Node `22.13.1` and runs typecheck, lint, tests, and Expo config validation

## Explicit non-goals of this foundation

No product tables, entities, repositories, business controllers, screens, or business APIs have been implemented.
The only temporary HTTP probe is `GET /api/internal/foundation/status`, gated to `local` and `test` profiles for connectivity validation.
