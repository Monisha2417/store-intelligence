import cv2
from ultralytics import YOLO
import supervision as sv

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open video
video = cv2.VideoCapture("sample.mp4")

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

# Output video
writer = cv2.VideoWriter(
    "output_tracking.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

# ByteTrack tracker
tracker = sv.ByteTrack()

frame_count = 0

while True:

    success, frame = video.read()

    if not success:
        break

    frame_count += 1

    # Process every 2nd frame
    if frame_count % 2 == 0:

        results = model(frame)[0]

        detections = sv.Detections.from_ultralytics(
            results
        )

        # Keep only persons
        detections = detections[
            detections.class_id == 0
        ]

        # Update tracker
        detections = tracker.update_with_detections(
            detections
        )

        # Draw boxes + IDs
        for i in range(len(detections)):

            x1, y1, x2, y2 = map(
                int,
                detections.xyxy[i]
            )

            tracker_id = detections.tracker_id[i]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"VIS_{tracker_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    writer.write(frame)

    if frame_count % 100 == 0:
        print(
            f"Processed {frame_count} frames"
        )

video.release()
writer.release()

print(f"Finished. Total frames: {frame_count}")
print("Saved output_tracking.mp4")