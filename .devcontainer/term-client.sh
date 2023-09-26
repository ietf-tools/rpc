#!/bin/zsh

if [ -n "$EDITOR_VSCODE" ]; then
  echo "Waiting for initialization script to complete... Please wait..."
  until [ -f /.dev-ready ]
  do
      sleep 2
  done

  zsh -i -c "npm run dev"
  clear
  echo "====== CLIENT DEV SERVER ======\n"
  echo "  Start the client dev server using command:"
  echo "  npm run dev\n"
  echo "================================\n"
fi

zsh
