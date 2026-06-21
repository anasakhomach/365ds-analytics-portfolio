from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
from streamlit.testing.v1 import AppTest


APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub import paths


def test_overview_builds_missing_local_search_index(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(paths, "DEFAULT_INDEX_DIR", tmp_path)
    st.cache_data.clear()
    st.cache_resource.clear()

    app = AppTest.from_file(str(APP_DIR / "streamlit_app.py")).run(timeout=60)

    assert not app.exception
    assert (tmp_path / "manifest.json").is_file()
    assert all("Search index has not been built yet" not in warning.value for warning in app.warning)
