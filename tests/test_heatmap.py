# PROMPT:
# Generate pytest tests for heatmap endpoint.
# Validate schema and endpoint availability.
#
# CHANGES MADE:
# Added heatmap-specific assertions.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_heatmap_endpoint_exists():

    response = client.get(
        "/stores/store_1/heatmap"
    )

    assert response.status_code == 200


def test_heatmap_response_structure():

    response = client.get(
        "/stores/store_1/heatmap"
    )

    data = response.json()

    assert "store_id" in data
    assert "heatmap" in data