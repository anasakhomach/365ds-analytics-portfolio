# Customer Engagement Analysis Report

## Executive Summary

- Registered students: 35,230.
- Onboarded students: 18,156 (51.5%).
- Total minutes watched: 1,835,588.
- Average minutes watched per engaged student: 101.10.
- Paying students watch about 23.12x more minutes than free-plan students on the average-minutes KPI.

## Current State

- Most watched course: `Introduction to Data and Data Science` with 333,266 minutes watched and an average rating of 4.86.
- Peak monthly total engagement: August 2022 with 318,585 minutes for `All` students.
- Peak monthly average engagement: March 2022 with 291.47 average minutes for `Paid` students.
- Top country by registered students: India (6,933).
- Top country by minutes watched: United States (449,029 minutes).

## Interpretation

- Introductory analytics courses dominate total watch time, showing strong demand for broad entry points into the platform.
- Paying students have much deeper average engagement, so conversion and retention work should focus on moving motivated free users into paid learning paths.
- Country rankings by registered students and watched minutes are related but not identical, so acquisition volume should be evaluated together with realized engagement.

## Recommendations

- Promote the strongest introductory courses as onboarding paths, then route students into adjacent paid curricula.
- Track monthly seasonality by student type so paid engagement dips can trigger targeted lifecycle campaigns.
- Pair country acquisition metrics with minutes-watched metrics before deciding where to scale marketing spend.

## Quiz Support

1. **Second course by total minutes watched:** SQL (data-derived; support: 234824.8)
2. **Top country by registered students in August 2022:** India, 996 students (data-derived; support: 996)
3. **Fifth country by registered students in September 2022:** Nigeria (data-derived; support: 135)
4. **Top country by free-plan minutes for July registrations:** India (data-derived; support: 10838.6)
5. **Top country by paying-student minutes for July registrations:** United States (data-derived; support: 41173.1)
6. **Highest monthly average minutes watched by paying students:** 291.47 (data-derived; support: March 2022)
7. **Highest monthly minutes watched by free-plan students:** 146258.9 (data-derived; support: August 2022)
8. **Lowest monthly onboarding rate:** June 2022 (data-derived; support: 0.4629)
9. **Overall onboarding rate:** 0.5154 (data-derived; support: 18156 / 35230)
10. **Paying to free-plan average minutes watched ratio:** 23.12 (data-derived; support: Question text is truncated in the converted brief)

## Notes

- Question 10 is truncated in the converted project brief, so the report records the data-derived paid/free average-minutes ratio.
- Tableau requirements are translated into Streamlit pages backed only by Gold marts.
- Raw MySQL dump files remain immutable under `source-datasets/`.
