# PROMPT:
# Generate pytest tests for anomaly detection endpoint.
# Cover endpoint availability and response schema.
#
# CHANGES MADE:
# Adapted to Store Intelligence anomaly response structure.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_anomalies_endpoint_exists():

    response = client.get(
        "/stores/store_1/anomalies"
    )

    assert response.status_code == 200


def test_anomalies_response_structure():

    response = client.get(
        "/stores/store_1/anomalies"
    )

    data = response.json()

    assert "store_id" in data
    assert "conversion_rate" in data
    assert "anomalies" in data


def test_anomalies_is_list():

    response = client.get(
        "/stores/store_1/anomalies"
    )

    data = response.json()

    assert isinstance(
        data["anomalies"],
        list
    )