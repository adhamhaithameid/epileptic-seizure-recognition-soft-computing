# Soft Computing Main Project

This repository contains a refactored Soft Computing course project for **Epileptic Seizure Recognition** with a full staged Cartesian benchmark.

## Open in Colab
- Direct URL: [epileptic_seizure_full_pipeline_colab.ipynb](https://colab.research.google.com/github/adhamhaithameid/soft-computing-main-project/blob/main/notebooks/colab/epileptic_seizure_full_pipeline_colab.ipynb)
- Notebook path: `notebooks/colab/epileptic_seizure_full_pipeline_colab.ipynb`

## Benchmark Design
- Tracks: `binary`, `multiclass`
- CV folds: `3`
- Preprocessing: `standard`, `minmax`, `robust`, `quantile`
- Reduction: `none`, `pca`, `lda_projection`, `svd`
- Selection: `none`, `filter_chi2`, `filter_anova`, `filter_correlation`, `wrapper_sfs`, `wrapper_rfe`, `embedded_l1`, `ga_selection`
- Classifiers: `knn`, `svm`, `decision_tree`, `logistic_regression`, `lda_classifier`, `mlp_ann`

## How combinations are counted
- Unique combinations: `4 x 4 x 8 x 6 x 2 = 1536`
- Fold evaluations: `1536 x 3 = 4608`

## Output Schema Contract
`results/metrics/cartesian_metrics_all.csv` columns:
- `track, fold, preprocessing, reduction, selection, model`
- `accuracy, precision, recall, f1, roc_auc, error_rate`
- `fit_time_sec, predict_time_sec, status, skip_reason`

`results/metrics/cartesian_run_manifest.json` fields:
- `expected_combos, expected_fold_evals`
- `completed_ok, skipped_or_failed, runtime_sec`
- `best_binary, best_multiclass`

## Run on Any Laptop (Exact Steps)

### A) Linux (NVIDIA GPU optional)
```bash
# 1) System dependencies
sudo pacman -Syu --needed git python python-pip base-devel

# 2) Clone repository
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/adhamhaithameid/soft-computing-main-project.git
cd soft-computing-main-project

# 3) Create and activate virtual environment
python -m venv .venv311
source .venv311/bin/activate

# 4) Install Python dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install --disable-pip-version-check -r requirements.txt

# 5) Environment check
python src/cli/check_env.py

# 6) Fetch/refresh dataset
python src/cli/fetch_data.py

# 7) Smoke test (quick)
python src/cli/run_experiments.py --fresh --max-rows 120 --checkpoint-every 30
python src/cli/validate_cartesian_outputs.py --allow-partial

# 8) Full run (real benchmark)
systemd-inhibit --what=sleep:idle --why="Soft computing full benchmark" \
bash -lc 'source .venv311/bin/activate && python src/cli/run_experiments.py --fresh --checkpoint-every 120'

# 9) Strict validation + paper drafts
python src/cli/validate_cartesian_outputs.py
python src/cli/generate_paper_drafts.py
```

### B) macOS (Apple Silicon / Intel)
```bash
# 1) Install basic tools (if needed)
xcode-select --install

# 2) Clone repository
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/adhamhaithameid/soft-computing-main-project.git
cd soft-computing-main-project

# 3) Create and activate virtual environment
python3 -m venv .venv311
source .venv311/bin/activate

# 4) Install dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install --disable-pip-version-check -r requirements.txt

# 5) Full run
caffeinate -dimsu bash -lc 'source .venv311/bin/activate && python src/cli/run_experiments.py --fresh --checkpoint-every 120'

# 6) Validate and generate drafts
python src/cli/validate_cartesian_outputs.py
python src/cli/generate_paper_drafts.py
```

### C) Windows (PowerShell)
```powershell
# 1) Clone repository
git clone https://github.com/adhamhaithameid/soft-computing-main-project.git
cd soft-computing-main-project

# 2) Create and activate virtual environment
python -m venv .venv311
.venv311\Scripts\Activate.ps1

# 3) Install dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install --disable-pip-version-check -r requirements.txt

# 4) Fetch + run + validate + drafts
python src/cli/fetch_data.py
python src/cli/run_experiments.py --fresh --checkpoint-every 120
python src/cli/validate_cartesian_outputs.py
python src/cli/generate_paper_drafts.py
```

### Resume after interruption (all platforms)
```bash
source .venv311/bin/activate
python src/cli/run_experiments.py --checkpoint-every 120
```

Do not use `--fresh` when resuming.

### High-CPU mode (real parallelism)
This project now supports explicit stage-level parallelism:
- `--jobs`: parallel model evaluations per stage
- `--selection-jobs`: parallel workers inside wrapper SFS

Use this on high-core laptops:
```bash
source .venv311/bin/activate
CORES=$(nproc)

# When using --jobs > 1, avoid nested thread oversubscription:
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export MPLBACKEND=Agg

systemd-inhibit --what=sleep:idle --why="Soft computing full benchmark" \
bash -lc "source .venv311/bin/activate && python src/cli/run_experiments.py --fresh --checkpoint-every 120 --jobs $CORES --selection-jobs $CORES"
```

## Run from Colab
1. Open the Colab link above.
2. Run all cells from top to bottom.
3. Use the config cell for smoke/full mode, checkpoint frequency, and method lists.
4. Download `colab_outputs.zip` from the final cell if needed.

## Interpreting failed/skipped rows
- `status="ok"`: combo executed and metrics are valid.
- `status="failed"`: combo was skipped or failed safely; details are in `skip_reason`.
- Known auto-fixes:
  - `chi2` uses non-negative transform when needed.
  - Feature/component counts are dynamically clamped to valid ranges.

## Main generated outputs
- `results/metrics/cartesian_metrics_all.csv`
- `results/metrics/cartesian_run_manifest.json`
- `results/tables/cartesian_summary_by_combo.csv`
- `results/tables/cartesian_rankings_binary.csv`
- `results/tables/cartesian_rankings_multiclass.csv`
- `results/reports/cartesian_comparison_report.md`
- `results/figures/cartesian_*.png`
- `paper/draft/*.md`

## Main entrypoints
- `src/cli/fetch_data.py`
- `src/cli/check_env.py`
- `src/cli/run_experiments.py`
- `src/cli/generate_paper_drafts.py`

## Project guides
- `PROJECT_MASTER_GUIDE.md`
- `FOLDER_STRUCTURE.md`
- `ABOUT.md`
