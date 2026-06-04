from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EventDB

router = APIRouter()


# -------------------------------------------------
# FUNNEL COMPUTATION
# -------------------------------------------------
def compute_funnel(db: Session, store_id: str):

    events = (
        db.query(EventDB)
        .filter(EventDB.store_id == store_id)
        .all()
    )

    sessions = {}

    for event in events:

        if event.is_staff:
            continue

        visitor_id = event.visitor_id

        if visitor_id not in sessions:
            sessions[visitor_id] = {
                "ENTRY": False,
                "ZONE": False,
                "BILLING": False,
                "PURCHASE": False
            }

        # -------------------------
        # ENTRY
        # -------------------------
        if event.event_type in ["ENTRY", "REENTRY"]:
            sessions[visitor_id]["ENTRY"] = True

        # -------------------------
        # ZONE VISIT
        # -------------------------
        elif event.event_type in [
            "ZONE_ENTER",
            "ZONE_DWELL"
        ]:
            sessions[visitor_id]["ZONE"] = True

        # -------------------------
        # BILLING
        # -------------------------
        elif event.event_type in [
            "BILLING",
            "BILLING_QUEUE_JOIN",
            "BILLING_QUEUE_ABANDON"
        ]:
            sessions[visitor_id]["BILLING"] = True

        # -------------------------
        # PURCHASE
        # -------------------------
        elif event.event_type == "PURCHASE":
            sessions[visitor_id]["PURCHASE"] = True

    # -------------------------------------------------
    # AGGREGATION
    # -------------------------------------------------

    entry_count = sum(
        1 for s in sessions.values()
        if s["ENTRY"]
    )

    zone_count = sum(
        1 for s in sessions.values()
        if s["ZONE"]
    )

    billing_count = sum(
        1 for s in sessions.values()
        if s["BILLING"]
    )

    purchase_count = sum(
        1 for s in sessions.values()
        if s["PURCHASE"]
    )

    # -------------------------------------------------
    # SAFE PERCENTAGE HELPER
    # -------------------------------------------------

    def percentage(part, total):
        if total == 0:
            return 0
        return round((part / total) * 100, 2)

    # -------------------------------------------------
    # RESPONSE
    # -------------------------------------------------

    return {
        "store_id": store_id,

        "entry": entry_count,
        "zone_visits": zone_count,
        "billing": billing_count,
        "purchase": purchase_count,

        "dropoffs": {
            "entry_to_zone": round(
                percentage(
                    entry_count - zone_count,
                    entry_count
                ),
                2
            ),

            "zone_to_billing": round(
                percentage(
                    zone_count - billing_count,
                    zone_count
                ),
                2
            ),

            "billing_to_purchase": round(
                percentage(
                    billing_count - purchase_count,
                    billing_count
                ),
                2
            )
        },

        "conversion_rate": percentage(
            purchase_count,
            entry_count
        )
    }


# -------------------------------------------------
# API ENDPOINT
# -------------------------------------------------
@router.get("/stores/{store_id}/funnel")
def get_funnel(
    store_id: str,
    db: Session = Depends(get_db)
):
    return compute_funnel(
        db,
        store_id
    )