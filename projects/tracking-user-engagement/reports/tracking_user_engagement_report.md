# Tracking User Engagement Report

## Executive Summary

- Q2 watched-student records increased from 7,639 in 2021 to 8,841 in 2022.
- Free-plan filtered average minutes increased from 14.21 to 16.04.
- Paid filtered average minutes decreased from 360.10 to 292.22.
- Only 7.24% of Q2 2022 watchers also watched in Q2 2021.

## Statistical Findings

- Free-plan test statistic: -3.9512; decision: reject the null.
- Paid test statistic: 5.1544; decision: fail to reject the null.
- Minutes watched and certificates issued have a correlation of 0.5126.
- Linear regression R-squared is 0.4678; a 1,200-minute learner is predicted to earn 4 certificates after rounding up.

## Interpretation

- The new platform additions appear to have improved free-plan engagement, but not paid-student minutes watched.
- Paid learners remain much deeper users, so the decline in paid average minutes deserves retention and product-path analysis.
- Certificate issuance rises with minutes watched, but the regression confirms study time is not the only driver of certificates.

## Recommendations

- Preserve the end-2021 engagement features that helped free users spend more time learning.
- Investigate paid-student behavior separately, especially whether new features shifted engagement into exams or career tracks not captured as video minutes.
- Use certificate prediction as a directional signal only; enrich the model with course mix, learner tenure, and exam activity before operational use.

## Quiz Support

1. **Refund-aware date_end expression:** IF(date_refunded IS NULL, date_end, date_refunded) AS date_end (course logic; support: Refund date replaces planned subscription end date.)
2. **Minutes watched calculation:** ROUND(SUM(seconds_watched) / 60, 2) (course logic; support: Seconds are aggregated before converting to rounded minutes.)
3. **Distribution of minutes watched:** The distribution is right-skewed (data-derived; support: Means remain above medians in every filtered segment.)
4. **99th percentile outlier filter:** data_no_outliers = data[data['minutes_watched'] < data['minutes_watched'].quantile(0.99)] (course logic; support: The project keeps observations lower than the 99th percentile.)
5. **Sample size and confidence intervals:** As sample size increases, the confidence interval narrows. (statistics; support: Standard error is standard deviation divided by square root of n.)
6. **Free-plan confidence interval conclusion:** The average minutes watched by students in Q2 2022 is higher than in Q2 2021. (data-derived; support: Q2 2022 filtered CI is above Q2 2021 filtered CI.)
7. **Paying-student confidence interval conclusion:** The students who watched in Q2 2021 had more minutes watched on average. (data-derived; support: Q2 2021 paid filtered CI is above Q2 2022 paid filtered CI.)
8. **Free-plan t-test result:** -4.0 - we reject the null hypothesis (data-derived; support: t = -3.9512)
9. **Paying-student t-test result:** 5.0 - we accept the null hypothesis (data-derived; support: t = 5.1544)
10. **Closest correlation coefficient:** 0.5 (data-derived; support: correlation = 0.5126)
13. **Dependence of Q2 2021 and Q2 2022 watching events:** The two events are dependent. (data-derived; support: joint = 0.0404; product = 0.2692)
14. **P(watched Q2 2021 | watched Q2 2022):** 7% (data-derived; support: 0.0724)
16. **Closest R-squared value:** 0.5 (data-derived; support: R-squared = 0.4678)
17. **Predicted certificates for 1200 minutes watched:** 4 (data-derived; support: raw prediction = 3.2381)

## Notes

- Outlier removal follows the course instruction: keep values below each segment's 99th percentile.
- Excel calculations are reproduced as Gold-backed Python/statistical outputs for repeatability.
- Raw source SQL remains immutable under `source-datasets/`.
