# Main application entry point
from camera import Camera
from detection import Detector
from tracking import Counter
from traffic_logging import Logger
from config import Config

import cv2
import time

if __name__ == "__main__":
    config = Config('config.yaml')
    camera = Camera(
        device_index=config.get('camera', 'device_index', 0),
        resolution=tuple(config.get('camera', 'resolution', [1280, 720]))
    )
    # Use YOLO11L.pt as the checkpoint file for YOLOv11
    detector = Detector(
        model_path='yolo11l.pt',
        conf_threshold=config.get('detection', 'confidence_threshold', 0.5)
    )
    counter = Counter(
        line_position=tuple(config.get('counting', 'line_position', [600, 400])),
        direction=config.get('counting', 'direction', 'vertical')
    )
    logger = Logger(
        output_csv=config.get('logging', 'output_csv', 'traffic_log.csv'),
        enable_encryption=config.get('logging', 'enable_encryption', True)
    )

    camera.open()
    prev_positions = []
    try:
        while True:
            frame = camera.read()
            detections = detector.detect(frame)
            
            # Draw detection overlays on frame
            class_names = {1: 'bicycle', 2: 'car', 3: 'motorcycle', 5: 'bus', 6: 'train', 7: 'truck'}
            frame_with_overlays = detector.draw_overlays(frame, detections, class_names)
            
            count = counter.update(detections, prev_positions)
            logger.log({
                'timestamp': time.time(),
                'count': count,
                'detections': detections
            })
            
            # Display frame with overlays
            cv2.imshow('Traffic Counter', frame_with_overlays)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
