from __future__ import annotations

import pandas as pd

from common import connect, write_dataframe
from journey_tools import group_by, remove_page_duplicates, remove_pages, split_journey


SCENARIOS = [
    ("all_sessions", "All", "last"),
    ("first_3_sessions", 3, "first"),
    ("last_3_sessions", 3, "last"),
    ("first_10_sessions", 10, "first"),
    ("last_10_sessions", 10, "last"),
]


def _clean_sessions(raw: pd.DataFrame) -> pd.DataFrame:
    sessions = raw.copy(deep=True)
    sessions["user_id"] = pd.to_numeric(sessions["user_id"], errors="raise").astype("int64")
    sessions["session_id"] = pd.to_numeric(sessions["session_id"], errors="raise").astype("int64")
    sessions["subscription_type"] = sessions["subscription_type"].astype("string").str.strip()
    sessions["user_journey"] = sessions["user_journey"].astype("string").str.strip()
    sessions["raw_journey_length"] = sessions["user_journey"].map(lambda journey: len(split_journey(journey))).astype("int64")
    return sessions.sort_values(["user_id", "session_id"]).reset_index(drop=True)


def _build_grouped_scenarios(sessions: pd.DataFrame) -> pd.DataFrame:
    scenario_frames: list[pd.DataFrame] = []
    for scenario_name, session_count, count_from in SCENARIOS:
        grouped = group_by(
            sessions,
            group_column="user_id",
            target_column="user_journey",
            sessions=session_count,
            count_from=count_from,
        )
        grouped = remove_pages(grouped, pages=[], target_column="user_journey")
        grouped = remove_page_duplicates(grouped, target_column="user_journey")
        grouped.insert(0, "scenario", scenario_name)
        grouped["journey_length"] = grouped["user_journey"].map(lambda journey: len(split_journey(journey))).astype("int64")
        scenario_frames.append(grouped)
    return pd.concat(scenario_frames, ignore_index=True)


def build_silver() -> dict[str, int]:
    with connect() as con:
        raw = con.execute("SELECT * FROM bronze.raw_user_journeys").fetchdf()
        sessions = _clean_sessions(raw)
        grouped = _build_grouped_scenarios(sessions)

        write_dataframe(con, "silver", "cleaned_sessions", sessions)
        write_dataframe(con, "silver", "grouped_journeys", grouped)

        return {
            "cleaned_sessions": len(sessions),
            "grouped_journeys": len(grouped),
        }


if __name__ == "__main__":
    counts = build_silver()
    for table, row_count in counts.items():
        print(f"{table}: {row_count} rows")
