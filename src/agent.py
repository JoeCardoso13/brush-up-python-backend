"""Teaching agent — gathers graph context and calls Claude to teach Python."""

import logging
import os
import anthropic
from pathlib import Path

from graph import TfidfIndex, get_context

logger = logging.getLogger("brush-up.agent")

MODEL = os.environ.get("BRUSH_UP_MODEL", "claude-sonnet-4-20250514")

_TUTOR_PROMPT_PATH = Path(__file__).resolve().parent.parent / "tutor_prompt.md"
_TUTOR_PROMPT = _TUTOR_PROMPT_PATH.read_text(encoding="utf-8")


def build_system_prompt(context: dict) -> str:
    """Build a system prompt from the tutor prompt + graph context."""
    if context["content"] is None:
        return (
            f"{_TUTOR_PROMPT}\n\n---\n\n"
            "The student asked about a topic not found in your notes. "
            "Help them rephrase or suggest related Python topics."
        )

    parts = [
        _TUTOR_PROMPT,
        "# Reference Notes\n\n"
        "Use these notes as your primary reference material. "
        "Stay grounded in this content when teaching.\n\n"
        f"## {context['topic']}\n\n{context['content']}",
    ]

    for name, content in context["neighbors"].items():
        parts.append(f"## {name}\n\n{content}")

    return "\n\n---\n\n".join(parts)


def build_messages(history: list[dict], question: str) -> list[dict]:
    """Append the user's question to conversation history."""
    return history + [{"role": "user", "content": question}]


def ask(graph, question: str, conversation_history: list[dict], *, client=None, index=None):
    """Find relevant context, call Claude, return (response_text, updated_history, usage).

    ``usage`` includes token counts and a ``retrieval`` dict with
    ``topic``, ``score``, and ``neighbors`` so callers can audit grounding.
    """
    if client is None:
        client = anthropic.Anthropic()
    if index is None:
        index = TfidfIndex(graph)

    matches = index.search(question, k=1)
    topic = matches[0][0] if matches else None
    score = matches[0][1] if matches else 0.0

    if topic:
        context = get_context(graph, topic)
        neighbor_count = len(context["neighbors"])
        logger.info(
            "retrieval topic=%r score=%.3f neighbors=%d question=%r",
            topic,
            score,
            neighbor_count,
            question,
        )
    else:
        context = {"topic": question, "content": None, "neighbors": {}}
        neighbor_count = 0
        logger.warning("retrieval no_match question=%r", question)

    system_prompt = build_system_prompt(context)
    messages = build_messages(conversation_history, question)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )

    assistant_text = response.content[0].text
    updated_history = messages + [{"role": "assistant", "content": assistant_text}]
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "retrieval": {
            "topic": topic,
            "score": round(score, 4),
            "neighbors": neighbor_count,
        },
    }

    return assistant_text, updated_history, usage
