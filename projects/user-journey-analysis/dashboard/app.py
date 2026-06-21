from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parents[1]
LOCAL_DB_PATH = PROJECT_DIR / "warehouse.duckdb"
CLOUD_DB_PATH = PROJECT_DIR.parents[1] / "apps" / "learning-hub" / "data" / "user-journey-analysis.duckdb"
DB_PATH = LOCAL_DB_PATH if LOCAL_DB_PATH.exists() else CLOUD_DB_PATH

st.set_page_config(page_title="User Journey Analysis", layout="wide")
st.title("User Journey Analysis")


@st.cache_data(show_spinner=False)
def query(database_path: str, sql: str) -> pd.DataFrame:
    path = Path(database_path)
    if not path.exists():
        raise FileNotFoundError(path)
    with duckdb.connect(database_path, read_only=True) as con:
        return con.execute(sql).fetchdf()


try:
    kpis = query(str(DB_PATH), "SELECT * FROM gold.mart_summary_kpis").iloc[0]
    page_count_data = query(str(DB_PATH), "SELECT * FROM gold.mart_page_count")
    presence_data = query(str(DB_PATH), "SELECT * FROM gold.mart_page_presence")
    destination_data = query(str(DB_PATH), "SELECT * FROM gold.mart_page_destinations")
    sequence_data = query(str(DB_PATH), "SELECT * FROM gold.mart_page_sequences")
    length_data = query(str(DB_PATH), "SELECT * FROM gold.mart_journey_length")
    quiz = query(str(DB_PATH), "SELECT * FROM gold.mart_quiz_answers")
except FileNotFoundError:
    st.error("Gold marts not found. Run the project pipeline first.")
    st.code(r".\.venv-365ds\Scripts\python.exe projects\user-journey-analysis\scripts\pipeline.py")
    st.stop()


scenario_options = sorted(page_count_data["scenario"].unique().tolist())
plan_options = ["All", "Annual", "Monthly", "Quarterly"]
page_options = sorted(destination_data["source_page"].unique().tolist())

filters = st.columns(4)
scenario = filters[0].selectbox("Scenario", scenario_options, index=scenario_options.index("all_sessions"))
plan = filters[1].selectbox("Subscription Type", plan_options)
source_page = filters[2].selectbox("Destination From", page_options, index=page_options.index("Pricing"))
sequence_length = filters[3].selectbox("Sequence Length", [2, 3, 4], index=1)

kpi_cols = st.columns(5)
kpi_cols[0].metric("Raw Sessions", f"{int(kpis['raw_rows']):,}")
kpi_cols[1].metric("Users", f"{int(kpis['unique_users']):,}")
kpi_cols[2].metric("Annual Users", f"{int(kpis['annual_users']):,}")
kpi_cols[3].metric("Monthly Users", f"{int(kpis['monthly_users']):,}")
kpi_cols[4].metric("Quarterly Users", f"{int(kpis['quarterly_users']):,}")

page_counts = page_count_data[
    (page_count_data["scenario"] == scenario)
    & (page_count_data["subscription_type"] == plan)
    & (page_count_data["rank"] <= 10)
]
presence = presence_data[
    (presence_data["scenario"] == scenario)
    & (presence_data["subscription_type"] == plan)
    & (presence_data["rank"] <= 10)
]
destinations = destination_data[
    (destination_data["scenario"] == scenario)
    & (destination_data["subscription_type"] == plan)
    & (destination_data["source_page"] == source_page)
    & (destination_data["rank"] <= 10)
]
sequences = sequence_data[
    (sequence_data["scenario"] == scenario)
    & (sequence_data["subscription_type"] == plan)
    & (sequence_data["sequence_length"] == sequence_length)
    & (sequence_data["rank"] <= 10)
].copy()
sequences["sequence_display"] = sequences["sequence"].str.replace("-", " -> ", regex=False)

left, right = st.columns(2)
left.plotly_chart(
    px.bar(page_counts, x="page_count", y="page", orientation="h", title="Top Page Count"),
    use_container_width=True,
)
right.plotly_chart(
    px.bar(presence, x="journey_presence", y="page", orientation="h", title="Top Page Presence"),
    use_container_width=True,
)

left, right = st.columns(2)
left.plotly_chart(
    px.bar(destinations, x="destination_count", y="next_page", orientation="h", title=f"Destinations After {source_page}"),
    use_container_width=True,
)
right.plotly_chart(
    px.bar(sequences, x="journey_count", y="sequence_display", orientation="h", title=f"Top {sequence_length}-Page Sequences"),
    use_container_width=True,
)

length_filtered = length_data[length_data["scenario"] == scenario]
st.plotly_chart(
    px.bar(
        length_filtered,
        x="subscription_type",
        y="avg_journey_length",
        title="Average Journey Length by Subscription Type",
    ),
    use_container_width=True,
)

st.subheader("Quiz-Supporting Results")
st.dataframe(quiz, use_container_width=True, hide_index=True)
