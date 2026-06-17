import duckdb
import pandas as pd

con = duckdb.connect('projects/real-estate-market-analysis/warehouse.duckdb')

print('--- Q2: Avg area of building type 1 ---')
print(con.execute("SELECT avg(area) FROM gold.mart_property_transactions WHERE building_id = 1").df())

print('\n--- Q3: Most common property type sold ---')
print(con.execute("SELECT property_type, COUNT(*) FROM gold.mart_property_transactions WHERE sold_flag = true GROUP BY property_type ORDER BY count(*) DESC").df())

print('\n--- Q4: Building with highest average property price ---')
print(con.execute("SELECT building_id, avg(price) FROM gold.mart_property_transactions GROUP BY building_id ORDER BY avg(price) DESC LIMIT 1").df())

print('\n--- Q5: Average cost of a building in Mexico ---')
print(con.execute("SELECT avg(price) FROM gold.mart_property_transactions WHERE country = 'Mexico'").df())

print('\n--- Q11: Shape of age distribution ---')
print(con.execute("SELECT age_interval, count FROM gold.mart_age_intervals ORDER BY age_interval").df())

print('\n--- Q12: Building with highest sales in 2004 ---')
print(con.execute("SELECT building_id, sum(price) FROM gold.mart_property_transactions WHERE sale_year = 2004 AND sold_flag = true GROUP BY building_id ORDER BY sum(price) DESC LIMIT 1").df())

print('\n--- Q13: States accounting for 82% of company revenue ---')
print(con.execute("""
WITH total_rev AS (SELECT sum(price) as total FROM gold.mart_property_transactions WHERE sold_flag = true),
state_rev AS (SELECT state, sum(price) as rev FROM gold.mart_property_transactions WHERE sold_flag = true GROUP BY state)
SELECT state, rev, rev / (SELECT total FROM total_rev) * 100 as pct_revenue
FROM state_rev ORDER BY rev DESC
""").df())

print('\n--- Q15: Yearly sales by building (to see decrease) ---')
print(con.execute("SELECT building_id, year, sales_count FROM gold.mart_yearly_sales_by_building ORDER BY building_id, year").df())
