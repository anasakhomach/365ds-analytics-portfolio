from __future__ import annotations

from typing import Protocol

from .llm_client import OpenAICompatibleClient
from .settings import AIRuntime


class EmbeddingClient(Protocol):
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...


class OpenAICompatibleEmbeddingClient:
    def __init__(self, runtime: AIRuntime, model: str) -> None:
        if not runtime.live_enabled or not runtime.api_key:
            raise ValueError("A live AI runtime with an API key is required for embeddings")
        self.runtime = runtime
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self._client().embeddings.create(
            model=self.model,
            input=texts,
            encoding_format="float",
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def _client(self):
        return OpenAICompatibleClient(self.runtime)._client()
