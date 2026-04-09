import pytest
from graph import build_graph


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
