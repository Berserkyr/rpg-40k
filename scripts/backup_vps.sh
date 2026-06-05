#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-$HOME/rpg-40k-backups}"
STAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="$BACKUP_DIR/rpg40k-$STAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

docker run --rm \
  -v rpg-40k_rpg40k_data:/data:ro \
  -v rpg-40k_rpg40k_saves:/saves:ro \
  -v "$BACKUP_DIR:/backup" \
  alpine tar -czf "/backup/$(basename "$ARCHIVE")" /data /saves

echo "Sauvegarde créée : $ARCHIVE"
