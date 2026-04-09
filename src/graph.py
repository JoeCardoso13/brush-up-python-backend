"""Builds a NetworkX DiGraph from Obsidian-style markdown notes."""

import difflib
import re
from pathlib import Path

import networkx as nx

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def extract_wikilinks(content: str) -> list[str]:
    """Return all [[wikilink]] targets found in content, preserving duplicates."""
    return WIKILINK_RE.findall(content)


def build_graph(notes_dir: Path) -> nx.DiGraph:
    """Build a DiGraph from all .md files in notes_dir."""
    graph = nx.DiGraph()
    notes_dir = Path(notes_dir)
    md_files = sorted(notes_dir.glob("*.md"))

    for path in md_files:
        title = path.stem
        content = path.read_text(encoding="utf-8")
        graph.add_node(title, content=content)

    for path in md_files:
        title = path.stem
        content = path.read_text(encoding="utf-8")
        for target in set(extract_wikilinks(content)):
            if target != title and graph.has_node(target):
                graph.add_edge(title, target)

    return graph


def get_node_content(graph: nx.DiGraph, topic: str) -> str | None:
    """Return the raw content of a topic node, or None if not found."""
    if topic not in graph:
        return None
    return graph.nodes[topic]["content"]


def get_context(graph: nx.DiGraph, topic: str) -> dict:
    """Gather 1-hop context: topic content + all neighbor content."""
    if topic not in graph:
        return {"topic": topic, "content": None, "neighbors": {}}

    neighbors = set(graph.successors(topic)) | set(graph.predecessors(topic))
    neighbors.discard(topic)

    return {
        "topic": topic,
        "content": graph.nodes[topic]["content"],
        "neighbors": {
            n: graph.nodes[n]["content"] for n in sorted(neighbors)
        },
    }


def find_topic(graph: nx.DiGraph, query: str) -> str | None:
    """Find the best matching topic node for a query string."""
    nodes = list(graph.nodes)

    # Exact case-insensitive match
    query_lower = query.lower()
    for name in nodes:
        if name.lower() == query_lower:
            return name

    # Fuzzy match
    matches = difflib.get_close_matches(query, nodes, n=1, cutoff=0.6)
    return matches[0] if matches else None
