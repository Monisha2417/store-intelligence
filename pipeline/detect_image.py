from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("test.jpg")

for result in results:
    for box in result.boxes:

        class_id = int(box.cls[0])

        if class_id == 0:  # person class

            print("Person detected")

            x1, y1, x2, y2 = box.xyxy[0]

            print(
                f"Box: {int(x1)}, {int(y1)}, {int(x2)}, {int(y2)}"
            )