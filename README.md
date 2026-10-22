# Cloud-Based Retail Stock Requirement Forecasting System

A university Cloud Computing project that forecasts daily retail
sales and estimates additional stock requirements through a
Streamlit dashboard.

The project uses synthetic demonstration data. Its effectiveness
for real retail operations has not been established.

## Project Objective

For a selected store-product code, the system:

1. Displays historical sales and data-quality findings.
2. Compares forecasting methods using chronological validation.
3. Evaluates the selected method on a later test period.
4. Displays seven-day sales forecasts.
5. Calculates additional stock from forecast sales, available
   inventory and an assumed safety stock.

## Dataset

- 73,100 records and 15 original columns.
- 5 stores and 20 product codes.
- 100 store-product combinations.
- 731 daily observations per combination.
- Recorded period: 1 January 2022 to 1 January 2024.

Source:
[Retail Store Inventory Forecasting Dataset](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset)

The publisher identifies the dataset as synthetic practice data.

## Data Preparation

The preparation notebook:

- Checks missing values and exact duplicates.
- Validates essential dates and numeric values.
- Checks conflicting store-product-date records.
- Checks missing dates within each series.
- Examines category and region consistency.
- Sorts daily histories and saves a prepared copy.
- Preserves the original dataset.

No missing values, exact duplicates or missing daily dates were
found. Category and region inconsistencies were documented
without inventing corrections.

The publisher-supplied Demand Forecast column was excluded from
model inputs because its generation process and future availability
were not verified.

## Forecasting Methods

- Naive
- Mean
- Seasonal Naive
- ARIMA(1,1,1)
- XGBoost

XGBoost uses historical sales lags, a shifted rolling average
and weekday features. Multi-day forecasts are generated recursively
without using unknown future actual sales.

## Evaluation Procedure

Each combination uses:

| Dataset | Period | Days |
|---|---|---:|
| Training | 2022-01-01 to 2023-11-06 | 675 |
| Validation | 2023-11-07 to 2023-12-04 | 28 |
| Test | 2023-12-05 to 2024-01-01 | 28 |

Validation and testing use four weekly seven-day forecasts.
Previously completed weeks become available history at subsequent
forecast origins.

Model selection uses validation MAE, with RMSE and model name
as tie-breakers. Test results do not change the selected methods.

## Results Across 100 Combinations

### Validation-Selected Methods

| Method | Combinations |
|---|---:|
| Mean | 41 |
| ARIMA | 28 |
| XGBoost | 23 |
| Naive | 7 |
| Seasonal Naive | 1 |

### Overall Test Comparison

| Approach | Average Per-Series MAE | Average Per-Series RMSE |
|---|---:|---:|
| Validation-selected methods | 89.80 | 108.53 |
| Mean baseline | 86.52 | 104.29 |

Selected methods had lower test MAE in 19 combinations.
Mean had lower MAE in 40 combinations.
The remaining 41 combinations selected Mean and tied.

The model-selection procedure did not outperform the Mean
baseline overall in this experiment.

These are forecasting errors measured in units sold,
not accuracy percentages.

## Future Forecasts

The saved forecasts cover 2–8 January 2024, immediately after
the dataset's last recorded date.

There are 700 daily forecasts covering 100 combinations.

These are not forecasts for the current calendar week.
Actual sales for the forecast dates are unavailable in the dataset,
so errors for those dates cannot yet be calculated.

## Stock Requirement

The simplified calculation is:

Additional stock =
ceil(max(0, total forecast sales + safety stock - available inventory))

Example for S001/P0001 using ARIMA:

- Seven-day forecast: approximately 961.73 units.
- Assumed available inventory: 300 units.
- Assumed safety stock: 50 units.
- Additional requirement: 712 units.

Inventory must refer to stock available at the forecast origin.
Historical beginning-of-day inventory is not automatically used
as current stock.

The calculation excludes incoming orders, supplier lead times,
storage capacity and ordering costs. It does not place orders.

## Dashboard Features

- Store and product selectors.
- Dataset overview and audit findings.
- Historical sales charts.
- Validation model comparison.
- Actual versus predicted test sales.
- Future forecasts for selected methods and the Mean baseline.
- Interactive stock calculator.
- CSV downloads.

Training and evaluation run in Jupyter notebooks.
The dashboard reads precomputed CSV outputs from app_data.
Changing inventory updates the stock calculation, not the forecast.

## Project Structure

```text
retail-learning-stage-1/
├── streamlit_app.py
├── requirements.txt
├── requirements-training.txt
├── requirements-dashboard.txt
├── app_data/
├── notebooks/
├── data/
├── reports/
└── docs/
