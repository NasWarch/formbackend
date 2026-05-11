#!/usr/bin/env bash
# ============================================================
# Backup PostgreSQL — pg_dump vers backup dir
# À mettre en cron : 0 3 * * * /root/monetization-lab/scripts/backup-db.sh
# ============================================================
set -euo pipefail

BACKUP_DIR="/root/monetization-lab/backups"
DB_NAME="monetization"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="${DB_NAME}_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

pg_dump "$DB_NAME" | gzip > "$BACKUP_DIR/$FILENAME"

# Garder les 30 derniers jours
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -mtime +30 -delete

echo "Backup: $BACKUP_DIR/$FILENAME ($(du -h "$BACKUP_DIR/$FILENAME" | cut -f1))"
