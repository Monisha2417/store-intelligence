# PROMPT:
# Generate pytest tests for funnel analytics endpoint.
# Validate endpoint availability and response schema.
#
# CHANGES MADE:
# Added project-specific fields.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_funnel_endpoint_exists():

    response = client.get(
        "/stores/store_1/funnel"
    )

    assert response.status_code == 200


def test_funnel_response_structure():

    response = client.get(
        "/stores/store_1/funnel"
    )

    data = response.json()

    assert "store_id" in data
    assert "conversion_rate" in data