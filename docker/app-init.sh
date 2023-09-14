#!/bin/sh -ae
cd /workspace
/usr/local/bin/wait-for db:5432 -- echo "PostgreSQL ready"
./manage.py migrate --no-input || true
./manage.py runserver 0.0.0.0:8000
