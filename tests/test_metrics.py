# PROMPT:
# Generate pytest tests for a FastAPI Store Intelligence API.
# Validate metrics endpoint, empty store behavior,
# conversion rate calculation and response structure.
#
# CHANGES MADE:
# Added project-specific assertions.
# Added conversion-rate validation.
# Adapted to current API schema.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_endpoint_exists():

    response = client.get(
        "/stores/store_1/metrics"
    )

    assert response.status_code == 200


def test_metrics_response_structure():

    response = client.get(
        "/stores/store_1/metrics"
    )

    data = response.json()

    assert "store_id" in data
    assert "unique_visitors" in data
    assert "entry" in data
    assert "exit" in data
    assert "conversion_rate" in data
    assert "avg_dwell_ms" in data


def test_empty_store_metrics():

    response = client.get(
        "/stores/nonexistent_store/metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["store_id"] == "nonexistent_store"
    assert data["conversion_rate"] == 0