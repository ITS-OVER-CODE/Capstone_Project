import cv2
import mediapipe as mp
import numpy as np
import time
import math
import pygame
import globals

pygame.init()



class YawnDetector:
    def __init__(self, counter, camera_manager):
        self.counter = counter
        self.camera_manager = camera_manager
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mouth_landmarks = [82, 87, 312, 317, 78, 308]
        self.last_yawn_time = 0

    def draw_landmarks(self, frame, landmarks):
        for landmark in landmarks:
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 1, (0, 255, 0), 1)

    def distance(self, landmark1, landmark2):
        x1, y1, z1 = landmark1.x, landmark1.y, landmark1.z
        x2, y2, z2 = landmark2.x, landmark2.y, landmark2.z
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def calculate_MAR(self, landmarks):
        ML = [landmarks[i] for i in self.mouth_landmarks]
        return ((self.distance(ML[0], ML[1]) + self.distance(ML[2], ML[3])) / (2 * self.distance(ML[4], ML[5])))

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.face_mesh.process(frame_rgb)


    def run(self):
        window_name = "Yawn"  # Unique name for this window
        cv2.namedWindow(window_name)
        while True:
            if globals.yawnON and globals.systemON:
                frame = self.camera_manager.get_frame()
                if frame is None:
                    continue

                results = self.process_frame(frame)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        self.draw_landmarks(frame, face_landmarks.landmark)

                        MAR = self.calculate_MAR(face_landmarks.landmark)
                        cv2.putText(frame, f'Average MAR: {MAR:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        current_time = time.time()
                        if MAR > 0.7 and current_time - self.last_yawn_time > 3:
                            self.counter.increment()
                            self.last_yawn_time = current_time
                            cv2.putText(frame, "Yawn Detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            print(f"Yawn Count: {self.counter.get_value()}")
                        else:
                            cv2.putText(frame, "Normal", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        self.counter.check_value()

                cv2.imshow(window_name, frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
            else:
            # Display a static message or blank frame when the conditions are not met
                blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(blank_frame, "System Paused", (180, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow(window_name, blank_frame)