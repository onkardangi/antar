.PHONY: start stop start-backend help

help:
	@echo "Antar local development"
	@echo ""
	@echo "  make start          Start Postgres, Redis, backend, and iOS Simulator"
	@echo "  make start-backend  Start Postgres, Redis, and backend only"
	@echo "  make start-android  Start Postgres, Redis, backend, and Android emulator"
	@echo "  make stop           Stop backend and mobile (leave Docker infra up)"
	@echo "  make stop-all       Stop backend, mobile, and Docker Compose infra"

start:
	./scripts/development/start-local.sh --ios

start-backend:
	./scripts/development/start-local.sh --no-mobile

start-android:
	./scripts/development/start-local.sh --android

stop:
	./scripts/development/stop-local.sh

stop-all:
	./scripts/development/stop-local.sh --infra
