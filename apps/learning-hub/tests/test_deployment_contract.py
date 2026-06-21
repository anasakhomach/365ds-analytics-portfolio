from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
APP_DIR = REPO_ROOT / "apps" / "learning-hub"


def test_streamlit_cloud_runtime_files_are_present() -> None:
    requirements = (APP_DIR / "requirements.txt").read_text(encoding="utf-8")
    for dependency in ("duckdb", "openai", "pandas", "plotly", "pyyaml", "scikit-learn", "streamlit"):
        assert dependency in requirements.lower()

    config = (REPO_ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")
    assert "[theme]" in config


def test_all_project_snapshots_are_committed_runtime_inputs() -> None:
    expected = {
        "real-estate-market-analysis.duckdb",
        "user-journey-analysis.duckdb",
        "checkout-flow-optimization.duckdb",
        "customer-engagement-analysis.duckdb",
        "tracking-user-engagement.duckdb",
    }
    assert {path.name for path in (APP_DIR / "data").glob("*.duckdb")} == expected


def test_public_repository_url_is_configurable() -> None:
    paths_source = (APP_DIR / "learning_hub" / "paths.py").read_text(encoding="utf-8")
    assert "LEARNING_HUB_REPOSITORY_URL" in paths_source
