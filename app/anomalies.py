from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import EventDB

router = APIRouter()


@router.get("/stores/{store_id}/anomalies")
def get_anomalies(store_id: str):

    db: Session = SessionLocal()

    try:

        events = db.query(EventDB).filter(
            EventDB.store_id == store_id
        ).all()

        anomalies = []

        visitors = set()
        purchasers = set()

        entry_count = 0
        purchase_count = 0
        queue_events = 0

        # ----------------------------------
        # PROCESS EVENTS
        # ----------------------------------
        for event in events:

            if event.is_staff:
                continue

            visitors.add(event.visitor_id)

            if event.event_type == "ENTRY":
                entry_count += 1

            elif event.event_type == "PURCHASE":
                purchasers.add(event.visitor_id)
                purchase_count += 1

            elif event.event_type == "BILLING_QUEUE_JOIN":
                queue_events += 1

        # ----------------------------------
        # CONVERSION RATE
        # ----------------------------------
        conversion_rate = (
            (len(purchasers) / len(visitors)) * 100
            if len(visitors) > 0
            else 0
        )

        # ----------------------------------
        # CONVERSION DROP
        # ----------------------------------
        if len(visitors) > 0 and conversion_rate < 20:

            anomalies.append({
                "type": "CONVERSION_DROP",
                "severity": (
                    "CRITICAL"
                    if conversion_rate < 10
                    else "WARN"
                ),
                "metric": round(conversion_rate, 2),
                "suggested_action":
                    "Review product placement and billing experience"
            })

        # ----------------------------------
        # NO PURCHASES
        # ----------------------------------
        if entry_count > 0 and purchase_count == 0:

            anomalies.append({
                "type": "NO_PURCHASES",
                "severity": "CRITICAL",
                "suggested_action":
                    "Check POS system, billing process, and inventory availability"
            })

        # ----------------------------------
        # BILLING QUEUE SPIKE
        # ----------------------------------
        if queue_events > 20:

            anomalies.append({
                "type": "BILLING_QUEUE_SPIKE",
                "severity": "WARN",
                "suggested_action":
                    "Open additional billing counters"
            })

        # ----------------------------------
        # DEAD ZONE DETECTION
        # ----------------------------------
        zone_activity = {}

        for event in events:

            if event.is_staff:
                continue

            if not event.zone_id:
                continue

            zone_activity[event.zone_id] = (
                zone_activity.get(
                    event.zone_id,
                    0
                ) + 1
            )

        if zone_activity:

            avg_activity = (
                sum(zone_activity.values())
                / len(zone_activity)
            )

            for zone, count in zone_activity.items():

                if count < (0.3 * avg_activity):

                    anomalies.append({
                        "type": "DEAD_ZONE",
                        "zone": zone,
                        "severity": "INFO",
                        "suggested_action":
                            "Inspect visibility, merchandising, and customer flow"
                    })

        # ----------------------------------
        # RESPONSE
        # ----------------------------------
        return {
            "store_id": store_id,
            "conversion_rate": round(
                conversion_rate,
                2
            ),
            "anomalies": anomalies
        }

    finally:
        db.close()