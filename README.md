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
- `execution_device, acceleration_backend`
- `best_binary, best_multiclass`

## Run on Linux, macOS, and Windows

### 1) One-time setup (all platforms)
```bash
git clone https://github.com/adhamhaithameid/soft-computing-main-project.git
cd soft-computing-main-project
python -m venv .venv311
```

- Linux/macOS activate:
```bash
source .venv311/bin/activate
```

- Windows PowerShell activate:
```powershell
.venv311\Scripts\Activate.ps1
```

- Install dependencies:
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install --disable-pip-version-check -r requirements.txt
```

### 2) Full pipeline (cross-platform command)
```bash
python run_all.py --fresh --device auto --checkpoint-every 120
```

Wrapper scripts are also available:
- Linux/macOS: `bash run_all.sh --fresh --device auto`
- Windows PowerShell: `.\run_all.ps1 -Fresh -Device auto`
- Windows cmd: `run_all.bat --fresh --device auto`

### 3) GPU mode (NVIDIA + RAPIDS, with fallback)
The benchmark now supports `--device {auto,cpu,gpu}`:
- `auto`: try GPU first, fallback to CPU when unavailable.
- `cpu`: force CPU mode.
- `gpu`: request GPU mode.
- `--strict-device`: fail if `gpu` cannot be enabled.

GPU acceleration is enabled through RAPIDS `cuml.accel` (zero-code-change sklearn acceleration where supported).  
For Linux/NVIDIA installation, use RAPIDS official instructions for your CUDA/Python version:
- https://docs.rapids.ai/install

Run with strict GPU requirement:
```bash
python src/cli/check_env.py --device gpu --strict-device
python src/cli/run_experiments.py --fresh --device gpu --strict-device --checkpoint-every 120
```

### Resume after interruption
```bash
python src/cli/run_experiments.py --device auto --checkpoint-every 120
```
Do not use `--fresh` when resuming.

### High-CPU mode (parallelism)
- `--jobs`: parallel model evaluations per stage
- `--selection-jobs`: parallel workers inside wrapper SFS

```bash
python src/cli/run_experiments.py --fresh --device cpu --checkpoint-every 120 --jobs 8 --selection-jobs 8
```

Apple Silicon full-core run:
```bash
source .venv311/bin/activate
CORES=$(sysctl -n hw.ncpu)
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export MPLBACKEND=Agg

caffeinate -dimsu bash -lc "source .venv311/bin/activate && python src/cli/run_experiments.py --fresh --device cpu --checkpoint-every 120 --jobs $CORES --selection-jobs $CORES"
```

Smoke-test then partial validation:
```bash
python src/cli/run_experiments.py --fresh --device cpu --max-rows 300 --checkpoint-every 30 --jobs 4 --selection-jobs 4
python src/cli/validate_cartesian_outputs.py --allow-partial
```

Full-run strict validation:
```bash
python src/cli/validate_cartesian_outputs.py
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
