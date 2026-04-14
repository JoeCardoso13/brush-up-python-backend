from pathlib import Path

import pytest
from graph import build_graph, TfidfIndex


@pytest.fixture
def mini_notes(tmp_path):
    """Create a small set of markdown notes exercising all edge cases."""
    files = {
        "Alpha.md": "Alpha links to [[Beta]] and [[Gamma]]. Also [[Beta]] again.",
        "Beta.md": "Beta links to [[Alpha]] and [[Delta]].",
        "Gamma.md": "Gamma is a leaf node. No links here.",
        "Delta.md": "Delta links to [[Delta]] which is self-referential.",
        "Epsilon.md": "A.k.a [[Beta]]",
        "Zeta.md": "Zeta links to [[Gamma]] and [[Alpha]].",
    }
    for name, content in files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    return tmp_path


@pytest.fixture
def mini_graph(mini_notes):
    """Build a DiGraph from the mini_notes fixture."""
    return build_graph(mini_notes)


@pytest.fixture
def tfidf_notes(tmp_path):
    """Notes with distinct Python-teaching vocabulary for TF-IDF tests."""
    files = {
        "Decorator.md": (
            "Decorators modify the behavior of a [[Function]] without changing its "
            "source code. A decorator is a higher-order function that takes a "
            "[[Function]] as input, wraps it inside a [[Closure]], and returns the "
            "wrapper. The @ syntax provides syntactic sugar for applying decorators."
        ),
        "List.md": (
            "A list is a mutable ordered [[Sequence]] that stores elements accessed "
            "by integer index. Lists support append, insert, and slicing operations. "
            "Unlike tuples, lists can grow and shrink dynamically."
        ),
        "Dictionary.md": (
            "A dictionary maps keys to values using a hash table. Keys must be "
            "hashable. Supports get, items, and update methods for lookup and "
            "modification of key-value pairs. Also known as an associative "
            "[[Collection]]."
        ),
        "For loop.md": (
            "A for loop iterates over elements in a [[Sequence]] or any "
            "[[Iterable]]. Use range for counter-based iteration. The loop "
            "variable is rebound on each pass through the body."
        ),
        "Class.md": (
            "A class is a blueprint for creating instances. Classes bundle data "
            "as attributes and behavior as methods. Defined with the class "
            "keyword. Supports inheritance from a parent [[Class]] and "
            "composition of [[Object]]s."
        ),
        "Recursion.md": (
            "Recursion occurs when a [[Function]] calls itself. Every recursive "
            "algorithm needs a base case to terminate. The call stack grows with "
            "each recursive invocation. A classic example is computing the "
            "factorial."
        ),
    }
    for name, content in files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    return tmp_path


@pytest.fixture
def tfidf_graph(tfidf_notes):
    """Build a DiGraph from the tfidf_notes fixture."""
    return build_graph(tfidf_notes)


@pytest.fixture
def tfidf_index(tfidf_graph):
    """Build a TfidfIndex from the tfidf_graph fixture."""
    return TfidfIndex(tfidf_graph)


@pytest.fixture(scope="session")
def real_graph():
    """Build a DiGraph from the real notes corpus."""
    return build_graph(Path(__file__).resolve().parent.parent / "notes")


@pytest.fixture(scope="session")
def real_index(real_graph):
    """Build a TfidfIndex from the real notes corpus."""
    return TfidfIndex(real_graph)
