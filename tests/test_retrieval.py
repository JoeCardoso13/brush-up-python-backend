"""Tests for TF-IDF retrieval — TfidfIndex in graph.py."""

import networkx as nx

from graph import TfidfIndex


# ── Group E: TfidfIndex construction ──────────────────────────────────


class TestTfidfIndexConstruction:
    def test_index_builds_from_graph(self, tfidf_graph):
        index = TfidfIndex(tfidf_graph)
        assert isinstance(index, TfidfIndex)

    def test_index_covers_all_nodes(self, tfidf_index):
        """Every graph node should be reachable via a title search."""
        for title in ("Decorator", "List", "Dictionary", "For loop", "Class", "Recursion"):
            results = tfidf_index.search(title, k=6)
            names = [name for name, _ in results]
            assert title in names, f"{title} not reachable via search"

    def test_index_empty_graph(self):
        empty = nx.DiGraph()
        index = TfidfIndex(empty)
        assert index.search("anything") == []

    def test_index_single_node_graph(self):
        g = nx.DiGraph()
        g.add_node("Solo", content="This document is about testing edge cases.")
        index = TfidfIndex(g)
        results = index.search("testing")
        assert len(results) == 1
        assert results[0][0] == "Solo"


# ── Group F: TfidfIndex search behavior ───────────────────────────────


class TestTfidfSearch:
    def test_returns_list_of_tuples(self, tfidf_index):
        results = tfidf_index.search("decorator")
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], float)

    def test_decorator_query(self, tfidf_index):
        results = tfidf_index.search("decorator wrapping higher-order")
        assert results[0][0] == "Decorator"

    def test_dictionary_query(self, tfidf_index):
        results = tfidf_index.search("key value pairs hash lookup")
        assert results[0][0] == "Dictionary"

    def test_recursion_query(self, tfidf_index):
        results = tfidf_index.search("recursive base case call stack")
        assert results[0][0] == "Recursion"

    def test_scores_descending(self, tfidf_index):
        results = tfidf_index.search("mutable ordered sequence")
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)

    def test_scores_between_zero_and_one(self, tfidf_index):
        results = tfidf_index.search("decorator")
        for _, score in results:
            assert 0.0 < score <= 1.0

    def test_default_k_is_three(self):
        # Purpose-built corpus: 5 notes all mentioning "python", so a search
        # for "python" matches all 5. Default k=3 must truncate to exactly 3.
        g = nx.DiGraph()
        for i in range(5):
            g.add_node(f"Topic{i}", content=f"Topic{i} is about python programming.")
        index = TfidfIndex(g)
        results = index.search("python")
        assert len(results) == 3

    def test_custom_k_truncates(self):
        # Same 5-note corpus. k=1 must return exactly 1, k=5 all 5.
        g = nx.DiGraph()
        for i in range(5):
            g.add_node(f"Topic{i}", content=f"Topic{i} is about python programming.")
        index = TfidfIndex(g)
        results_one = index.search("python", k=1)
        assert len(results_one) == 1
        results_five = index.search("python", k=5)
        assert len(results_five) == 5

    def test_threshold_filters(self, tfidf_index):
        results_low = tfidf_index.search("decorator wrapping", threshold=0.01)
        results_high = tfidf_index.search("decorator wrapping", threshold=0.9)
        assert len(results_high) < len(results_low)

    def test_no_match_returns_empty(self, tfidf_index):
        results = tfidf_index.search("quantum entanglement spacetime")
        assert results == []

    def test_empty_query_returns_empty(self, tfidf_index):
        assert tfidf_index.search("") == []
        assert tfidf_index.search("   ") == []

    def test_case_insensitive(self, tfidf_index):
        results = tfidf_index.search("DICTIONARY HASH LOOKUP")
        assert results[0][0] == "Dictionary"

    def test_partial_overlap_multiple_results(self, tfidf_index):
        results = tfidf_index.search("iterating over elements in a sequence")
        names = [name for name, _ in results]
        assert "List" in names
        assert "For loop" in names


# ── Group G: TF-IDF title boost & wikilink handling ───────────────────


class TestTfidfTitleBoostAndWikilinks:
    def test_title_match_ranks_first(self, tfidf_index):
        results = tfidf_index.search("recursion")
        assert results[0][0] == "Recursion"

    def test_title_boost_beats_body_mention(self):
        """A note titled 'Sorting' should outrank a note that mentions sorting in body."""
        g = nx.DiGraph()
        g.add_node("Sorting", content="Sorting arranges items in order.")
        g.add_node("Algorithms", content="Common algorithms include sorting and searching.")
        index = TfidfIndex(g)
        results = index.search("sorting")
        assert results[0][0] == "Sorting"

    def test_wikilink_brackets_stripped(self, tfidf_index):
        """Both Decorator and Recursion contain [[Function]] — searching
        'function' must find both, proving brackets were stripped."""
        results = tfidf_index.search("function", k=6)
        names = [name for name, _ in results]
        assert "Decorator" in names
        assert "Recursion" in names

    def test_wikilink_text_searchable(self, tfidf_index):
        # "Closure" only appears as [[Closure]] in Decorator note
        results = tfidf_index.search("Closure")
        names = [name for name, _ in results]
        assert "Decorator" in names

    def test_multiword_title_boost(self, tfidf_index):
        results = tfidf_index.search("for loop")
        assert results[0][0] == "For loop"

    def test_body_relevance_not_suppressed(self, tfidf_index):
        # None of "mutable", "append", "slicing" are in the title "List"
        # but they're all in the body — body signal must not be drowned by title boost
        results = tfidf_index.search("mutable append slicing")
        assert results[0][0] == "List"
