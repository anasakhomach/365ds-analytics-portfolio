from __future__ import annotations

from pathlib import Path

import streamlit as st
from streamlit.testing.v1 import AppTest


REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_SLUGS = (
    "real-estate-market-analysis",
    "user-journey-analysis",
    "checkout-flow-optimization",
    "customer-engagement-analysis",
    "tracking-user-engagement",
)


def test_project_dashboards_do_not_share_cached_query_results() -> None:
    st.cache_data.clear()
    failures: dict[str, list[str]] = {}

    for slug in PROJECT_SLUGS:
        dashboard = REPO_ROOT / "projects" / slug / "dashboard" / "app.py"
        app = AppTest.from_file(str(dashboard)).run(timeout=30)
        errors = [exception.value for exception in app.exception]
        if errors:
            failures[slug] = errors

    assert failures == {}
