"""Tests for main.py — CLI chat loop."""

from unittest.mock import patch, MagicMock

from main import main


@patch("main.build_graph")
@patch("main.ask")
@patch("builtins.input", side_effect=["quit"])
def test_quit_exits_cleanly(mock_input, mock_ask, mock_build):
    mock_build.return_value = MagicMock()
    main()
    mock_ask.assert_not_called()


@patch("main.build_graph")
@patch("main.ask")
@patch("builtins.input", side_effect=["exit"])
def test_exit_exits_cleanly(mock_input, mock_ask, mock_build):
    mock_build.return_value = MagicMock()
    main()
    mock_ask.assert_not_called()


@patch("main.build_graph")
@patch("main.ask", return_value=("Here is my answer.", [], {"input_tokens": 0, "output_tokens": 0}))
@patch("builtins.input", side_effect=["What is a class?", "quit"])
def test_question_produces_output(mock_input, mock_ask, mock_build, capsys):
    mock_build.return_value = MagicMock()
    main()
    mock_ask.assert_called_once()
    captured = capsys.readouterr()
    assert "Here is my answer." in captured.out


@patch("main.build_graph")
@patch("main.ask")
@patch("builtins.input", side_effect=EOFError)
def test_eof_exits_cleanly(mock_input, mock_ask, mock_build):
    mock_build.return_value = MagicMock()
    main()  # should not raise
    mock_ask.assert_not_called()


@patch("main.build_graph")
@patch("main.ask")
@patch("builtins.input", side_effect=["", "  ", "quit"])
def test_empty_input_skipped(mock_input, mock_ask, mock_build):
    mock_build.return_value = MagicMock()
    main()
    mock_ask.assert_not_called()
