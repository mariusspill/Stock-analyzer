#!/usr/bin/env bash
# One-time migration: copy the stockdb from a *native* MySQL install on this
# host into the containerised database.
#
# The mysqldump/mysql clients used here are the ones inside the db container,
# reaching back to the host over host.docker.internal. That means this works
# even if the host has no usable MySQL client on PATH, and the dump file never
# passes through a host shell that could re-encode it.
set -euo pipefail
cd "$(dirname "$0")/.."

NATIVE_HOST="${NATIVE_SQL_HOST:-host.docker.internal}"
NATIVE_PORT="${NATIVE_SQL_PORT:-3306}"
NATIVE_USER="${NATIVE_SQL_USER:-root}"
NATIVE_DB="${NATIVE_SQL_DATABASE:-stockdb}"

if [ -z "${NATIVE_SQL_PW:-}" ]; then
  read -r -s -p "Password for $NATIVE_USER on $NATIVE_HOST:$NATIVE_PORT: " NATIVE_SQL_PW
  echo
fi

name="native_import_$(date +%Y-%m-%dT%H%M%S).sql.gz"

echo "Exporting $NATIVE_DB from $NATIVE_HOST:$NATIVE_PORT ..."
docker compose exec -T -e NATIVE_PW="$NATIVE_SQL_PW" db sh -c '
  set -e
  mysqldump -h '"$NATIVE_HOST"' -P '"$NATIVE_PORT"' -u '"$NATIVE_USER"' -p"$NATIVE_PW" \
    --single-transaction --quick --routines --triggers \
    --default-character-set=utf8mb4 \
    '"$NATIVE_DB"' | gzip -9 > "/backups/'"$name"'"
'

echo "Exported to backups/$name ($(du -h "backups/$name" | cut -f1))"
echo
echo "Load it into the container with:"
echo "  ./scripts/db_restore.sh backups/$name"
