from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import EventDB, EventBatch

router = APIRouter()


# -------------------------------------------------
# SINGLE EVENT INGEST
# -------------------------------------------------
def ingest_single_event(event):

    db = SessionLocal()

    try:

        exists = db.query(EventDB).filter(
            EventDB.event_id == event["event_id"]
        ).first()

        if exists:
            return

        db_event = EventDB(
            event_id=event["event_id"],
            store_id=event["store_id"],
            camera_id=event["camera_id"],
            visitor_id=event["visitor_id"],
            event_type=event["event_type"],
            timestamp=event["timestamp"],
            zone_id=event.get("zone_id"),
            dwell_ms=event.get("dwell_ms", 0),
            is_staff=event.get("is_staff", False),
            confidence=event.get("confidence", 0.0)
        )

        db.add(db_event)
        db.commit()

    finally:
        db.close()


# -------------------------------------------------
# BATCH INGEST
# -------------------------------------------------
@router.post("/events/ingest")
def ingest_events(batch: EventBatch):

    db: Session = SessionLocal()

    try:

        inserted = 0
        duplicates = 0

        for event in batch.events:

            exists = db.query(EventDB).filter(
                EventDB.event_id == event.event_id
            ).first()

            if exists:
                duplicates += 1
                continue

            db_event = EventDB(
                event_id=event.event_id,
                store_id=event.store_id,
                camera_id=event.camera_id,
                visitor_id=event.visitor_id,
                event_type=event.event_type,
                timestamp=event.timestamp,
                zone_id=event.zone_id,
                dwell_ms=event.dwell_ms,
                is_staff=event.is_staff,
                confidence=event.confidence
            )

            db.add(db_event)
            inserted += 1

        db.commit()

        return {
            "status": "success",
            "inserted": inserted,
            "duplicates": duplicates,
            "total_received": len(batch.events)
        }

    finally:
        db.close()