#!/usr/bin/env bash
set -e

# Start Frontend (Next.js)
cd "$(dirname "$0")/frontend"
export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8000/api}"

echo "🚀 CoproMaintenance Frontend — http://localhost:3000"
exec npx next start -p 3000 -H 0.0.0.0
