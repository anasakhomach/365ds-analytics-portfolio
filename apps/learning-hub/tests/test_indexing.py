from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.indexing import build_local_index, check_index_inputs, load_local_index


def test_index_inputs_include_all_projects() -> None:
    manifest = check_index_inputs()
    assert manifest.document_count >= 50
    assert manifest.chunk_count >= manifest.document_count


def test_local_index_retrieves_project_context(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    index = load_local_index(tmp_path)
    results = index.search("Which projects use SQL-first medallion layers?", limit=5)
    assert results
    assert all(result.metadata["project_slug"] for result in results)
    assert any("gold" in result.text.lower() or "medallion" in result.text.lower() for result in results)
