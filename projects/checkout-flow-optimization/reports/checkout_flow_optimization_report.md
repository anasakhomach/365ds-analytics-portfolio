# Checkout Flow Optimization Report

## Executive Summary

- Analysis window: July 2022 through January 2023.
- Total carts: 5,001.
- Total checkout attempts: 4,334.
- Successful checkout attempts: 1,372.
- Overall checkout success rate: 31.7%.
- Course-formula cart abandonment rate: 13.3%.

## Current State

- Highest success-rate month: August 2022 at 47.1%.
- Highest abandonment-rate month: October 2022 at 37.5%.
- Most common checkout error: `number field is required` with 1,220 attempts.
- November 2022 has more checkout attempts than carts under the course formula, so the report keeps the formula visible and does not clamp negative abandonment.

## Business Objective

Improve checkout completion by reducing preventable payment failures and making card-entry feedback clearer across desktop and mobile.

## Hypothesis

Most friction comes from payment-form validation and card-decline states. Better real-time validation, clearer field labels, and alternate payment options should lift successful checkout attempts.

## Actionable Insights

- Add real-time validation for card number, expiry year, CVV, ZIP, and required-name fields before payment submission.
- Review mobile checkout form sizing and keyboard behavior because device mix materially affects error exposure.
- Add alternate payment options and clearer issuer-decline messaging for declined-card errors.

## Quiz Support

1. **Highest monthly checkout attempts:** November 2022 (data-derived; support: 2250)
2. **Lowest monthly checkout attempts:** October 2022, 173 attempts (data-derived; support: 173)
3. **Highest monthly purchase carts:** November 2022 (data-derived; support: 2220)
4. **Two highest monthly cart abandonment rates:** October 2022 and August 2022 (data-derived; support: 0.3755, 0.3439)
5. **Most frequent desktop error in September 2022:** year field is required (data-derived; support: 32)
6. **Third most common overall error:** Your card was declined. (data-derived; support: 367)
7. **Third most common desktop error:** Your card was declined. (data-derived; support: 3)
8. **Opportunity size using prompt assumptions:** $648 (course-prompt-assumption; support: ((0.40 - 0.34) * 360 * 30))

## Quiz Option Note

- Several data-derived answers do not match the multiple-choice options in the converted project brief. The SQL marts keep the visible CTE logic and raw dump counts as the source of truth.
- The opportunity-sizing question is calculated from the prompt assumptions rather than the observed January data.

## Reproducibility

- Dashboard reads only `gold.*` marts.
- Raw MySQL dump remains immutable under `source-datasets/`.
- DuckDB is canonical; MySQL CLI is reserved for validation if dump behavior diverges.
