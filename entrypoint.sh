#!/bin/bash
set -eo pipefail
shopt -s nullglob

python manage.py migrate --noinput || echo "Migration failed"
python manage.py collectstatic --noinput

exec "$@"
