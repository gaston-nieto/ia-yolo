from ultralytics import YOLO

model = YOLO("yolov8s.pt")
model.train(
    data="cows.yaml",
    epochs=100,
    imgsz=640,
    batch=32,
    name="cows_train"
)