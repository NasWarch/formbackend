#!/usr/bin/env bash
set -e

# Start Backend (FastAPI)
cd "$(dirname "$0")/backend"
source venv/bin/activate
export COPRO_DSN="sqlite+aiosqlite:///./copro_maintenance.db"
export COPRO_SECRET_KEY="change-me-in-production"
export COPRO_PORT="${Copro_PORT:-8000}"

echo "🚀 CoproMaintenance Backend — http://0.0.0.0:${COPRO_PORT}"
exec uvicorn app.main:app --host 0.0.0.0 --port "$COPRO_PORT"
