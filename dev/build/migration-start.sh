#!/bin/bash -e

echo "Running migrations..."
./manage.py migrate

echo "Done!"
