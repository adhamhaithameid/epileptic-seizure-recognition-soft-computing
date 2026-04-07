#!/usr/bin/env zsh
set -e

if [[ -f ".venv311/bin/activate" ]]; then
  source .venv311/bin/activate
elif [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

python 04_src/fetch_data.py
python 04_src/check_env.py
python 04_src/run_experiments.py
python 04_src/generate_paper_drafts.py

echo "All steps completed."
