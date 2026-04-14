"""End-to-end API checks using the real FastAPI lifespan."""

import importlib

from fastapi.testclient import TestClient

from budget import DEFAULT_INPUT_BUDGET, DEFAULT_OUTPUT_BUDGET, record_usage


def _fresh_api_module():
    import api

    return importlib.reload(api)


class TestApiE2E:
    def test_health_endpoint_uses_real_startup_state(self):
        api = _fresh_api_module()

        with TestClient(api.app, raise_server_exceptions=True) as client:
            resp = client.get("/api/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["topics"] > 0

    def test_budget_exceeded_short_circuits_before_external_api_call(self):
        api = _fresh_api_module()

        with TestClient(api.app, raise_server_exceptions=True) as client:
            record_usage(
                api.app.state.budgets,
                "heavy-user",
                DEFAULT_INPUT_BUDGET,
                DEFAULT_OUTPUT_BUDGET,
            )

            resp = client.post(
                "/api/chat",
                json={
                    "user_id": "heavy-user",
                    "question": "Explain classes",
                    "conversation_history": [],
                },
            )

        assert resp.status_code == 429
        assert resp.json()["error"] == "budget_exceeded"

    def test_removed_usage_endpoint_returns_404(self):
        api = _fresh_api_module()

        with TestClient(api.app, raise_server_exceptions=True) as client:
            resp = client.get("/api/usage/test-user")

        assert resp.status_code == 404
