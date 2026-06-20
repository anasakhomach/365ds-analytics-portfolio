from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.assistant import LearningAssistant
from learning_hub.indexing import build_local_index, load_local_index
from learning_hub.settings import load_ai_settings, resolve_ai_runtime


class FakeLLMClient:
    def __init__(self) -> None:
        self.messages: list[dict[str, str]] = []

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.messages = messages
        return "Synthesized portfolio answer with citations."

    def stream(self, messages: list[dict[str, str]]):
        self.messages = messages
        yield "Streamed "
        yield "portfolio "
        yield "answer."


class RateLimitedLLMClient:
    def complete(self, messages: list[dict[str, str]]) -> str:
        raise FakeProviderError("shared key rate limited", status_code=429)

    def stream(self, messages: list[dict[str, str]]):
        raise FakeProviderError("shared key rate limited", status_code=429)
        yield ""


class ConnectionFailedLLMClient:
    def complete(self, messages: list[dict[str, str]]) -> str:
        raise FakeProviderError("gateway unreachable")

    def stream(self, messages: list[dict[str, str]]):
        raise FakeProviderError("gateway unreachable")
        yield ""


class FakeProviderError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class FreeQuotaLLMClient:
    def complete(self, messages: list[dict[str, str]]) -> str:
        raise FakeProviderError("Payment required: free quota exhausted", status_code=402)

    def stream(self, messages: list[dict[str, str]]):
        raise FakeProviderError("Payment required: free quota exhausted", status_code=402)
        yield ""


def test_assistant_answers_with_citations(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path))
    response = assistant.answer("Which projects use medallion layers?")
    assert response.route == "rag"
    assert response.citations
    assert "indexed project sources" in response.answer


def test_assistant_routes_tracking_model_question_to_gold_data(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path))
    response = assistant.answer(
        "What is the R-squared value and 1200 minute prediction?",
        project_slug="tracking-user-engagement",
    )
    assert response.route == "data"
    assert response.data_result is not None
    assert "r_squared" in response.data_result.columns


def test_assistant_refuses_when_no_context_is_found(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path))
    response = assistant.answer("zxqv impossible unrelated alien banana", project_slug="checkout-flow-optimization")
    assert response.route == "rag_no_context"
    assert "I don't know" in response.answer


def test_assistant_uses_llm_client_when_context_exists(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    response = assistant.answer("Which projects use medallion layers?")

    assert response.route == "llm_rag"
    assert response.answer == "Synthesized portfolio answer with citations."
    assert response.citations
    assert any("Cite sources" in message["content"] for message in llm_client.messages)


def test_assistant_passes_recent_history_to_llm_prompt(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    assistant.answer(
        "Does that mean DuckDB plays the role of the DWH?",
        history=[
            {"role": "user", "content": "How does DuckDB fit into this project?"},
            {"role": "assistant", "content": "DuckDB stores the Bronze, Silver, and Gold marts."},
        ],
    )

    prompt = "\n".join(message["content"] for message in llm_client.messages)
    assert "Recent conversation" in prompt
    assert "How does DuckDB fit into this project?" in prompt
    assert "DuckDB stores the Bronze, Silver, and Gold marts." in prompt


def test_assistant_answers_runtime_model_questions_without_rag(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    runtime = resolve_ai_runtime(
        load_ai_settings(
            {
                "LEARNING_HUB_AI_MODE": "provider",
                "LEARNING_HUB_PROVIDER": "openai_compatible",
                "LEARNING_HUB_BASE_URL": "https://api.groq.com/openai/v1",
                "LEARNING_HUB_CHAT_MODEL": "llama-3.3-70b-versatile",
            }
        ),
        session_api_key="visitor-key",
    )
    assistant = LearningAssistant(index=load_local_index(tmp_path), runtime=runtime)

    response = assistant.answer("Which model are you?")

    assert response.route == "runtime"
    assert "llama-3.3-70b-versatile" in response.answer
    assert "openai_compatible" in response.answer
    assert "session" in response.answer
    assert "LinearRegression" not in response.answer


def test_assistant_answers_help_questions_without_rag_or_llm(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    response = assistant.answer("how can you help me")

    assert response.route == "capabilities"
    assert "explain the five analytics projects" in response.answer.lower()
    assert "approved Gold marts" in response.answer
    assert "project instructions" not in response.answer.lower()
    assert llm_client.messages == []


def test_assistant_answers_greetings_without_rag_or_llm(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    response = assistant.answer("hi")

    assert response.route == "capabilities"
    assert "Hi" in response.answer
    assert "ask about the projects" in response.answer
    assert llm_client.messages == []


def test_assistant_answers_sql_capability_questions_without_rag_or_llm(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    response = assistant.answer("can you run or write sql queies")

    assert response.route == "capabilities"
    assert "read-only" in response.answer
    assert "gold.*" in response.answer
    assert "writes" in response.answer
    assert llm_client.messages == []


def test_follow_up_question_uses_recent_history_for_retrieval(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path))

    response = assistant.answer(
        "Does it play the role of a DWH?",
        history=[
            {"role": "user", "content": "How does DuckDB fit into this project?"},
            {"role": "assistant", "content": "DuckDB is the local warehouse for the medallion layers."},
        ],
    )

    assert response.route == "rag"
    joined = " ".join(citation.path for citation in response.citations).lower()
    assert response.citations
    assert "duckdb" in response.answer.lower() or "warehouse" in response.answer.lower() or "data_flow" in joined


def test_sql_first_medallion_question_uses_project_traits(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path))

    response = assistant.answer("Which projects use SQL-first medallion layers?")

    assert response.route == "project_traits"
    assert "Checkout Flow Optimization" in response.answer
    assert "Customer Engagement Analysis" in response.answer
    assert "Tracking User Engagement" in response.answer
    assert "Real Estate Market Analysis" in response.answer
    assert "Python-first" in response.answer


def test_langgraph_backend_matches_custom_for_structured_questions(tmp_path: Path) -> None:
    if importlib.util.find_spec("langgraph") is None:
        pytest.skip("langgraph is not installed")
    build_local_index(tmp_path)
    assistant = LearningAssistant(
        index=load_local_index(tmp_path),
        agent_backend="langgraph",
        thread_id="test-langgraph-structured",
    )

    response = assistant.answer("Which projects use SQL-first medallion layers?")

    assert response.route == "project_traits"
    assert "Checkout Flow Optimization" in response.answer
    assert "Tracking User Engagement" in response.answer


def test_langgraph_backend_can_route_to_safe_gold_data(tmp_path: Path) -> None:
    if importlib.util.find_spec("langgraph") is None:
        pytest.skip("langgraph is not installed")
    build_local_index(tmp_path)
    assistant = LearningAssistant(
        index=load_local_index(tmp_path),
        agent_backend="langgraph",
        thread_id="test-langgraph-data",
    )

    response = assistant.answer(
        "What is the R-squared value and 1200 minute prediction?",
        project_slug="tracking-user-engagement",
    )

    assert response.route == "data"
    assert response.data_result is not None
    assert "r_squared" in response.data_result.columns


def test_langgraph_backend_answers_capability_questions(tmp_path: Path) -> None:
    if importlib.util.find_spec("langgraph") is None:
        pytest.skip("langgraph is not installed")
    build_local_index(tmp_path)
    assistant = LearningAssistant(
        index=load_local_index(tmp_path),
        agent_backend="langgraph",
        thread_id="test-langgraph-capabilities",
    )

    response = assistant.answer("how can you help me")

    assert response.route == "capabilities"
    assert "approved Gold marts" in response.answer


def test_assistant_streams_llm_answer_when_context_exists(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    response_shell, chunks = assistant.stream_answer("Which projects use medallion layers?")
    streamed = "".join(chunks)

    assert response_shell.route == "llm_rag"
    assert streamed == "Streamed portfolio answer."
    assert response_shell.citations


def test_assistant_does_not_call_llm_when_context_is_missing(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    llm_client = FakeLLMClient()
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=llm_client)

    response = assistant.answer("zxqv impossible unrelated alien banana", project_slug="checkout-flow-optimization")

    assert response.route == "rag_no_context"
    assert llm_client.messages == []


def test_assistant_classifies_rate_limit_fallback_and_prompts_byok(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=RateLimitedLLMClient())

    response = assistant.answer("Which projects use medallion layers?")

    assert response.route == "rag"
    assert response.provider_error is not None
    assert response.provider_error.category == "rate_limit"
    assert "shared demo key is temporarily busy" in response.answer
    assert "session API key" in response.answer


def test_assistant_classifies_openrouter_free_quota_as_rate_limit(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=FreeQuotaLLMClient())

    response = assistant.answer("Which projects use medallion layers?")

    assert response.provider_error is not None
    assert response.provider_error.category == "rate_limit"
    assert "free quota" in response.answer.lower()


def test_assistant_classifies_connection_failure_without_byok_prompt(tmp_path: Path) -> None:
    build_local_index(tmp_path)
    assistant = LearningAssistant(index=load_local_index(tmp_path), llm_client=ConnectionFailedLLMClient())

    response = assistant.answer("Which projects use medallion layers?")

    assert response.provider_error is not None
    assert response.provider_error.category == "connection"
    assert "provider or gateway is unreachable" in response.answer
