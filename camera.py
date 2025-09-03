import cv2

class Camera:
    def __init__(self, device_index=0, resolution=(1280, 720)):
        self.device_index = device_index
        self.resolution = resolution
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.device_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        if not self.cap.isOpened():
            raise IOError(f"Cannot open camera {self.device_index}")

    def read(self):
        if self.cap is None:
            self.open()
        ret, frame = self.cap.read()
        if not ret:
            raise IOError("Failed to read frame from camera")
        return frame

    def release(self):
        if self.cap:
            self.cap.release()
