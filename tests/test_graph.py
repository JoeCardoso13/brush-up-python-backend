"""Tests for graph.py — knowledge graph builder."""

from graph import (
    extract_wikilinks,
    build_graph,
    get_node_content,
    get_context,
    find_topic,
)


# ── Group A: extract_wikilinks ──────────────────────────────────────────


class TestExtractWikilinks:
    def test_single_link(self):
        assert extract_wikilinks("See [[Class]] for details.") == ["Class"]

    def test_multiple_links(self):
        text = "A [[Class]] uses [[Method]]s and [[Attribute]]s."
        assert extract_wikilinks(text) == ["Class", "Method", "Attribute"]

    def test_duplicate_links(self):
        text = "[[Foo]] is great. [[Foo]] again. And [[Foo]]."
        assert extract_wikilinks(text) == ["Foo", "Foo", "Foo"]

    def test_no_links(self):
        assert extract_wikilinks("Just plain text, no links.") == []

    def test_empty_string(self):
        assert extract_wikilinks("") == []

    def test_link_with_spaces(self):
        text = "See [[Class method]] and [[Variable reassignment]]."
        assert extract_wikilinks(text) == ["Class method", "Variable reassignment"]

    def test_mixed_content(self):
        text = (
            "Some text with [[Link1]].\n"
            "```python\n"
            "code_here()\n"
            "```\n"
            "More text with [[Link2]]."
        )
        assert extract_wikilinks(text) == ["Link1", "Link2"]


# ── Group B: build_graph structure ──────────────────────────────────────


class TestBuildGraph:
    def test_node_count(self, mini_graph):
        assert mini_graph.number_of_nodes() == 6

    def test_node_names(self, mini_graph):
        expected = {"Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"}
        assert set(mini_graph.nodes) == expected

    def test_node_content_attached(self, mini_notes, mini_graph):
        for node in mini_graph.nodes:
            content = mini_graph.nodes[node]["content"]
            file_content = (mini_notes / f"{node}.md").read_text(encoding="utf-8")
            assert content == file_content

    def test_edge_count(self, mini_graph):
        # Alpha->Beta, Alpha->Gamma, Beta->Alpha, Beta->Delta,
        # Epsilon->Beta, Zeta->Gamma, Zeta->Alpha = 7 edges
        # Delta->Delta is self-loop, excluded
        assert mini_graph.number_of_edges() == 7

    def test_no_self_loops(self, mini_graph):
        for u, v in mini_graph.edges:
            assert u != v, f"Self-loop found: {u} -> {v}"

    def test_no_duplicate_edges(self, mini_graph):
        edges = list(mini_graph.edges)
        assert len(edges) == len(set(edges))

    def test_directed_edges(self, mini_graph):
        # Gamma links to nothing, so no Gamma -> anything edge
        assert not mini_graph.has_edge("Gamma", "Alpha")
        assert not mini_graph.has_edge("Gamma", "Beta")
        # But Alpha -> Gamma exists
        assert mini_graph.has_edge("Alpha", "Gamma")

    def test_empty_directory(self, tmp_path):
        graph = build_graph(tmp_path)
        assert graph.number_of_nodes() == 0
        assert graph.number_of_edges() == 0

    def test_non_md_files_ignored(self, tmp_path):
        (tmp_path / "notes.txt").write_text("not a note")
        (tmp_path / "script.py").write_text("not a note")
        (tmp_path / "Real.md").write_text("A real note.")
        graph = build_graph(tmp_path)
        assert set(graph.nodes) == {"Real"}

    def test_alias_note_edges(self, mini_graph):
        # Epsilon is "A.k.a [[Beta]]" — should have edge to Beta
        assert mini_graph.has_edge("Epsilon", "Beta")
        assert mini_graph.out_degree("Epsilon") == 1


# ── Group C: get_node_content ───────────────────────────────────────────


class TestGetNodeContent:
    def test_existing_topic(self, mini_graph):
        content = get_node_content(mini_graph, "Gamma")
        assert content == "Gamma is a leaf node. No links here."

    def test_nonexistent_topic(self, mini_graph):
        assert get_node_content(mini_graph, "Nonexistent") is None

    def test_preserves_raw_content(self, mini_graph):
        content = get_node_content(mini_graph, "Alpha")
        assert "[[Beta]]" in content  # wikilinks remain in raw content


# ── Group D: get_context ────────────────────────────────────────────────


class TestGetContext:
    def test_includes_topic_content(self, mini_graph):
        ctx = get_context(mini_graph, "Alpha")
        assert ctx["topic"] == "Alpha"
        assert "Alpha links to" in ctx["content"]

    def test_includes_successors(self, mini_graph):
        ctx = get_context(mini_graph, "Alpha")
        # Alpha -> Beta and Alpha -> Gamma
        assert "Beta" in ctx["neighbors"]
        assert "Gamma" in ctx["neighbors"]

    def test_includes_predecessors(self, mini_graph):
        ctx = get_context(mini_graph, "Alpha")
        # Beta -> Alpha and Zeta -> Alpha
        assert "Beta" in ctx["neighbors"]
        assert "Zeta" in ctx["neighbors"]

    def test_no_self_in_neighbors(self, mini_graph):
        ctx = get_context(mini_graph, "Alpha")
        assert "Alpha" not in ctx["neighbors"]

    def test_bidirectional_neighbor_once(self, mini_graph):
        # Alpha <-> Beta — Beta appears once in Alpha's neighbors
        ctx = get_context(mini_graph, "Alpha")
        assert "Beta" in ctx["neighbors"]
        # neighbors is a dict so inherently deduplicated; just check content
        assert ctx["neighbors"]["Beta"] == "Beta links to [[Alpha]] and [[Delta]]."

    def test_nonexistent_topic(self, mini_graph):
        ctx = get_context(mini_graph, "Nope")
        assert ctx == {"topic": "Nope", "content": None, "neighbors": {}}

    def test_leaf_node_has_predecessor_neighbors(self, mini_graph):
        # Gamma has no outgoing links, but Alpha -> Gamma and Zeta -> Gamma
        ctx = get_context(mini_graph, "Gamma")
        assert "Alpha" in ctx["neighbors"]
        assert "Zeta" in ctx["neighbors"]


# ── Group E: find_topic ─────────────────────────────────────────────────


class TestFindTopic:
    def test_exact_match(self, mini_graph):
        assert find_topic(mini_graph, "Alpha") == "Alpha"

    def test_case_insensitive(self, mini_graph):
        assert find_topic(mini_graph, "alpha") == "Alpha"

    def test_fuzzy_match(self, mini_graph):
        assert find_topic(mini_graph, "Alph") == "Alpha"

    def test_multi_word_query(self):
        """Test with a graph that has multi-word node names."""
        import networkx as nx

        g = nx.DiGraph()
        g.add_node("Class method", content="...")
        g.add_node("Class variable", content="...")
        assert find_topic(g, "class method") == "Class method"

    def test_no_match(self, mini_graph):
        assert find_topic(mini_graph, "xyzzy") is None

    def test_fuzzy_prefers_closest(self, mini_graph):
        # "Bet" should match "Beta" not "Zeta"
        assert find_topic(mini_graph, "Bet") == "Beta"
