#!/usr/bin/env zsh
set -e

if [[ -f ".venv311/bin/activate" ]]; then
  source .venv311/bin/activate
elif [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

python run_all.py "$@"
