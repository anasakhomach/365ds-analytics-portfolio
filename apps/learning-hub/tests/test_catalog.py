from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.catalog import describe_gold_tables, load_catalog, validate_catalog


def test_catalog_references_existing_project_artifacts() -> None:
    projects = load_catalog()
    assert len(projects) == 5
    assert validate_catalog(projects) == []


def test_catalog_gold_tables_exist_in_warehouses() -> None:
    for project in load_catalog():
        table_descriptions = describe_gold_tables(project)
        described = {table.name for table in table_descriptions}
        assert described == set(project.gold_tables)
        assert all(table.row_count is not None for table in table_descriptions)


def test_catalog_includes_documents_and_code_for_each_project() -> None:
    for project in load_catalog():
        assert project.document_paths
        assert project.code_paths
        assert project.readme_path in project.document_paths


def test_catalog_tracks_project_architecture_traits() -> None:
    projects = load_catalog()
    by_slug = {project.slug: project for project in projects}

    assert by_slug["real-estate-market-analysis"].traits["workflow"] == "python_first_medallion"
    assert by_slug["checkout-flow-optimization"].traits["workflow"] == "sql_first_medallion"
    assert by_slug["customer-engagement-analysis"].traits["workflow"] == "sql_first_medallion"
    assert by_slug["tracking-user-engagement"].traits["workflow"] == "sql_first_medallion"
    assert {project.traits["analytics_engine"] for project in projects} == {"duckdb"}
    assert {project.traits["visualization"] for project in projects} == {"streamlit"}
