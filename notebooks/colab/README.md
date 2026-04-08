# Colab Notebook

- Main notebook: `epileptic_seizure_full_pipeline_colab.ipynb`
- Direct Colab URL: https://colab.research.google.com/github/adhamhaithameid/soft-computing-main-project/blob/main/notebooks/colab/epileptic_seizure_full_pipeline_colab.ipynb

## Purpose
Run the full staged Cartesian benchmark in Google Colab with all requested methods:
- Preprocessing: Standard, MinMax, Robust, Quantile
- Reduction: none, PCA, LDA projection, SVD
- Selection: none, chi2, ANOVA, correlation, SFS, RFE, embedded L1, GA
- Classifiers: KNN, SVM, Decision Tree, Logistic Regression, LDA classifier, MLP/ANN

## Outputs
The notebook writes outputs under `results/*` and `paper/draft/*`, then packages artifacts as `colab_outputs.zip`.

See full steps in `docs/guides/colab_workflow.md`.
