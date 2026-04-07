# Folder Structure

```text
soft computing - research/
├── 01_lectures/
│   ├── Lecture PDFs
│   └── README.md
├── 02_data/
│   ├── raw/
│   │   └── epileptic_seizure_recognition/
│   │       ├── epileptic_seizure_data.csv
│   │       └── metadata.json
│   ├── interim/
│   ├── processed/
│   │   ├── features_numeric.csv
│   │   └── targets.csv
│   └── links.md
├── 03_notebooks/
│   ├── colab/
│   │   ├── epileptic_seizure_full_pipeline_colab.ipynb
│   │   └── README.md
│   ├── kaggle/
│   └── local/
├── 04_src/
│   ├── check_env.py
│   ├── fetch_data.py
│   ├── run_experiments.py
│   └── generate_paper_drafts.py
├── 05_results/
│   ├── metrics/
│   │   ├── metrics_all.csv
│   │   └── run_summary.json
│   ├── folds/
│   │   └── fold_metrics.csv
│   ├── tables/
│   │   ├── summary_accuracy.csv
│   │   ├── confusion_matrix_best_binary.csv
│   │   ├── confusion_matrix_best_multiclass.csv
│   │   ├── dataset_descriptive_stats.csv
│   │   ├── covariance_matrix.csv
│   │   └── correlation_matrix.csv
│   └── figures/
├── 06_paper/
│   ├── template/
│   │   └── Fill your Project Information in this document.docx
│   ├── draft/
│   │   └── paper section markdown files
│   ├── tables/
│   ├── figures/
│   └── references/
├── 07_docs/
│   ├── plans, status, and logs
│   ├── 11_lecture_understanding.md
│   └── 12_colab_workflow.md
├── .gitignore
├── README.md
├── PROJECT_MASTER_GUIDE.md
├── FOLDER_STRUCTURE.md
├── requirements.txt
└── run_all.sh
```

## Simplification Done
To reduce clutter:
- Removed temporary folder `tmp/`.
- Removed unused empty directories under `04_src/`.
- Added top-level guides so understanding the project does not require opening many nested files.
