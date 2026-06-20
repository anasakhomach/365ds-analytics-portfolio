from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from .settings import AIRuntime


Message = dict[str, str]


@dataclass(frozen=True)
class ProviderErrorInfo:
    category: str
    message: str
    action: str


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


def classify_provider_error(exc: Exception) -> ProviderErrorInfo:
    status_code = _status_code(exc)
    text = f"{type(exc).__name__} {exc}".lower()

    if (
        status_code in {402, 429}
        or "rate limit" in text
        or "rate_limit" in text
        or "quota" in text
        or "payment required" in text
        or "insufficient credit" in text
        or "free-models-per-day" in text
        or "free quota" in text
    ):
        return ProviderErrorInfo(
            category="rate_limit",
            message="The shared demo key is temporarily busy, rate-limited, or out of free quota.",
            action="Continue in local mode, wait a moment, or enter your own session API key.",
        )
    if status_code in {401, 403} or "unauthorized" in text or "invalid api key" in text or "authentication" in text:
        return ProviderErrorInfo(
            category="auth",
            message="The selected provider rejected the configured key.",
            action="Use a fresh owner key or enter a valid session API key for the selected provider.",
        )
    if (
        status_code in {400, 404}
        and ("model" in text or "not found" in text or "does not exist" in text)
    ):
        return ProviderErrorInfo(
            category="invalid_model",
            message="The selected model is unavailable for this provider or key.",
            action="Choose another preset model or enter a supported custom model ID.",
        )
    if (
        status_code is None
        and (
            "apiconnectionerror" in text
            or "connection" in text
            or "connect" in text
            or "timeout" in text
            or "unreachable" in text
            or "name resolution" in text
        )
    ):
        return ProviderErrorInfo(
            category="connection",
            message="The selected provider or gateway is unreachable.",
            action="Check the provider/base URL, switch providers, or start the LiteLLM gateway profile.",
        )
    return ProviderErrorInfo(
        category="other",
        message="Live model synthesis failed.",
        action="Use local mode, try a different provider/model, or enter a fresh session API key.",
    )


def _status_code(exc: Exception) -> int | None:
    direct = getattr(exc, "status_code", None)
    if isinstance(direct, int):
        return direct
    response = getattr(exc, "response", None)
    response_code = getattr(response, "status_code", None)
    return response_code if isinstance(response_code, int) else None
