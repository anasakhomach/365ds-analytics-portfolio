# User Journey Analysis Report

## Executive Summary

- Raw sessions: 9,935.
- Unique users: 1,350.
- Subscription mix: 931 Annual, 376 Monthly, 43 Quarterly users.
- Top all-session page after preprocessing: Homepage (2,679 visits).
- Average all-session journey length after preprocessing: 10.4 pages.

## Business Findings

- Checkout, Log in, Coupon, Homepage, and Sign up dominate late-stage journeys, so friction analysis should focus on conversion and account/payment steps.
- Quarterly purchasers show Homepage, Log in, and Sign up as their top pages, suggesting a shorter evaluation pattern before purchase.
- The strongest four-page pattern in the last-three-session view is `Log in-Homepage-Log in-Checkout`, appearing in 49 journeys.

## Quiz Answers

1. **Records after grouping first three sessions:** 1350
2. **Third most popular page for quarterly users:** Sign up
3. **Fourth most popular destination after Pricing:** Courses
4. **Average journey length for last three sessions:** 3.6
5. **Fourth highest page presence for last three sessions:** Homepage
6. **Most popular sequence of four pages count for last three sessions:** 49

## Reproducibility

- Dashboard reads only `gold.*` marts.
- Raw source files are treated as immutable inputs.
- Session ordering uses `session_id` ascending because no timestamp exists.
