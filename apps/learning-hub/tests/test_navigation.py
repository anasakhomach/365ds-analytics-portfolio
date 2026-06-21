from __future__ import annotations

import sys
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.navigation import CORE_PAGES, PROJECT_PAGES, navigation_errors


def test_navigation_has_stable_unique_pathnames() -> None:
    pages = (*CORE_PAGES, *PROJECT_PAGES)
    paths = [page.url_path for page in pages]

    assert len(paths) == len(set(paths))
    assert set(paths) == {
        "",
        "projects",
        "real-estate",
        "user-journey",
        "checkout-flow",
        "customer-engagement",
        "tracking-engagement",
        "ai-helper",
        "quiz-data",
        "lineage",
    }
    assert all("/" not in path for path in paths)


def test_navigation_includes_all_five_project_dashboards() -> None:
    assert {page.key for page in PROJECT_PAGES} == {
        "real-estate-market-analysis",
        "user-journey-analysis",
        "checkout-flow-optimization",
        "customer-engagement-analysis",
        "tracking-user-engagement",
    }
    assert navigation_errors() == []

