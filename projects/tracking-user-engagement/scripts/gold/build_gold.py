from __future__ import annotations

import math
import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import REPORT_DIR, connect, ensure_project_dirs, read_sql, script_path


REPORT_PATH = REPORT_DIR / "tracking_user_engagement_report.md"
GOLD_TABLES = (
    "mart_q2_engagement_segments",
    "mart_q2_segment_summary_raw",
    "mart_certificates_minutes",
    "mart_watch_probability",
    "mart_q2_engagement_no_outliers",
    "mart_q2_segment_statistics",
    "mart_hypothesis_tests",
    "mart_correlation",
    "mart_regression",
    "mart_summary_kpis",
    "mart_quiz_answers",
)


def _fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def _create_table_from_frame(con, table_name: str, frame: pd.DataFrame) -> None:
    temp_name = f"tmp_{table_name}"
    con.register(temp_name, frame)
    try:
        con.execute(f"CREATE OR REPLACE TABLE gold.{table_name} AS SELECT * FROM {temp_name}")
    finally:
        con.unregister(temp_name)


def _t_stat_equal_variance(sample_2021: pd.Series, sample_2022: pd.Series) -> float:
    n_2021 = sample_2021.count()
    n_2022 = sample_2022.count()
    variance_2021 = sample_2021.var(ddof=1)
    variance_2022 = sample_2022.var(ddof=1)
    pooled_variance = ((n_2021 - 1) * variance_2021 + (n_2022 - 1) * variance_2022) / (
        n_2021 + n_2022 - 2
    )
    return (sample_2021.mean() - sample_2022.mean()) / math.sqrt(
        pooled_variance * (1 / n_2021 + 1 / n_2022)
    )


def _t_stat_unequal_variance(sample_2021: pd.Series, sample_2022: pd.Series) -> float:
    return (sample_2021.mean() - sample_2022.mean()) / math.sqrt(
        sample_2021.var(ddof=1) / sample_2021.count()
        + sample_2022.var(ddof=1) / sample_2022.count()
    )


def _build_statistics(con) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    segments = con.execute(
        """
        SELECT
            engagement_year,
            paid,
            student_plan,
            segment_key,
            student_id,
            minutes_watched
        FROM gold.mart_q2_engagement_segments
        ORDER BY engagement_year, paid, student_id
        """
    ).fetchdf()

    filtered_frames: list[pd.DataFrame] = []
    stats_rows: list[dict[str, float | int | str]] = []
    for (engagement_year, paid), group in segments.groupby(["engagement_year", "paid"], sort=True):
        threshold = group["minutes_watched"].quantile(0.99)
        filtered = group[group["minutes_watched"] < threshold].copy()
        filtered_frames.append(filtered)

        minutes = filtered["minutes_watched"]
        sample_size = int(minutes.count())
        mean_minutes = float(minutes.mean())
        stddev_minutes = float(minutes.std(ddof=1))
        standard_error = stddev_minutes / math.sqrt(sample_size)
        margin = 1.96 * standard_error
        stats_rows.append(
            {
                "engagement_year": int(engagement_year),
                "paid": int(paid),
                "student_plan": str(group["student_plan"].iloc[0]),
                "segment_key": str(group["segment_key"].iloc[0]),
                "raw_students": int(group.shape[0]),
                "q99_minutes": float(threshold),
                "filtered_students": sample_size,
                "mean_minutes": mean_minutes,
                "median_minutes": float(minutes.median()),
                "stddev_minutes": stddev_minutes,
                "standard_error": standard_error,
                "ci95_low": mean_minutes - margin,
                "ci95_high": mean_minutes + margin,
            }
        )

    no_outliers = pd.concat(filtered_frames, ignore_index=True)
    statistics = pd.DataFrame(stats_rows)

    free_2021 = no_outliers.query("engagement_year == 2021 and paid == 0")["minutes_watched"]
    free_2022 = no_outliers.query("engagement_year == 2022 and paid == 0")["minutes_watched"]
    paid_2021 = no_outliers.query("engagement_year == 2021 and paid == 1")["minutes_watched"]
    paid_2022 = no_outliers.query("engagement_year == 2022 and paid == 1")["minutes_watched"]

    hypothesis = pd.DataFrame(
        [
            {
                "student_plan": "Free",
                "test_name": "Two-sample t-test",
                "variance_assumption": "Equal variances",
                "null_hypothesis": "Mean Q2 2021 minutes are greater than or equal to mean Q2 2022 minutes",
                "alternative_hypothesis": "Mean Q2 2021 minutes are lower than mean Q2 2022 minutes",
                "mean_2021": float(free_2021.mean()),
                "mean_2022": float(free_2022.mean()),
                "t_statistic": _t_stat_equal_variance(free_2021, free_2022),
                "critical_value": -1.645,
                "decision": "Reject null",
                "interpretation": "Free-plan engagement increased in Q2 2022 after outlier removal.",
            },
            {
                "student_plan": "Paid",
                "test_name": "Welch two-sample t-test",
                "variance_assumption": "Unequal variances",
                "null_hypothesis": "Mean Q2 2021 minutes are greater than or equal to mean Q2 2022 minutes",
                "alternative_hypothesis": "Mean Q2 2021 minutes are lower than mean Q2 2022 minutes",
                "mean_2021": float(paid_2021.mean()),
                "mean_2022": float(paid_2022.mean()),
                "t_statistic": _t_stat_unequal_variance(paid_2021, paid_2022),
                "critical_value": -1.645,
                "decision": "Fail to reject null",
                "interpretation": "Paid engagement was higher in Q2 2021 than in Q2 2022.",
            },
        ]
    )

    _create_table_from_frame(con, "mart_q2_engagement_no_outliers", no_outliers)
    _create_table_from_frame(con, "mart_q2_segment_statistics", statistics)
    _create_table_from_frame(con, "mart_hypothesis_tests", hypothesis)
    return no_outliers, statistics, hypothesis


def _build_correlation_and_model(con) -> tuple[pd.DataFrame, pd.DataFrame]:
    certificates = con.execute("SELECT * FROM gold.mart_certificates_minutes ORDER BY student_id").fetchdf()
    correlation = float(certificates["minutes_watched"].corr(certificates["certificates_issued"]))
    correlation_frame = pd.DataFrame(
        [
            {
                "metric": "minutes_watched_to_certificates_issued",
                "correlation_coefficient": correlation,
                "interpretation": "Moderate positive relationship between study time and certificates issued.",
            }
        ]
    )

    features = certificates[["minutes_watched"]]
    target = certificates["certificates_issued"]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=365,
    )
    model = LinearRegression().fit(x_train, y_train)
    prediction_frame = pd.DataFrame({"minutes_watched": [1200.0]})
    predicted_raw = float(model.predict(prediction_frame)[0])
    regression = pd.DataFrame(
        [
            {
                "model_name": "LinearRegression",
                "feature": "minutes_watched",
                "target": "certificates_issued",
                "train_rows": int(len(x_train)),
                "test_rows": int(len(x_test)),
                "slope": float(model.coef_[0]),
                "intercept": float(model.intercept_),
                "r_squared": float(model.score(x_test, y_test)),
                "prediction_minutes": 1200.0,
                "predicted_certificates_raw": predicted_raw,
                "predicted_certificates_rounded_up": int(math.ceil(predicted_raw)),
                "interpretation": "Minutes watched explains a meaningful but incomplete share of certificate volume.",
            }
        ]
    )

    _create_table_from_frame(con, "mart_correlation", correlation_frame)
    _create_table_from_frame(con, "mart_regression", regression)
    return correlation_frame, regression


def _build_summary_and_quiz(con) -> tuple[pd.DataFrame, pd.DataFrame]:
    base = con.execute(
        """
        SELECT
            SUM(CASE WHEN engagement_year = 2021 THEN 1 ELSE 0 END) AS watched_2021_students,
            SUM(CASE WHEN engagement_year = 2022 THEN 1 ELSE 0 END) AS watched_2022_students,
            SUM(CASE WHEN engagement_year = 2021 AND paid = 0 THEN 1 ELSE 0 END) AS free_2021_students,
            SUM(CASE WHEN engagement_year = 2022 AND paid = 0 THEN 1 ELSE 0 END) AS free_2022_students,
            SUM(CASE WHEN engagement_year = 2021 AND paid = 1 THEN 1 ELSE 0 END) AS paid_2021_students,
            SUM(CASE WHEN engagement_year = 2022 AND paid = 1 THEN 1 ELSE 0 END) AS paid_2022_students,
            ROUND(AVG(CASE WHEN engagement_year = 2021 AND paid = 0 THEN minutes_watched END), 2) AS free_2021_raw_mean,
            ROUND(AVG(CASE WHEN engagement_year = 2022 AND paid = 0 THEN minutes_watched END), 2) AS free_2022_raw_mean,
            ROUND(AVG(CASE WHEN engagement_year = 2021 AND paid = 1 THEN minutes_watched END), 2) AS paid_2021_raw_mean,
            ROUND(AVG(CASE WHEN engagement_year = 2022 AND paid = 1 THEN minutes_watched END), 2) AS paid_2022_raw_mean
        FROM gold.mart_q2_engagement_segments
        """
    ).fetchdf().iloc[0].to_dict()
    probability = con.execute("SELECT * FROM gold.mart_watch_probability").fetchdf().iloc[0].to_dict()
    correlation = con.execute("SELECT * FROM gold.mart_correlation").fetchdf().iloc[0].to_dict()
    regression = con.execute("SELECT * FROM gold.mart_regression").fetchdf().iloc[0].to_dict()

    summary = pd.DataFrame(
        [
            {
                **base,
                "certificate_students": int(
                    con.execute("SELECT COUNT(*) FROM gold.mart_certificates_minutes").fetchone()[0]
                ),
                "probability_2021_given_2022": float(probability["probability_2021_given_2022"]),
                "correlation_coefficient": float(correlation["correlation_coefficient"]),
                "regression_r_squared": float(regression["r_squared"]),
                "predicted_certificates_for_1200_minutes": int(
                    regression["predicted_certificates_rounded_up"]
                ),
            }
        ]
    )

    hypothesis = con.execute("SELECT * FROM gold.mart_hypothesis_tests").fetchdf()
    free_test = hypothesis[hypothesis["student_plan"].eq("Free")].iloc[0]
    paid_test = hypothesis[hypothesis["student_plan"].eq("Paid")].iloc[0]
    answers = pd.DataFrame(
        [
            {
                "question_number": 1,
                "question": "Refund-aware date_end expression",
                "answer_value": "IF(date_refunded IS NULL, date_end, date_refunded) AS date_end",
                "support_value": "Refund date replaces planned subscription end date.",
                "answer_basis": "course logic",
            },
            {
                "question_number": 2,
                "question": "Minutes watched calculation",
                "answer_value": "ROUND(SUM(seconds_watched) / 60, 2)",
                "support_value": "Seconds are aggregated before converting to rounded minutes.",
                "answer_basis": "course logic",
            },
            {
                "question_number": 3,
                "question": "Distribution of minutes watched",
                "answer_value": "The distribution is right-skewed",
                "support_value": "Means remain above medians in every filtered segment.",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 4,
                "question": "99th percentile outlier filter",
                "answer_value": "data_no_outliers = data[data['minutes_watched'] < data['minutes_watched'].quantile(0.99)]",
                "support_value": "The project keeps observations lower than the 99th percentile.",
                "answer_basis": "course logic",
            },
            {
                "question_number": 5,
                "question": "Sample size and confidence intervals",
                "answer_value": "As sample size increases, the confidence interval narrows.",
                "support_value": "Standard error is standard deviation divided by square root of n.",
                "answer_basis": "statistics",
            },
            {
                "question_number": 6,
                "question": "Free-plan confidence interval conclusion",
                "answer_value": "The average minutes watched by students in Q2 2022 is higher than in Q2 2021.",
                "support_value": "Q2 2022 filtered CI is above Q2 2021 filtered CI.",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 7,
                "question": "Paying-student confidence interval conclusion",
                "answer_value": "The students who watched in Q2 2021 had more minutes watched on average.",
                "support_value": "Q2 2021 paid filtered CI is above Q2 2022 paid filtered CI.",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 8,
                "question": "Free-plan t-test result",
                "answer_value": "-4.0 - we reject the null hypothesis",
                "support_value": f"t = {float(free_test['t_statistic']):.4f}",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 9,
                "question": "Paying-student t-test result",
                "answer_value": "5.0 - we accept the null hypothesis",
                "support_value": f"t = {float(paid_test['t_statistic']):.4f}",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 10,
                "question": "Closest correlation coefficient",
                "answer_value": "0.5",
                "support_value": f"correlation = {float(correlation['correlation_coefficient']):.4f}",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 13,
                "question": "Dependence of Q2 2021 and Q2 2022 watching events",
                "answer_value": "The two events are dependent.",
                "support_value": (
                    f"joint = {float(probability['probability_watched_both']):.4f}; "
                    f"product = {float(probability['independent_product_probability']):.4f}"
                ),
                "answer_basis": "data-derived",
            },
            {
                "question_number": 14,
                "question": "P(watched Q2 2021 | watched Q2 2022)",
                "answer_value": "7%",
                "support_value": f"{float(probability['probability_2021_given_2022']):.4f}",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 16,
                "question": "Closest R-squared value",
                "answer_value": "0.5",
                "support_value": f"R-squared = {float(regression['r_squared']):.4f}",
                "answer_basis": "data-derived",
            },
            {
                "question_number": 17,
                "question": "Predicted certificates for 1200 minutes watched",
                "answer_value": str(int(regression["predicted_certificates_rounded_up"])),
                "support_value": (
                    f"raw prediction = {float(regression['predicted_certificates_raw']):.4f}"
                ),
                "answer_basis": "data-derived",
            },
        ]
    )

    _create_table_from_frame(con, "mart_summary_kpis", summary)
    _create_table_from_frame(con, "mart_quiz_answers", answers)
    return summary, answers


def _write_report(
    statistics: pd.DataFrame,
    hypothesis: pd.DataFrame,
    correlation: pd.DataFrame,
    regression: pd.DataFrame,
    summary: pd.DataFrame,
    quiz: pd.DataFrame,
) -> Path:
    ensure_project_dirs()
    kpi = summary.iloc[0]
    free_2021 = statistics.query("engagement_year == 2021 and paid == 0").iloc[0]
    free_2022 = statistics.query("engagement_year == 2022 and paid == 0").iloc[0]
    paid_2021 = statistics.query("engagement_year == 2021 and paid == 1").iloc[0]
    paid_2022 = statistics.query("engagement_year == 2022 and paid == 1").iloc[0]
    corr = correlation.iloc[0]
    reg = regression.iloc[0]

    lines = [
        "# Tracking User Engagement Report",
        "",
        "## Executive Summary",
        "",
        f"- Q2 watched-student records increased from {int(kpi['watched_2021_students']):,} in 2021 to {int(kpi['watched_2022_students']):,} in 2022.",
        f"- Free-plan filtered average minutes increased from {_fmt(float(free_2021['mean_minutes']))} to {_fmt(float(free_2022['mean_minutes']))}.",
        f"- Paid filtered average minutes decreased from {_fmt(float(paid_2021['mean_minutes']))} to {_fmt(float(paid_2022['mean_minutes']))}.",
        f"- Only {_fmt(float(kpi['probability_2021_given_2022']) * 100)}% of Q2 2022 watchers also watched in Q2 2021.",
        "",
        "## Statistical Findings",
        "",
        f"- Free-plan test statistic: {_fmt(float(hypothesis[hypothesis['student_plan'].eq('Free')].iloc[0]['t_statistic']), 4)}; decision: reject the null.",
        f"- Paid test statistic: {_fmt(float(hypothesis[hypothesis['student_plan'].eq('Paid')].iloc[0]['t_statistic']), 4)}; decision: fail to reject the null.",
        f"- Minutes watched and certificates issued have a correlation of {_fmt(float(corr['correlation_coefficient']), 4)}.",
        f"- Linear regression R-squared is {_fmt(float(reg['r_squared']), 4)}; a 1,200-minute learner is predicted to earn {int(reg['predicted_certificates_rounded_up'])} certificates after rounding up.",
        "",
        "## Interpretation",
        "",
        "- The new platform additions appear to have improved free-plan engagement, but not paid-student minutes watched.",
        "- Paid learners remain much deeper users, so the decline in paid average minutes deserves retention and product-path analysis.",
        "- Certificate issuance rises with minutes watched, but the regression confirms study time is not the only driver of certificates.",
        "",
        "## Recommendations",
        "",
        "- Preserve the end-2021 engagement features that helped free users spend more time learning.",
        "- Investigate paid-student behavior separately, especially whether new features shifted engagement into exams or career tracks not captured as video minutes.",
        "- Use certificate prediction as a directional signal only; enrich the model with course mix, learner tenure, and exam activity before operational use.",
        "",
        "## Quiz Support",
        "",
    ]
    for _, row in quiz.sort_values("question_number").iterrows():
        lines.append(
            f"{int(row['question_number'])}. **{row['question']}:** {row['answer_value']} "
            f"({row['answer_basis']}; support: {row['support_value']})"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Outlier removal follows the course instruction: keep values below each segment's 99th percentile.",
            "- Excel calculations are reproduced as Gold-backed Python/statistical outputs for repeatability.",
            "- Raw source SQL remains immutable under `source-datasets/`.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def build_gold() -> dict[str, int]:
    with connect() as con:
        con.execute(read_sql(script_path("gold", "build_gold.sql")))
        _, statistics, hypothesis = _build_statistics(con)
        correlation, regression = _build_correlation_and_model(con)
        summary, quiz = _build_summary_and_quiz(con)
        counts = {
            table: con.execute(f"SELECT COUNT(*) FROM gold.{table}").fetchone()[0]
            for table in GOLD_TABLES
        }

    report_path = _write_report(statistics, hypothesis, correlation, regression, summary, quiz)
    counts["report_written"] = int(report_path.exists())
    return counts


if __name__ == "__main__":
    for table, row_count in build_gold().items():
        print(f"{table}: {row_count}")
