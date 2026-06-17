# Naming Conventions

- Schemas use medallion names: `bronze`, `silver`, `gold`.
- Raw source tables keep source names: `checkout_actions`, `checkout_carts`.
- Gold dashboard tables use `mart_*` names.
- Dates use `*_date` for daily grain and `*_month` for month grain.
- Counts use `count_*` for course-compatible exports and `*_attempts` or `*_carts` for dashboard labels.
