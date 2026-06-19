from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_DIR / "warehouse.duckdb"

st.set_page_config(page_title="Tracking User Engagement", layout="wide")
st.title("Tracking User Engagement")


@st.cache_data(show_spinner=False)
def query(sql: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        raise FileNotFoundError(DB_PATH)
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        return con.execute(sql).fetchdf()


try:
    kpis = query("SELECT * FROM gold.mart_summary_kpis").iloc[0]
    segments = query("SELECT * FROM gold.mart_q2_engagement_segments")
    no_outliers = query("SELECT * FROM gold.mart_q2_engagement_no_outliers")
    statistics = query("SELECT * FROM gold.mart_q2_segment_statistics ORDER BY engagement_year, paid")
    hypothesis = query("SELECT * FROM gold.mart_hypothesis_tests ORDER BY student_plan")
    certificates = query("SELECT * FROM gold.mart_certificates_minutes ORDER BY student_id")
    correlation = query("SELECT * FROM gold.mart_correlation").iloc[0]
    regression = query("SELECT * FROM gold.mart_regression").iloc[0]
    probability = query("SELECT * FROM gold.mart_watch_probability").iloc[0]
    quiz = query("SELECT * FROM gold.mart_quiz_answers ORDER BY question_number")
except FileNotFoundError:
    st.error("Gold marts not found. Run the project pipeline first.")
    st.code(r".\.venv-365ds\Scripts\python.exe projects\tracking-user-engagement\scripts\pipeline.py")
    st.stop()


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


selected_plan = st.segmented_control("Plan", ["Free", "Paid"], default="Free")
selected_year = st.segmented_control("Distribution Year", [2021, 2022], default=2022)

kpi_cols = st.columns(5)
kpi_cols[0].metric("Q2 2021 Watchers", f"{int(kpis['watched_2021_students']):,}")
kpi_cols[1].metric("Q2 2022 Watchers", f"{int(kpis['watched_2022_students']):,}")
kpi_cols[2].metric("P(2021 | 2022)", pct(float(kpis["probability_2021_given_2022"])))
kpi_cols[3].metric("Certificate Corr", f"{float(kpis['correlation_coefficient']):.3f}")
kpi_cols[4].metric("1200 Min Prediction", f"{int(kpis['predicted_certificates_for_1200_minutes'])} certs")

engagement_tab, distribution_tab, statistics_tab, prediction_tab = st.tabs(
    ["Engagement", "Distribution", "Statistics", "Prediction"]
)

with engagement_tab:
    summary = statistics.copy()
    summary["period"] = "Q2 " + summary["engagement_year"].astype(str)
    left, right = st.columns([3, 2])
    left.plotly_chart(
        px.bar(
            summary,
            x="period",
            y="filtered_students",
            color="student_plan",
            barmode="group",
            title="Engaged Students After 99th Percentile Filtering",
            color_discrete_map={"Free": "#2f80ed", "Paid": "#f58518"},
            text="filtered_students",
        ),
        use_container_width=True,
    )
    right.plotly_chart(
        px.bar(
            summary,
            x="period",
            y="mean_minutes",
            color="student_plan",
            barmode="group",
            title="Filtered Average Minutes Watched",
            color_discrete_map={"Free": "#2f80ed", "Paid": "#f58518"},
            text=summary["mean_minutes"].round(1),
        ),
        use_container_width=True,
    )
    st.dataframe(
        summary[
            [
                "engagement_year",
                "student_plan",
                "raw_students",
                "filtered_students",
                "q99_minutes",
                "mean_minutes",
                "median_minutes",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with distribution_tab:
    raw_selection = segments[
        segments["student_plan"].eq(selected_plan) & segments["engagement_year"].eq(selected_year)
    ]
    clean_selection = no_outliers[
        no_outliers["student_plan"].eq(selected_plan)
        & no_outliers["engagement_year"].eq(selected_year)
    ].copy()
    st.plotly_chart(
        px.histogram(
            clean_selection,
            x="minutes_watched",
            nbins=60,
            title=f"{selected_plan} Q2 {selected_year} Minutes Watched Below 99th Percentile",
            color_discrete_sequence=["#4c78a8"],
        ),
        use_container_width=True,
    )
    raw_count, clean_count = len(raw_selection), len(clean_selection)
    st.caption(f"Raw rows: {raw_count:,}. Filtered rows: {clean_count:,}. Removed: {raw_count - clean_count:,}.")

with statistics_tab:
    stat_view = statistics.copy()
    stat_view["period_plan"] = "Q2 " + stat_view["engagement_year"].astype(str) + " " + stat_view["student_plan"]
    fig = go.Figure()
    fig.add_bar(
        x=stat_view["period_plan"],
        y=stat_view["mean_minutes"],
        marker_color=["#2f80ed" if plan == "Free" else "#f58518" for plan in stat_view["student_plan"]],
        error_y=dict(
            type="data",
            symmetric=False,
            array=stat_view["ci95_high"] - stat_view["mean_minutes"],
            arrayminus=stat_view["mean_minutes"] - stat_view["ci95_low"],
        ),
    )
    fig.update_layout(title="95% Confidence Intervals For Filtered Mean Minutes", yaxis_title="Mean minutes")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    left.subheader("Hypothesis Tests")
    left.dataframe(
        hypothesis[
            [
                "student_plan",
                "variance_assumption",
                "mean_2021",
                "mean_2022",
                "t_statistic",
                "decision",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    right.subheader("Watching Events")
    right.metric("Watched Both Years", f"{int(probability['watched_both_students']):,}")
    right.metric("P(2021 | 2022)", pct(float(probability["probability_2021_given_2022"])))
    right.metric(
        "Dependence",
        "Dependent" if int(probability["events_are_dependent"]) == 1 else "Independent",
    )

with prediction_tab:
    slope = float(regression["slope"])
    intercept = float(regression["intercept"])
    line_x = pd.Series([0.0, float(certificates["minutes_watched"].max())])
    line_y = intercept + slope * line_x
    fig = px.scatter(
        certificates,
        x="minutes_watched",
        y="certificates_issued",
        opacity=0.65,
        title="Minutes Watched And Certificates Issued",
        color_discrete_sequence=["#3a7d44"],
    )
    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            name="Linear fit",
            line=dict(color="#d62728", width=3),
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    model_cols = st.columns(4)
    model_cols[0].metric("Correlation", f"{float(correlation['correlation_coefficient']):.3f}")
    model_cols[1].metric("R-squared", f"{float(regression['r_squared']):.3f}")
    model_cols[2].metric("Slope", f"{slope:.6f}")
    model_cols[3].metric("Predicted Certs", int(regression["predicted_certificates_rounded_up"]))

    st.subheader("Quiz Support")
    st.dataframe(quiz, use_container_width=True, hide_index=True)
