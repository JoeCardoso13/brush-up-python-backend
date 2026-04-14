"""Tests for budget.py — in-memory per-user token budget tracking."""

import pytest

from budget import (
    DEFAULT_INPUT_BUDGET,
    DEFAULT_OUTPUT_BUDGET,
    check_budget,
    record_usage,
    get_usage,
)


@pytest.fixture
def budgets():
    """Fresh empty budgets dict for each test."""
    return {}


# ── check_budget ──────────────────────────────────────────────────────


class TestCheckBudget:
    def test_new_user_within_budget(self, budgets):
        assert check_budget(budgets, "user-1") is True

    def test_input_budget_exceeded(self, budgets):
        record_usage(budgets, "user-1", 1000, 0)
        assert check_budget(budgets, "user-1", max_input_tokens=500) is False

    def test_output_budget_exceeded(self, budgets):
        record_usage(budgets, "user-1", 0, 1000)
        assert check_budget(budgets, "user-1", max_output_tokens=500) is False

    def test_exactly_at_limit_is_over(self, budgets):
        record_usage(budgets, "user-1", 100, 0)
        assert check_budget(budgets, "user-1", max_input_tokens=100) is False

    def test_within_both_limits(self, budgets):
        record_usage(budgets, "user-1", 50, 50)
        assert check_budget(budgets, "user-1", max_input_tokens=100, max_output_tokens=100) is True

    def test_default_input_budget_is_250k(self):
        assert DEFAULT_INPUT_BUDGET == 250_000

    def test_default_output_budget_is_60k(self):
        assert DEFAULT_OUTPUT_BUDGET == 60_000

    def test_uses_default_budgets_when_not_specified(self, budgets):
        record_usage(budgets, "user-1", DEFAULT_INPUT_BUDGET, 0)
        assert check_budget(budgets, "user-1") is False

    def test_uses_default_output_budget_when_not_specified(self, budgets):
        record_usage(budgets, "user-1", 0, DEFAULT_OUTPUT_BUDGET)
        assert check_budget(budgets, "user-1") is False

    def test_just_under_default_budgets_is_within(self, budgets):
        record_usage(budgets, "user-1", DEFAULT_INPUT_BUDGET - 1, DEFAULT_OUTPUT_BUDGET - 1)
        assert check_budget(budgets, "user-1") is True


# ── record_usage ─────────────────────────────────────────────────────


class TestRecordUsage:
    def test_accumulates(self, budgets):
        record_usage(budgets, "user-1", 100, 50)
        record_usage(budgets, "user-1", 200, 75)
        usage = get_usage(budgets, "user-1")
        assert usage["total_input_tokens"] == 300
        assert usage["total_output_tokens"] == 125

    def test_returns_updated_totals(self, budgets):
        result = record_usage(budgets, "user-1", 100, 50)
        assert result == {"total_input_tokens": 100, "total_output_tokens": 50}

    def test_separate_users(self, budgets):
        record_usage(budgets, "user-1", 100, 50)
        record_usage(budgets, "user-2", 200, 75)
        assert get_usage(budgets, "user-1")["total_input_tokens"] == 100
        assert get_usage(budgets, "user-2")["total_input_tokens"] == 200


# ── get_usage ─────────────────────────────────────────────────────────


class TestGetUsage:
    def test_unknown_user_returns_zeros(self, budgets):
        usage = get_usage(budgets, "nobody")
        assert usage == {"total_input_tokens": 0, "total_output_tokens": 0}

    def test_after_recording(self, budgets):
        record_usage(budgets, "user-1", 300, 150)
        usage = get_usage(budgets, "user-1")
        assert usage == {"total_input_tokens": 300, "total_output_tokens": 150}
