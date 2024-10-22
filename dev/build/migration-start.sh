#!/bin/bash -e

echo "Running migrations..."
env DJANGO_SETTINGS_MODULE=rpctracker.settings.production \
    ./manage.py migrate

echo "Done!"
