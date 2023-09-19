#!/bin/zsh

if [ -n "$EDITOR_VSCODE" ]; then
  zsh -i -c "./manage.py runserver 8001"
  clear
  echo "====== BACKEND API SERVER ======\n"
  echo "  Start the server using command:"
  echo "  ./manage.py runserver 8001\n"
  echo "================================\n"
fi
zsh
