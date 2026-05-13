#!/usr/bin/env bash
if ! pgrep -f "hiddencostreport.cli ui"; then
  cd $HOME/hiddencostreport
  source .venv/bin/activate
  nohup python -m hiddencostreport.cli ui &
fi

