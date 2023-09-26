#!/bin/zsh

if [ -n "$EDITOR_VSCODE" ]; then
  echo "Waiting for initialization script to complete... Please wait..."
  until [ -f /.dev-ready ]
  do
      sleep 2
  done

  zsh -i -c "./manage.py runserver 8001"
  clear
  echo "====== BACKEND API SERVER ======\n"
  echo "  Start the server using command:"
  echo "  ./manage.py runserver 8001\n"
  echo "================================\n"
fi
zsh
