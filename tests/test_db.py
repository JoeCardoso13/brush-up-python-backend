"""Tests for db.py — SQLite budget tracking."""

import pytest

from db import init_db, check_budget, record_usage, get_usage


@pytest.fixture
def conn():
    """In-memory SQLite connection for testing."""
    connection = init_db(":memory:")
    yield connection
    connection.close()


# ── Group I: init_db ───────────────────────────────────────────────────


class TestInitDb:
    def test_creates_users_table(self, conn):
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert any(row["name"] == "users" for row in tables)

    def test_idempotent(self, conn):
        init_db(":memory:")  # calling again should not error


# ── Group J: check_budget ──────────────────────────────────────────────


class TestCheckBudget:
    def test_new_user_within_budget(self, conn):
        assert check_budget(conn, "user-1") is True

    def test_input_budget_exceeded(self, conn):
        record_usage(conn, "user-1", 1000, 0)
        assert check_budget(conn, "user-1", max_input_tokens=500) is False

    def test_output_budget_exceeded(self, conn):
        record_usage(conn, "user-1", 0, 1000)
        assert check_budget(conn, "user-1", max_output_tokens=500) is False

    def test_exactly_at_limit_is_over(self, conn):
        record_usage(conn, "user-1", 100, 0)
        assert check_budget(conn, "user-1", max_input_tokens=100) is False

    def test_within_both_limits(self, conn):
        record_usage(conn, "user-1", 50, 50)
        assert check_budget(conn, "user-1", max_input_tokens=100, max_output_tokens=100) is True


# ── Group K: record_usage ─────────────────────────────────────────────


class TestRecordUsage:
    def test_accumulates(self, conn):
        record_usage(conn, "user-1", 100, 50)
        record_usage(conn, "user-1", 200, 75)
        usage = get_usage(conn, "user-1")
        assert usage["total_input_tokens"] == 300
        assert usage["total_output_tokens"] == 125

    def test_returns_updated_totals(self, conn):
        result = record_usage(conn, "user-1", 100, 50)
        assert result == {"total_input_tokens": 100, "total_output_tokens": 50}

    def test_separate_users(self, conn):
        record_usage(conn, "user-1", 100, 50)
        record_usage(conn, "user-2", 200, 75)
        assert get_usage(conn, "user-1")["total_input_tokens"] == 100
        assert get_usage(conn, "user-2")["total_input_tokens"] == 200


# ── Group L: get_usage ─────────────────────────────────────────────────


class TestGetUsage:
    def test_nonexistent_user(self, conn):
        assert get_usage(conn, "nobody") is None

    def test_new_user_zeros(self, conn):
        check_budget(conn, "user-1")  # creates the user
        usage = get_usage(conn, "user-1")
        assert usage == {"total_input_tokens": 0, "total_output_tokens": 0}
