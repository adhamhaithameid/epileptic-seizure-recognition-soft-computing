# Results and Discussion

- Best binary combination (current run): **svm | quantile | pca | none**
- Best multiclass combination (current run): **mlp_ann | minmax | pca | none**

## Binary Top Rankings

|   rank | preprocessing   | reduction   | selection   | model   |   accuracy |       f1 |   delta_vs_baseline_accuracy |
|-------:|:----------------|:------------|:------------|:--------|-----------:|---------:|-----------------------------:|
|      1 | quantile        | pca         | none        | svm     |   0.976261 | 0.939349 |                  0.00026087  |
|      2 | quantile        | none        | none        | svm     |   0.976    | 0.938647 |                  0           |
|      3 | quantile        | svd         | none        | svm     |   0.974608 | 0.934881 |                 -0.00139127  |
|      4 | quantile        | none        | embedded_l1 | svm     |   0.973565 | 0.932277 |                 -0.00243477  |
|      5 | standard        | svd         | none        | svm     |   0.971913 | 0.927855 |                 -0.00408677  |
|      6 | minmax          | svd         | none        | mlp_ann |   0.971826 | 0.930178 |                  0.000347924 |
|      7 | minmax          | pca         | none        | svm     |   0.971739 | 0.927276 |                 -0.00426074  |
|      8 | robust          | svd         | none        | svm     |   0.971652 | 0.927163 |                 -0.00434768  |
|      9 | robust          | pca         | none        | svm     |   0.971565 | 0.926851 |                 -0.00443469  |
|     10 | standard        | none        | none        | mlp_ann |   0.971478 | 0.926708 |                  0           |
|     11 | minmax          | pca         | none        | mlp_ann |   0.971304 | 0.928282 |                 -0.000173883 |
|     12 | standard        | pca         | none        | svm     |   0.971217 | 0.925894 |                 -0.0047825   |

## Multiclass Top Rankings

|   rank | preprocessing   | reduction   | selection          | model   |   accuracy |       f1 |   delta_vs_baseline_accuracy |
|-------:|:----------------|:------------|:-------------------|:--------|-----------:|---------:|-----------------------------:|
|      1 | minmax          | pca         | none               | mlp_ann |   0.685651 | 0.685026 |                   0.0109559  |
|      2 | standard        | none        | none               | mlp_ann |   0.674696 | 0.675497 |                   0          |
|      3 | standard        | svd         | none               | mlp_ann |   0.671305 | 0.671783 |                  -0.00339042 |
|      4 | standard        | pca         | none               | mlp_ann |   0.670869 | 0.671112 |                  -0.00382601 |
|      5 | robust          | none        | none               | mlp_ann |   0.66974  | 0.670368 |                  -0.00495582 |
|      6 | robust          | none        | embedded_l1        | mlp_ann |   0.66313  | 0.663652 |                  -0.0115651  |
|      7 | robust          | pca         | none               | mlp_ann |   0.662174 | 0.662394 |                  -0.0125217  |
|      8 | standard        | none        | embedded_l1        | mlp_ann |   0.662    | 0.6624   |                  -0.0126957  |
|      9 | minmax          | pca         | filter_correlation | mlp_ann |   0.653479 | 0.65257  |                  -0.0212169  |
|     10 | minmax          | pca         | embedded_l1        | mlp_ann |   0.650609 | 0.648896 |                  -0.0240868  |
|     11 | minmax          | svd         | none               | mlp_ann |   0.649914 | 0.646735 |                  -0.0247814  |
|     12 | robust          | svd         | none               | mlp_ann |   0.649218 | 0.648807 |                  -0.0254779  |

## Notes
- Discuss methods with highest F1 and accuracy gains over baseline (`none + none`).
- Explain failed/skipped patterns using `status` and `skip_reason`.
- Compare preprocessing/reduction/selection impacts by track.
