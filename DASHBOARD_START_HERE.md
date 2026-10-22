# Dashboard update: use your computed results

This update contains the dashboard code, not your locally generated CSV files.
Copy its files into your existing `retail-learning-stage-1` project root.
Keep your existing notebooks, docs, data, reports and app_data folder.

Required layout:

```text
retail-learning-stage-1/
    streamlit_app.py
    requirements-dashboard.txt
    app_data/
        history.csv
        future_forecasts.csv
        validation_metrics.csv
        test_metrics.csv
        test_predictions.csv
        quality_summary.csv
        metadata.json
    notebooks/
    data/
    reports/
    docs/
```

## Local launch in Windows VS Code

Open a Command Prompt terminal in the existing project root. Run separately:

```bat
.venv\Scripts\activate
python -m pip install -r requirements-dashboard.txt
python -m streamlit run streamlit_app.py
```

Open the Local URL shown by Streamlit. If 8501 is occupied, stop your previous
dashboard or use the new port displayed in the terminal.

## Roman Urdu checklist

1. ZIP extract karein. `streamlit_app.py`, `requirements-dashboard.txt` aur yeh guide apne existing project folder mein copy karein.
2. `app_data` wahi rehne dein jo aapne notebook se export kiya hai.
3. Commands run karke dashboard open karein.
4. S001/P0001 aur phir S001/P0002 select karein. Model aur forecasts change hone chahiye.
5. Data quality tab mein actual audit findings check karein.
6. Forecast and evaluation tab mein validation aur test charts dekhein.
7. S001/P0001 aur Validation-selected method select karke inventory 300, safety stock 50 enter karein. Expected requirement 712 units hai.
8. Inventory 2000 karke dobara calculate karein. Expected requirement zero hai.
9. Mean baseline view select karne par forecast cards, test metrics aur stock calculation sab Mean use karein.
10. Abhi GitHub update karne se pehle local dashboard verify karein. Report aur presentation baad mein in actual results se finalize hongi.

## What this dashboard does

- Five tabs: overview, audit, selected sales history, forecasts/evaluation, stock planner.
- Store and product dropdowns use available saved forecast pairs.
- All 100 pairs appear when all 100 pairs are included in your exported data.
- The original validation selection is preserved. A baseline view is an explicit comparison, not a retrospective change to model selection.
- Future forecasts refer to dataset-relative dates. They are not automatically forecasts for the current calendar week.
- Input changes calculate stock; they do not retrain models or generate new sales forecasts.
- The app does not upload retailer files, retrain models, place orders or use a managed cloud database.
- No model packages or API server are needed to display saved outputs.

## Dependencies

`requirements-dashboard.txt` contains only dashboard dependencies.
Keep the training notebook requirements separately, including statsmodels,
scikit-learn and xgboost. For deployment, the dashboard requirements can later
be copied into the repository's root requirements.txt after reviewing it.

## Documentation update

Append to docs/PROGRESS_LOG.md after your own verification:

```markdown
| Date | Work | Evidence | Next |
|---|---|---|---|
| [actual date] | Added multiple-series Streamlit dashboard | Store/product selection, audit, charts and stock calculation verified locally | GitHub and Streamlit deployment |
```

Append to docs/LEARNING_NOTES.md after verification:

```markdown
## Dashboard Architecture
Training and evaluation run in Jupyter notebooks. Prepared CSV files are
exported into app_data. Streamlit reads these saved results and provides
interactive selectors, charts, downloads and stock calculations.

The displayed forecasts are precomputed. Inventory inputs change only the
stock estimate. Model selections were based on validation, not test results.
The Mean baseline achieved lower average test error across the experiment.
```

## Validation boundary

The supplied update is checked against representative artificial CSV fixtures
matching your export schema. Your actual seven app_data files were generated
on your laptop and are not included here. Local verification with those files
and live deployment verification are still required.
