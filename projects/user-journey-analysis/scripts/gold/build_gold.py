from __future__ import annotations

from itertools import product
from pathlib import Path

import pandas as pd

from common import REPORT_DIR, connect, ensure_project_dirs, write_dataframe
from journey_tools import (
    VALID_PLANS,
    journey_length,
    page_count,
    page_destinations,
    page_presence,
    page_sequences,
)


REPORT_PATH = REPORT_DIR / "user_journey_analysis_report.md"
PLANS = ("All", *VALID_PLANS)
SEQUENCE_LENGTHS = (2, 3, 4)
DESTINATION_PAGES = (
    "Homepage",
    "Pricing",
    "Courses",
    "Checkout",
    "Sign up",
    "Log in",
    "Coupon",
    "Career tracks",
)


def _ranked(frame: pd.DataFrame, count_column: str) -> pd.DataFrame:
    if frame.empty:
        frame["rank"] = pd.Series(dtype="int64")
        return frame
    ranked = frame.copy()
    ranked["rank"] = range(1, len(ranked) + 1)
    return ranked[["rank", *[col for col in ranked.columns if col != "rank"]]]


def _metric_frames(grouped: pd.DataFrame) -> dict[str, pd.DataFrame]:
    page_count_rows: list[pd.DataFrame] = []
    presence_rows: list[pd.DataFrame] = []
    destination_rows: list[pd.DataFrame] = []
    sequence_rows: list[pd.DataFrame] = []
    length_rows: list[pd.DataFrame] = []

    for scenario, plan in product(grouped["scenario"].unique(), PLANS):
        scenario_data = grouped[grouped["scenario"] == scenario]

        counts = _ranked(page_count(scenario_data, plan), "page_count")
        counts.insert(0, "subscription_type", plan)
        counts.insert(0, "scenario", scenario)
        page_count_rows.append(counts)

        presence = _ranked(page_presence(scenario_data, plan), "journey_presence")
        presence.insert(0, "subscription_type", plan)
        presence.insert(0, "scenario", scenario)
        presence_rows.append(presence)

        lengths = journey_length(scenario_data, plan)
        if lengths.empty:
            length_summary = pd.DataFrame(
                [{
                    "scenario": scenario,
                    "subscription_type": plan,
                    "journey_count": 0,
                    "avg_journey_length": 0.0,
                    "median_journey_length": 0.0,
                    "min_journey_length": 0,
                    "max_journey_length": 0,
                }]
            )
        else:
            length_summary = pd.DataFrame(
                [{
                    "scenario": scenario,
                    "subscription_type": plan,
                    "journey_count": len(lengths),
                    "avg_journey_length": round(float(lengths["journey_length"].mean()), 1),
                    "median_journey_length": round(float(lengths["journey_length"].median()), 1),
                    "min_journey_length": int(lengths["journey_length"].min()),
                    "max_journey_length": int(lengths["journey_length"].max()),
                }]
            )
        length_rows.append(length_summary)

        for page in DESTINATION_PAGES:
            destinations = _ranked(page_destinations(scenario_data, page, plan), "destination_count")
            destinations.insert(0, "source_page", page)
            destinations.insert(0, "subscription_type", plan)
            destinations.insert(0, "scenario", scenario)
            destination_rows.append(destinations)

        for sequence_length in SEQUENCE_LENGTHS:
            sequences = _ranked(page_sequences(scenario_data, sequence_length, plan), "journey_count")
            sequences.insert(0, "sequence_length", sequence_length)
            sequences.insert(0, "subscription_type", plan)
            sequences.insert(0, "scenario", scenario)
            sequence_rows.append(sequences)

    return {
        "mart_page_count": pd.concat(page_count_rows, ignore_index=True),
        "mart_page_presence": pd.concat(presence_rows, ignore_index=True),
        "mart_page_destinations": pd.concat(destination_rows, ignore_index=True),
        "mart_page_sequences": pd.concat(sequence_rows, ignore_index=True),
        "mart_journey_length": pd.concat(length_rows, ignore_index=True),
    }


def _quiz_answers(marts: dict[str, pd.DataFrame]) -> pd.DataFrame:
    page_count_mart = marts["mart_page_count"]
    destination_mart = marts["mart_page_destinations"]
    presence_mart = marts["mart_page_presence"]
    sequences_mart = marts["mart_page_sequences"]
    length_mart = marts["mart_journey_length"]

    def value_at(frame: pd.DataFrame, column: str, **filters: object) -> object:
        selected = frame.copy()
        for key, value in filters.items():
            selected = selected[selected[key] == value]
        if selected.empty:
            return None
        return selected.iloc[0][column]

    answers = [
        {
            "question": "Records after grouping first three sessions",
            "answer": int(value_at(length_mart, "journey_count", scenario="first_3_sessions", subscription_type="All")),
            "supporting_metric": "first_3_sessions grouped journeys",
        },
        {
            "question": "Third most popular page for quarterly users",
            "answer": value_at(page_count_mart, "page", scenario="all_sessions", subscription_type="Quarterly", rank=3),
            "supporting_metric": "page_count rank 3",
        },
        {
            "question": "Fourth most popular destination after Pricing",
            "answer": value_at(destination_mart, "next_page", scenario="all_sessions", subscription_type="All", source_page="Pricing", rank=4),
            "supporting_metric": "Pricing destination rank 4",
        },
        {
            "question": "Average journey length for last three sessions",
            "answer": value_at(length_mart, "avg_journey_length", scenario="last_3_sessions", subscription_type="All"),
            "supporting_metric": "last_3_sessions avg_journey_length",
        },
        {
            "question": "Fourth highest page presence for last three sessions",
            "answer": value_at(presence_mart, "page", scenario="last_3_sessions", subscription_type="All", rank=4),
            "supporting_metric": "page_presence rank 4",
        },
        {
            "question": "Most popular sequence of four pages count for last three sessions",
            "answer": int(value_at(sequences_mart, "journey_count", scenario="last_3_sessions", subscription_type="All", sequence_length=4, rank=1)),
            "supporting_metric": value_at(sequences_mart, "sequence", scenario="last_3_sessions", subscription_type="All", sequence_length=4, rank=1),
        },
    ]
    return pd.DataFrame(answers)


def _summary_kpis(raw: pd.DataFrame, grouped: pd.DataFrame) -> pd.DataFrame:
    all_sessions = grouped[grouped["scenario"] == "all_sessions"]
    return pd.DataFrame(
        [{
            "raw_rows": len(raw),
            "unique_users": raw["user_id"].nunique(),
            "unique_sessions": raw["session_id"].nunique(),
            "annual_users": all_sessions[all_sessions["subscription_type"] == "Annual"]["user_id"].nunique(),
            "monthly_users": all_sessions[all_sessions["subscription_type"] == "Monthly"]["user_id"].nunique(),
            "quarterly_users": all_sessions[all_sessions["subscription_type"] == "Quarterly"]["user_id"].nunique(),
            "avg_all_session_journey_length": round(float(all_sessions["journey_length"].mean()), 1),
        }]
    )


def _write_report(kpis: pd.DataFrame, quiz: pd.DataFrame, marts: dict[str, pd.DataFrame]) -> Path:
    ensure_project_dirs()
    kpi = kpis.iloc[0]
    top_page = marts["mart_page_count"].query("scenario == 'all_sessions' and subscription_type == 'All' and rank == 1").iloc[0]
    top_sequence = marts["mart_page_sequences"].query(
        "scenario == 'last_3_sessions' and subscription_type == 'All' and sequence_length == 4 and rank == 1"
    ).iloc[0]

    lines = [
        "# User Journey Analysis Report",
        "",
        "## Executive Summary",
        "",
        f"- Raw sessions: {int(kpi['raw_rows']):,}.",
        f"- Unique users: {int(kpi['unique_users']):,}.",
        f"- Subscription mix: {int(kpi['annual_users'])} Annual, {int(kpi['monthly_users'])} Monthly, {int(kpi['quarterly_users'])} Quarterly users.",
        f"- Top all-session page after preprocessing: {top_page['page']} ({int(top_page['page_count']):,} visits).",
        f"- Average all-session journey length after preprocessing: {kpi['avg_all_session_journey_length']} pages.",
        "",
        "## Business Findings",
        "",
        "- Checkout, Log in, Coupon, Homepage, and Sign up dominate late-stage journeys, so friction analysis should focus on conversion and account/payment steps.",
        "- Quarterly purchasers show Homepage, Log in, and Sign up as their top pages, suggesting a shorter evaluation pattern before purchase.",
        f"- The strongest four-page pattern in the last-three-session view is `{top_sequence['sequence']}`, appearing in {int(top_sequence['journey_count'])} journeys.",
        "",
        "## Quiz Answers",
        "",
    ]
    for index, row in quiz.iterrows():
        lines.append(f"{index + 1}. **{row['question']}:** {row['answer']}")

    lines.extend(
        [
            "",
            "## Reproducibility",
            "",
            "- Dashboard reads only `gold.*` marts.",
            "- Raw source files are treated as immutable inputs.",
            "- Session ordering uses `session_id` ascending because no timestamp exists.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def build_gold() -> dict[str, int]:
    with connect() as con:
        raw = con.execute("SELECT * FROM bronze.raw_user_journeys").fetchdf()
        grouped = con.execute("SELECT * FROM silver.grouped_journeys").fetchdf()
        con.execute("CREATE SCHEMA IF NOT EXISTS gold")

        marts = _metric_frames(grouped)
        kpis = _summary_kpis(raw, grouped)
        quiz = _quiz_answers(marts)

        write_dataframe(con, "gold", "mart_summary_kpis", kpis)
        for table, frame in marts.items():
            write_dataframe(con, "gold", table, frame)
        write_dataframe(con, "gold", "mart_quiz_answers", quiz)

        counts = {
            "mart_summary_kpis": len(kpis),
            **{table: len(frame) for table, frame in marts.items()},
            "mart_quiz_answers": len(quiz),
        }

    report_path = _write_report(kpis, quiz, marts)
    counts["report_written"] = int(report_path.exists())
    return counts


if __name__ == "__main__":
    counts = build_gold()
    for table, row_count in counts.items():
        print(f"{table}: {row_count}")
