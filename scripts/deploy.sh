#!/usr/bin/env bash
# ============================================================
# Deploy script — rsync + docker compose up -d
# ============================================================
set -euo pipefail

APP_DIR="/root/monetization-lab"
REMOTE_USER="root"
REMOTE_HOST="localhost"  # Changez pour l'IP du serveur de production

echo "=== Deploy: rsync ==="
rsync -avz --delete \
    --exclude '.env' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude '*.pyc' \
    "$APP_DIR/" \
    "$REMOTE_USER@$REMOTE_HOST:$APP_DIR/"

echo "=== Deploy: docker compose ==="
ssh "$REMOTE_USER@$REMOTE_HOST" "cd $APP_DIR && docker compose up -d --build"

echo "=== Deploy: health check ==="
sleep 3
curl -f "http://$REMOTE_HOST:8000/health" && echo " — OK" || echo " — FAILED"

echo "=== Deploy done ==="
