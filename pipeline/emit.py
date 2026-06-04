import uuid
from datetime import datetime, timezone
import json
import random


EVENT_TYPES = [
    "ENTRY",
    "EXIT",
    "ZONE_ENTER",
    "ZONE_EXIT",
    "ZONE_DWELL",
    "BILLING_QUEUE_JOIN",
    "BILLING_QUEUE_ABANDON",
    "REENTRY",
    "PURCHASE"
]


def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "store_id": "STORE_BLR_001",
        "camera_id": "CAM_ENTRY_01",
        "visitor_id": f"VIS_{random.randint(1, 1000)}",
        "event_type": random.choice(EVENT_TYPES),

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "zone_id": random.choice([
            None,
            "SKINCARE",
            "COSMETICS",
            "BILLING"
        ]),

        "dwell_ms": random.randint(
            0,
            60000
        ),

        "is_staff": False,

        "confidence": round(
            random.uniform(0.5, 1.0),
            2
        ),

        "metadata": {
            "queue_depth": random.randint(0, 10),
            "sku_zone": random.choice([
                None,
                "MOISTURISER",
                "SERUM",
                "MAKEUP"
            ]),
            "session_seq": random.randint(1, 20)
        }
    }


if __name__ == "__main__":
    event = generate_event()

    print(
        json.dumps(
            event,
            indent=2
        )
    )