from __future__ import annotations

import json
import pickle
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .documents import TextChunk, chunk_documents, collect_documents
from .paths import DEFAULT_INDEX_DIR


LOCAL_INDEX_FILE = "local_index.pkl"
MANIFEST_FILE = "manifest.json"


@dataclass(frozen=True)
class SearchResult:
    text: str
    metadata: dict[str, str]
    score: float


@dataclass(frozen=True)
class IndexManifest:
    backend: str
    created_at: str
    document_count: int
    chunk_count: int
    embedding_model: str
    index_path: str


class LocalSearchIndex:
    def __init__(self, chunks: list[TextChunk], vectorizer: TfidfVectorizer, matrix) -> None:
        self.chunks = chunks
        self.vectorizer = vectorizer
        self.matrix = matrix

    @classmethod
    def build(cls, chunks: list[TextChunk]) -> "LocalSearchIndex":
        if not chunks:
            raise ValueError("Cannot build an index with zero chunks")
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50000,
        )
        matrix = vectorizer.fit_transform([chunk.text for chunk in chunks])
        return cls(chunks=chunks, vectorizer=vectorizer, matrix=matrix)

    def search(
        self,
        query: str,
        project_slug: str | None = None,
        limit: int = 6,
    ) -> list[SearchResult]:
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        ranked = scores.argsort()[::-1]
        results: list[SearchResult] = []
        for index in ranked:
            chunk = self.chunks[int(index)]
            if project_slug and chunk.metadata.get("project_slug") != project_slug:
                continue
            score = float(scores[int(index)])
            if score <= 0:
                continue
            results.append(SearchResult(text=chunk.text, metadata=chunk.metadata, score=score))
            if len(results) >= limit:
                break
        return results


def build_local_index(index_dir: Path = DEFAULT_INDEX_DIR) -> IndexManifest:
    documents = collect_documents()
    chunks = chunk_documents(documents)
    index = LocalSearchIndex.build(chunks)
    index_dir.mkdir(parents=True, exist_ok=True)
    with (index_dir / LOCAL_INDEX_FILE).open("wb") as handle:
        pickle.dump(index, handle)

    manifest = IndexManifest(
        backend="local_tfidf",
        created_at=datetime.now(timezone.utc).isoformat(),
        document_count=len(documents),
        chunk_count=len(chunks),
        embedding_model="sklearn:TfidfVectorizer",
        index_path=str(index_dir),
    )
    (index_dir / MANIFEST_FILE).write_text(
        json.dumps(asdict(manifest), indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def check_index_inputs() -> IndexManifest:
    documents = collect_documents()
    chunks = chunk_documents(documents)
    return IndexManifest(
        backend="local_tfidf",
        created_at="not-written",
        document_count=len(documents),
        chunk_count=len(chunks),
        embedding_model="sklearn:TfidfVectorizer",
        index_path=str(DEFAULT_INDEX_DIR),
    )


def load_local_index(index_dir: Path = DEFAULT_INDEX_DIR) -> LocalSearchIndex:
    path = index_dir / LOCAL_INDEX_FILE
    if not path.exists():
        raise FileNotFoundError(f"Missing local index: {path}")
    with path.open("rb") as handle:
        return pickle.load(handle)


def load_manifest(index_dir: Path = DEFAULT_INDEX_DIR) -> dict[str, object]:
    path = index_dir / MANIFEST_FILE
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
