# Data Flow

## Source

Raw input lives under `source-datasets/User Journey Analysis In Python/user_journey_raw.csv`.

The source contains one row per user session:

- `user_id`
- `session_id`
- `subscription_type`
- `user_journey`

## Layers

1. Bronze loads the raw CSV unchanged.
2. Silver validates types, preserves session-level data, groups sessions by scenario, optionally supports page removal, and then removes consecutive duplicate pages.
3. Gold creates page counts, page presence, destinations, sequence rankings, journey length metrics, and quiz-supporting results.
4. Streamlit reads only Gold marts from `warehouse.duckdb`.

## Required Preprocessing Order

The project instructions require grouping/removing pages before duplicate cleanup:

1. group selected sessions
2. optionally remove selected pages
3. remove consecutive duplicate pages

The pipeline follows this order for all default scenarios.
