import uuid
import time


class EventFactory:

    @staticmethod
    def create_event(
        store_id,
        camera_id,
        visitor_id,
        event_type,
        session_id,
        is_reentry=False,
        zone_id=None,
        dwell_time=None,
        confidence=0.9
    ):

        return {
            "event_id": str(uuid.uuid4()),

            "store_id": store_id,
            "camera_id": camera_id,

            "visitor_id": visitor_id,
            "event_type": event_type,

            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),

            "zone_id": zone_id,

            "confidence": confidence,

            "metadata": {
                "session_id": session_id,
                "is_reentry": is_reentry,
                "dwell_time": dwell_time
            }
        }