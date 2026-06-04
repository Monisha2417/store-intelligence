# PROMPT:
# Generate pytest tests for FastAPI health endpoint.
#
# CHANGES MADE:
# Adapted for Store Intelligence API.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data