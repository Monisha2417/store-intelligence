from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import EventDB

router = APIRouter()


# -------------------------------------------------
# METRICS ENGINE
# -------------------------------------------------
def compute_metrics(db: Session, store_id: str):

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    if not events:
        return {
            "store_id": store_id,
            "unique_visitors": 0,
            "entry": 0,
            "exit": 0,
            "purchase": 0,
            "conversion_rate": 0,
            "avg_dwell_ms": 0
        }

    visitors = set()
    purchasers = set()

    entry_count = 0
    exit_count = 0

    dwell_total = 0
    dwell_count = 0

    for e in events:

        if e.is_staff:
            continue

        visitors.add(e.visitor_id)

        # -------------------------
        # EVENT COUNTS
        # -------------------------
        if e.event_type == "ENTRY":
            entry_count += 1

        elif e.event_type == "EXIT":
            exit_count += 1

        elif e.event_type == "PURCHASE":
            purchasers.add(e.visitor_id)

        # -------------------------
        # DWELL
        # -------------------------
        if e.dwell_ms and e.dwell_ms > 0:
            dwell_total += e.dwell_ms
            dwell_count += 1

    avg_dwell = (
        dwell_total / dwell_count
        if dwell_count
        else 0
    )

    purchase_count = len(purchasers)

    conversion_rate = (
        (purchase_count / len(visitors)) * 100
        if visitors
        else 0
    )

    return {
        "store_id": store_id,
        "unique_visitors": len(visitors),
        "entry": entry_count,
        "exit": exit_count,
        "purchase": purchase_count,
        "conversion_rate": round(
            conversion_rate,
            2
        ),
        "avg_dwell_ms": round(
            avg_dwell,
            2
        )
    }


# -------------------------------------------------
# API ENDPOINT
# -------------------------------------------------
@router.get("/stores/{store_id}/metrics")
def get_metrics(store_id: str):

    db = SessionLocal()

    try:
        return compute_metrics(
            db,
            store_id
        )

    finally:
        db.close()