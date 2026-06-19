from __future__ import annotations

from pathlib import Path

import pandas as pd

from common import REPORT_DIR, connect, ensure_project_dirs, read_sql, script_path


REPORT_PATH = REPORT_DIR / "customer_engagement_analysis_report.md"
GOLD_TABLES = (
    "mart_student_engagement",
    "mart_course_performance",
    "mart_monthly_engagement",
    "mart_monthly_registrations",
    "mart_country_registered",
    "mart_country_minutes",
    "mart_summary_kpis",
    "mart_quiz_answers",
)


def _fmt_number(value: float) -> str:
    return f"{value:,.0f}"


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _write_report(
    kpis: pd.DataFrame,
    courses: pd.DataFrame,
    monthly: pd.DataFrame,
    countries_registered: pd.DataFrame,
    countries_minutes: pd.DataFrame,
    quiz: pd.DataFrame,
) -> Path:
    ensure_project_dirs()
    kpi = kpis.iloc[0]
    top_course = courses.iloc[0]
    top_registered_country = countries_registered.iloc[0]
    top_minutes_country = countries_minutes.iloc[0]
    peak_minutes = monthly.sort_values(["total_minutes_watched", "watched_month"], ascending=[False, True]).iloc[0]
    peak_average = monthly.sort_values(["average_minutes_watched", "watched_month"], ascending=[False, True]).iloc[0]

    lines = [
        "# Customer Engagement Analysis Report",
        "",
        "## Executive Summary",
        "",
        f"- Registered students: {_fmt_number(float(kpi['registered_students']))}.",
        f"- Onboarded students: {_fmt_number(float(kpi['onboarded_students']))} ({_pct(float(kpi['onboarding_rate']))}).",
        f"- Total minutes watched: {_fmt_number(float(kpi['total_minutes_watched']))}.",
        f"- Average minutes watched per engaged student: {float(kpi['average_minutes_watched']):,.2f}.",
        f"- Paying students watch about {float(kpi['paid_to_free_average_ratio']):.2f}x more minutes than free-plan students on the average-minutes KPI.",
        "",
        "## Current State",
        "",
        f"- Most watched course: `{top_course['course_title']}` with {_fmt_number(float(top_course['total_minutes_watched']))} minutes watched and an average rating of {float(top_course['average_rating']):.2f}.",
        f"- Peak monthly total engagement: {peak_minutes['watched_month']:%B %Y} with {_fmt_number(float(peak_minutes['total_minutes_watched']))} minutes for `{peak_minutes['user_type']}` students.",
        f"- Peak monthly average engagement: {peak_average['watched_month']:%B %Y} with {float(peak_average['average_minutes_watched']):,.2f} average minutes for `{peak_average['user_type']}` students.",
        f"- Top country by registered students: {top_registered_country['country_name']} ({_fmt_number(float(top_registered_country['registered_students']))}).",
        f"- Top country by minutes watched: {top_minutes_country['country_name']} ({_fmt_number(float(top_minutes_country['total_minutes_watched']))} minutes).",
        "",
        "## Interpretation",
        "",
        "- Introductory analytics courses dominate total watch time, showing strong demand for broad entry points into the platform.",
        "- Paying students have much deeper average engagement, so conversion and retention work should focus on moving motivated free users into paid learning paths.",
        "- Country rankings by registered students and watched minutes are related but not identical, so acquisition volume should be evaluated together with realized engagement.",
        "",
        "## Recommendations",
        "",
        "- Promote the strongest introductory courses as onboarding paths, then route students into adjacent paid curricula.",
        "- Track monthly seasonality by student type so paid engagement dips can trigger targeted lifecycle campaigns.",
        "- Pair country acquisition metrics with minutes-watched metrics before deciding where to scale marketing spend.",
        "",
        "## Quiz Support",
        "",
    ]
    for _, row in quiz.iterrows():
        lines.append(f"{int(row['question_number'])}. **{row['question']}:** {row['answer_value']} ({row['answer_basis']}; support: {row['support_value']})")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Question 10 is truncated in the converted project brief, so the report records the data-derived paid/free average-minutes ratio.",
            "- Tableau requirements are translated into Streamlit pages backed only by Gold marts.",
            "- Raw MySQL dump files remain immutable under `source-datasets/`.",
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
        courses = con.execute("SELECT * FROM gold.mart_course_performance ORDER BY course_rank").fetchdf()
        monthly = con.execute("SELECT * FROM gold.mart_monthly_engagement ORDER BY watched_month, user_type").fetchdf()
        countries_registered = con.execute(
            """
            SELECT
                country_name,
                COUNT(DISTINCT student_id) AS registered_students
            FROM gold.mart_student_engagement
            GROUP BY country_name
            ORDER BY registered_students DESC, country_name
            """
        ).fetchdf()
        countries_minutes = con.execute(
            """
            SELECT
                country_name,
                ROUND(SUM(minutes_watched), 2) AS total_minutes_watched
            FROM gold.mart_student_engagement
            WHERE date_watched IS NOT NULL
            GROUP BY country_name
            ORDER BY total_minutes_watched DESC, country_name
            """
        ).fetchdf()
        quiz = con.execute("SELECT * FROM gold.mart_quiz_answers ORDER BY question_number").fetchdf()

    report_path = _write_report(kpis, courses, monthly, countries_registered, countries_minutes, quiz)
    counts["report_written"] = int(report_path.exists())
    return counts


if __name__ == "__main__":
    for table, row_count in build_gold().items():
        print(f"{table}: {row_count}")
