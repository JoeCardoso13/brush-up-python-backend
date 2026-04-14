"""CLI chat loop for the Python teaching agent."""

from pathlib import Path

from agent import ask
from graph import build_graph, TfidfIndex

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"


def main():
    graph = build_graph(NOTES_DIR)
    index = TfidfIndex(graph)
    history = []

    print("Python Tutor (type 'quit' or 'exit' to stop)\n")

    try:
        while True:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() in ("quit", "exit"):
                break
            response, history, _ = ask(graph, question, history, index=index)
            print(f"\nTutor: {response}\n")
    except (EOFError, KeyboardInterrupt):
        pass

    print("Goodbye!")


if __name__ == "__main__":
    main()
