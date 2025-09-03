# test_detection.py - Simple test for detection module
from detection import Detector
from camera import Camera
import cv2

def test_detection():
    try:
        camera = Camera()
        camera.open()
        detector = Detector(model_path='yolo11l.pt')
        
        frame = camera.read()
        detections = detector.detect(frame)
        
        print(f"Detected {len(detections)} objects")
        for i, det in enumerate(detections):
            print(f"Detection {i}: Class {det['class']}, Confidence {det['confidence']:.2f}")
        
        # Draw overlays and display
        class_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
        frame_with_overlays = detector.draw_overlays(frame, detections, class_names)
        
        cv2.imshow('Detection Test', frame_with_overlays)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        camera.release()
        
    except Exception as e:
        print(f"Error in test: {e}")

if __name__ == "__main__":
    test_detection()
