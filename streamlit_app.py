"""Retail planning dashboard. Training is performed in the project notebooks."""
from pathlib import Path
import json
import math

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "app_data"

st.set_page_config(page_title="Retail Stock Planner", page_icon="📦", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1450px;}
.hero {padding: 1.6rem 1.8rem; border-radius: 18px;
       background: linear-gradient(120deg,#123b56,#147d83); color: white; margin-bottom: 1.1rem;}
.hero h1 {color:white; padding:0; font-size:2.25rem;}
.hero p {margin: .5rem 0 0; color: #e0f2f1;}
[data-testid="stMetric"] {border:1px solid #d8e4eb; border-radius:12px; padding:1rem;}
button[data-baseweb="tab"] {font-size:1rem;}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def read_csv(filename, modified):
    # The modification time is part of the cache key so updated files reload.
    table = pd.read_csv(DATA / filename)
    if "Date" in table.columns:
        table["Date"] = pd.to_datetime(table["Date"], errors="raise")
    return table


def load_table(filename, columns):
    path = DATA / filename
    if not path.is_file():
        raise ValueError(f"Missing app_data/{filename}. Run the notebook export cell first.")
    table = read_csv(filename, path.stat().st_mtime_ns)
    missing = set(columns) - set(table.columns)
    if missing:
        raise ValueError(f"{filename} is missing columns: {', '.join(sorted(missing))}")
    return table


def select_pair(table, store, product):
    return table[(table["Store ID"] == store) & (table["Product ID"] == product)].copy()


def stock_requirement(predictions, inventory, safety):
    values = [float(value) for value in predictions]
    if not values or not all(math.isfinite(value) and value >= 0 for value in values):
        raise ValueError("Forecast values must be finite and nonnegative.")
    if not all(math.isfinite(value) and value >= 0 for value in [inventory, safety]):
        raise ValueError("Inventory and safety stock must be finite and nonnegative.")
    return math.ceil(max(0, sum(values) + safety - inventory))


def csv_download(label, table, filename, key):
    st.download_button(label, table.to_csv(index=False).encode("utf-8"),
                       file_name=filename, mime="text/csv", key=key)


try:
    history = load_table("history.csv", ["Date", "Store ID", "Product ID", "Units Sold", "Inventory Level"])
    forecasts = load_table("future_forecasts.csv", ["Date", "Store ID", "Product ID", "Selected model", "Selected forecast", "Mean forecast"])
    validation = load_table("validation_metrics.csv", ["Store ID", "Product ID", "Model", "Validation MAE", "Validation RMSE"])
    test_metrics = load_table("test_metrics.csv", ["Store ID", "Product ID", "Selected model", "Selected test MAE", "Selected test RMSE", "Mean test MAE", "Mean test RMSE"])
    test_predictions = load_table("test_predictions.csv", ["Date", "Store ID", "Product ID", "Actual sales", "Selected forecast", "Mean forecast"])
    quality = load_table("quality_summary.csv", ["check", "value"])
    metadata = json.loads((DATA / "metadata.json").read_text(encoding="utf-8"))
except (ValueError, OSError, KeyError) as error:
    st.error(str(error))
    st.info("Place the seven exported files inside app_data, next to streamlit_app.py.")
    st.stop()

st.sidebar.title("📦 Retail planner")
st.sidebar.caption("Explore sales. Review forecasts. Plan stock.")
store = st.sidebar.selectbox("Store", sorted(forecasts["Store ID"].unique()))
products = forecasts.loc[forecasts["Store ID"] == store, "Product ID"].unique()
product = st.sidebar.selectbox("Product code", sorted(products))

pair_history = select_pair(history, store, product).sort_values("Date")
pair_forecast = select_pair(forecasts, store, product).sort_values("Date")
pair_validation = select_pair(validation, store, product).sort_values(["Validation MAE", "Validation RMSE", "Model"])
pair_test = select_pair(test_metrics, store, product)
pair_test_predictions = select_pair(test_predictions, store, product).sort_values("Date")

try:
    horizon = int(metadata["forecast_horizon_days"])
    if pair_history.empty or pair_validation.empty or len(pair_test) != 1:
        raise ValueError("Selected pair has incomplete historical or evaluation results.")
    if len(pair_forecast) != horizon or pair_forecast["Date"].duplicated().any():
        raise ValueError("Selected pair has an incomplete future forecast.")
    expected = pd.date_range(pair_history["Date"].max() + pd.Timedelta(days=1), periods=horizon, freq="D")
    if list(pair_forecast["Date"]) != list(expected):
        raise ValueError("Forecast dates must immediately follow the recorded history.")
    if pair_forecast["Selected model"].nunique() != 1:
        raise ValueError("Selected model is inconsistent across forecast rows.")
    selected_model = pair_forecast["Selected model"].iloc[0]
    metrics = pair_test.iloc[0]
    if selected_model != metrics["Selected model"] or selected_model != pair_validation.iloc[0]["Model"]:
        raise ValueError("Forecast, validation and test model selections disagree.")
    for column in ["Selected forecast", "Mean forecast"]:
        if not pair_forecast[column].map(lambda value: math.isfinite(float(value)) and float(value) >= 0).all():
            raise ValueError("Future forecast contains invalid values.")
    if len(pair_test_predictions) != int(metadata["test_days"]) or pair_test_predictions["Date"].duplicated().any():
        raise ValueError("Selected pair has incomplete test predictions.")
except (ValueError, KeyError, TypeError) as error:
    st.error(str(error))
    st.stop()

mode = st.sidebar.radio("Forecast to explore", ["Validation-selected method", "Mean baseline"])
forecast_column = "Selected forecast" if mode == "Validation-selected method" else "Mean forecast"
active_model = selected_model if mode == "Validation-selected method" else "Mean"
mae_column = "Selected test MAE" if mode == "Validation-selected method" else "Mean test MAE"
rmse_column = "Selected test RMSE" if mode == "Validation-selected method" else "Mean test RMSE"
st.sidebar.info("Saved forecasts from notebook experiments. Selecting an option does not retrain models or change the original validation selection.")

st.markdown("""<div class="hero"><h1>Retail Stock Planner</h1>
<p>Understand past sales, inspect forecast quality and estimate additional stock.</p></div>""", unsafe_allow_html=True)
st.caption(f"STORE {store}  ·  PRODUCT CODE {product}  ·  VIEWING {active_model}  ·  {horizon}-DAY HORIZON")
st.warning("Synthetic prototype: product/category and store/region labels are inconsistent. Real retail usefulness has not been established.")

start_date = pair_forecast["Date"].min().strftime("%d %b %Y")
end_date = pair_forecast["Date"].max().strftime("%d %b %Y")
st.info(f"Forecast dates: {start_date} to {end_date}. These follow the dataset end date, not today's date. Future actual sales are unavailable.")

cards = st.columns(4)
cards[0].metric("Forecast total · units", f"{pair_forecast[forecast_column].sum():,.2f}")
cards[1].metric("Test MAE · units", f"{metrics[mae_column]:,.2f}")
cards[2].metric("Test RMSE · units", f"{metrics[rmse_column]:,.2f}")
cards[3].metric("Historical daily records", f"{len(pair_history):,}")
st.caption("Test errors describe the earlier 28-day evaluation period. They are not error measurements for the future forecast.")

overview, audit, explore, evaluate, stock = st.tabs([
    "1 · Overview", "2 · Data quality", "3 · Sales history", "4 · Forecast & evaluation", "5 · Stock planner"
])

with overview:
    st.subheader("From records to a stock estimate")
    st.write("The notebook checks the raw data, prepares daily histories, compares five forecasting methods and evaluates the selected method on later dates. This dashboard displays those saved outputs.")
    cols = st.columns(3)
    cols[0].metric("Stores", history["Store ID"].nunique())
    cols[1].metric("Product codes", history["Product ID"].nunique())
    cols[2].metric("Forecast combinations", len(forecasts[["Store ID", "Product ID"]].drop_duplicates()))
    st.write(f"Recorded dates: {history['Date'].min():%d %b %Y} to {history['Date'].max():%d %b %Y}.")
    left, right = st.columns(2)
    with left:
        st.markdown("**Monthly sales · all stores and products**")
        monthly = history.groupby("Date")["Units Sold"].sum().resample("MS").sum()
        complete = monthly[monthly.index + pd.offsets.MonthEnd(0) <= history["Date"].max()]
        st.line_chart(complete, color="#16858b")
        st.caption("Incomplete final month omitted. Month length affects totals.")
    with right:
        st.markdown("**Recorded sales by store**")
        st.bar_chart(history.groupby("Store ID")["Units Sold"].sum(), color="#16858b")
        st.caption("Units sold measure volume, not profitability.")
    st.markdown("**Overall test evidence · all combinations**")
    overall = pd.DataFrame({"Approach": ["Validation-selected methods", "Mean baseline"],
        "Average per-series MAE": [test_metrics["Selected test MAE"].mean(), test_metrics["Mean test MAE"].mean()],
        "Average per-series RMSE": [test_metrics["Selected test RMSE"].mean(), test_metrics["Mean test RMSE"].mean()]})
    st.dataframe(overall.round(2), hide_index=True, width="stretch")
    if overall.iloc[1]["Average per-series MAE"] < overall.iloc[0]["Average per-series MAE"]:
        st.info("The Mean baseline had lower average test MAE overall. Model selection did not demonstrate an overall improvement on this experiment.")
    counts = test_metrics["Selected model"].value_counts().rename("Combinations")
    st.bar_chart(counts, color="#16858b")

with audit:
    st.subheader("What was checked before modelling?")
    labels = {"raw_rows":"Original rows", "prepared_rows":"Prepared rows", "missing_cells":"Missing cells", "exact_duplicates":"Exact duplicate rows", "invalid_required_rows":"Invalid required rows", "store_product_combinations":"Store-product combinations", "series_with_gaps":"Series with missing dates", "products_with_multiple_categories":"Products with multiple categories", "stores_with_multiple_regions":"Stores with multiple regions", "sales_above_beginning_inventory":"Sales above beginning inventory"}
    quality_view = quality.copy()
    quality_view["check"] = quality_view["check"].map(lambda name: labels.get(name, name))
    quality_view.columns = ["Check", "Result"]
    st.dataframe(quality_view, hide_index=True, width="stretch")
    st.write("Preparation converted dates and essential numeric fields, checked invalid values and daily keys, and sorted records. No missing-value filling was needed in the recorded audit. The raw dataset was preserved.")
    st.write("High sales were retained because they were not established errors. Publisher-supplied Demand Forecast was excluded from predictor inputs. Category and region inconsistencies were documented without inventing corrections.")
    st.caption("The history export contains five fields for the dashboard; the original dataset contains fifteen columns.")
    csv_download("Download audit findings", quality, "quality_summary.csv", "audit_csv")

with explore:
    st.subheader(f"Daily history · {store} / {product}")
    days = st.select_slider("Display window", options=[30, 90, 180, "All"], value="All")
    daily = pair_history.set_index("Date")["Units Sold"]
    history_chart = pd.DataFrame({"Daily sales": daily, "Trailing 7-day mean": daily.rolling(7).mean()})
    if days != "All":
        history_chart = history_chart.tail(int(days))
    st.line_chart(history_chart, color=["#70b7c5", "#ee9d34"])
    st.caption("The trailing mean is a historical summary, not a forecast. The window changes only the displayed history.")
    st.dataframe(pair_history.sort_values("Date", ascending=False), hide_index=True, width="stretch")
    st.caption("Table is newest first; charts use chronological order. Historical inventory is a recorded beginning-of-day value.")
    csv_download("Download selected sales history", pair_history, f"{store}_{product}_history.csv", "history_csv")

with evaluate:
    st.subheader("Model selection used validation data")
    st.dataframe(pair_validation[["Model", "Validation MAE", "Validation RMSE"]].round(2), hide_index=True, width="stretch")
    st.write(f"Original validation-selected method: **{selected_model}**. Lower MAE ranked first, followed by RMSE and model name for ties. Test results did not change this selection.")
    st.markdown("**Earlier test period · actual sales versus forecasts**")
    test_chart = pair_test_predictions.set_index("Date")[["Actual sales", "Selected forecast", "Mean forecast"]]
    st.line_chart(test_chart, color=["#243746", "#16858b", "#ee9d34"])
    st.caption("Four weekly seven-day forecasts. Completed weeks become observed history at the next forecast origin. MAE is average absolute error; RMSE gives greater weight to larger errors. Neither is an accuracy percentage.")
    st.markdown(f"**Future forecast · {start_date} to {end_date}**")
    st.line_chart(pair_forecast.set_index("Date")[["Selected forecast", "Mean forecast"]], color=["#16858b", "#ee9d34"])
    st.dataframe(pair_forecast.round(2), hide_index=True, width="stretch")
    csv_download("Download future forecasts", pair_forecast, f"{store}_{product}_forecast.csv", "forecast_csv")

with stock:
    st.subheader("Estimate additional stock")
    st.write(f"Using **{active_model}** forecast: **{pair_forecast[forecast_column].sum():,.2f} units** over {horizon} days.")
    st.caption("Enter stock available at the forecast origin. The last historical inventory record does not establish this quantity.")
    with st.form(f"stock_{store}_{product}_{forecast_column}"):
        left, right = st.columns(2)
        inventory = left.number_input("Available inventory · units", min_value=0, value=0, step=1)
        safety = right.number_input("Assumed safety stock · units", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Calculate additional stock", type="primary")
    if submitted:
        requirement = stock_requirement(pair_forecast[forecast_column], inventory, safety)
        st.metric("Additional units required", f"{requirement:,}")
        st.write(f"Round up max(0, {pair_forecast[forecast_column].sum():,.2f} + {safety:,} − {inventory:,}) = **{requirement:,} units**.")
        if requirement == 0:
            st.success("Entered inventory covers the point forecast plus the assumed safety stock.")
        else:
            st.success(f"Estimated additional requirement: {requirement:,} units.")
        result = pd.DataFrame([{"Store ID":store, "Product ID":product, "Method":active_model, "Forecast start":start_date, "Forecast end":end_date, "Forecast units":pair_forecast[forecast_column].sum(), "Available inventory":inventory, "Assumed safety stock":safety, "Additional units":requirement}])
        csv_download("Download stock estimate", result, f"{store}_{product}_stock.csv", "stock_csv")
    st.info("This simplified estimate assumes replenishment can be available when needed. It excludes incoming orders, supplier lead time, capacity and order costs. Safety stock is user-assumed; no service level is guaranteed. No order is placed.")

st.divider()
st.caption("University prototype · Synthetic data · Seven-day point forecasts · Offline model evaluation · Interactive stock calculations")
