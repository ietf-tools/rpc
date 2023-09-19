#!/bin/bash

cd /workspace

# Add /workspace as a safe git directory
git config --global --add safe.directory /workspace

# Turn off git info in zsh prompt (causes slowdowns)
git config oh-my-zsh.hide-info 1

# Wait for DB container
echo "Waiting for DB container to come online ..."
/usr/local/bin/wait-for db:5432 -- echo "PostgreSQL ready"

# Run migrations
./manage.py migrate --no-input || true

echo "-----------------------------------------------------------------"
echo "Ready!"
echo "-----------------------------------------------------------------"
