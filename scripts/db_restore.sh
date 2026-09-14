#!/usr/bin/env bash
# Restore a dump into the containerised database.
#
#   ./scripts/db_restore.sh                 # newest dump in backups/
#   ./scripts/db_restore.sh backups/x.sql.gz
#
# This REPLACES the current contents of the database.
set -euo pipefail
cd "$(dirname "$0")/.."

file="${1:-$(ls -1t backups/*.sql.gz 2>/dev/null | head -1 || true)}"
if [ -z "$file" ] || [ ! -f "$file" ]; then
  echo "No dump found. Pass one explicitly, or run ./scripts/db_dump.sh first." >&2
  exit 1
fi

base="$(basename "$file")"
echo "About to overwrite the database with $file"
read -r -p "Type 'yes' to continue: " confirm
[ "$confirm" = "yes" ] || { echo "Aborted."; exit 1; }

docker compose exec -T db sh -c '
  set -e
  gunzip -c "/backups/'"$base"'" | mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"
'

echo "Restored $file"
# A full dump carries the alembic_version table with it, so the restored
# database already knows which migration it is on. Confirm, then apply anything
# newer that has landed in the meantime.
echo "Verify the migration state:"
echo "  docker compose run --rm migrate alembic current"
echo "  docker compose run --rm migrate alembic upgrade head"
