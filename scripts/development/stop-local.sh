#!/usr/bin/env bash
# Stop local Antar processes started by start-local.sh.
#
# Usage:
#   ./scripts/development/stop-local.sh           # backend + mobile
#   ./scripts/development/stop-local.sh --infra   # also docker compose down
#   make stop
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOCAL_DIR="${ROOT}/.local"
STOP_INFRA=0

for arg in "$@"; do
  case "${arg}" in
    --infra|--all) STOP_INFRA=1 ;;
    -h|--help)
      sed -n '2,8p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown argument: ${arg}" >&2
      echo "Usage: $0 [--infra]" >&2
      exit 1
      ;;
  esac
done

stop_pidfile() {
  local name="$1"
  local pidfile="$2"
  if [[ ! -f "${pidfile}" ]]; then
    return 0
  fi
  local pid
  pid="$(cat "${pidfile}")"
  if [[ -n "${pid}" ]] && kill -0 "${pid}" 2>/dev/null; then
    echo "==> Stopping ${name} (pid ${pid})"
    # Maven wrapper may leave a child Java process; kill the process group when possible.
    kill "${pid}" 2>/dev/null || true
    # Also stop spring-boot java on known Antar ports if still listening.
    sleep 1
    if kill -0 "${pid}" 2>/dev/null; then
      kill -9 "${pid}" 2>/dev/null || true
    fi
  fi
  rm -f "${pidfile}"
}

stop_pidfile "mobile" "${LOCAL_DIR}/mobile.pid"
stop_pidfile "backend" "${LOCAL_DIR}/backend.pid"

# Fall back: stop Antar backend by foundation-status port from .env / mobile .env.
SERVER_PORT=8080
if [[ -f "${ROOT}/.env" ]]; then
  # shellcheck disable=SC1091
  set -a
  source "${ROOT}/.env"
  set +a
fi
if [[ -f "${ROOT}/mobile/.env" ]]; then
  mobile_url="$(
    grep -E '^[[:space:]]*EXPO_PUBLIC_API_BASE_URL=' "${ROOT}/mobile/.env" \
      | tail -1 \
      | cut -d= -f2- \
      | tr -d '[:space:]"'\'''
  )"
  if [[ "${mobile_url}" =~ :([0-9]+)$ ]]; then
    SERVER_PORT="${BASH_REMATCH[1]}"
  fi
fi

if curl -sf "http://127.0.0.1:${SERVER_PORT}/api/internal/foundation/status" 2>/dev/null \
  | grep -q '"service":"antar-backend"'; then
  echo "==> Stopping Antar backend on port ${SERVER_PORT}"
  pid="$(lsof -nP -iTCP:"${SERVER_PORT}" -sTCP:LISTEN -t 2>/dev/null | head -1 || true)"
  if [[ -n "${pid}" ]]; then
    kill "${pid}" 2>/dev/null || true
    sleep 1
    if kill -0 "${pid}" 2>/dev/null; then
      kill -9 "${pid}" 2>/dev/null || true
    fi
  fi
fi

# Metro / Expo on 8081 if we started it (best-effort; only if pidfile was present we already tried).
# Leave Metro alone if the user started it outside this script.

if [[ "${STOP_INFRA}" -eq 1 ]]; then
  echo "==> Stopping Docker Compose infrastructure"
  (
    cd "${ROOT}"
    docker compose down
  )
else
  echo "==> Leaving Docker Compose infrastructure running (use --infra to stop it)"
fi

echo "Stopped."
