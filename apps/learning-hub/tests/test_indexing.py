from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.indexing import build_chroma_index, build_local_index, check_index_inputs, load_local_index
from learning_hub.settings import load_ai_settings


def test_index_inputs_include_all_projects() -> None:
    manifest = check_index_inputs()
    assert manifest.document_count >= 50
    assert manifest.chunk_count >= manifest.document_count
    assert len(manifest.source_hash) == 64


def test_local_index_retrieves_project_context(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    index = load_local_index(tmp_path)
    results = index.search("Which projects use SQL-first medallion layers?", limit=5)
    assert results
    assert all(result.metadata["project_slug"] for result in results)
    assert any("gold" in result.text.lower() or "medallion" in result.text.lower() for result in results)


class FakeEmbeddingClient:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[float(index), 1.0] for index, _ in enumerate(texts)]

    def embed_query(self, text: str) -> list[float]:
        return [0.0, 1.0]


class FakeCollection:
    def __init__(self) -> None:
        self.ids: list[str] = []
        self.documents: list[str] = []
        self.metadatas: list[dict[str, str]] = []
        self.embeddings: list[list[float]] = []

    def upsert(self, ids, documents, metadatas, embeddings) -> None:
        self.ids.extend(ids)
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)
        self.embeddings.extend(embeddings)


class FakeChromaClient:
    def __init__(self) -> None:
        self.collection = FakeCollection()

    def delete_collection(self, name: str) -> None:
        self.collection = FakeCollection()

    def get_or_create_collection(self, name: str, metadata=None, embedding_function=None):
        return self.collection


def test_chroma_index_builds_with_injected_clients(tmp_path: Path) -> None:
    settings = load_ai_settings({"LEARNING_HUB_EMBEDDING_BACKEND": "chroma_openai_compatible"})
    chroma_client = FakeChromaClient()

    manifest = build_chroma_index(
        index_dir=tmp_path,
        settings=settings,
        embedding_client=FakeEmbeddingClient(),
        chroma_client=chroma_client,
    )

    assert manifest.backend == "chroma_openai_compatible"
    assert manifest.embedding_model == "text-embedding-3-small"
    assert manifest.chunk_count == len(chroma_client.collection.ids)
    assert len(manifest.source_hash) == 64
