"""Builds a NetworkX DiGraph from Obsidian-style markdown notes."""

import logging
import math
import re
from pathlib import Path

import networkx as nx

logger = logging.getLogger("brush-up.graph")

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TOKEN_RE = re.compile(r"[a-z0-9]+")


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

    logger.info(
        "graph built: %d nodes, %d edges from %s",
        graph.number_of_nodes(),
        graph.number_of_edges(),
        notes_dir,
    )
    return graph


def get_node_content(graph: nx.DiGraph, topic: str) -> str | None:
    """Return the raw content of a topic node, or None if not found."""
    if topic not in graph:
        return None
    return graph.nodes[topic]["content"]


def _strip_wikilinks(text: str) -> str:
    """Replace [[target]] with target, removing bracket markup."""
    return WIKILINK_RE.sub(r"\1", text)


def get_context(graph: nx.DiGraph, topic: str) -> dict:
    """Gather 1-hop context: topic content + all neighbor content.

    Wikilink brackets are stripped so the content is clean for display
    in system prompts.
    """
    if topic not in graph:
        return {"topic": topic, "content": None, "neighbors": {}}

    neighbors = set(graph.successors(topic)) | set(graph.predecessors(topic))
    neighbors.discard(topic)

    return {
        "topic": topic,
        "content": _strip_wikilinks(graph.nodes[topic]["content"]),
        "neighbors": {
            n: _strip_wikilinks(graph.nodes[n]["content"]) for n in sorted(neighbors)
        },
    }



def _normalize_text(text: str) -> list[str]:
    """Lowercase text and extract alphanumeric tokens."""
    return TOKEN_RE.findall(text.lower())


def _searchable_content(title: str, content: str) -> str:
    """Combine title and body text, stripping wikilink markup but keeping link text."""
    cleaned_content = WIKILINK_RE.sub(r"\1", content)
    # Repeat the title to create a strong but bounded title signal.
    return f"{title} {title} {title} {cleaned_content}"


class TfidfIndex:
    """A small TF-IDF index over graph node titles and note content."""

    def __init__(self, graph: nx.DiGraph):
        self._documents: list[tuple[str, dict[str, float], float]] = []
        self._idf: dict[str, float] = {}

        nodes = list(graph.nodes(data=True))
        if not nodes:
            return

        tokenized_docs: list[tuple[str, list[str]]] = []
        document_frequency: dict[str, int] = {}

        for title, attrs in nodes:
            tokens = _normalize_text(_searchable_content(title, attrs.get("content", "")))
            tokenized_docs.append((title, tokens))
            for token in set(tokens):
                document_frequency[token] = document_frequency.get(token, 0) + 1

        doc_count = len(tokenized_docs)
        self._idf = {
            token: math.log((1 + doc_count) / (1 + freq)) + 1.0
            for token, freq in document_frequency.items()
        }

        for title, tokens in tokenized_docs:
            if not tokens:
                self._documents.append((title, {}, 0.0))
                continue

            term_counts: dict[str, int] = {}
            for token in tokens:
                term_counts[token] = term_counts.get(token, 0) + 1

            token_count = len(tokens)
            vector = {
                token: (count / token_count) * self._idf[token]
                for token, count in term_counts.items()
            }
            norm = math.sqrt(sum(weight * weight for weight in vector.values()))
            self._documents.append((title, vector, norm))

        logger.info(
            "tfidf index built: %d documents, %d terms",
            len(self._documents),
            len(self._idf),
        )

    def search(self, query: str, k: int = 3, threshold: float = 0.05) -> list[tuple[str, float]]:
        """Return up to k (title, score) matches by cosine similarity."""
        if not query or not query.strip() or not self._documents or k <= 0:
            return []

        query_tokens = _normalize_text(query)
        if not query_tokens:
            return []

        query_counts: dict[str, int] = {}
        for token in query_tokens:
            if token in self._idf:
                query_counts[token] = query_counts.get(token, 0) + 1

        if not query_counts:
            return []

        token_count = len(query_tokens)
        query_vector = {
            token: (count / token_count) * self._idf[token]
            for token, count in query_counts.items()
        }
        query_norm = math.sqrt(sum(weight * weight for weight in query_vector.values()))
        if query_norm == 0.0:
            return []

        scored: list[tuple[str, float]] = []
        for title, doc_vector, doc_norm in self._documents:
            if doc_norm == 0.0:
                continue
            dot = sum(query_vector[token] * doc_vector.get(token, 0.0) for token in query_vector)
            if dot == 0.0:
                continue
            score = dot / (query_norm * doc_norm)
            if score >= threshold:
                scored.append((title, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        results = scored[:k]

        if results:
            logger.debug(
                "tfidf search query=%r top=%s score=%.3f candidates=%d",
                query,
                results[0][0],
                results[0][1],
                len(scored),
            )
        else:
            logger.debug("tfidf search query=%r no_matches", query)

        return results
