from __future__ import annotations

from typing import Iterable, Protocol

from .settings import AIRuntime


Message = dict[str, str]


class LLMClient(Protocol):
    def complete(self, messages: list[Message]) -> str:
        ...

    def stream(self, messages: list[Message]) -> Iterable[str]:
        ...


class OpenAICompatibleClient:
    def __init__(self, runtime: AIRuntime, temperature: float = 0.2) -> None:
        if not runtime.live_enabled or not runtime.api_key:
            raise ValueError("A live AI runtime with an API key is required")
        self.runtime = runtime
        self.temperature = temperature

    def complete(self, messages: list[Message]) -> str:
        completion = self._client().chat.completions.create(
            model=self.runtime.chat_model,
            messages=messages,
            temperature=self.temperature,
        )
        return completion.choices[0].message.content or ""

    def stream(self, messages: list[Message]) -> Iterable[str]:
        stream = self._client().chat.completions.create(
            model=self.runtime.chat_model,
            messages=messages,
            temperature=self.temperature,
            stream=True,
        )
        for chunk in stream:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def _client(self):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the OpenAI Python SDK to enable live model calls.") from exc

        headers = {}
        if self.runtime.provider == "openrouter":
            if self.runtime.settings.site_url:
                headers["HTTP-Referer"] = self.runtime.settings.site_url
            headers["X-OpenRouter-Title"] = self.runtime.settings.app_title

        return OpenAI(
            api_key=self.runtime.api_key,
            base_url=self.runtime.base_url,
            default_headers=headers or None,
        )


def create_llm_client(runtime: AIRuntime) -> LLMClient | None:
    if not runtime.live_enabled:
        return None
    return OpenAICompatibleClient(runtime)
