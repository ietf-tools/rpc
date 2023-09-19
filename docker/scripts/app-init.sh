#!/bin/bash

cd /workspace

# Add /workspace as a safe git directory
git config --global --add safe.directory /workspace

# Turn off git info in zsh prompt (causes slowdowns)
git config oh-my-zsh.hide-info 1

# Wait for DB container
echo "Waiting for DB container to come online..."
/usr/local/bin/wait-for db:5432 -- echo "PostgreSQL ready"

# Run migrations
echo "Running migrations..."
./manage.py migrate --no-input || true

if [ -z "$EDITOR_VSCODE" ]; then
  echo "-----------------------------------------------------------------"
  echo "Ready!"
  echo "-----------------------------------------------------------------"

  zsh
  exit 0
fi
