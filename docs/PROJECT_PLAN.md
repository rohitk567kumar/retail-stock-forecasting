# Project plan and completion checklist

Objective: forecast daily sales for a selected store-product pair, then estimate stock needed over the same horizon. Use clear beginner/intermediate Python with Markdown explanations in each notebook. Maintain an honest report of actual work.

| Stage | Deliverables and acceptance criteria | Status |
|---|---|---|
| 1. Dataset and provenance | Raw CSV, source, license, hash and field meanings | Complete in this package |
| 2. Audit and preprocessing | Missing/duplicate/invalid checks; gaps and business limitations; separate prepared CSV | Complete in this package |
| 3. EDA | Five labelled charts and explanations; all-store overview and selectable pair | Complete in this package |
| 4. Modelling notebook | Chronological split diagram/table, baselines, ARIMA, XGBoost, past-only features, beginner explanations | Pending guided stage |
| 5. Evaluation | Validation-based selection; held-out MAE/RMSE; rolling-origin checks on validation; per-pair results; honest limitations | Pending guided stage |
| 6. Stock notebook | Worked formula, same-horizon inputs, safety-stock and lead-time assumptions, meaningful checks | Pending guided stage |
| 7. Dashboard | Attractive readable layout; overview/audit/explore/forecast/stock tabs; store/product dropdowns; horizon selection within supported results; forecast dates and model metrics; downloads and input validation | Pending guided stage |
| 8. GitHub and Streamlit | Updated dependency files, deployment guide, no secrets or virtual environment committed; verify hosted selectors and calculations | Pending guided stage |
| 9. Final report | Problem, dataset, methodology, actual results, architecture, screenshots, limitations, citations and deployment evidence | Pending guided stage |
| 10. Presentation and Q&A | Attractive readable slides based on measured results; demo script; English slide text and Roman Urdu speaker explanations | Pending guided stage |

## Rules
- Prefer small readable cells and familiar pandas operations.
- Record only observed findings; no invented accuracy or deployment claims.
- Keep the target as Units Sold; explain that recorded sales may not equal unconstrained demand.
- Never train on later dates and test on earlier dates.
- Fit learned transformations on training data only.
- Keep a final test block untouched during model choice. Full-data teaching EDA is descriptive, not permission to tune on test outcomes.
- Multiple stores/products must have real computed results, not duplicated values.
- Decide live training versus precomputed forecasts using actual run cost; label the mode clearly in the UI.
- Forecasts start after the dataset end date, not automatically after today's date.
- Report Streamlit hosting as Streamlit hosting. AWS components remain a proposed alternative unless actually deployed.
- User reviews and runs each stage before the next guided stage.
