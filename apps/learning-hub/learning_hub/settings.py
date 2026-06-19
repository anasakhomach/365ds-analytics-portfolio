from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


VALID_AI_MODES = {"local", "provider", "gateway"}
VALID_PROVIDERS = {"openai_compatible", "openrouter", "litellm"}
VALID_EMBEDDING_BACKENDS = {"local_tfidf", "chroma_openai_compatible"}


@dataclass(frozen=True)
class AISettings:
    mode: str
    provider: str
    base_url: str
    chat_model: str
    embedding_backend: str
    embedding_model: str
    enable_byok: bool
    owner_api_key: str | None
    owner_api_key_source: str | None
    site_url: str | None
    app_title: str


@dataclass(frozen=True)
class AIRuntime:
    settings: AISettings
    effective_mode: str
    live_enabled: bool
    provider: str
    base_url: str
    chat_model: str
    api_key: str | None
    api_key_source: str | None
    reason: str

    def safe_label(self) -> str:
        source = self.api_key_source or "none"
        status = "live" if self.live_enabled else "local fallback"
        return (
            f"{status} | mode={self.effective_mode} | provider={self.provider} | "
            f"model={self.chat_model} | key_source={source}"
        )


def load_ai_settings(env: Mapping[str, str] | None = None) -> AISettings:
    values = env if env is not None else os.environ
    provider = _choice(values.get("LEARNING_HUB_PROVIDER"), VALID_PROVIDERS, "litellm")
    mode = _choice(values.get("LEARNING_HUB_AI_MODE"), VALID_AI_MODES, "gateway")
    embedding_backend = _choice(
        values.get("LEARNING_HUB_EMBEDDING_BACKEND"),
        VALID_EMBEDDING_BACKENDS,
        "local_tfidf",
    )

    owner_key, owner_source = _owner_key(values, provider)
    return AISettings(
        mode=mode,
        provider=provider,
        base_url=values.get("LEARNING_HUB_BASE_URL") or _default_base_url(provider),
        chat_model=values.get("LEARNING_HUB_CHAT_MODEL") or _default_chat_model(provider),
        embedding_backend=embedding_backend,
        embedding_model=values.get("LEARNING_HUB_EMBEDDING_MODEL") or "text-embedding-3-small",
        enable_byok=_truthy(values.get("LEARNING_HUB_ENABLE_BYOK"), default=True),
        owner_api_key=owner_key,
        owner_api_key_source=owner_source,
        site_url=values.get("LEARNING_HUB_SITE_URL"),
        app_title=values.get("LEARNING_HUB_APP_TITLE") or "365DS Learning Hub",
    )


def resolve_ai_runtime(settings: AISettings, session_api_key: str | None = None) -> AIRuntime:
    if settings.mode == "local":
        return AIRuntime(
            settings=settings,
            effective_mode="local",
            live_enabled=False,
            provider=settings.provider,
            base_url=settings.base_url,
            chat_model=settings.chat_model,
            api_key=None,
            api_key_source=None,
            reason="Local mode is configured.",
        )

    api_key = None
    key_source = None
    if settings.enable_byok and session_api_key:
        api_key = session_api_key.strip()
        key_source = "session"
    elif settings.owner_api_key:
        api_key = settings.owner_api_key
        key_source = settings.owner_api_key_source

    if not api_key:
        return AIRuntime(
            settings=settings,
            effective_mode="local",
            live_enabled=False,
            provider=settings.provider,
            base_url=settings.base_url,
            chat_model=settings.chat_model,
            api_key=None,
            api_key_source=None,
            reason="No API key was provided, so the hub is using local retrieval.",
        )

    return AIRuntime(
        settings=settings,
        effective_mode=settings.mode,
        live_enabled=True,
        provider=settings.provider,
        base_url=settings.base_url,
        chat_model=settings.chat_model,
        api_key=api_key,
        api_key_source=key_source,
        reason="Live model calls are enabled.",
    )


def _choice(value: str | None, allowed: set[str], default: str) -> str:
    normalized = (value or default).strip().lower()
    return normalized if normalized in allowed else default


def _truthy(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _default_base_url(provider: str) -> str:
    if provider == "openrouter":
        return "https://openrouter.ai/api/v1"
    if provider == "litellm":
        return "http://localhost:4000/v1"
    return "https://api.openai.com/v1"


def _default_chat_model(provider: str) -> str:
    if provider == "openrouter":
        return "~openai/gpt-latest"
    if provider == "litellm":
        return "365ds-chat"
    return "gpt-4o-mini"


def _owner_key(values: Mapping[str, str], provider: str) -> tuple[str | None, str | None]:
    key_order = ["LEARNING_HUB_API_KEY"]
    if provider == "openrouter":
        key_order.append("OPENROUTER_API_KEY")
    elif provider == "litellm":
        key_order.append("LITELLM_API_KEY")
    else:
        key_order.append("OPENAI_API_KEY")

    for key in key_order:
        value = values.get(key)
        if value and value.strip():
            return value.strip(), key
    return None, None
