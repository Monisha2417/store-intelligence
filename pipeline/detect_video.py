import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("sample.mp4")

frame_count = 0

while True:

    success, frame = video.read()

    if not success:
        break

    frame_count += 1

    # Process every 30th frame
    if frame_count % 30 != 0:
        continue

    results = model(frame)

    person_count = 0

    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])

            if class_id == 0:
                person_count += 1

    print(
        f"Frame {frame_count}: {person_count} people detected"
    )

video.release()

print("Finished")