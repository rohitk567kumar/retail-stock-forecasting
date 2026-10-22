# My Learning Notes

## 1. Project Objective

Develop a cloud-hosted prototype that forecasts daily sales and
estimates additional stock requirements for a selected store-product code.

The forecasting workflow can be reused for other retailers, but models
must be trained and evaluated using their own suitable historical data.
Training alone does not guarantee reliable forecasts.

## 2. Prediction Target

The prediction target is Units Sold per day.

We will forecast the next seven days after the last recorded date.
We will then calculate additional stock using the forecast total,
available inventory and an assumed safety stock.

Changing inventory affects the stock calculation, not the sales forecast.

## 3. Dataset and Audit Findings

- The dataset contains 73,100 rows and 15 columns.
- There are 5 stores and 20 product codes.
- There are 100 store-product combinations.
- Each combination contains 731 daily records.
- Records cover 1 January 2022 to 1 January 2024.
- No missing values or exact duplicate rows were found.
- No invalid essential values or conflicting daily keys were found.
- No missing dates were found within the store-product histories.
- No rows had Units Sold greater than beginning-of-day Inventory Level.

## 4. Data Preparation Decisions

- The original CSV was preserved unchanged.
- Dates were converted to datetime.
- Essential numeric fields were converted and validated.
- Records were sorted by Store ID, Product ID and Date.
- A separate prepared dataset was saved as retail_checked.csv.
- Missing-value filling was unnecessary because none were found.
- No outliers were removed because high sales were not established errors.
- Missing dates would require investigation rather than automatic zero filling.
- The publisher's Demand Forecast column was excluded from model inputs
  because its generation process and future availability were not verified.
- No scaling or categorical encoding was required for the models used here.

## 5. Business and Dataset Limitations

- The dataset is synthetic practice data.
- Each Product ID appears under multiple categories.
- Each Store ID appears under multiple regions.
- Product codes are treated as synthetic series identifiers,
  not verified real-world product identities.
- Removing Category does not resolve the product-identity inconsistency.
- Beginning-of-day inventory does not establish stock availability
  at the start of the future forecast period.
- Recorded sales may not represent total customer demand,
  particularly when stock availability limits sales.
- These limitations were documented without inventing corrections.
- The project demonstrates a forecasting workflow; its usefulness for
  real inventory decisions has not been established.

## 6. Chart Observations

### Monthly Sales

Monthly totals fluctuate without a clear sustained upward or downward
trend. July 2023 has the highest total and February 2023 has the lowest.

Month length affects monthly totals, so average daily sales would be
needed for a fair comparison. The incomplete January 2024 month was
excluded from the monthly chart.

### Sales by Store

Total recorded sales are similar across the five stores.
S003 has the highest total, with relatively small differences.
Units sold do not measure profitability.

### Sales by Product

P0016 has the highest recorded sales across all stores.
The top 10 product codes have similar totals, around 500,000 units each.
Historical rankings do not establish future demand.

### Daily Sales: S001/P0001

Daily sales fluctuate substantially. The trailing seven-day average
smooths historical fluctuations but is not a future forecast.

No clear sustained trend is visible. The chart alone does not
establish seasonality.

### Sales Distribution: S001/P0001

The distribution is right-skewed, with more low-sales days and fewer
high-sales days.

| Statistic | Value |
|---|---:|
| Daily observations | 731 |
| Mean | 137.31 |
| Standard deviation | 108.19 |
| Minimum | 0 |
| 25th percentile | 47 |
| Median | 109 |
| 75th percentile | 202 |
| Maximum | 461 |

High values were retained because they were not established data errors.

## 7. Training, Validation and Testing

- Training data is used to fit the forecasting models.
- Validation predictions are compared with actual sales to select a model.
- Test data evaluates the selected model after selection is fixed.

The records were split chronologically rather than randomly.
This reflects forecasting, where future observations are unavailable
when a prediction is made.

The full-data EDA was descriptive. Test outcomes were not used to
choose model settings or change the selected model.

## 8. Evaluated Series and Data Split

The first experiment used S001/P0001 to understand and verify the
workflow before extending it to other combinations.

| Dataset | Start Date | End Date | Days |
|---|---|---|---:|
| Training | 2022-01-01 | 2023-11-06 | 675 |
| Validation | 2023-11-07 | 2023-12-04 | 28 |
| Test | 2023-12-05 | 2024-01-01 | 28 |

Results for this series do not establish performance for all
store-product combinations.

## 9. Weekly Rolling Evaluation

The forecast horizon was seven days.

Validation and testing each contained four weekly forecasts.
At each weekly forecast origin, only previously observed sales were used.

After a week ended, its actual sales became available for the next
week's forecast. Actual sales within the week being forecast were
not used to update that week's predictions.

## 10. Forecasting Methods

### Naive

Predicts the last observed day's sales for every day of the next week.

### Mean

Predicts the average of all historical sales available before each
forecast week.

### Seasonal Naive

Repeats the previous seven observed daily sales values for the next week.
This tests a weekly-repeat rule; it does not prove weekly seasonality.

### ARIMA

Models relationships in historical sales.
The initial configuration was ARIMA(1,1,1).

The model was refitted at each weekly forecast origin.
Negative forecasts were clipped to zero.

### XGBoost

Learns a relationship between past-sales features and daily sales.

The initial settings were:
- n_estimators: 150
- max_depth: 3
- learning_rate: 0.05
- objective: reg:squarederror
- random_state: 42
- n_jobs: 1

These settings were not tuned using test results.
Negative forecasts were clipped to zero.

## 11. XGBoost Feature Preparation

| Feature | Meaning |
|---|---|
| lag_1 | Sales one day before the target date |
| lag_7 | Sales seven days before the target date |
| lag_14 | Sales fourteen days before the target date |
| mean_7 | Average sales over the seven days before the target date |
| weekday | Target weekday, with Monday = 0 |
| target_sales | Actual sales the model learns to predict |

Rolling averages were shifted by one day to exclude the target value.

The first 14 training rows lacked sufficient lag history.
Therefore, 675 training observations produced 661 feature-table rows.
The original dataset remained unchanged.

For multi-day forecasting, predictions were appended to the available
history to construct subsequent days' features. Unknown future actual
sales were not used. This is recursive forecasting.

## 12. Evaluation Metrics

### Mean Absolute Error: MAE

The average absolute difference between actual and predicted sales.

MAE = mean(abs(actual sales - predicted sales))

### Root Mean Squared Error: RMSE

The square root of the average squared prediction error.
It gives greater weight to larger errors.

RMSE = sqrt(mean((actual sales - predicted sales)^2))

Both metrics are measured in units sold.
Lower values indicate lower errors.
Neither metric is an accuracy percentage.

## 13. Validation Results

| Model | Validation MAE | Validation RMSE |
|---|---:|---:|
| Naive | 133.86 | 181.65 |
| Mean | 93.82 | 114.75 |
| Seasonal Naive | 135.43 | 170.58 |
| ARIMA | 93.78 | 114.73 |
| XGBoost | 99.35 | 118.70 |

ARIMA was selected using the lowest validation MAE.
Its MAE advantage over Mean was approximately 0.04 units,
which is negligible in practical terms.

XGBoost did not outperform ARIMA or Mean in this experiment.

## 14. Test Results

The selected ARIMA model and the Mean baseline were evaluated
on the same test dates using the same weekly procedure.

| Model | Test MAE | Test RMSE |
|---|---:|---:|
| ARIMA | 72.96 | 86.06 |
| Mean | 72.91 | 86.02 |

Mean had slightly lower test errors, but the differences were negligible.
Test results were not used to change the selected model.

The lower test errors compared with validation do not prove improvement:
the two periods contain different observations.

## 15. Main Modelling Findings

Both ARIMA and Mean produced nearly constant forecasts around
137–138 units during testing.

Neither method captured the large daily fluctuations well.
ARIMA did not demonstrate a meaningful practical advantage over
the simple Mean baseline.

These findings apply to the selected synthetic S001/P0001 series,
the evaluated dates and the configurations used.

Performance for other series or real retailers remains unverified.

## 16. Result Files

The results-saving code writes the following files to:

reports/model_results/S001_P0001/

- validation_metrics.csv
- test_metrics.csv
- data_split.csv
- validation_predictions.csv
- test_predictions.csv

The test comparison chart is saved to:

reports/figures/06_test_forecast_comparison.png

CSV files retain unrounded calculated values.
Displayed comparison tables are rounded for readability.

## 17. Additional Stock Calculation

The planned calculation is:

Additional stock =
ceil(max(0, total forecast sales + safety stock - available inventory))

Available inventory must refer to stock available at the forecast origin.
Safety stock is a user-assumed buffer, not a model prediction.

This simplified calculation does not model supplier lead times,
incoming orders, storage capacity or order costs.

## 18. Current Progress and Next Steps

Completed:
- Dataset inspection and quality checks.
- Data preparation and five EDA charts.
- Chronological training, validation and test split.
- Validation comparison of five forecasting methods.
- ARIMA selection based on validation MAE.
- Test evaluation of ARIMA against the Mean baseline.
- Test forecast comparison chart.

Next:
1. Refit the selected ARIMA model on all 731 observations.
2. Forecast 2–8 January 2024, immediately after the last recorded date.
3. Save the future forecast with dates, store, product and model details.
4. Implement and verify the stock calculation.
5. Extend the workflow to other store-product combinations.
6. Build the improved dashboard with clear selectors and limitations.
7. Update GitHub and verify the Streamlit deployment.
8. Prepare the final report, presentation and Q&A notes.

Actual sales for the future forecast dates are not provided in this
dataset, so forecast errors for those dates cannot yet be calculated.


## Future Forecast and Stock Calculation

The final ARIMA model was fitted on all 731 observations.
Estimated sales for 2–8 January 2024 totalled approximately 961.73 units.

With assumed available inventory of 300 units and safety stock
of 50 units, the estimated additional requirement was 712 units.

These inventory inputs are illustrative assumptions.
Actual sales for the forecast dates are unavailable, so forecast
accuracy for these dates cannot yet be evaluated.