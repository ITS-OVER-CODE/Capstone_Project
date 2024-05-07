import cv2
from threading import Thread, Lock

class CameraManager:
    def __init__(self, source=1):
        self.cap = cv2.VideoCapture(source)
        self.lock = Lock()
        self.frame = None
        self.running = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()
