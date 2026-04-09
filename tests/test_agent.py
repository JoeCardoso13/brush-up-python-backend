"""Tests for agent.py — teaching agent with mocked Anthropic API."""

from unittest.mock import MagicMock

import networkx as nx

from agent import build_system_prompt, build_messages, ask


def _make_mock_client(response_text="Here is my explanation."):
    """Create a mock Anthropic client that returns a canned response."""
    client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=response_text)]
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 50
    client.messages.create.return_value = mock_response
    return client


def _make_test_graph():
    """Create a small graph for agent tests."""
    g = nx.DiGraph()
    g.add_node("Class", content="Classes are blueprints for [[Object]]s.")
    g.add_node("Object", content="Everything in Python is an [[Object]].")
    g.add_edge("Class", "Object")
    g.add_edge("Object", "Class")
    return g


# ── Group F: build_system_prompt ────────────────────────────────────────


class TestBuildSystemPrompt:
    def test_contains_topic_content(self):
        context = {
            "topic": "Class",
            "content": "Classes are blueprints.",
            "neighbors": {},
        }
        prompt = build_system_prompt(context)
        assert "Classes are blueprints." in prompt

    def test_contains_neighbor_content(self):
        context = {
            "topic": "Class",
            "content": "Classes are blueprints.",
            "neighbors": {"Object": "Everything is an Object."},
        }
        prompt = build_system_prompt(context)
        assert "Everything is an Object." in prompt
        assert "Object" in prompt

    def test_contains_tutor_methodology(self):
        context = {
            "topic": "Class",
            "content": "Classes are blueprints.",
            "neighbors": {},
        }
        prompt = build_system_prompt(context)
        assert "Socratic" in prompt
        assert "Teaching Methodology" in prompt

    def test_no_topic_found(self):
        context = {"topic": "xyzzy", "content": None, "neighbors": {}}
        prompt = build_system_prompt(context)
        assert isinstance(prompt, str)
        assert "Socratic" in prompt  # tutor prompt still present


# ── Group G: build_messages ─────────────────────────────────────────────


class TestBuildMessages:
    def test_first_message_no_history(self):
        msgs = build_messages([], "What is a class?")
        assert msgs == [{"role": "user", "content": "What is a class?"}]

    def test_appends_to_history(self):
        history = [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello!"},
        ]
        msgs = build_messages(history, "What is a class?")
        assert len(msgs) == 3
        assert msgs[-1] == {"role": "user", "content": "What is a class?"}

    def test_preserves_history_order(self):
        history = [
            {"role": "user", "content": "First"},
            {"role": "assistant", "content": "Response"},
        ]
        msgs = build_messages(history, "Second")
        assert msgs[0]["content"] == "First"
        assert msgs[1]["content"] == "Response"
        assert msgs[2]["content"] == "Second"


# ── Group H: ask (mocked API) ──────────────────────────────────────────


class TestAsk:
    def test_calls_api_with_correct_model(self, monkeypatch):
        graph = _make_test_graph()
        client = _make_mock_client()
        ask(graph, "What is a class?", [], client=client)
        call_kwargs = client.messages.create.call_args
        assert "claude" in call_kwargs.kwargs.get("model", "").lower() or \
               "claude" in (call_kwargs.args[0] if call_kwargs.args else "").lower()

    def test_returns_response_text(self):
        graph = _make_test_graph()
        client = _make_mock_client("Classes are blueprints for objects.")
        response, _, _ = ask(graph, "What is a class?", [], client=client)
        assert response == "Classes are blueprints for objects."

    def test_updates_conversation_history(self):
        graph = _make_test_graph()
        client = _make_mock_client("Here is my answer.")
        _, history, _ = ask(graph, "What is a class?", [], client=client)
        assert len(history) == 2
        assert history[0] == {"role": "user", "content": "What is a class?"}
        assert history[1] == {"role": "assistant", "content": "Here is my answer."}

    def test_returns_usage(self):
        graph = _make_test_graph()
        client = _make_mock_client()
        _, _, usage = ask(graph, "What is a class?", [], client=client)
        assert usage == {"input_tokens": 100, "output_tokens": 50}

    def test_handles_unknown_topic(self):
        graph = _make_test_graph()
        client = _make_mock_client("I'm not sure about that topic.")
        response, history, _ = ask(graph, "xyzzy plugh", [], client=client)
        assert response == "I'm not sure about that topic."
        # API was still called
        client.messages.create.assert_called_once()
