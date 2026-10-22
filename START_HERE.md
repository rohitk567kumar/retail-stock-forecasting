# Retail forecasting: guided rebuild, Stage 1

Use this new folder alongside your existing project. Do not replace the live dashboard yet.

## Run on Windows in VS Code
1. Extract the ZIP and open the inner `retail-learning-stage-1` folder.
2. Open a Command Prompt terminal.
3. Run each command separately:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

4. Install/enable Microsoft's Python and Jupyter extensions in VS Code if needed.
5. Open `notebooks/01_dataset_preparation_and_eda.ipynb`.
6. Choose **Select Kernel → Python Environments → .venv**.
7. Run cells from top to bottom. The provided copy includes execution outputs for reference.
8. Read each Markdown explanation and `docs/STAGE_1_FINDINGS.md`.

Roman Urdu: Dataset ZIP mein mojood hai. Is stage mein model train nahi hoga. Pehle data aur charts ko samajhna hai. Cell 11 mein store/product badal kar charts dekhein.

## Maintained documentation
- `docs/PROJECT_PLAN.md`: every requested stage and its acceptance criteria.
- `docs/PROGRESS_LOG.md`: completed work, evidence and pending work.
- `docs/DECISION_LOG.md`: why each data/model decision was made.
- `docs/STAGE_1_FINDINGS.md`: generated quality findings.
- `docs/LEARNING_NOTES.md`: your own explanations and questions.
- `docs/dataset_source.json`: provenance, license and original hash.

The prepared CSV, audit tables and five PNG charts are included. Rerunning the notebook regenerates them. The raw file remains unchanged. Model results from the old package are not presented as newly trained results here.
