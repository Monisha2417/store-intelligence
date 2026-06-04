import random
import uuid
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import EventDB

from pipeline.store_layout import StoreLayout

STORE_ID = "STORE_BLR_002"


def seed_database():
    db = SessionLocal()

    # Clear old data
    db.query(EventDB).delete()
    db.commit()

    # create layout INSIDE function (important fix)
    layout = StoreLayout()
    zones = list(layout.zones.keys())

    for visitor_num in range(1, 301):

        visitor_id = f"VISITOR_{visitor_num}"

        base_time = datetime.now() - timedelta(
            minutes=random.randint(1, 1000)
        )

        # ENTRY
        db.add(EventDB(
            event_id=str(uuid.uuid4()),
            store_id=STORE_ID,
            visitor_id=visitor_id,
            camera_id="CAM_1",
            event_type="ENTRY",
            zone_id="FOH",
            timestamp=base_time,
            is_staff=False
        ))

        # ZONE VISITS (SAFE FIX HERE)
        safe_zone_pool = [z for z in zones if z not in ["FOH"]]

        k = min(random.randint(1, 3), len(safe_zone_pool))

        visited_zones = random.sample(safe_zone_pool, k)

        for zone in visited_zones:
            db.add(EventDB(
                event_id=str(uuid.uuid4()),
                store_id=STORE_ID,
                visitor_id=visitor_id,
                camera_id="CAM_1",
                event_type="ZONE_DWELL",
                zone_id=zone,
                timestamp=base_time,
                dwell_ms=random.randint(30000, 180000),
                is_staff=False
            ))

        # 20% reach billing
        reached_billing = random.random() < 0.20

        if reached_billing:

            db.add(EventDB(
                event_id=str(uuid.uuid4()),
                store_id=STORE_ID,
                visitor_id=visitor_id,
                camera_id="CAM_1",
                event_type="BILLING_QUEUE_JOIN",
                zone_id="BILLING",
                timestamp=base_time + timedelta(minutes=5),
                is_staff=False
            ))

            # 75% purchase
            if random.random() < 0.75:
                db.add(EventDB(
                    event_id=str(uuid.uuid4()),
                    store_id=STORE_ID,
                    visitor_id=visitor_id,
                    camera_id="CAM_1",
                    event_type="PURCHASE",
                    zone_id="CHECKOUT",
                    timestamp=base_time + timedelta(minutes=7),
                    is_staff=False
                ))
            else:
                db.add(EventDB(
                    event_id=str(uuid.uuid4()),
                    store_id=STORE_ID,
                    visitor_id=visitor_id,
                    camera_id="CAM_1",
                    event_type="BILLING_QUEUE_ABANDON",
                    zone_id="CHECKOUT",
                    timestamp=base_time + timedelta(minutes=6),
                    is_staff=False
                ))

        # EXIT
        db.add(EventDB(
            event_id=str(uuid.uuid4()),
            store_id=STORE_ID,
            visitor_id=visitor_id,
            camera_id="CAM_1",
            event_type="EXIT",
            zone_id="ENTRANCE",
            timestamp=base_time + timedelta(minutes=10),
            is_staff=False
        ))

    db.commit()
    db.close()

    print("Seeded 300 visitors successfully")


if __name__ == "__main__":
    seed_database()