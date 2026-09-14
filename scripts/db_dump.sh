#!/usr/bin/env bash
# Dump the containerised database to backups/stockdb_<timestamp>.sql.gz
#
# mysqldump runs inside the db container and writes straight into the mounted
# backups/ directory. Nothing is piped through the host shell -- that is
# deliberate: redirecting mysqldump output with `>` in Windows PowerShell
# produces a UTF-16 file that MySQL cannot restore.
set -euo pipefail
cd "$(dirname "$0")/.."

name="stockdb_$(date +%Y-%m-%dT%H%M%S).sql.gz"

echo "Dumping to backups/$name ..."
docker compose exec -T db sh -c '
  set -e
  mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" \
    --single-transaction --quick --routines --triggers \
    --default-character-set=utf8mb4 \
    "$MYSQL_DATABASE" | gzip -9 > "/backups/'"$name"'"
'

echo "Done: backups/$name ($(du -h "backups/$name" | cut -f1))"
