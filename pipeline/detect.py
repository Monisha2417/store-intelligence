import cv2
import time
import uuid
from ultralytics import YOLO
import supervision as sv

from pipeline.session_manager import SessionManager
from pipeline.store_layout import StoreLayout
from pipeline.event_factory import EventFactory
from pipeline.event_bus import event_queue


# -----------------------------
# INIT
# -----------------------------
VIDEO_PATH = "sample.mp4"

STORE_ID = "STORE_BLR_001"
CAMERA_ID = "CAM_ENTRY_01"

model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()

session_manager = SessionManager()
store_layout = StoreLayout()

# prevents spam events
last_zone = {}
emitted_entry = set()


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("❌ Failed to open video")
        return

    frame_count = 0

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        height, width = frame.shape[:2]

        results = model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)

        # only PERSON class
        detections = detections[detections.class_id == 0]

        detections = tracker.update_with_detections(detections)

        # active tracks for exit detection
        active_tracks = set()

        for i in range(len(detections)):

            track_id = int(detections.tracker_id[i])
            active_tracks.add(track_id)

            x1, y1, x2, y2 = map(int, detections.xyxy[i])

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # -----------------------------
            # SCALE TO 0–1000 SYSTEM
            # -----------------------------
            sx = int((cx / width) * 1000)
            sy = int((cy / height) * 1000)

            # -----------------------------
            # SESSION
            # -----------------------------
            session = session_manager.get_or_create_session(track_id)

            visitor_id = session["visitor_id"]

            # -----------------------------
            # ZONE DETECTION
            # -----------------------------
            zone = store_layout.get_zone(sx, sy)

            # prevent zone spam
            if last_zone.get(visitor_id) != zone:

                last_zone[visitor_id] = zone

                event = EventFactory.create_event(
                    store_id=STORE_ID,
                    camera_id=CAMERA_ID,
                    visitor_id=visitor_id,
                    event_type="ZONE_ENTER",
                    session_id=visitor_id,
                    zone_id=zone
                )

                event_queue.put(event)

                print(f"[ZONE] {visitor_id} -> {zone}")

            # -----------------------------
            # ENTRY (ONLY ONCE)
            # -----------------------------
            if visitor_id not in emitted_entry:

                emitted_entry.add(visitor_id)

                event = EventFactory.create_event(
                    STORE_ID,
                    CAMERA_ID,
                    visitor_id,
                    "ENTRY",
                    visitor_id,
                    session_id=visitor_id
                )

                event_queue.put(event)

                print(f"[EVENT] ENTRY -> {visitor_id}")

        # -----------------------------
        # EXIT DETECTION
        # -----------------------------
        session_manager.mark_missing(active_tracks)

        # emit exits
        for track_id, session in list(session_manager.sessions.items()):

            if session.get("exit_emitted"):

                event = EventFactory.create_event(
                    STORE_ID,
                    CAMERA_ID,
                    session["visitor_id"],
                    "EXIT",
                    session["visitor_id"],
                    session_id=session["visitor_id"],
                    dwell_time=session.get("dwell_time")
                )

                event_queue.put(event)

                print(f"[EVENT] EXIT -> {session['visitor_id']}")

        # -----------------------------
        # LOGGING
        # -----------------------------
        if frame_count % 100 == 0:
            print(f"Processed {frame_count} frames")

        time.sleep(0.03)

    cap.release()

    print(f"✅ Finished. Frames processed: {frame_count}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_pipeline()