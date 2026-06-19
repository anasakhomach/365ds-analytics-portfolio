from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.settings import load_ai_settings, resolve_ai_runtime


def test_settings_default_to_gateway_but_fall_back_without_key() -> None:
    settings = load_ai_settings({})
    runtime = resolve_ai_runtime(settings)

    assert settings.mode == "gateway"
    assert settings.provider == "litellm"
    assert runtime.effective_mode == "local"
    assert runtime.live_enabled is False
    assert runtime.api_key is None


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
