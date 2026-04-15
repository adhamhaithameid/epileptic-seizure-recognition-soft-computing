# Cartesian Comparison Report

## Binary Top 10

|   rank | preprocessing   | reduction   | selection    | model   |   accuracy |     f1 |   delta_vs_baseline_accuracy |
|-------:|:----------------|:------------|:-------------|:--------|-----------:|-------:|-----------------------------:|
|      1 | quantile        | pca         | none         | svm     |     0.9797 | 0.9483 |                       0.0003 |
|      2 | quantile        | none        | none         | svm     |     0.9794 | 0.9476 |                       0      |
|      3 | quantile        | svd         | none         | svm     |     0.9776 | 0.9429 |                      -0.0018 |
|      4 | quantile        | none        | embedded_l1  | svm     |     0.9768 | 0.941  |                      -0.0026 |
|      5 | robust          | pca         | none         | svm     |     0.9739 | 0.9332 |                      -0.0055 |
|      6 | minmax          | svd         | none         | mlp_ann |     0.9738 | 0.9352 |                       0.0021 |
|      7 | robust          | svd         | none         | svm     |     0.9734 | 0.9319 |                      -0.006  |
|      8 | quantile        | none        | ga_selection | svm     |     0.9726 | 0.93   |                      -0.0068 |
|      9 | robust          | svd         | none         | mlp_ann |     0.9724 | 0.9298 |                       0.0007 |
|     10 | minmax          | pca         | none         | mlp_ann |     0.972  | 0.9296 |                       0.0003 |

## Multiclass Top 10

| rank   | preprocessing   | reduction   | selection   | model   | accuracy   | f1   | delta_vs_baseline_accuracy   |
|--------|-----------------|-------------|-------------|---------|------------|------|------------------------------|