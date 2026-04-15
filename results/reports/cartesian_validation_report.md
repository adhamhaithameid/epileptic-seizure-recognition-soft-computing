# Cartesian Validation Report

- Timestamp (UTC): 2026-04-10T15:26:19.797989+00:00
- Expected combos: 1536
- Expected fold evals: 4608
- Metrics rows: 1200
- Completed ok: 1128
- Skipped or failed: 72
- Completed ok (%): 94.00%
- Figures found: 11
- Mode: partial allowed
- Runtime (sec): 1007.10
- Runtime (HH:MM:SS): 00:16:47
- Execution device: cpu
- Acceleration backend: none
- Checkpoint percent: 5
- Run label: notebook_local_local_medium_cpu
- Platform profile: local
- Started (UTC): 2026-04-10T15:08:44.498488+00:00
- Finished (UTC): 2026-04-10T15:25:31.616417+00:00
- Validation runtime (sec): 0.013

Validation result: PASS

## Top Skip Reasons
- selection_failed: ValueError: Found array with 1 feature(s) (shape=(700, 1)) while a minimum of 2 is required by SequentialFeatureSelector.: 36
- selection_failed: ValueError: Found array with 1 feature(s) (shape=(7666, 1)) while a minimum of 2 is required by RFE.: 24
- selection_failed: ValueError: Found array with 1 feature(s) (shape=(7667, 1)) while a minimum of 2 is required by RFE.: 12

## Notes
- Missing track coverage values: multiclass