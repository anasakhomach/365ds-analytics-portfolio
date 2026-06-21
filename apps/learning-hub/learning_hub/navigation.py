from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .paths import APP_DIR


@dataclass(frozen=True)
class PageDefinition:
    key: str
    title: str
    url_path: str
    icon: str
    source: str | None = None


CORE_PAGES = (
    PageDefinition("overview", "Portfolio Overview", "", ":material/home:"),
    PageDefinition("projects", "Project Explorer", "projects", ":material/folder_open:"),
    PageDefinition("ai-helper", "AI Learning Helper", "ai-helper", ":material/chat:"),
    PageDefinition("quiz-data", "Quiz And Data Coach", "quiz-data", ":material/query_stats:"),
    PageDefinition("lineage", "Architecture And Lineage", "lineage", ":material/account_tree:"),
)


PROJECT_PAGES = (
    PageDefinition(
        "real-estate-market-analysis",
        "Real Estate Market Analysis",
        "real-estate",
        ":material/apartment:",
        "../../projects/real-estate-market-analysis/dashboard/app.py",
    ),
    PageDefinition(
        "user-journey-analysis",
        "User Journey Analysis",
        "user-journey",
        ":material/route:",
        "../../projects/user-journey-analysis/dashboard/app.py",
    ),
    PageDefinition(
        "checkout-flow-optimization",
        "Checkout Flow Optimization",
        "checkout-flow",
        ":material/shopping_cart_checkout:",
        "../../projects/checkout-flow-optimization/dashboard/app.py",
    ),
    PageDefinition(
        "customer-engagement-analysis",
        "Customer Engagement Analysis",
        "customer-engagement",
        ":material/groups:",
        "../../projects/customer-engagement-analysis/dashboard/app.py",
    ),
    PageDefinition(
        "tracking-user-engagement",
        "Tracking User Engagement",
        "tracking-engagement",
        ":material/monitoring:",
        "../../projects/tracking-user-engagement/dashboard/app.py",
    ),
)


def page_source(page: PageDefinition) -> Path:
    if page.source is None:
        raise ValueError(f"Page {page.key!r} has no file source.")
    return (APP_DIR / page.source).resolve()


def navigation_errors() -> list[str]:
    errors: list[str] = []
    pages = (*CORE_PAGES, *PROJECT_PAGES)
    paths = [page.url_path for page in pages]
    if len(paths) != len(set(paths)):
        errors.append("Navigation URL paths must be unique.")

    for page in PROJECT_PAGES:
        source = page_source(page)
        if not source.is_file():
            errors.append(f"Missing page source for {page.key}: {source}")
    return errors
