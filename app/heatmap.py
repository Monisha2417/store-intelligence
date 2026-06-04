from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import EventDB

router = APIRouter()


@router.get("/stores/{store_id}/heatmap")
def get_heatmap(store_id: str):

    db: Session = SessionLocal()

    try:

        events = db.query(EventDB).filter(
            EventDB.store_id == store_id
        ).all()

        if not events:
            return {
                "store_id": store_id,
                "heatmap": {},
                "data_confidence": "LOW"
            }

        zones = {}

        visitors = set()

        for event in events:

            visitors.add(event.visitor_id)

            if not event.zone_id:
                continue

            if event.zone_id not in zones:
                zones[event.zone_id] = {
                    "visits": 0,
                    "total_dwell": 0
                }

            zones[event.zone_id]["visits"] += 1
            zones[event.zone_id]["total_dwell"] += (
                event.dwell_ms or 0
            )

        if not zones:
            return {
                "store_id": store_id,
                "heatmap": {},
                "data_confidence": "LOW"
            }

        max_visits = max(
            z["visits"]
            for z in zones.values()
        )

        result = {}

        for zone_name, data in zones.items():

            visits = data["visits"]

            avg_dwell = (
                data["total_dwell"] / visits
                if visits
                else 0
            )

            score = (
                (visits / max_visits) * 100
                if max_visits
                else 0
            )

            result[zone_name] = {
                "visits": visits,
                "avg_dwell_ms": round(avg_dwell, 2),
                "score": round(score, 2)
            }

        confidence = (
            "HIGH"
            if len(visitors) >= 20
            else "LOW"
        )

        return {
            "store_id": store_id,
            "heatmap": result,
            "data_confidence": confidence
        }

    finally:
        db.close()