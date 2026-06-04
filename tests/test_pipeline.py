import uuid

def sample_event(event_type="ENTRY"):

    return {
    "event_id": str(uuid.uuid4()),
    "store_id": "store_1",
    "camera_id": "cam_1",
    "visitor_id": "visitor_1",
    "event_type": event_type,
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

def test_event_has_required_fields():

    event = sample_event()

    required = [
    "event_id",
    "store_id",
    "camera_id",
    "visitor_id",
    "event_type",
    "timestamp",
    "confidence"
    ]

    for field in required:
        assert field in event

def test_reentry_event_supported():

    event = sample_event(
        "REENTRY"
    )

    assert event["event_type"] == "REENTRY"

def test_staff_flag_exists():

    event = sample_event()

    assert "is_staff" in event

def test_metadata_exists():

    event = sample_event()

    assert "metadata" in event