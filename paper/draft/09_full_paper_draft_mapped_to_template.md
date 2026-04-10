# Project Title
Epileptic Seizure Recognition with a Full Cartesian Soft Computing Benchmark

## Authors
- Student Name: [Fill Your Name]
- Course: Soft Computing (CSC425)
- Instructor: Dr. Ahmed Anter
- Semester: Spring 2026

## Abstract
Epileptic seizure recognition from electroencephalogram (EEG) signals remains a clinically important yet technically difficult task because EEG recordings are noisy, nonstationary, high dimensional, and strongly variable across subjects, sessions, and recording setups. Many published studies report high detection or classification performance, but fair comparison is often limited by inconsistent preprocessing choices, heterogeneous feature pipelines, different evaluation protocols, and incomplete reporting of failure cases. This project addresses that gap by developing a reproducible, end to end soft computing benchmark that evaluates preprocessing, feature reduction, feature selection, and classification under one deterministic Cartesian experiment design. The framework uses standardized paths, schema-controlled outputs, checkpointed execution, and paper-ready reporting assets.

Two prediction tracks are evaluated: binary seizure recognition and multiclass seizure state classification. The benchmark enumerates four preprocessing methods, four reduction options, eight feature selection strategies, and six classifiers under three fold stratified cross validation. This results in 1,536 unique method combinations and 4,608 fold level evaluations. The workflow includes explicit guardrails for mathematically invalid combinations, including dynamic parameter clamping, nonnegative transformation support for chi square feature selection, and robust skip logging with status and skip reason fields. Instead of terminating the run at the first invalid stage, the engine records structured failure rows and continues, preserving total accounting and enabling transparent post hoc analysis of error modes.

In the validated full run on Apple Silicon M1, all 4,608 fold evaluations were executed and recorded, with 4,392 successful evaluations and 216 safely skipped or failed evaluations linked to documented low dimensional feature selection edge cases. The strongest binary pipeline combined quantile preprocessing, principal component analysis, no additional feature selection, and a support vector machine, achieving accuracy 0.976261, F1 score 0.939349, and ROC AUC 0.995438. The strongest multiclass pipeline combined minmax scaling, principal component analysis, no additional selection, and a multilayer perceptron, achieving accuracy 0.685651 and F1 score 0.685026.

Beyond model scores, the project contributes a reproducible benchmarking template for course and research experimentation. Outputs include fold level metrics, run manifests, ranking tables for binary and multiclass tracks, baseline deltas, comparison reports, and visualization suites including heatmaps, top N performance charts, fold variance analysis, and binary ROC curves. The resulting pipeline supports transparent method comparison, reproducible experimentation, and direct integration into research paper drafting for students. It also provides a practical foundation for future work in hyperparameter optimization, statistical significance testing, cross dataset generalization, and deployment aware evaluation for real time seizure monitoring systems.

From an implementation perspective, the benchmark supports resumable execution, deterministic iteration order, and schema validation checks that confirm expected combination coverage and metric completeness. This design minimizes silent errors and makes long runs feasible on commodity laptops and cloud notebooks. The project therefore balances algorithmic breadth with engineering rigor: every evaluated configuration is traceable, every skip is explainable, and every aggregate result can be regenerated from raw fold outputs. As a result, the study offers both strong empirical baselines and a reusable workflow for future soft computing coursework and thesis level research.

## Keywords
Soft Computing, Epileptic Seizure Recognition, Cartesian Benchmark, Feature Reduction, Feature Selection, Genetic Algorithm, Classification

## 1. Introduction
Epileptic seizure recognition is a high-impact classification problem in biomedical signal processing, where robust automation can support neurologists in early and reliable decision-making. Although many studies report strong results on seizure datasets, practical reproducibility remains difficult because pipelines vary widely in preprocessing, feature engineering, model selection, and evaluation protocol [R1]-[R8]. This makes direct method-to-method comparison less transparent and often non-repeatable.

Foundational EEG benchmark studies and patient-specific seizure-detection works [R9], [R10] have motivated a large body of classical and modern machine-learning approaches. However, course projects still face a recurring gap: moving from isolated model experiments to a complete and auditable comparative framework that can test multiple soft-computing stages under a single protocol.

To address this gap, this project introduces a fully refactored Cartesian benchmark framework for the Epileptic Seizure Recognition dataset. The main contributions are:
1. A deterministic staged evaluation engine covering preprocessing, reduction, selection, and classification families in one run (`1536` unique pipelines, `4608` fold evaluations).
2. A dual-track protocol (binary and multiclass) with standardized metrics, timing statistics, and reproducible output schemas.
3. Robust execution logic with safe handling of mathematically invalid combinations through skip-reason logging instead of pipeline termination.
4. End-to-end reporting artifacts (rankings, deltas, plots, and draft sections) that map directly to research-paper writing requirements.

This structure enables fairer comparison between techniques and provides a practical template for reproducible soft-computing experimentation.

Paper organization: Section 2 summarizes related work, Section 3 details methodology, Section 4 describes the staged model design, Section 5 reports preprocessing/reduction/selection/classification results with statistical tests and confusion-matrix analysis, and Section 6 concludes with future directions.

## 2. Related Work
Recent seizure-detection studies span classical machine learning, hybrid feature engineering, and deep-learning-assisted classifiers. Reported performance is often high on Bonn EEG and CHB-MIT variants, but direct comparison remains difficult because preprocessing, feature pipelines, and validation protocols vary across papers.

| Ref No. | Paper | Year | Methods | Reported Results |
|:--:|:--|:--:|:--|:--|
| [R1] | Siddiqui et al., *Brain Informatics* | 2020 | Review of ML classifiers for seizure detection | Summarized classifier trends and highlighted EEG noise/non-stationarity challenges. |
| [R2] | Liu et al., *Technology and Health Care* | 2017 | Temporal + wavelet features + kernel ELM | Reported satisfactory accuracy with lower computation time. |
| [R3] | Chen et al., *BMC Med Inform Decis Mak* | 2023 | DWT + entropy/STD feature fusion + RF feature selection + CNN | Bonn interictal/ictal: 99.9% accuracy; New Delhi interictal/ictal: 100% in their setup. |
| [R4] | Khalid et al., *DIGITAL HEALTH* | 2024 | ICA + prediction-probability features (FIR) + SVM | Reported 98.4% accuracy. |
| [R5] | Saranya & Bharathi, *JIFS* | 2024 | Hybrid IANFIS-LightGBM | Reported strongest classification performance among compared methods on Bonn and CHB-MIT records. |
| [R6] | Atlam et al., *Applied Sciences* | 2025 | PCA + DWT hybrid feature selection + SMOTE + SVM | Reported 97.30% accuracy, 99.62% AUC, 93.08% F1. |
| [R7] | Berrich & Guennoun, *Scientific Reports* | 2025 | PCA-based dimensionality reduction + CNN-SVM/DNN-SVM | Proposed hybrid deep+SVM EEG detection framework with dimensionality reduction. |
| [R8] | Chakrabarti et al., *JAISE* | 2022 | Moving-window pediatric seizure recognition with RF/DT/ANN/ensemble | RF best: 91.9% accuracy, 94.1% sensitivity, 89.7% specificity. |
| [R9] | Andrzejak et al., *Physical Review E* | 2001 | Nonlinear dynamics analysis of EEG brain states | Foundational EEG-state analysis used in building the widely used Bonn benchmark structure. |
| [R10] | Shoeb et al., *IEEE EMBC* | 2004 | Patient-specific seizure onset detection from EEG | Early influential patient-specific onset-detection framework. |

## 3. Methodology
### 3.1 Dataset
- Dataset: Epileptic Seizure Recognition
- Samples: 11,500
- Features: 178 numeric predictors
- Targets:
  - Binary track: class 1 vs classes 2-5
  - Multiclass track: original five classes

### 3.2 Preprocessing
- `standard`
- `minmax`
- `robust`
- `quantile`

### 3.3 Feature Reduction
- `none`
- `pca`
- `lda_projection`
- `svd`

### 3.4 Feature Selection
- `none`
- `filter_chi2`
- `filter_anova`
- `filter_correlation`
- `wrapper_sfs`
- `wrapper_rfe`
- `embedded_l1`
- `ga_selection`

### 3.5 Classifiers
- `knn`
- `svm`
- `decision_tree`
- `logistic_regression`
- `lda_classifier`
- `mlp_ann`

### 3.6 Evaluation Protocol
- 3-fold stratified CV (primary Cartesian protocol)
- Additional 80/20 train-test holdout (secondary protocol for confusion-matrix comparison)
- Metrics: accuracy, precision, recall, f1, roc_auc (binary), error_rate
- Runtime metrics: fit and prediction time
- Confusion matrix terms recorded for holdout comparison: TN, FP, FN, TP
- Failure handling: logged per fold with `status` and `skip_reason`

## 4. Proposed Model
The project uses a deterministic staged Cartesian engine:
1. Load and clean data.
2. For each track and fold, apply each preprocessing method.
3. Apply each reduction method.
4. Apply each selection method.
5. Train/evaluate each classifier.
6. Save fold-level metrics and status rows.
7. Aggregate rankings, baseline deltas, and plots.

Combination math:
- Unique combos = `4 x 4 x 8 x 6 x 2 = 1536`
- Fold evaluations = `1536 x 3 = 4608`

## 5. Results and Discussion
### 5.1 Data Set Description
The Epileptic Seizure Recognition dataset contains `11,500` samples and `178` numeric predictor features. The target has five classes in its original form, and this study uses two tracks: (1) binary seizure vs non-seizure and (2) multiclass seizure-state recognition. Data cleaning was applied by coercing non-numeric values to numeric and imputing missing feature values with median values per feature.

### 5.2 Required Result Files
- `results/metrics/cartesian_metrics_all.csv`
- `results/metrics/cartesian_run_manifest.json`
- `results/tables/cartesian_summary_by_combo.csv`
- `results/tables/cartesian_rankings_binary.csv`
- `results/tables/cartesian_rankings_multiclass.csv`
- `results/reports/cartesian_comparison_report.md`
- `results/tables/dataset_descriptive_stats.csv`
- `results/tables/covariance_matrix.csv`
- `results/tables/correlation_matrix.csv`
- `results/tables/statistical_tests_summary.csv`
- `results/tables/holdout_80_20_binary_classifier_comparison.csv`
- `results/tables/holdout_overfit_analysis.csv`

### 5.3 Preprocessing Phase Results
#### 5.3.1 Data Visualization, Missing Values, and Binning
- Data visualization was performed through the correlation heat map (`results/figures/correlation_heatmap.png`) and stage-level benchmark plots in `results/figures/cartesian_*.png`.
- Missing values were handled by median imputation after numeric coercion; no residual missing values remained for model input.
- A binning process was used for chi-square statistical testing by applying quantile-based bins (quintiles) on selected high-variance features.

#### 5.3.2 Descriptive Statistics and Matrix Analysis
Descriptive statistics (min, max, mean, variance, standard deviation, skewness, kurtosis) were computed for all `178` features and stored in `results/tables/dataset_descriptive_stats.csv`.
Examples:
- `X1`: min `-1839`, max `1726`, mean `-11.58`, variance `27432.07`, std `165.63`, skewness `-0.454`, kurtosis `19.07`.
- `X2`: min `-1838`, max `1713`, mean `-10.91`, variance `27575.79`, std `166.06`, skewness `-0.432`, kurtosis `18.30`.

Covariance and correlation matrices were generated (`results/tables/covariance_matrix.csv`, `results/tables/correlation_matrix.csv`) and visualized with a heat map. These analyses confirmed strong inter-feature dependency patterns, motivating dimensionality reduction and feature selection phases.

#### 5.3.3 Statistical Tests (Chi-square, t-test, ANOVA)
From `results/tables/statistical_tests_summary.csv`, three high-variance features were analyzed:
- `X101`: t-test p-value `0.5557`, ANOVA p-value `0.2358`, chi-square p-value `< 1e-10`.
- `X48`: t-test p-value `0.8377`, ANOVA p-value `0.7444`, chi-square p-value `< 1e-10`.
- `X102`: t-test p-value `0.2781`, ANOVA p-value `0.0906`, chi-square p-value `< 1e-10`.

Interpretation: linear mean-difference tests (t-test/ANOVA) were weak for these specific features, while chi-square on binned distributions detected strong class-related distribution shifts.

### 5.4 Feature Reduction and Feature Selection Results
The Cartesian results show that dimensionality-reduction impact differs by track:
- Binary track mean accuracy by reduction: `none (0.8973)`, `pca (0.8964)`, `svd (0.8934)`, `lda_projection (0.8384)`.
- Multiclass track mean accuracy by reduction: `pca (0.4337)`, `svd (0.4210)`, `none (0.3995)`, `lda_projection (0.3095)`.

Interpretation:
- PCA and SVD improved multiclass general behavior versus no reduction.
- LDA projection was the weakest reduction in both tracks for this dataset under the tested classifier mix.
- Feature-selection behavior was mixed: wrapper methods were strong on binary means, while `none`/filter methods remained competitive on multiclass means.

### 5.5 Full Run Snapshot (April 9, 2026, M1 CPU)
- Total fold evaluations: `4608 / 4608`
- Successful rows: `4392`
- Skipped/failed rows: `216`
- Runtime: `5294.26 sec` (`88.24 min`)
- Execution device: `cpu`
- Acceleration backend: `none` (no GPU acceleration in this validated run)

Best pipelines from `cartesian_run_manifest.json`:
- Binary: `svm + quantile + pca + none`  
  `accuracy=0.976261`, `precision=0.960050`, `recall=0.919563`, `f1=0.939349`, `roc_auc=0.995438`
- Multiclass: `mlp_ann + minmax + pca + none`  
  `accuracy=0.685651`, `precision=0.685624`, `recall=0.685660`, `f1=0.685026`

### 5.6 Top-Ranked Pipelines (Cartesian Accuracy)
Binary track (top 5):

| Rank | Preprocessing | Reduction | Selection | Model | Accuracy | F1 | Delta vs baseline accuracy |
|:---:|:---|:---|:---|:---|---:|---:|---:|
| 1 | quantile | pca | none | svm | 0.976261 | 0.939349 | +0.000261 |
| 2 | quantile | none | none | svm | 0.976000 | 0.938647 | +0.000000 |
| 3 | quantile | svd | none | svm | 0.974608 | 0.934881 | -0.001391 |
| 4 | quantile | none | embedded_l1 | svm | 0.973565 | 0.932277 | -0.002435 |
| 5 | standard | svd | none | svm | 0.971913 | 0.927855 | -0.004087 |

Multiclass track (top 5):

| Rank | Preprocessing | Reduction | Selection | Model | Accuracy | F1 | Delta vs baseline accuracy |
|:---:|:---|:---|:---|:---|---:|---:|---:|
| 1 | minmax | pca | none | mlp_ann | 0.685651 | 0.685026 | +0.010956 |
| 2 | standard | none | none | mlp_ann | 0.674696 | 0.675497 | +0.000000 |
| 3 | standard | svd | none | mlp_ann | 0.671305 | 0.671783 | -0.003390 |
| 4 | standard | pca | none | mlp_ann | 0.670869 | 0.671112 | -0.003826 |
| 5 | robust | none | none | mlp_ann | 0.669740 | 0.670368 | -0.004956 |

### 5.7 80/20 Holdout Split Results and Confusion Matrix Comparison
In addition to K-fold results, an explicit `80% train / 20% test` binary experiment was executed (`results/tables/holdout_80_20_binary_classifier_comparison.csv`).

| Model | Accuracy | Error Rate | Precision | Recall | F1 | ROC AUC | TN | FP | FN | TP |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| mlp_ann | 0.9743 | 0.0257 | 0.9546 | 0.9152 | 0.9345 | 0.9887 | 1820 | 20 | 39 | 421 |
| svm | 0.9709 | 0.0291 | 0.9538 | 0.8978 | 0.9250 | 0.9965 | 1820 | 20 | 47 | 413 |
| decision_tree | 0.9422 | 0.0578 | 0.8978 | 0.8022 | 0.8473 | 0.8592 | 1798 | 42 | 91 | 369 |
| knn | 0.9317 | 0.0683 | 0.9935 | 0.6630 | 0.7953 | 0.9218 | 1838 | 2 | 155 | 305 |
| lda_classifier | 0.8213 | 0.1787 | 0.9298 | 0.1152 | 0.2050 | 0.4979 | 1836 | 4 | 407 | 53 |
| logistic_regression | 0.8157 | 0.1843 | 0.9500 | 0.0826 | 0.1520 | 0.4997 | 1838 | 2 | 422 | 38 |

This table provides confusion-matrix components and requested metrics (accuracy, error rate, precision, recall, F-measure, ROC) for each classifier.

### 5.8 Overfitting and Underfitting Interpretation
From `results/tables/holdout_overfit_analysis.csv`, generalization gaps (train accuracy minus test accuracy) were:
- Decision Tree: `0.0410` (moderate overfitting tendency).
- MLP: `0.0257` (mild overfitting).
- SVM, KNN, Logistic Regression, and LDA classifier: mild gaps.

Underfitting signals were visible for Logistic Regression and LDA classifier because both train and test accuracies stayed low relative to SVM/MLP, suggesting limited model capacity for this feature space under default hyperparameters.

### 5.9 Failure and Skip Analysis
All `216` non-OK rows were safe failures in feature selection edge cases:
- `72`: SequentialFeatureSelector requires at least 2 features (`shape=(700, 1)` after prior stages).
- `72`: `n_features_to_select` must be strictly less than available features.
- `48`: RFE requires at least 2 features (`shape=(7667, 1)`).
- `24`: RFE requires at least 2 features (`shape=(7666, 1)`).

This pattern indicates the failure handling behaved as intended: invalid low-dimensional combinations were logged and skipped without stopping the full benchmark.

### 5.10 Discussion
- Binary performance was dominated by SVM and MLP variants, with strong precision-recall balance in both Cartesian and holdout analyses.
- Multiclass performance was strongest with MLP under `minmax + pca`, supporting the value of reduction before multiclass classification.
- Wrapper/embedded selectors were useful in specific binary settings but did not universally dominate multiclass outcomes.
- The added holdout and confusion-matrix analyses provide a more complete practical view than a single aggregate accuracy score.


## 6. Conclusion and Future Work
This project delivers a complete and reproducible soft-computing benchmark for epileptic seizure recognition, unifying all requested method families in a single Cartesian framework. The final run achieved full accounting (`4608/4608` fold evaluations), with safe continuation despite invalid edge-case combinations (`216` skip/failed rows logged with explicit reasons). This demonstrates both methodological coverage and execution robustness.

Empirically, binary performance was strongest with SVM-based pipelines, while multiclass performance was strongest with MLP/ANN-based pipelines under `minmax + pca`. These outcomes suggest that, for this dataset, preprocessing and reduction choices contributed more consistently to top-ranked performance than aggressive wrapper/embedded selection in most high-performing combinations.

Future work:
1. Perform targeted hyperparameter optimization on the best-performing pipeline families per track.
2. Add statistical significance testing (for example, paired tests across folds) for top-ranked methods.
3. Extend benchmarking to additional course datasets to evaluate cross-dataset generalization.
4. Add deployment-oriented profiling (latency/memory) for real-time or edge inference scenarios.

## 7. References
[R1] Siddiqui, M. K., Morales-Menendez, R., Huang, X., & Hussain, N. (2020). A review of epileptic seizure detection using machine learning classifiers. *Brain Informatics, 7*(1), 5. https://doi.org/10.1186/s40708-020-00105-1

[R2] Liu, Q., Zhao, X., Hou, Z., & Liu, H. (2017). Epileptic seizure detection based on the kernel extreme learning machine. *Technology and Health Care, 25*(1_suppl), 399-409. https://doi.org/10.3233/THC-171343

[R3] Chen, W., Wang, Y., Ren, Y., Jiang, H., Du, G., Zhang, J., & Li, J. (2023). An automated detection of epileptic seizures EEG using CNN classifier based on feature fusion with high accuracy. *BMC Medical Informatics and Decision Making, 23*(1), 96. https://doi.org/10.1186/s12911-023-02180-w

[R4] Khalid, M., Raza, A., Akhtar, A., Rustam, F., Ballester, J. B., Rodriguez, C. L., Díez, I. D. L. T., & Ashraf, I. (2024). Diagnosing epileptic seizures using combined features from independent components and prediction probability from EEG data. *DIGITAL HEALTH, 10*, 20552076241277185. https://doi.org/10.1177/20552076241277185

[R5] Saranya, D., & Bharathi, A. (2024). Automatic detection of epileptic seizure using machine learning-based IANFIS-LightGBM system. *Journal of Intelligent & Fuzzy Systems, 46*(1), 2463-2482. https://doi.org/10.3233/JIFS-233430

[R6] Atlam, H. F., Aderibigbe, G. E., & Nadeem, M. S. (2025). Effective Epileptic Seizure Detection with Hybrid Feature Selection and SMOTE-Based Data Balancing Using SVM Classifier. *Applied Sciences, 15*(9), 4690. https://doi.org/10.3390/app15094690

[R7] Berrich, Y., & Guennoun, Z. (2025). EEG-based epilepsy detection using CNN-SVM and DNN-SVM with feature dimensionality reduction by PCA. *Scientific Reports, 15*(1), 14313. https://doi.org/10.1038/s41598-025-95831-z

[R8] Chakrabarti, S., Swetapadma, A., & Pattnaik, P. K. (2022). An improved method for recognizing pediatric epileptic seizures based on advanced learning and moving window technique. *Journal of Ambient Intelligence and Smart Environments, 14*(1), 39-59. https://doi.org/10.3233/AIS-210042

[R9] Andrzejak, R. G., Lehnertz, K., Mormann, F., Rieke, C., David, P., & Elger, C. E. (2001). Indications of nonlinear deterministic and finite-dimensional structures in time series of brain electrical activity: Dependence on recording region and brain state. *Physical Review E, 64*(6), 061907. https://doi.org/10.1103/PhysRevE.64.061907

[R10] Shoeb, A., Edwards, H., Connolly, J., Bourgeois, B., Treves, T., & Guttag, J. (2004). Patient-specific seizure onset detection. *The 26th Annual International Conference of the IEEE Engineering in Medicine and Biology Society, 3*, 419-422. https://doi.org/10.1109/IEMBS.2004.1403183

[R11] Kode, H., Elleithy, K., & Almazaydeh, L. (2024). Epileptic Seizure Detection in EEG Signals Using Machine Learning and Deep Learning Techniques. *IEEE Access, 12*, 80657-80668. https://doi.org/10.1109/access.2024.3409581

[R12] Zhao, X., Yoshida, N., Ueda, T., Sugano, H., & Tanaka, T. (2023). Epileptic seizure detection by using interpretable machine learning models. *Journal of Neural Engineering, 20*(1), 015002. https://doi.org/10.1088/1741-2552/acb089

[R13] Qureshi, M. M., & Kaleem, M. (2023). EEG-based seizure prediction with machine learning. *Signal, Image and Video Processing, 17*(4), 1543-1554. https://doi.org/10.1007/s11760-022-02363-4

[R14] Jemal, I., Abou-Abbas, L., Henni, K., Mitiche, A., & Mezghani, N. (2024). Domain adaptation for EEG-based, cross-subject epileptic seizure prediction. *Frontiers in Neuroinformatics, 18*, 1303380. https://doi.org/10.3389/fninf.2024.1303380

[R15] Pontes, E. D., Pinto, M., Lopes, F., & Teixeira, C. (2024). Concept-drifts adaptation for machine learning EEG epilepsy seizure prediction. *Scientific Reports, 14*(1), 8204. https://doi.org/10.1038/s41598-024-57744-1

[R16] Sigsgaard, G. M., & Gu, Y. (2024). Comparison of patient non-specific seizure detection using multi-modal signals. *Neuroscience Informatics, 4*(1), 100152. https://doi.org/10.1016/j.neuri.2023.100152

[R17] Rukhsar, S., & Tiwari, A. K. (2023). Lightweight convolution transformer for cross-patient seizure detection in multi-channel EEG signals. *Computer Methods and Programs in Biomedicine, 242*, 107856. https://doi.org/10.1016/j.cmpb.2023.107856

[R18] Zhang, Y., Xiao, T., Wang, Z., Lv, H., Wang, S., Feng, H., Zhao, S., & Zhao, Y. (2023). Hybrid Network for Patient-Specific Seizure Prediction from EEG Data. *International Journal of Neural Systems, 33*(11), 2350056. https://doi.org/10.1142/s0129065723500569

[R19] Li, C., Deng, Z., Song, R., Liu, X., Qian, R., & Chen, X. (2023). EEG-Based Seizure Prediction via Model Uncertainty Learning. *IEEE Transactions on Neural Systems and Rehabilitation Engineering, 31*, 180-191. https://doi.org/10.1109/TNSRE.2022.3217929

[R20] Mao, T., Li, C., Zhao, Y., Song, R., & Chen, X. (2023). EEG-Based Seizure Prediction Via GhostNet and Imbalanced Learning. *IEEE Sensors Letters, 7*(12), 1-4. https://doi.org/10.1109/LSENS.2023.3330327

[R21] Pan, Y., Dong, F., Wu, J., & Xu, Y. (2023). Downsampling of EEG Signals for Deep Learning-Based Epilepsy Detection. *IEEE Sensors Letters, 7*(12), 1-4. https://doi.org/10.1109/LSENS.2023.3332392

[R22] Deng, Z., Li, C., Song, R., Liu, X., Qian, R., & Chen, X. (2024). Centroid-Guided Domain Incremental Learning for EEG-Based Seizure Prediction. *IEEE Transactions on Instrumentation and Measurement, 73*, 1-13. https://doi.org/10.1109/TIM.2023.3334330

[R23] Zhang, Z., Ji, T., Xiao, M., Wang, W., Yu, G., Lin, T., Jiang, Y., Zhou, X., & Lin, Z. (2024). Cross-patient automatic epileptic seizure detection using patient-adversarial neural networks with spatio-temporal EEG augmentation. *Biomedical Signal Processing and Control, 89*, 105664. https://doi.org/10.1016/j.bspc.2023.105664

[R24] Ji, D., He, L., Dong, X., Li, H., Zhong, X., Liu, G., & Zhou, W. (2024). Epileptic Seizure Prediction Using Spatiotemporal Feature Fusion on EEG. *International Journal of Neural Systems, 34*(08), 2450041. https://doi.org/10.1142/s0129065724500412

[R25] Liu, Y., Xu, C., Wen, Z., & Dong, Y. (2025). Trust EEG epileptic seizure detection via evidential multi-view learning. *Information Sciences, 694*, 121699. https://doi.org/10.1016/j.ins.2024.121699

[R26] Dokare, I., & Gupta, S. (2025). Optimized seizure detection leveraging band-specific insights from limited EEG channels. *Health Information Science and Systems, 13*(1), 30. https://doi.org/10.1007/s13755-025-00348-4

[R27] Kunekar, P., Gupta, M. K., & Gaur, P. (2024). Detection of epileptic seizure in EEG signals using machine learning and deep learning techniques. *Journal of Engineering and Applied Science, 71*(1), 21. https://doi.org/10.1186/s44147-023-00353-y

[R28] Lemoine, É., Toffa, D., Xu, A. Q., Tessier, J. D., Jemel, M., Lesage, F., Nguyen, D. K., & Bou Assi, E. (2025). Improving diagnostic accuracy of routine EEG for epilepsy using deep learning. *Brain Communications, 7*(5), fcaf319. https://doi.org/10.1093/braincomms/fcaf319

[R29] Deng, Z., Li, C., Zhao, G., & Chen, X. (2025). Incremental Learning for Patient-Specific EEG-Based Seizure Detection. *IEEE Transactions on Neural Systems and Rehabilitation Engineering, 33*, 4512-4522. https://doi.org/10.1109/TNSRE.2025.3628907

[R30] Zhao, Y., Liu, A., Li, C., Wang, L., Qian, R., & Chen, X. (2026). Generalizable Seizure Prediction With LLMs: Converting EEG to Textual Representations. *IEEE Journal of Biomedical and Health Informatics, 30*(3), 2589-2602. https://doi.org/10.1109/JBHI.2025.3593337

[R31] Jang, D., Jung, K. Y., Jeon, Y. G., Kim, T. J., Lee, S. K., & Min, K. Y. (2026). Single-channel EEG-based seizure prediction using deep learning. *Scientific Reports*. https://doi.org/10.1038/s41598-026-44670-7

[R32] Darankoum, D., Villalba, M., Allioux, C., Caraballo, B., Dumont, C., Gronlier, E., Roucard, C., Roche, Y., Habermacher, C., Grudinin, S., & Volle, J. (2026). From epilepsy seizure classification to detection: A deep learning-based approach for raw EEG signals. *Neuroscience Informatics, 6*(1), 100263. https://doi.org/10.1016/j.neuri.2026.100263

[R33] Naghipour, J., Ghazizadeh, R., & Hadi, M. (2026). GAN-based deep learning strategy for advanced EEG focal and non-focal classification in epilepsy. *Signal, Image and Video Processing, 20*(3), 106. https://doi.org/10.1007/s11760-026-05155-2

[R34] Lin, Y., Dong, L., Jiang, Y., & Lian, J. (2025). Epileptic EEG classification via deep learning-based strange attractor. *Biomedical Signal Processing and Control, 100*, 106965. https://doi.org/10.1016/j.bspc.2024.106965

[R35] Dong, C., Sun, D., Zhang, Z., & Luo, B. (2025). EEG-based patient-specific seizure prediction based on Spatial–Temporal Hypergraph Attention Transformer. *Biomedical Signal Processing and Control, 100*, 107075. https://doi.org/10.1016/j.bspc.2024.107075

[R36] Wang, Z., Song, X., Chen, L., Nan, J., Sun, Y., Pang, M., Zhang, K., Liu, X., & Ming, D. (2024). Research progress of epileptic seizure prediction methods based on EEG. *Cognitive Neurodynamics, 18*(5), 2731-2750. https://doi.org/10.1007/s11571-024-10109-w

[R37] Poorani, S., & Balasubramanie, P. (2023). Deep learning based epileptic seizure detection with EEG data. *International Journal of System Assurance Engineering and Management*. https://doi.org/10.1007/s13198-022-01845-5

[R38] Diao, Y., Fang, J., Ding, Y., Zhao, Y., Meng, H., & Xu, Y. (2025). Temporal-Focal Attention on EEG for Cross-Patient Epileptic Seizure Detection. *2025 IEEE 22nd International Symposium on Biomedical Imaging (ISBI)*, 1-4. https://doi.org/10.1109/ISBI60581.2025.10980801

[R39] Shoeb, A., Kharbouch, A., Soegaard, J., Schachter, S., & Guttag, J. (2011). An algorithm for detecting seizure termination in scalp EEG. *2011 Annual International Conference of the IEEE Engineering in Medicine and Biology Society*, 1443-1446. https://doi.org/10.1109/IEMBS.2011.6090357

[R40] Shao, C., Li, C., Song, R., Xu, G., & Chen, X. (2025). Feature Unlearning for EEG-Based Seizure Prediction. *IEEE Internet of Things Journal, 12*(8), 10974-10986. https://doi.org/10.1109/JIOT.2024.3514666
