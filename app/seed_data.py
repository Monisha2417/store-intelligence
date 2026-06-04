import random
import uuid
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import EventDB


db = SessionLocal()

STORE_ID = "STORE_BLR_002"

zones = [
    "ENTRANCE",
    "SNACKS",
    "DAIRY",
    "BEVERAGES",
    "CHECKOUT"
]

for visitor_num in range(1, 301):

    visitor_id = f"VISITOR_{visitor_num}"

    base_time = datetime.now() - timedelta(
        minutes=random.randint(1, 1000)
    )

    entry_event = EventDB(
        event_id=str(uuid.uuid4()),
        store_id=STORE_ID,
        visitor_id=visitor_id,
        camera_id="CAM_1",
        event_type="ENTRY",
        zone_id="ENTRANCE",
        timestamp=base_time,
        is_staff=False
    )

    db.add(entry_event)

    visited_zones = random.sample(
        zones[1:-1],
        random.randint(1, 3)
    )

    for zone in visited_zones:

        db.add(
            EventDB(
                event_id=str(uuid.uuid4()),
                store_id=STORE_ID,
                visitor_id=visitor_id,
                camera_id="CAM_1",
                event_type="ZONE_DWELL",
                zone_id=zone,
                timestamp=base_time,
                is_staff=False
            )
        )

    if random.random() < 0.18:

        db.add(
            EventDB(
                event_id=str(uuid.uuid4()),
                store_id=STORE_ID,
                visitor_id=visitor_id,
                camera_id="CAM_1",
                event_type="PURCHASE",
                zone_id="CHECKOUT",
                timestamp=base_time,
                is_staff=False
            )
        )

db.commit()
db.close()

print("Seeded 300 visitors")