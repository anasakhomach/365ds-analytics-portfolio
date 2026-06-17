# Real Estate Market Analysis Report

## Executive Summary

- Portfolio size: 267 properties, with 195 sold and 72 still available.
- Total sold-property revenue: $52,539,739.
- Average sold price: $269,435; average sold area: 899.87 sq ft.
- Average deal satisfaction: 3.60/5.
- Customer age and property price correlation: -0.1745.

## Business Findings

- Most common sold building group: Building 2.
- Second-highest state by sold-property count: Nevada.
- Most common customer age interval among known individual buyers: (36.0, 42.0].
- Highest average satisfaction country: Canada.
- Highest revenue year: 2007.0.
- Available properties in the highest price interval: 6.

## Interpretation

The dataset is concentrated in US residential apartment sales, especially California. Buyer age and property price show only a weak relationship, so development strategy should emphasize geography, building performance, and price bands more than age alone.

## Reproducibility

- Warehouse: `C:\Users\Nitro\data-analytics-project\365ds-demo-projects\projects\real-estate-market-analysis\warehouse.duckdb`
- Dashboard reads only `gold.*` marts.
- Raw files are treated as immutable source inputs.

## Quiz Answers

Here are the answers to the project quiz based on our analysis:
1. **Q1:** `.merge()`
2. **Q2:** 928
3. **Q3:** Apartment
4. **Q4:** Building 4 ($290,239)
5. **Q5:** $338,181
6. **Q6:** Nevada
7. **Q7:** 36-42
8. **Q8:** 6
9. **Q9:** Negative correlation
10. **Q10:** Canada
11. **Q11:** Positively skewed
12. **Q12:** Building 1
13. **Q13:** California, Nevada, Colorado/Oregon (The data shows CA is ~63.7%, NV ~9.0%, AZ ~5.4%, OR ~5.0%, CO ~4.9%)
14. **Q14:** 2007
15. **Q15:** Building 1
