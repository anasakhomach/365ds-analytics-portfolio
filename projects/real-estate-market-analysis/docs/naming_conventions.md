# Naming Conventions

- Schemas use medallion names: `bronze`, `silver`, `gold`.
- Raw Bronze tables use `raw_<source>`.
- Silver tables use `cleaned_<entity>` and `property_transactions`.
- Gold marts use `mart_<business_question>`.
- Columns use snake_case.
- Date columns end with `_date`, month keys use `YYYY-MM`, and yearly fields use integer years.
