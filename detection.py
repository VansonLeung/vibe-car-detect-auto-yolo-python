# Detection module using YOLOv11 (Ultralytics)
from ultralytics import YOLO
import cv2

class Detector:
    def __init__(self, model_path='YOLO11L.pt', conf_threshold=0.5, car_classes=None):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        # List of class indices for cars (update as per YOLO11L.pt class mapping)
        self.car_classes = car_classes if car_classes is not None else [1, 2, 3, 5, 6, 7]  # Example: car, truck, bus, van

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        for r in results:
            for box in r.boxes:
                if box.conf >= self.conf_threshold and int(box.cls) in self.car_classes:
                    detections.append({
                        'bbox': box.xyxy[0].tolist(),
                        'confidence': float(box.conf),
                        'class': int(box.cls)
                    })
        return detections

    @staticmethod
    def draw_overlays(frame, detections, class_names=None):
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            label = str(det.get('class', 'car'))
            if class_names:
                label = class_names.get(det['class'], label)
            conf = det.get('confidence', 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        return frame
