import cv2
import time
import uuid
from datetime import datetime, timezone

from ultralytics import YOLO
import supervision as sv

from pipeline.event_bus import event_queue

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("sample.mp4")
tracker = sv.ByteTrack()

visitor_map = {}
next_visitor_id = 1

visitor_state = {}
previous_positions = {}

entered = set()
exited = set()


def get_visitor_id(tracker_id):
    global next_visitor_id

    if tracker_id not in visitor_map:
        visitor_map[tracker_id] = f"VIS_{next_visitor_id}"
        next_visitor_id += 1

    return visitor_map[tracker_id]


def is_reentry(visitor_id):
    return visitor_state.get(visitor_id, {}).get("active") is False


def set_active(visitor_id, active: bool):
    visitor_state[visitor_id] = {"active": active}


def create_event(visitor_id, event_type):

    return {
        "event_id": str(uuid.uuid4()),
        "store_id": "STORE_BLR_001",
        "camera_id": "CAM_ENTRY_01",
        "visitor_id": visitor_id,
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "zone_id": None,
        "dwell_ms": 0,
        "is_staff": False,
        "confidence": 0.9,
        "metadata": {"session_seq": 1}
    }


while True:

    success, frame = video.read()
    if not success:
        break

    results = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(results)
    detections = detections[detections.class_id == 0]

    detections = tracker.update_with_detections(detections)

    height = frame.shape[0]
    line_y = height // 2

    for i in range(len(detections)):

        tracker_id = detections.tracker_id[i]
        if tracker_id is None:
            continue

        tracker_id = int(tracker_id)
        visitor_id = get_visitor_id(tracker_id)

        x1, y1, x2, y2 = map(int, detections.xyxy[i])
        center_y = (y1 + y2) // 2

        if tracker_id in previous_positions:

            prev_y = previous_positions[tracker_id]

            # ENTRY / REENTRY
            if (
                prev_y < line_y
                and center_y >= line_y
                and tracker_id not in entered
            ):

                entered.add(tracker_id)

                event_type = "REENTRY" if is_reentry(visitor_id) else "ENTRY"
                set_active(visitor_id, True)

                event_queue.put(create_event(visitor_id, event_type))

            # EXIT
            elif (
                prev_y > line_y
                and center_y <= line_y
                and tracker_id not in exited
            ):

                exited.add(tracker_id)
                set_active(visitor_id, False)

                event_queue.put(create_event(visitor_id, "EXIT"))

        previous_positions[tracker_id] = center_y

    time.sleep(0.03)  # simulates real-time FPS control

video.release()
print("STREAMING FINISHED")