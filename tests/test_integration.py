"""Integration tests against the real 127-note corpus."""

from unittest.mock import MagicMock

import pytest

from agent import ask


def _make_mock_client(response_text="Here is my explanation."):
    """Create a mock Anthropic client that returns a canned response."""
    client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=response_text)]
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 50
    client.messages.create.return_value = mock_response
    return client


# ── Smoke tests ──────────────────────────────────────────────────────


class TestRealCorpusSmoke:
    def test_graph_loads_all_notes(self, real_graph):
        assert len(real_graph.nodes) >= 120
        for node in real_graph.nodes:
            content = real_graph.nodes[node].get("content", "")
            assert content, f"Node {node!r} has no content"

    def test_index_builds_and_searches(self, real_index):
        results = real_index.search("python", k=5)
        assert len(results) > 0
        for name, score in results:
            assert isinstance(name, str)
            assert 0.0 < score <= 1.0


# ── Retrieval disambiguation ────────────────────────────────────────


class TestRealCorpusRetrieval:
    def test_variable_shadowing_disambiguates(self, real_index):
        results = real_index.search("variable shadowing", k=3)
        assert results[0][0] == "Variable shadowing"

    def test_string_interpolation_disambiguates(self, real_index):
        results = real_index.search("string interpolation f-string", k=3)
        assert results[0][0] == "String interpolation"

    def test_type_error_disambiguates(self, real_index):
        results = real_index.search("TypeError exception", k=3)
        assert results[0][0] == "TypeError"

    def test_method_resolution_order(self, real_index):
        results = real_index.search("method resolution order MRO", k=3)
        names = [name for name, _ in results]
        assert "Method resolution order" in names
        assert "MRO" in names

    def test_natural_language_query(self, real_index):
        results = real_index.search("how do I loop over a list", k=3)
        assert results[0][0] == "For loop"

    def test_alias_note_retrievable(self, real_index):
        results = real_index.search("MRO", k=3)
        names = [name for name, _ in results]
        assert "MRO" in names


# ── Full chain: search -> context -> system prompt ───────────────────


class TestRealCorpusFullChain:
    def test_full_chain_grounds_in_correct_note(self, real_graph, real_index):
        client = _make_mock_client()
        ask(
            real_graph,
            "What is variable shadowing?",
            [],
            client=client,
            index=real_index,
        )
        system_prompt = client.messages.create.call_args.kwargs["system"]
        assert "Variable shadowing" in system_prompt
        assert "syntactical difference" in system_prompt

    def test_system_prompt_no_wikilink_brackets(self, real_graph, real_index):
        client = _make_mock_client()
        ask(
            real_graph,
            "What is variable shadowing?",
            [],
            client=client,
            index=real_index,
        )
        system_prompt = client.messages.create.call_args.kwargs["system"]
        assert "[[" not in system_prompt, "Raw wikilink brackets leaked into system prompt"
        assert "]]" not in system_prompt, "Raw wikilink brackets leaked into system prompt"


# ── Diverse phrasing: same topic, different questions ──────────────


class TestDiversePhrasings:
    """Multiple natural-language phrasings of the same concept must all
    ground on the correct note.  This catches brittleness in TF-IDF
    retrieval — if grounding only works for near-title queries, the
    Zettelkasten isn't really being leveraged."""

    @pytest.mark.parametrize(
        "question",
        [
            "how do for loops work in python",
            "iterating over a list with a loop",
            "what is the syntax for looping through a sequence",
            "how to use for element in collection",
        ],
    )
    def test_for_loop_phrasings(self, real_index, question):
        results = real_index.search(question, k=3)
        names = [name for name, _ in results]
        assert "For loop" in names, f"Expected 'For loop' for: {question!r}, got {names}"

    def test_decorator_direct(self, real_index):
        results = real_index.search("what is a decorator in python", k=3)
        names = [name for name, _ in results]
        assert "Decorator" in names, f"Expected 'Decorator', got {names}"

    @pytest.mark.xfail(
        reason="Decorator note is very short; indirect phrasings lose to notes "
        "with more keyword overlap (Method, Function). Retrieval improvement needed.",
        strict=False,
    )
    @pytest.mark.parametrize(
        "question",
        [
            "how does the @ symbol work on functions",
            "modifying a method with a wrapper",
        ],
    )
    def test_decorator_indirect_phrasings(self, real_index, question):
        results = real_index.search(question, k=3)
        names = [name for name, _ in results]
        assert "Decorator" in names, f"Expected 'Decorator' for: {question!r}, got {names}"

    def test_inheritance_direct(self, real_index):
        results = real_index.search("how does inheritance work", k=3)
        names = [name for name, _ in results]
        assert "Inheritance" in names, f"Expected 'Inheritance', got {names}"

    @pytest.mark.xfail(
        reason="Inheritance note is code-heavy with little keyword-rich prose; "
        "indirect phrasings lose to Class, Super, Composition. Retrieval improvement needed.",
        strict=False,
    )
    @pytest.mark.parametrize(
        "question",
        [
            "what is a subclass superclass hierarchy",
            "how to create a child class in python",
            "is-a relationship between classes",
        ],
    )
    def test_inheritance_indirect_phrasings(self, real_index, question):
        results = real_index.search(question, k=3)
        names = [name for name, _ in results]
        assert "Inheritance" in names, f"Expected 'Inheritance' for: {question!r}, got {names}"

    def test_comprehension_direct(self, real_index):
        results = real_index.search("list comprehension syntax", k=3)
        names = [name for name, _ in results]
        assert "Comprehension" in names, f"Expected 'Comprehension', got {names}"

    def test_comprehension_domain_vocabulary(self, real_index):
        results = real_index.search("how do I use selection and transformation on iterables", k=3)
        names = [name for name, _ in results]
        assert "Comprehension" in names, f"Expected 'Comprehension', got {names}"

    @pytest.mark.xfail(
        reason="'shorthand for building a list from a loop' shares more vocabulary "
        "with For loop / Loop than Comprehension. Retrieval improvement needed.",
        strict=False,
    )
    def test_comprehension_indirect_phrasing(self, real_index):
        results = real_index.search("shorthand for building a list from a loop", k=3)
        names = [name for name, _ in results]
        assert "Comprehension" in names, f"Expected 'Comprehension', got {names}"

    @pytest.mark.parametrize(
        "question",
        [
            "what is variable scope in python",
            "function scope and nested functions",
            "global and nonlocal statements",
        ],
    )
    def test_scope_phrasings(self, real_index, question):
        results = real_index.search(question, k=3)
        names = [name for name, _ in results]
        assert "Scope" in names, f"Expected 'Scope' for: {question!r}, got {names}"

    @pytest.mark.xfail(
        reason="'where can I use an identifier after initializing it' shares more "
        "vocabulary with Identifier than Scope. Retrieval improvement needed.",
        strict=False,
    )
    def test_scope_indirect_phrasing(self, real_index):
        results = real_index.search("where can I use an identifier after initializing it", k=3)
        names = [name for name, _ in results]
        assert "Scope" in names, f"Expected 'Scope', got {names}"


# ── Negative grounding: must NOT retrieve wrong note ───────────────


class TestNegativeGrounding:
    """Verify that retrieval doesn't confuse unrelated topics.
    A question about topic A should not ground on topic B."""

    def test_decorator_not_for_loop(self, real_index):
        results = real_index.search("what is a decorator in python", k=1)
        assert results[0][0] != "For loop"

    def test_for_loop_not_while(self, real_index):
        results = real_index.search("for loop iteration over a list", k=1)
        assert results[0][0] != "While"

    def test_inheritance_not_composition(self, real_index):
        results = real_index.search("subclass superclass is-a relationship", k=1)
        assert results[0][0] != "Composition"

    def test_scope_not_variable_shadowing(self, real_index):
        """Scope and Variable shadowing are related but distinct —
        a generic scope question should ground on Scope, not its neighbor."""
        results = real_index.search("what is variable scope in python", k=1)
        assert results[0][0] != "Variable shadowing"

    def test_dictionary_not_list(self, real_index):
        results = real_index.search("key value pairs hash lookup", k=1)
        assert results[0][0] != "List"

    def test_constructor_not_initializer(self, real_index):
        """Constructor and Initializer are closely related — retrieval
        should still distinguish them."""
        results = real_index.search("constructor function call to create objects", k=1)
        assert results[0][0] != "Initializer"


# ── Score sanity: grounding must be confident ──────────────────────


MINIMUM_CONFIDENT_SCORE = 0.10


class TestScoreSanity:
    """When retrieval matches the right note, the score should be
    meaningfully above the threshold.  A 'correct' match at score 0.06
    means the grounding is barely there — one vocabulary shift away
    from failing."""

    @pytest.mark.parametrize(
        "question, expected_topic",
        [
            ("what is a for loop", "For loop"),
            ("what is a decorator", "Decorator"),
            ("list comprehension syntax", "Comprehension"),
            ("what is variable scope", "Scope"),
            ("variable shadowing in python", "Variable shadowing"),
            ("string interpolation f-string", "String interpolation"),
            ("what is a dictionary", "Dictionary"),
        ],
    )
    def test_confident_score(self, real_index, question, expected_topic):
        results = real_index.search(question, k=3)
        matched = [(name, score) for name, score in results if name == expected_topic]
        assert matched, f"{expected_topic!r} not in results for {question!r}"
        score = matched[0][1]
        assert score >= MINIMUM_CONFIDENT_SCORE, (
            f"Score {score:.4f} for {expected_topic!r} is below confidence "
            f"threshold {MINIMUM_CONFIDENT_SCORE} — grounding is fragile"
        )

    @pytest.mark.xfail(
        reason="Inheritance note is code-heavy; 'what is inheritance' doesn't "
        "retrieve it in top-3. Retrieval improvement needed.",
        strict=False,
    )
    def test_confident_score_inheritance(self, real_index):
        results = real_index.search("what is inheritance", k=3)
        matched = [(name, score) for name, score in results if name == "Inheritance"]
        assert matched, f"'Inheritance' not in results, got {[n for n, _ in results]}"
        assert matched[0][1] >= MINIMUM_CONFIDENT_SCORE

    def test_top_result_always_above_threshold(self, real_index):
        """For any straightforward Python question, the top result should
        clear the confidence bar — otherwise we're serving ungrounded answers."""
        questions = [
            "how do I define a class",
            "what are boolean values",
            "explain the self parameter",
            "how does polymorphism work",
            "what is encapsulation",
        ]
        for question in questions:
            results = real_index.search(question, k=1)
            assert results, f"No results for {question!r}"
            _, score = results[0]
            assert score >= MINIMUM_CONFIDENT_SCORE, (
                f"Top score {score:.4f} for {question!r} is below "
                f"confidence threshold {MINIMUM_CONFIDENT_SCORE}"
            )
