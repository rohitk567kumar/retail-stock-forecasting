# Decision log

| Decision | Reason |
|---|---|
| Keep raw CSV unchanged | Reproducibility and recovery |
| Use full dataset for audit | A single-pair demo hid the available combinations |
| Preserve synthetic inconsistencies and document them | No verified correction can be inferred |
| Stop on essential invalid values/conflicting keys | Silent fixes can change the meaning of data |
| No automatic outlier deletion | High sales may be valid observations |
| No categorical encoding or scaling yet | The chosen forecasting model determines these needs |
| Exclude publisher Demand Forecast from model inputs | Its provenance and future availability are not verified |
| Keep free hosting and training mode explicit | Saved outputs and live inference must be distinguishable |
| Deliver in guided stages | User must understand the notebook and explain the project |
