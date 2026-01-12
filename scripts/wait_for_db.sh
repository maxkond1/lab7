#!/bin/sh
# wait_for_db.sh
# Robust DB wait that works on slim images (no psql required).
set -e

host="${1:-db}"
shift

# Optional: allow passing host:port
case "$host" in
  *:*)
    _h="${host%%:*}"
    _p="${host##*:}"
    host="$_h"
    export DB_PORT="${DB_PORT:-$_p}"
    ;;
esac

: "${DB_PORT:=5432}"

# Prefer DB_* variables, fallback to POSTGRES_* for backward compatibility.
: "${DB_NAME:=${POSTGRES_DB:-}}"
: "${DB_USER:=${POSTGRES_USER:-}}"
: "${DB_PASSWORD:=${POSTGRES_PASSWORD:-}}"

if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
  echo "DB credentials are not set (DB_NAME/DB_USER/DB_PASSWORD or POSTGRES_DB/POSTGRES_USER/POSTGRES_PASSWORD)." >&2
  exit 1
fi

python - <<'PY'
import os, sys, time
import psycopg2

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "5432"))
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

timeout = int(os.getenv("DB_WAIT_TIMEOUT", "60"))
start = time.time()

while True:
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        conn.close()
        print("Postgres is up - executing command", file=sys.stderr)
        break
    except Exception:
        if time.time() - start > timeout:
            print(f"Postgres is unavailable after {timeout}s - giving up", file=sys.stderr)
            raise
        print("Postgres is unavailable - sleeping", flush=True)
        time.sleep(1)
PY

exec "$@"
