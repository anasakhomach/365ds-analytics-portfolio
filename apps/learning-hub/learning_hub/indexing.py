from __future__ import annotations

import json
import pickle
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .documents import TextChunk, chunk_documents, collect_documents
from .embeddings import EmbeddingClient, OpenAICompatibleEmbeddingClient
from .paths import DEFAULT_INDEX_DIR
from .settings import AISettings, load_ai_settings, resolve_ai_runtime


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
    source_hash: str


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


class ChromaSearchIndex:
    def __init__(self, collection, embedding_client: EmbeddingClient) -> None:
        self.collection = collection
        self.embedding_client = embedding_client

    def search(
        self,
        query: str,
        project_slug: str | None = None,
        limit: int = 6,
    ) -> list[SearchResult]:
        where = {"project_slug": project_slug} if project_slug else None
        raw = self.collection.query(
            query_embeddings=[self.embedding_client.embed_query(query)],
            where=where,
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )
        documents = raw.get("documents", [[]])[0]
        metadatas = raw.get("metadatas", [[]])[0]
        distances = raw.get("distances", [[]])[0]
        results: list[SearchResult] = []
        for text, metadata, distance in zip(documents, metadatas, distances, strict=False):
            score = 1.0 / (1.0 + float(distance))
            results.append(SearchResult(text=text, metadata=metadata, score=score))
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
        source_hash=_source_hash(chunks),
    )
    (index_dir / MANIFEST_FILE).write_text(
        json.dumps(asdict(manifest), indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def build_chroma_index(
    index_dir: Path = DEFAULT_INDEX_DIR,
    settings: AISettings | None = None,
    embedding_client: EmbeddingClient | None = None,
    chroma_client=None,
) -> IndexManifest:
    settings = settings or load_ai_settings()
    documents = collect_documents()
    chunks = chunk_documents(documents)
    if not chunks:
        raise ValueError("Cannot build an index with zero chunks")

    embedding_client = embedding_client or _embedding_client(settings)
    chroma_client = chroma_client or _persistent_chroma_client(index_dir, reset=True)
    collection_name = "learning_hub_chunks"
    try:
        chroma_client.delete_collection(collection_name)
    except Exception:
        pass
    collection = chroma_client.get_or_create_collection(
        collection_name,
        metadata={"embedding_model": settings.embedding_model},
        embedding_function=None,
    )

    batch_size = 64
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        texts = [chunk.text for chunk in batch]
        collection.upsert(
            ids=[chunk.id for chunk in batch],
            documents=texts,
            metadatas=[chunk.metadata for chunk in batch],
            embeddings=embedding_client.embed_texts(texts),
        )

    index_dir.mkdir(parents=True, exist_ok=True)
    manifest = IndexManifest(
        backend="chroma_openai_compatible",
        created_at=datetime.now(timezone.utc).isoformat(),
        document_count=len(documents),
        chunk_count=len(chunks),
        embedding_model=settings.embedding_model,
        index_path=str(index_dir),
        source_hash=_source_hash(chunks),
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
        source_hash=_source_hash(chunks),
    )


def load_local_index(index_dir: Path = DEFAULT_INDEX_DIR) -> LocalSearchIndex:
    path = index_dir / LOCAL_INDEX_FILE
    if not path.exists():
        raise FileNotFoundError(f"Missing local index: {path}")
    with path.open("rb") as handle:
        return pickle.load(handle)


def load_chroma_index(
    index_dir: Path = DEFAULT_INDEX_DIR,
    settings: AISettings | None = None,
    embedding_client: EmbeddingClient | None = None,
    chroma_client=None,
) -> ChromaSearchIndex:
    settings = settings or load_ai_settings()
    embedding_client = embedding_client or _embedding_client(settings)
    chroma_client = chroma_client or _persistent_chroma_client(index_dir)
    collection = chroma_client.get_or_create_collection(
        "learning_hub_chunks",
        metadata={"embedding_model": settings.embedding_model},
        embedding_function=None,
    )
    return ChromaSearchIndex(collection=collection, embedding_client=embedding_client)


def build_index(index_dir: Path = DEFAULT_INDEX_DIR, settings: AISettings | None = None) -> IndexManifest:
    settings = settings or load_ai_settings()
    if settings.embedding_backend == "chroma_openai_compatible":
        return build_chroma_index(index_dir=index_dir, settings=settings)
    return build_local_index(index_dir=index_dir)


def load_search_index(index_dir: Path = DEFAULT_INDEX_DIR, settings: AISettings | None = None):
    settings = settings or load_ai_settings()
    if settings.embedding_backend == "chroma_openai_compatible":
        runtime = resolve_ai_runtime(settings)
        if runtime.live_enabled:
            return load_chroma_index(index_dir=index_dir, settings=settings)
    return load_local_index(index_dir=index_dir)


def load_manifest(index_dir: Path = DEFAULT_INDEX_DIR) -> dict[str, object]:
    path = index_dir / MANIFEST_FILE
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _embedding_client(settings: AISettings) -> EmbeddingClient:
    runtime = resolve_ai_runtime(settings)
    if not runtime.live_enabled:
        raise RuntimeError("Chroma indexing requires a configured API key for embeddings.")
    return OpenAICompatibleEmbeddingClient(runtime, model=settings.embedding_model)


def _persistent_chroma_client(index_dir: Path, reset: bool = False):
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Install chromadb to enable Chroma indexing.") from exc

    chroma_dir = index_dir / "chroma"
    if reset and chroma_dir.exists():
        shutil.rmtree(chroma_dir)
    chroma_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(chroma_dir))


def _source_hash(chunks: list[TextChunk]) -> str:
    digest = json.dumps(
        [
            {
                "id": chunk.id,
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ],
        sort_keys=True,
    ).encode("utf-8", errors="replace")
    import hashlib

    return hashlib.sha256(digest).hexdigest()
