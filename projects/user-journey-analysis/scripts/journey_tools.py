from __future__ import annotations

from collections import Counter
from typing import Iterable

import pandas as pd


VALID_PLANS = ("Annual", "Monthly", "Quarterly")


def split_journey(journey: object) -> list[str]:
    if pd.isna(journey):
        return []
    return [page for page in str(journey).split("-") if page != ""]


def join_pages(pages: Iterable[str]) -> str:
    return "-".join(pages)


def remove_page_duplicates(data: pd.DataFrame, target_column: str = "user_journey") -> pd.DataFrame:
    cleaned = data.copy(deep=True)

    def compress(journey: object) -> str:
        pages = split_journey(journey)
        deduped: list[str] = []
        for page in pages:
            if not deduped or deduped[-1] != page:
                deduped.append(page)
        return join_pages(deduped)

    cleaned[target_column] = cleaned[target_column].map(compress)
    return cleaned


def group_by(
    data: pd.DataFrame,
    group_column: str = "user_id",
    target_column: str = "user_journey",
    sessions: int | str = "All",
    count_from: str = "last",
) -> pd.DataFrame:
    if sessions != "All":
        sessions = int(sessions)
        if sessions < 1:
            raise ValueError("sessions must be 'All' or a positive integer")
    if count_from not in {"first", "last"}:
        raise ValueError("count_from must be either 'first' or 'last'")

    ordered = data.sort_values([group_column, "session_id"]).copy(deep=True)
    rows: list[dict[str, object]] = []

    for group_value, group in ordered.groupby(group_column, sort=True):
        selected = group
        if sessions != "All":
            selected = group.head(sessions) if count_from == "first" else group.tail(sessions)

        row: dict[str, object] = {
            group_column: group_value,
            target_column: join_pages(selected[target_column].tolist()),
            "session_count": int(len(selected)),
        }
        if "subscription_type" in selected.columns:
            row["subscription_type"] = selected["subscription_type"].iloc[0]
        rows.append(row)

    return pd.DataFrame(rows)


def remove_pages(
    data: pd.DataFrame,
    pages: list[str],
    target_column: str = "user_journey",
) -> pd.DataFrame:
    cleaned = data.copy(deep=True)
    page_set = set(pages)
    cleaned[target_column] = cleaned[target_column].map(
        lambda journey: join_pages(page for page in split_journey(journey) if page not in page_set)
    )
    return cleaned


def _filter_plan(data: pd.DataFrame, plan: str = "All") -> pd.DataFrame:
    if plan == "All":
        return data
    return data[data["subscription_type"] == plan]


def page_count(data: pd.DataFrame, plan: str = "All", target_column: str = "user_journey") -> pd.DataFrame:
    filtered = _filter_plan(data, plan)
    counts: Counter[str] = Counter()
    for journey in filtered[target_column]:
        counts.update(split_journey(journey))
    return pd.DataFrame(counts.most_common(), columns=["page", "page_count"])


def page_presence(data: pd.DataFrame, plan: str = "All", target_column: str = "user_journey") -> pd.DataFrame:
    filtered = _filter_plan(data, plan)
    counts: Counter[str] = Counter()
    for journey in filtered[target_column]:
        counts.update(set(split_journey(journey)))
    return pd.DataFrame(counts.most_common(), columns=["page", "journey_presence"])


def page_destinations(
    data: pd.DataFrame,
    page: str,
    plan: str = "All",
    target_column: str = "user_journey",
) -> pd.DataFrame:
    filtered = _filter_plan(data, plan)
    counts: Counter[str] = Counter()
    for journey in filtered[target_column]:
        pages = split_journey(journey)
        for current, next_page in zip(pages, pages[1:]):
            if current == page:
                counts[next_page] += 1
    return pd.DataFrame(counts.most_common(), columns=["next_page", "destination_count"])


def page_sequences(
    data: pd.DataFrame,
    n: int,
    plan: str = "All",
    target_column: str = "user_journey",
) -> pd.DataFrame:
    if n < 1:
        raise ValueError("n must be a positive integer")

    filtered = _filter_plan(data, plan)
    counts: Counter[str] = Counter()
    for journey in filtered[target_column]:
        pages = split_journey(journey)
        seen = {join_pages(pages[index : index + n]) for index in range(max(0, len(pages) - n + 1))}
        counts.update(seen)
    return pd.DataFrame(counts.most_common(), columns=["sequence", "journey_count"])


def journey_length(data: pd.DataFrame, plan: str = "All", target_column: str = "user_journey") -> pd.DataFrame:
    filtered = _filter_plan(data, plan).copy()
    filtered["journey_length"] = filtered[target_column].map(lambda journey: len(split_journey(journey)))
    return filtered[["user_id", "subscription_type", "journey_length"]]
