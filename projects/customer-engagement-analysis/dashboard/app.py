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
CLOUD_DB_PATH = PROJECT_DIR.parents[1] / "apps" / "learning-hub" / "data" / "customer-engagement-analysis.duckdb"
DB_PATH = LOCAL_DB_PATH if LOCAL_DB_PATH.exists() else CLOUD_DB_PATH

st.set_page_config(page_title="Customer Engagement Analysis", layout="wide")
st.title("Customer Engagement Analysis")


@st.cache_data(show_spinner=False)
def query(database_path: str, sql: str) -> pd.DataFrame:
    path = Path(database_path)
    if not path.exists():
        raise FileNotFoundError(path)
    with duckdb.connect(database_path, read_only=True) as con:
        return con.execute(sql).fetchdf()


try:
    kpis = query(str(DB_PATH), "SELECT * FROM gold.mart_summary_kpis").iloc[0]
    monthly = query(str(DB_PATH), "SELECT * FROM gold.mart_monthly_engagement ORDER BY watched_month, user_type")
    registrations = query(
        str(DB_PATH),
        "SELECT * FROM gold.mart_monthly_registrations ORDER BY registration_month, user_type",
    )
    country_registered = query(str(DB_PATH), "SELECT * FROM gold.mart_country_registered")
    country_minutes = query(str(DB_PATH), "SELECT * FROM gold.mart_country_minutes")
    courses = query(str(DB_PATH), "SELECT * FROM gold.mart_course_performance ORDER BY course_rank")
    quiz = query(str(DB_PATH), "SELECT * FROM gold.mart_quiz_answers ORDER BY question_number")
except FileNotFoundError:
    st.error("Gold marts not found. Run the project pipeline first.")
    st.code(r".\.venv-365ds\Scripts\python.exe projects\customer-engagement-analysis\scripts\pipeline.py")
    st.stop()


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


user_types = ["All", "Free", "Paid"]
selected_user_type = st.segmented_control("User Type", user_types, default="All")
registration_months = sorted(country_registered["registration_month"].dt.strftime("%b %Y").unique().tolist())
selected_registration_month = st.select_slider(
    "Registration Month",
    options=registration_months,
    value=registration_months[-1],
)

kpi_cols = st.columns(5)
kpi_cols[0].metric("Registered", f"{int(kpis['registered_students']):,}")
kpi_cols[1].metric("Onboarded", f"{int(kpis['onboarded_students']):,}", pct(float(kpis["onboarding_rate"])))
kpi_cols[2].metric("Minutes Watched", f"{float(kpis['total_minutes_watched']):,.0f}")
kpi_cols[3].metric("Avg Minutes", f"{float(kpis['average_minutes_watched']):,.2f}")
kpi_cols[4].metric("Paid / Free Avg", f"{float(kpis['paid_to_free_average_ratio']):.2f}x")

trend_tab, country_tab, course_tab = st.tabs(["Engagement", "Countries", "Onboarding And Courses"])

with trend_tab:
    trend = monthly[monthly["user_type"].eq(selected_user_type)]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(
        x=trend["watched_month"],
        y=trend["total_minutes_watched"],
        name="Minutes",
        marker_color="#2f80ed",
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=trend["watched_month"],
            y=trend["average_minutes_watched"],
            name="Average Minutes",
            mode="lines+markers",
            line=dict(color="#1b4332", width=3),
        ),
        secondary_y=True,
    )
    fig.update_layout(title="Monthly Minutes And Average Minutes Watched", legend_orientation="h")
    fig.update_yaxes(title_text="Total minutes", secondary_y=False)
    fig.update_yaxes(title_text="Average minutes", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(trend, use_container_width=True, hide_index=True)

with country_tab:
    month_dt = pd.to_datetime(selected_registration_month, format="%b %Y")
    reg = (
        country_registered[
            country_registered["user_type"].eq(selected_user_type)
            & country_registered["registration_month"].eq(month_dt)
        ]
        .sort_values(["registered_students", "country_name"], ascending=[False, True])
        .head(5)
    )
    mins = (
        country_minutes[
            country_minutes["user_type"].eq(selected_user_type)
            & country_minutes["registration_month"].eq(month_dt)
        ]
        .sort_values(["total_minutes_watched", "country_name"], ascending=[False, True])
        .head(5)
    )
    left, right = st.columns(2)
    left.plotly_chart(
        px.bar(
            reg.sort_values("registered_students"),
            x="registered_students",
            y="country_name",
            orientation="h",
            title="Registered Students By Country",
            color_discrete_sequence=["#4c78a8"],
            text="registered_students",
        ),
        use_container_width=True,
    )
    right.plotly_chart(
        px.bar(
            mins.sort_values("total_minutes_watched"),
            x="total_minutes_watched",
            y="country_name",
            orientation="h",
            title="Minutes Watched By Country",
            color_discrete_sequence=["#f58518"],
            text="total_minutes_watched",
        ),
        use_container_width=True,
    )

with course_tab:
    reg_trend = registrations[registrations["user_type"].eq("All")].copy()
    reg_trend["not_onboarded_students"] = reg_trend["registered_students"] - reg_trend["onboarded_students"]
    fig = go.Figure()
    fig.add_bar(
        x=reg_trend["registration_month"],
        y=reg_trend["not_onboarded_students"],
        name="Not Onboarded",
        marker_color="#9c755f",
    )
    fig.add_bar(
        x=reg_trend["registration_month"],
        y=reg_trend["onboarded_students"],
        name="Onboarded",
        marker_color="#59a14f",
    )
    fig.update_layout(title="Registered And Onboarded Students", barmode="stack", legend_orientation="h")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns([3, 2])
    top_courses = courses.head(10)
    left.dataframe(
        courses[
            [
                "course_rank",
                "course_title",
                "total_minutes_watched",
                "average_minutes",
                "number_of_ratings",
                "average_rating",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    right.plotly_chart(
        px.bar(
            top_courses.sort_values("total_minutes_watched"),
            x="total_minutes_watched",
            y="course_title",
            orientation="h",
            title="Top Courses By Minutes Watched",
            color_discrete_sequence=["#e15759"],
        ),
        use_container_width=True,
    )
    st.subheader("Quiz Support")
    st.dataframe(quiz, use_container_width=True, hide_index=True)
