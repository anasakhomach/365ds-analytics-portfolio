from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from learning_hub.assistant import LearningAssistant
from learning_hub.indexing import build_local_index, load_local_index


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
