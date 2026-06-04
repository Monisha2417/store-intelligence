from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import SessionLocal
from app.models import EventDB

router = APIRouter()


@router.get("/health")
def health():

    db: Session = SessionLocal()

    try:

        stores = {}

        events = db.query(EventDB).all()

        for event in events:

            if event.store_id not in stores:
                stores[event.store_id] = []

            stores[event.store_id].append(event.timestamp)

        store_status = {}

        now = datetime.now(timezone.utc)

        for store_id, timestamps in stores.items():

            latest = max(timestamps)

            try:
                last_event_time = datetime.fromisoformat(
                    latest.replace("Z", "+00:00")
                )

                lag_minutes = (
                    now - last_event_time
                ).total_seconds() / 60

                status = (
                    "STALE_FEED"
                    if lag_minutes > 10
                    else "ACTIVE"
                )

            except Exception:
                lag_minutes = None
                status = "UNKNOWN"

            store_status[store_id] = {
                "last_event_timestamp": latest,
                "feed_status": status,
                "lag_minutes": (
                    round(lag_minutes, 2)
                    if lag_minutes is not None
                    else None
                )
            }

        return {
            "status": "healthy",
            "service": "store-intelligence-api",
            "stores": store_status
        }

    finally:
        db.close()