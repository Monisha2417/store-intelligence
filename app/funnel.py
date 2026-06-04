from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EventDB

router = APIRouter()


# -------------------------------------------------
# FUNNEL COMPUTATION
# -------------------------------------------------
def compute_funnel(db: Session, store_id: str):

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    sessions = {}

    for e in events:

        if e.is_staff:
            continue

        vid = e.visitor_id

        if vid not in sessions:
            sessions[vid] = {
                "ENTRY": False,
                "ZONE": False,
                "BILLING": False,
                "PURCHASE": False
            }

        if e.event_type in ["ENTRY", "REENTRY"]:
            sessions[vid]["ENTRY"] = True

        elif e.event_type in ["ZONE_ENTER", "ZONE_DWELL"]:
            sessions[vid]["ZONE"] = True

        elif e.event_type in [
            "BILLING",
            "BILLING_QUEUE_JOIN"
        ]:
            sessions[vid]["BILLING"] = True

        elif e.event_type == "PURCHASE":
            sessions[vid]["PURCHASE"] = True

    # -------------------------------------------------
    # AGGREGATION
    # -------------------------------------------------
    entry = sum(
        1 for s in sessions.values()
        if s["ENTRY"]
    )

    zone = sum(
        1 for s in sessions.values()
        if s["ZONE"]
    )

    billing = sum(
        1 for s in sessions.values()
        if s["BILLING"]
    )

    purchase = sum(
        1 for s in sessions.values()
        if s["PURCHASE"]
    )

    def safe_div(a, b):
        return round((a / b) * 100, 2) if b else 0

    return {
        "store_id": store_id,

        "entry": entry,
        "zone_visits": zone,
        "billing": billing,
        "purchase": purchase,

        "dropoffs": {
            "entry_to_zone":
                safe_div(entry - zone, entry),

            "zone_to_billing":
                safe_div(zone - billing, zone),

            "billing_to_purchase":
                safe_div(billing - purchase, billing)
        },

        "conversion_rate":
            safe_div(purchase, entry)
    }


# -------------------------------------------------
# API ENDPOINT
# -------------------------------------------------
@router.get("/stores/{store_id}/funnel")
def get_funnel(
    store_id: str,
    db: Session = Depends(get_db)
):
    return compute_funnel(db, store_id)