from typing import Optional, Dict, Any, List, Literal

from pydantic import BaseModel, Field

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Float
)

from app.database import Base


# -------------------------------------------------
# PYDANTIC MODELS
# -------------------------------------------------

class Event(BaseModel):

    event_id: str
    store_id: str
    camera_id: str
    visitor_id: str

    event_type: Literal[
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

    timestamp: str

    zone_id: Optional[str] = None

    dwell_ms: int = 0

    is_staff: bool = False

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    metadata: Optional[
        Dict[str, Any]
    ] = None


class EventBatch(BaseModel):
    events: List[Event]


# -------------------------------------------------
# SQLALCHEMY MODEL
# -------------------------------------------------

class EventDB(Base):

    __tablename__ = "events"

    event_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(
        String,
        nullable=False
    )

    camera_id = Column(
        String,
        nullable=False
    )

    visitor_id = Column(
        String,
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    timestamp = Column(
        String,
        nullable=False
    )

    zone_id = Column(
        String,
        nullable=True
    )

    dwell_ms = Column(
        Integer,
        default=0
    )

    is_staff = Column(
        Boolean,
        default=False
    )

    confidence = Column(
        Float,
        default=0.0
    )