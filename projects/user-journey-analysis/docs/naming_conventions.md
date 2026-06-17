# Naming Conventions

- Schemas use medallion names: `bronze`, `silver`, `gold`.
- Bronze tables use `raw_<source>`.
- Silver tables use `cleaned_<entity>` and `grouped_<entity>`.
- Gold marts use `mart_<business_question>`.
- Scenario keys are lowercase snake case, such as `all_sessions`, `first_3_sessions`, and `last_3_sessions`.
- Sequence labels use page names joined by ` -> ` for display.
