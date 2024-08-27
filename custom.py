from ultralytics import YOLO
model  = YOLO("yolov10s.pt")

data_config = "F:\Github\Project\yolov8-multiple-vehicle-counting\dataset.yaml"

model.train(data = data_config, epochs = 2, batch = 20, imgsz = 640)

model.save("yolov10_custom_cocc.pt")