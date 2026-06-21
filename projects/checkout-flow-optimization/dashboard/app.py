from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parents[1]
LOCAL_DB_PATH = PROJECT_DIR / "warehouse.duckdb"
CLOUD_DB_PATH = PROJECT_DIR.parents[1] / "apps" / "learning-hub" / "data" / "checkout-flow-optimization.duckdb"
DB_PATH = LOCAL_DB_PATH if LOCAL_DB_PATH.exists() else CLOUD_DB_PATH

st.set_page_config(page_title="Checkout Flow Optimization", layout="wide")
st.title("Checkout Flow Optimization")


@st.cache_data(show_spinner=False)
def query(database_path: str, sql: str) -> pd.DataFrame:
    path = Path(database_path)
    if not path.exists():
        raise FileNotFoundError(path)
    with duckdb.connect(database_path, read_only=True) as con:
        return con.execute(sql).fetchdf()


try:
    kpis = query(str(DB_PATH), "SELECT * FROM gold.mart_summary_kpis").iloc[0]
    monthly = query(str(DB_PATH), "SELECT * FROM gold.mart_monthly_checkout ORDER BY checkout_month")
    errors = query(str(DB_PATH), "SELECT * FROM gold.mart_error_rankings ORDER BY rank")
    error_device = query(str(DB_PATH), "SELECT * FROM gold.mart_checkout_errors")
    device = query(str(DB_PATH), "SELECT * FROM gold.mart_device_distribution")
    quiz = query(str(DB_PATH), "SELECT * FROM gold.mart_quiz_answers ORDER BY question_number")
except FileNotFoundError:
    st.error("Gold marts not found. Run the project pipeline first.")
    st.code(r".\.venv-365ds\Scripts\python.exe projects\checkout-flow-optimization\scripts\pipeline.py")
    st.stop()


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


month_labels = monthly["checkout_month"].dt.strftime("%b %Y").tolist()
selected_months = st.multiselect("Months", month_labels, default=month_labels)
selected_devices = st.multiselect("Devices", sorted(device["device"].tolist()), default=sorted(device["device"].tolist()))

filtered_monthly = monthly[monthly["checkout_month"].dt.strftime("%b %Y").isin(selected_months)]
filtered_error_device = error_device[error_device["device"].isin(selected_devices)]

kpi_cols = st.columns(5)
kpi_cols[0].metric("Carts", f"{int(kpis['total_carts']):,}")
kpi_cols[1].metric("Checkout Attempts", f"{int(kpis['total_checkout_attempts']):,}")
kpi_cols[2].metric("Successful", f"{int(kpis['successful_checkout_attempts']):,}")
kpi_cols[3].metric("Success Rate", pct(float(kpis["checkout_success_rate"])))
kpi_cols[4].metric("Abandonment", pct(float(kpis["cart_abandonment_rate"])))

success_tab, abandonment_tab, errors_tab = st.tabs(["Checkout Success", "Cart Abandonment", "Errors And Devices"])

with success_tab:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(
        x=filtered_monthly["checkout_month"],
        y=filtered_monthly["count_total_checkout_attempts"],
        name="Attempts",
        marker_color="#3dafb8",
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_monthly["checkout_month"],
            y=filtered_monthly["checkout_success_rate"],
            name="Success Rate",
            mode="lines+markers",
            line=dict(color="#293343", width=3),
        ),
        secondary_y=True,
    )
    fig.update_layout(title="Monthly Checkout Success Rate", legend_orientation="h")
    fig.update_yaxes(title_text="Checkout attempts", secondary_y=False)
    fig.update_yaxes(title_text="Success rate", tickformat=".0%", range=[0, 1], secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(
        filtered_monthly[
            [
                "checkout_month",
                "count_total_checkout_attempts",
                "count_successful_checkout_attempts",
                "checkout_success_rate",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with abandonment_tab:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(
        x=filtered_monthly["checkout_month"],
        y=filtered_monthly["count_total_carts"],
        name="Carts",
        marker_color="#8cdae3",
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_monthly["checkout_month"],
            y=filtered_monthly["cart_abandonment_rate"],
            name="Abandonment Rate",
            mode="lines+markers",
            line=dict(color="#550000", width=3),
        ),
        secondary_y=True,
    )
    fig.update_layout(title="Monthly Cart Abandonment Rate", legend_orientation="h")
    fig.update_yaxes(title_text="Carts", secondary_y=False)
    fig.update_yaxes(title_text="Abandonment rate", tickformat=".0%", range=[-0.1, 1], secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The course formula is `(carts - checkout attempts) / carts`; negative values are preserved when attempts exceed carts.")
    st.dataframe(
        filtered_monthly[
            [
                "checkout_month",
                "count_total_carts",
                "count_total_checkout_attempts",
                "cart_abandonment_rate",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with errors_tab:
    left, right = st.columns([2, 1])
    top_errors = errors.head(10)
    stacked = (
        filtered_error_device[filtered_error_device["error_message"].isin(top_errors["error_message"])]
        .pivot_table(index="error_message", columns="device", values="attempt_count", aggfunc="sum", fill_value=0)
        .reset_index()
    )
    left.plotly_chart(
        px.bar(
            stacked,
            y="error_message",
            x=[col for col in stacked.columns if col != "error_message"],
            orientation="h",
            title="Checkout Error Messages",
            color_discrete_map={"desktop": "#293343", "mobile": "#3a9ea7"},
        ).update_layout(yaxis={"categoryorder": "total ascending"}, legend_title_text="Device"),
        use_container_width=True,
    )
    right.plotly_chart(
        px.bar(
            device,
            y="device",
            x="attempt_share",
            orientation="h",
            text=device["attempt_share"].map(pct),
            title="Desktop vs Mobile",
            color="device",
            color_discrete_map={"desktop": "#293343", "mobile": "#3a9ea7"},
        ).update_xaxes(tickformat=".0%"),
        use_container_width=True,
    )
    st.subheader("Quiz Support")
    st.dataframe(quiz, use_container_width=True, hide_index=True)
