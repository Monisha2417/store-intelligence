import cv2
import json
import uuid
from datetime import datetime, timezone

from ultralytics import YOLO
import supervision as sv

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("sample.mp4")

tracker = sv.ByteTrack()

previous_positions = {}
entered = set()
exited = set()

OUTPUT_FILE = "events.jsonl"


def create_event(store_id, camera_id, visitor_id, event_type, seq=1):

    return {
        "event_id": str(uuid.uuid4()),
        "store_id": store_id,
        "camera_id": camera_id,
        "visitor_id": f"VIS_{visitor_id}",
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "zone_id": None,
        "dwell_ms": 0,
        "is_staff": False,
        "confidence": 0.90,
        "metadata": {
            "queue_depth": None,
            "sku_zone": None,
            "session_seq": seq
        }
    }


with open(OUTPUT_FILE, "w") as f:

    frame_count = 0

    while True:

        success, frame = video.read()

        if not success:
            break

        frame_count += 1

        height = frame.shape[0]
        width = frame.shape[1]

        line_y = height // 2

        results = model(frame, verbose=False)[0]

        detections = sv.Detections.from_ultralytics(results)

        detections = detections[detections.class_id == 0]

        detections = tracker.update_with_detections(detections)

        for i in range(len(detections)):

            if detections.tracker_id[i] is None:
                continue

            tracker_id = int(detections.tracker_id[i])

            x1, y1, x2, y2 = map(
                int,
                detections.xyxy[i]
            )

            center_y = (y1 + y2) // 2

            if tracker_id in previous_positions:

                prev_y = previous_positions[tracker_id]

                # ENTRY
                if (
                    prev_y < line_y
                    and center_y >= line_y
                    and tracker_id not in entered
                ):

                    entered.add(tracker_id)

                    event = create_event(
                        "STORE_BLR_001",
                        "CAM_ENTRY_01",
                        tracker_id,
                        "ENTRY",
                        len(entered)
                    )

                    f.write(json.dumps(event) + "\n")

                # EXIT
                elif (
                    prev_y > line_y
                    and center_y <= line_y
                    and tracker_id not in exited
                ):

                    exited.add(tracker_id)

                    event = create_event(
                        "STORE_BLR_001",
                        "CAM_ENTRY_01",
                        tracker_id,
                        "EXIT",
                        len(exited)
                    )

                    f.write(json.dumps(event) + "\n")

            previous_positions[tracker_id] = center_y

video.release()

print("Done.")
print(f"Events saved to {OUTPUT_FILE}")