import cv2
from ultralytics import YOLO
import supervision as sv

model = YOLO("yolov8n.pt")
video = cv2.VideoCapture("sample.mp4")

tracker = sv.ByteTrack()

# -----------------------------
# IDENTITY + SESSION STATE
# -----------------------------
visitor_map = {}
next_visitor_id = 1

visitor_state = {}
# visitor_state[visitor_id] = {"active": bool}


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


while True:

    success, frame = video.read()
    if not success:
        break

    results = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(results)
    detections = detections[detections.class_id == 0]

    detections = tracker.update_with_detections(detections)

    for i in range(len(detections)):

        tracker_id = detections.tracker_id[i]
        if tracker_id is None:
            continue

        tracker_id = int(tracker_id)
        visitor_id = get_visitor_id(tracker_id)

        print(f"TRACKED: {visitor_id}")

video.release()
print("Tracking finished")