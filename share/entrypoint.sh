#!/bin/sh

[ -n "$1" ] && exec "$@"

python3 manage.py migrate --noinput
exec gunicorn3 --log-level debug --bind 0.0.0.0:80 reactoweb.wsgi
