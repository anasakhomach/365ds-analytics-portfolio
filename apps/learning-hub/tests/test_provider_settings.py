from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.settings import load_ai_settings, resolve_ai_runtime
from learning_hub.provider_catalog import key_provider_warning


def test_settings_default_to_openrouter_provider_but_fall_back_without_key() -> None:
    settings = load_ai_settings({})
    runtime = resolve_ai_runtime(settings)

    assert settings.mode == "provider"
    assert settings.provider == "openrouter"
    assert settings.chat_model == "cohere/north-mini-code:free"
    assert settings.agent_backend == "custom"
    assert runtime.effective_mode == "local"
    assert runtime.live_enabled is False
    assert runtime.api_key is None


def test_agent_backend_accepts_custom_langgraph_and_auto() -> None:
    assert load_ai_settings({"LEARNING_HUB_AGENT_BACKEND": "custom"}).agent_backend == "custom"
    assert load_ai_settings({"LEARNING_HUB_AGENT_BACKEND": "langgraph"}).agent_backend == "langgraph"
    assert load_ai_settings({"LEARNING_HUB_AGENT_BACKEND": "auto"}).agent_backend == "auto"
    assert load_ai_settings({"LEARNING_HUB_AGENT_BACKEND": "surprise"}).agent_backend == "custom"


def test_learning_hub_api_key_takes_precedence_over_aliases() -> None:
    settings = load_ai_settings(
        {
            "LEARNING_HUB_PROVIDER": "openrouter",
            "LEARNING_HUB_API_KEY": "hub-key",
            "OPENROUTER_API_KEY": "openrouter-key",
            "OPENAI_API_KEY": "openai-key",
        }
    )
    runtime = resolve_ai_runtime(settings)

    assert runtime.live_enabled is True
    assert runtime.api_key == "hub-key"
    assert runtime.api_key_source == "LEARNING_HUB_API_KEY"
    assert runtime.base_url == "https://openrouter.ai/api/v1"


def test_openrouter_alias_provides_owner_default_key() -> None:
    settings = load_ai_settings({"OPENROUTER_API_KEY": "openrouter-owner-key"})
    runtime = resolve_ai_runtime(settings)

    assert runtime.live_enabled is True
    assert runtime.provider == "openrouter"
    assert runtime.api_key == "openrouter-owner-key"
    assert runtime.api_key_source == "OPENROUTER_API_KEY"
    assert runtime.base_url == "https://openrouter.ai/api/v1"


def test_groq_provider_has_first_class_defaults_and_key_alias() -> None:
    settings = load_ai_settings(
        {
            "LEARNING_HUB_PROVIDER": "groq",
            "GROQ_API_KEY": "groq-owner-key",
        }
    )
    runtime = resolve_ai_runtime(settings)

    assert settings.mode == "provider"
    assert settings.base_url == "https://api.groq.com/openai/v1"
    assert settings.chat_model == "llama-3.3-70b-versatile"
    assert runtime.live_enabled is True
    assert runtime.api_key == "groq-owner-key"
    assert runtime.api_key_source == "GROQ_API_KEY"


def test_runtime_ui_overrides_are_applied_without_mutating_environment_defaults() -> None:
    settings = load_ai_settings(
        {"OPENROUTER_API_KEY": "openrouter-owner-key"},
        overrides={
            "LEARNING_HUB_PROVIDER": "groq",
            "LEARNING_HUB_CHAT_MODEL": "openai/gpt-oss-120b",
        },
    )
    runtime = resolve_ai_runtime(settings, session_api_key="visitor-groq-key")

    assert settings.provider == "groq"
    assert settings.base_url == "https://api.groq.com/openai/v1"
    assert settings.chat_model == "openai/gpt-oss-120b"
    assert runtime.api_key == "visitor-groq-key"
    assert runtime.api_key_source == "session"
    assert "visitor-groq-key" not in runtime.safe_label()


def test_key_provider_warning_catches_openrouter_key_sent_to_groq() -> None:
    warning = key_provider_warning("groq", "sk-or-v1-example")

    assert warning is not None
    assert "OpenRouter key" in warning
    assert "Groq" in warning


def test_key_provider_warning_catches_groq_key_sent_to_openrouter() -> None:
    warning = key_provider_warning("openrouter", "gsk_example")

    assert warning is not None
    assert "Groq key" in warning
    assert "OpenRouter" in warning


def test_byok_session_key_overrides_env_without_mutating_settings() -> None:
    settings = load_ai_settings(
        {
            "LEARNING_HUB_PROVIDER": "openai_compatible",
            "LEARNING_HUB_API_KEY": "owner-key",
            "LEARNING_HUB_BASE_URL": "https://gateway.example/v1",
        }
    )
    runtime = resolve_ai_runtime(settings, session_api_key="visitor-key")

    assert runtime.api_key == "visitor-key"
    assert runtime.api_key_source == "session"
    assert settings.owner_api_key == "owner-key"
    assert "visitor-key" not in runtime.safe_label()


def test_local_mode_ignores_configured_keys() -> None:
    settings = load_ai_settings(
        {
            "LEARNING_HUB_AI_MODE": "local",
            "LEARNING_HUB_API_KEY": "owner-key",
        }
    )
    runtime = resolve_ai_runtime(settings)

    assert runtime.effective_mode == "local"
    assert runtime.live_enabled is False
    assert runtime.api_key is None


def test_litellm_does_not_use_upstream_openai_key_as_gateway_key() -> None:
    settings = load_ai_settings(
        {
            "LEARNING_HUB_PROVIDER": "litellm",
            "OPENAI_API_KEY": "upstream-openai-key",
        }
    )
    runtime = resolve_ai_runtime(settings)

    assert runtime.live_enabled is False
    assert runtime.api_key is None


def test_litellm_is_not_the_default_unreachable_provider() -> None:
    settings = load_ai_settings({})

    assert settings.provider == "openrouter"
    assert settings.base_url != "http://litellm:4000/v1"
