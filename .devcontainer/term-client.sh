#!/bin/zsh

if [ -n "$EDITOR_VSCODE" ]; then
  zsh -i -c "npm run dev"
  clear
  echo "====== CLIENT DEV SERVER ======\n"
  echo "  Start the client dev server using command:"
  echo "  npm run dev\n"
  echo "================================\n"
fi

zsh
