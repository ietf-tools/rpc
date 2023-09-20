#!/bin/bash

cd /workspace

# Add /workspace as a safe git directory
git config --global --add safe.directory /workspace

# Turn off git info in zsh prompt (causes slowdowns)
git config oh-my-zsh.hide-info 1

# Run nginx
echo "Starting nginx..."
sudo nginx

# Wait for DB container
echo "Waiting for DB container to come online..."
/usr/local/bin/wait-for db:5432 -- echo "PostgreSQL ready"

# Install client dependencies
cd client
npm install
cd ..

# Run migrations
echo "Running migrations..."
./manage.py migrate --no-input || true

if [ -z "$EDITOR_VSCODE" ]; then
  echo "-----------------------------------------------------------------"
  echo "Ready!"
  echo "-----------------------------------------------------------------"
  echo "Launching tmux..."

  tmux start-server
  tmux new-session -d -s dev -c '/workspace'
  sleep 1
  tmux send-keys './manage.py runserver 8001' Enter
  tmux split-window -h -c '/workspace/client'
  tmux send-keys 'npm run dev' Enter
  tmux -2 attach-session -d -c '/workspace'

  echo "You've exited tmux. Send "exit" to stop the containers and quit."
  zsh
  exit 0
fi
