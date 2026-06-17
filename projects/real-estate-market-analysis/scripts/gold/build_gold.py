from __future__ import annotations

from pathlib import Path

import pandas as pd

from common import PROJECT_DIR, REPORT_DIR, connect, ensure_project_dirs


SQL_PATH = Path(__file__).with_name("create_marts.sql")
REPORT_PATH = REPORT_DIR / "real_estate_market_analysis_report.md"


def _currency(value: float | int | None) -> str:
    if pd.isna(value):
        return "n/a"
    return f"${value:,.0f}"


def _number(value: float | int | None, digits: int = 2) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value:,.{digits}f}"


def _top_value(df: pd.DataFrame, column: str) -> str:
    if df.empty:
        return "n/a"
    return str(df.iloc[0][column])


def write_report() -> Path:
    ensure_project_dirs()
    with connect(read_only=True) as con:
        kpis = con.execute("SELECT * FROM gold.mart_summary_kpis").fetchdf().iloc[0]
        building = con.execute("SELECT * FROM gold.mart_building_performance ORDER BY sold_properties DESC, building_id").fetchdf()
        country = con.execute("SELECT * FROM gold.mart_country_performance ORDER BY avg_deal_satisfaction DESC, country").fetchdf()
        state = con.execute("SELECT * FROM gold.mart_state_distribution ORDER BY sold_properties DESC, state").fetchdf()
        age = con.execute("SELECT * FROM gold.mart_age_intervals ORDER BY sold_properties DESC").fetchdf()
        price = con.execute("SELECT * FROM gold.mart_price_intervals ORDER BY max_price DESC").fetchdf()
        revenue_year = con.execute(
            """
            SELECT sale_year, SUM(total_revenue) AS total_revenue
            FROM gold.mart_yearly_sales_by_building
            GROUP BY sale_year
            ORDER BY total_revenue DESC
            """
        ).fetchdf()

    second_state = state.iloc[1]["state"] if len(state) > 1 else "n/a"
    top_age = _top_value(age, "age_interval")
    top_building = _top_value(building, "building_label")
    highest_satisfaction_country = _top_value(country, "country")
    top_revenue_year = str(revenue_year.iloc[0]["sale_year"]) if not revenue_year.empty else "n/a"
    top_price_interval_available = int(price.iloc[0]["available_properties"]) if not price.empty else 0

    lines = [
        "# Real Estate Market Analysis Report",
        "",
        "## Executive Summary",
        "",
        f"- Portfolio size: {int(kpis['total_properties'])} properties, with {int(kpis['sold_properties'])} sold and {int(kpis['available_properties'])} still available.",
        f"- Total sold-property revenue: {_currency(kpis['total_revenue'])}.",
        f"- Average sold price: {_currency(kpis['avg_sold_price'])}; average sold area: {_number(kpis['avg_sold_area'])} sq ft.",
        f"- Average deal satisfaction: {_number(kpis['avg_deal_satisfaction'])}/5.",
        f"- Customer age and property price correlation: {_number(kpis['age_price_correlation'], 4)}.",
        "",
        "## Business Findings",
        "",
        f"- Most common sold building group: {top_building}.",
        f"- Second-highest state by sold-property count: {second_state}.",
        f"- Most common customer age interval among known individual buyers: {top_age}.",
        f"- Highest average satisfaction country: {highest_satisfaction_country}.",
        f"- Highest revenue year: {top_revenue_year}.",
        f"- Available properties in the highest price interval: {top_price_interval_available}.",
        "",
        "## Interpretation",
        "",
        "The dataset is concentrated in US residential apartment sales, especially California. Buyer age and property price show only a weak relationship, so development strategy should emphasize geography, building performance, and price bands more than age alone.",
        "",
        "## Reproducibility",
        "",
        f"- Warehouse: `{PROJECT_DIR / 'warehouse.duckdb'}`",
        "- Dashboard reads only `gold.*` marts.",
        "- Raw files are treated as immutable source inputs.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def build_gold() -> dict[str, int]:
    with connect() as con:
        con.execute(SQL_PATH.read_text(encoding="utf-8"))
        tables = [
            "mart_property_transactions",
            "mart_summary_kpis",
            "mart_building_performance",
            "mart_country_performance",
            "mart_state_distribution",
            "mart_age_intervals",
            "mart_price_intervals",
            "mart_monthly_revenue",
            "mart_yearly_sales_by_building",
            "mart_correlation_metrics",
        ]
        counts = {
            table: con.execute(f"SELECT COUNT(*) FROM gold.{table}").fetchone()[0]
            for table in tables
        }

    report_path = write_report()
    counts["report_written"] = int(report_path.exists())
    return counts


if __name__ == "__main__":
    counts = build_gold()
    for table, row_count in counts.items():
        print(f"{table}: {row_count}")
