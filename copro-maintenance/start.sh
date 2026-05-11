#!/usr/bin/env bash
set -e

# Start all services for CoproMaintenance
echo "🚀 CoproMaintenance — Starting all services..."

# Start backend
echo "→ Starting backend..."
cd "$(dirname "$0")/backend"
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "→ Starting frontend..."
cd "$(dirname "$0")/frontend"
npx next start -p 3000 &
FRONTEND_PID=$!

echo ""
echo "✅ Backend:  http://localhost:8000"
echo "✅ Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
