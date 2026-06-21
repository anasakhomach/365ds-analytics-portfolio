from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parents[1]
LOCAL_DB_PATH = PROJECT_DIR / "warehouse.duckdb"
CLOUD_DB_PATH = PROJECT_DIR.parents[1] / "apps" / "learning-hub" / "data" / "real-estate-market-analysis.duckdb"
DB_PATH = LOCAL_DB_PATH if LOCAL_DB_PATH.exists() else CLOUD_DB_PATH

st.set_page_config(page_title="Real Estate Market Analysis", layout="wide")
st.title("Real Estate Market Analysis")


@st.cache_data(show_spinner=False)
def query(sql: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        raise FileNotFoundError(DB_PATH)
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        return con.execute(sql).fetchdf()


try:
    kpis = query("SELECT * FROM gold.mart_summary_kpis").iloc[0]
    transactions = query("SELECT * FROM gold.mart_property_transactions")
    monthly_revenue = query("SELECT * FROM gold.mart_monthly_revenue")
    building = query("SELECT * FROM gold.mart_building_performance")
    state = query("SELECT * FROM gold.mart_state_distribution")
    country = query("SELECT * FROM gold.mart_country_performance")
    age = query("SELECT * FROM gold.mart_age_intervals")
    yearly = query("SELECT * FROM gold.mart_yearly_sales_by_building")
except FileNotFoundError:
    st.error("Gold marts not found. Run the project pipeline first.")
    st.code(r".\.venv-365ds\Scripts\python.exe projects\real-estate-market-analysis\scripts\pipeline.py")
    st.stop()


def currency(value: float) -> str:
    return f"${value:,.0f}"


country_options = ["All"] + sorted(transactions["country"].dropna().unique().tolist())
building_options = ["All"] + sorted(transactions["building_label"].dropna().unique().tolist())

filters = st.columns([1, 1, 2])
selected_country = filters[0].selectbox("Country", country_options)
selected_building = filters[1].selectbox("Building", building_options)

filtered = transactions.copy()
if selected_country != "All":
    filtered = filtered[filtered["country"] == selected_country]
if selected_building != "All":
    filtered = filtered[filtered["building_label"] == selected_building]

sold = filtered[filtered["sold_flag"]]

kpi_cols = st.columns(5)
kpi_cols[0].metric("Properties", f"{len(filtered):,}")
kpi_cols[1].metric("Sold", f"{len(sold):,}")
kpi_cols[2].metric("Revenue", currency(float(sold["revenue"].sum())))
kpi_cols[3].metric("Avg Sold Price", currency(float(sold["price"].mean())) if not sold.empty else "n/a")
kpi_cols[4].metric("Age/Price Corr.", f"{float(kpis['age_price_correlation']):.3f}")

left, right = st.columns(2)
left.plotly_chart(
    px.line(monthly_revenue, x="sale_month", y="total_revenue", markers=True, title="Monthly Revenue"),
    use_container_width=True,
)
right.plotly_chart(
    px.bar(building, x="building_label", y="sold_properties", color="avg_price", title="Sales by Building"),
    use_container_width=True,
)

left, right = st.columns(2)
left.plotly_chart(
    px.bar(state, x="state", y="sold_properties", text="cumulative_share", title="Sold Properties by State"),
    use_container_width=True,
)
right.plotly_chart(
    px.bar(country, x="country", y="avg_deal_satisfaction", title="Deal Satisfaction by Country"),
    use_container_width=True,
)

left, right = st.columns(2)
left.plotly_chart(
    px.bar(age, x="age_interval", y="sold_properties", title="Buyer Age Distribution"),
    use_container_width=True,
)
right.plotly_chart(
    px.area(yearly, x="sale_year", y="sold_properties", color="building_label", title="Yearly Sales by Building"),
    use_container_width=True,
)

st.subheader("Filtered Sold Property Detail")
st.dataframe(
    sold[
        [
            "property_id",
            "building_label",
            "sale_date",
            "price",
            "area",
            "country",
            "state",
            "age_at_purchase",
            "deal_satisfaction",
        ]
    ].sort_values(["sale_date", "property_id"], ascending=[False, True]),
    use_container_width=True,
    hide_index=True,
)
