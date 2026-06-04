import cv2
from ultralytics import YOLO
import supervision as sv

# Load model
model = YOLO("yolov8n.pt")

# Open video
video = cv2.VideoCapture("sample.mp4")

# Tracker
tracker = sv.ByteTrack()

# Store previous positions
previous_positions = {}

# Prevent duplicate events
entered = set()
exited = set()

frame_count = 0

while True:

    success, frame = video.read()

    if not success:
        break

    frame_count += 1

    height = frame.shape[0]
    width = frame.shape[1]

    # Red line at middle
    line_y = height // 2

    if frame_count == 1:
        print(f"Frame Size: {width} x {height}")
        print(f"Line Position: {line_y}")

    # Detect people
    results = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(
        results
    )

    # Keep only persons
    detections = detections[
        detections.class_id == 0
    ]

    # Track
    detections = tracker.update_with_detections(
        detections
    )

    # Draw line
    cv2.line(
        frame,
        (0, line_y),
        (width, line_y),
        (0, 0, 255),
        2
    )

    for i in range(len(detections)):

        if detections.tracker_id[i] is None:
            continue

        tracker_id = int(
            detections.tracker_id[i]
        )

        x1, y1, x2, y2 = map(
            int,
            detections.xyxy[i]
        )

        center_y = (y1 + y2) // 2

        # Draw center point
        cv2.circle(
            frame,
            ((x1 + x2) // 2, center_y),
            5,
            (255, 0, 0),
            -1
        )

        if tracker_id in previous_positions:

            prev_y = previous_positions[
                tracker_id
            ]

            # Debug every 30 frames
            if frame_count % 30 == 0:
                print(
                    f"VIS_{tracker_id} | prev={prev_y} current={center_y}"
                )

            # ENTRY
            if (
                prev_y < line_y
                and center_y >= line_y
                and tracker_id not in entered
            ):

                entered.add(tracker_id)

                print(
                    f"ENTRY -> VIS_{tracker_id}"
                )

            # EXIT
            elif (
                prev_y > line_y
                and center_y <= line_y
                and tracker_id not in exited
            ):

                exited.add(tracker_id)

                print(
                    f"EXIT -> VIS_{tracker_id}"
                )

        previous_positions[
            tracker_id
        ] = center_y

        # Bounding box
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

    cv2.imshow(
        "Entry Exit Detection",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:
        break

video.release()
cv2.destroyAllWindows()

print("\nFinished")
print(f"Entries detected: {len(entered)}")
print(f"Exits detected: {len(exited)}")