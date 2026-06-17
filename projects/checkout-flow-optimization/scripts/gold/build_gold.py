from __future__ import annotations

from pathlib import Path

import pandas as pd

from common import REPORT_DIR, connect, ensure_project_dirs, read_sql, script_path


REPORT_PATH = REPORT_DIR / "checkout_flow_optimization_report.md"
GOLD_TABLES = (
    "mart_daily_checkout_steps",
    "mart_monthly_checkout",
    "mart_checkout_errors",
    "mart_error_rankings",
    "mart_device_distribution",
    "mart_monthly_error_device",
    "mart_summary_kpis",
    "mart_quiz_answers",
)


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _write_report(
    kpis: pd.DataFrame,
    monthly: pd.DataFrame,
    errors: pd.DataFrame,
    quiz: pd.DataFrame,
) -> Path:
    ensure_project_dirs()
    kpi = kpis.iloc[0]
    best_success = monthly.sort_values(["checkout_success_rate", "checkout_month"], ascending=[False, True]).iloc[0]
    worst_abandonment = monthly.sort_values(["cart_abandonment_rate", "checkout_month"], ascending=[False, True]).iloc[0]
    top_error = errors.iloc[0]

    lines = [
        "# Checkout Flow Optimization Report",
        "",
        "## Executive Summary",
        "",
        f"- Analysis window: July 2022 through January 2023.",
        f"- Total carts: {int(kpi['total_carts']):,}.",
        f"- Total checkout attempts: {int(kpi['total_checkout_attempts']):,}.",
        f"- Successful checkout attempts: {int(kpi['successful_checkout_attempts']):,}.",
        f"- Overall checkout success rate: {_pct(float(kpi['checkout_success_rate']))}.",
        f"- Course-formula cart abandonment rate: {_pct(float(kpi['cart_abandonment_rate']))}.",
        "",
        "## Current State",
        "",
        f"- Highest success-rate month: {best_success['checkout_month']:%B %Y} at {_pct(float(best_success['checkout_success_rate']))}.",
        f"- Highest abandonment-rate month: {worst_abandonment['checkout_month']:%B %Y} at {_pct(float(worst_abandonment['cart_abandonment_rate']))}.",
        f"- Most common checkout error: `{top_error['error_message']}` with {int(top_error['total_attempts']):,} attempts.",
        "- November 2022 has more checkout attempts than carts under the course formula, so the report keeps the formula visible and does not clamp negative abandonment.",
        "",
        "## Business Objective",
        "",
        "Improve checkout completion by reducing preventable payment failures and making card-entry feedback clearer across desktop and mobile.",
        "",
        "## Hypothesis",
        "",
        "Most friction comes from payment-form validation and card-decline states. Better real-time validation, clearer field labels, and alternate payment options should lift successful checkout attempts.",
        "",
        "## Actionable Insights",
        "",
        "- Add real-time validation for card number, expiry year, CVV, ZIP, and required-name fields before payment submission.",
        "- Review mobile checkout form sizing and keyboard behavior because device mix materially affects error exposure.",
        "- Add alternate payment options and clearer issuer-decline messaging for declined-card errors.",
        "",
        "## Quiz Support",
        "",
    ]
    for _, row in quiz.iterrows():
        lines.append(f"{int(row['question_number'])}. **{row['question']}:** {row['answer_value']} ({row['answer_basis']}; support: {row['support_value']})")

    lines.extend(
        [
            "",
            "## Quiz Option Note",
            "",
            "- Several data-derived answers do not match the multiple-choice options in the converted project brief. The SQL marts keep the visible CTE logic and raw dump counts as the source of truth.",
            "- The opportunity-sizing question is calculated from the prompt assumptions rather than the observed January data.",
            "",
            "## Reproducibility",
            "",
            "- Dashboard reads only `gold.*` marts.",
            "- Raw MySQL dump remains immutable under `source-datasets/`.",
            "- DuckDB is canonical; MySQL CLI is reserved for validation if dump behavior diverges.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def build_gold() -> dict[str, int]:
    with connect() as con:
        con.execute(read_sql(script_path("gold", "build_gold.sql")))
        counts = {
            table: con.execute(f"SELECT COUNT(*) FROM gold.{table}").fetchone()[0]
            for table in GOLD_TABLES
        }
        kpis = con.execute("SELECT * FROM gold.mart_summary_kpis").fetchdf()
        monthly = con.execute("SELECT * FROM gold.mart_monthly_checkout").fetchdf()
        errors = con.execute("SELECT * FROM gold.mart_error_rankings ORDER BY rank").fetchdf()
        quiz = con.execute("SELECT * FROM gold.mart_quiz_answers ORDER BY question_number").fetchdf()

    report_path = _write_report(kpis, monthly, errors, quiz)
    counts["report_written"] = int(report_path.exists())
    return counts


if __name__ == "__main__":
    for table, row_count in build_gold().items():
        print(f"{table}: {row_count}")
