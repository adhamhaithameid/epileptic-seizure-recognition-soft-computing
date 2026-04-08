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

## Run locally
```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
python -m pip install --disable-pip-version-check -r requirements.txt
./run_all.sh
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
