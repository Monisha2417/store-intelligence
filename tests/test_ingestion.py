from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def create_event():

    return {
    "event_id": str(uuid.uuid4()),
    "store_id": "store_1",
    "camera_id": "cam_1",
    "visitor_id": "visitor_1",
    "event_type": "ENTRY",
    "timestamp": "2026-03-03T14:22:10Z",
    "zone_id": None,
    "dwell_ms": 0,
    "is_staff": False,
    "confidence": 0.9,
    "metadata": {
        "queue_depth": None,
        "sku_zone": None,
        "session_seq": 1
    }
}

def test_ingest_endpoint_exists():

    payload = {
    "events": [create_event()]
    }

    response = client.post(
    "/events/ingest",
        json=payload
    )

    assert response.status_code == 200

def test_ingest_response_structure():

    payload = {
        "events": [create_event()]
    }

    response = client.post(
        "/events/ingest",
        json=payload
    )

    data = response.json()

    assert "status" in data
    assert "inserted" in data
    assert "duplicates" in data
    assert "total_received" in data

    response = client.post(
    "/events/ingest",
    json=payload
    )

    data = response.json()

    assert "status" in data
    assert "inserted" in data
    assert "duplicates" in data
    assert "total_received" in data

def test_duplicate_event_handling():

    event = create_event()

    payload = {
    "events": [event]
    }

    response1 = client.post(
        "/events/ingest",
        json=payload
    )

    response2 = client.post(
        "/events/ingest",
        json=payload
    )

    data = response2.json()

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert data["duplicates"] >= 1