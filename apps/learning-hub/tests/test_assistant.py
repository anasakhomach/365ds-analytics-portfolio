from __future__ import annotations

import sys
from pathlib import Path

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
