from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderPreset:
    key: str
    label: str
    default_mode: str
    base_url: str
    default_model: str
    model_options: tuple[str, ...]
    key_aliases: tuple[str, ...]
    allow_custom_base_url: bool = False


PROVIDER_PRESETS: dict[str, ProviderPreset] = {
    "openrouter": ProviderPreset(
        key="openrouter",
        label="OpenRouter",
        default_mode="provider",
        base_url="https://openrouter.ai/api/v1",
        default_model="~openai/gpt-latest",
        model_options=(
            "~openai/gpt-latest",
            "openai/gpt-4o-mini",
        ),
        key_aliases=("OPENROUTER_API_KEY",),
    ),
    "groq": ProviderPreset(
        key="groq",
        label="Groq",
        default_mode="provider",
        base_url="https://api.groq.com/openai/v1",
        default_model="llama-3.3-70b-versatile",
        model_options=(
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
        ),
        key_aliases=("GROQ_API_KEY",),
    ),
    "litellm": ProviderPreset(
        key="litellm",
        label="LiteLLM Gateway",
        default_mode="gateway",
        base_url="http://litellm:4000/v1",
        default_model="365ds-chat",
        model_options=("365ds-chat",),
        key_aliases=("LITELLM_API_KEY",),
    ),
    "openai_compatible": ProviderPreset(
        key="openai_compatible",
        label="OpenAI-Compatible",
        default_mode="provider",
        base_url="https://api.openai.com/v1",
        default_model="gpt-4o-mini",
        model_options=("gpt-4o-mini", "gpt-4.1-mini"),
        key_aliases=("OPENAI_API_KEY",),
        allow_custom_base_url=True,
    ),
}

PROVIDER_ORDER = ("openrouter", "groq", "openai_compatible", "litellm")


def get_provider_preset(provider: str) -> ProviderPreset:
    return PROVIDER_PRESETS.get(provider, PROVIDER_PRESETS["openrouter"])


def provider_labels() -> dict[str, str]:
    return {key: PROVIDER_PRESETS[key].label for key in PROVIDER_ORDER}


def model_options(provider: str) -> tuple[str, ...]:
    return get_provider_preset(provider).model_options
