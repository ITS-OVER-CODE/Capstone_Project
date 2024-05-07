import cv2
import mediapipe as mp
import numpy as np
import time
import math
import pygame
import globals
from datetime import datetime, timedelta

pygame.init()
class EyeDetectorMesh:
    def __init__(self, counter, camera_manager):
        self.counter = counter
        self.camera_manager = camera_manager
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        self.mp_drawing = mp.solutions.drawing_utils
        self.left_eye = [160, 158, 144, 153, 33, 133]
        self.right_eye = [385,387,380,373,263,362]
        self.last_yawn_time = 0
        self.eyes_closed_start = None
        self.timer = [True, True, True, True, True]

    def draw_landmarks(self, frame, landmarks):
        for landmark in landmarks:
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 1, (0, 255, 0), 1)

    def distance(self, landmark1, landmark2):
        x1, y1, z1 = landmark1.x, landmark1.y, landmark1.z
        x2, y2, z2 = landmark2.x, landmark2.y, landmark2.z
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def calculate_EARL(self, landmarks):
        EARL = [landmarks[i] for i in self.left_eye]
        return ((self.distance(EARL[0], EARL[2]) + self.distance(EARL[1], EARL[3])) / ( self.distance(EARL[4], EARL[5])))
    
    def calculate_EARR(self, landmarks):
        EARL = [landmarks[i] for i in self.right_eye]
        return ((self.distance(EARL[0], EARL[2]) + self.distance(EARL[1], EARL[3])) / (self.distance(EARL[4], EARL[5])))

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.face_mesh.process(frame_rgb)
    
    def run(self):
        window_name = "Eye"  # Unique name for this window
        cv2.namedWindow(window_name)
        while True:
            if globals.eyeON and globals.systemON:
                frame = self.camera_manager.get_frame()
                if frame is None:
                    continue

                results = self.process_frame(frame)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        self.draw_landmarks(frame, face_landmarks.landmark)

                        EAR_left = self.calculate_EARL(face_landmarks.landmark)
                        EAR_right = self.calculate_EARR(face_landmarks.landmark)
                        EAR = (EAR_left + EAR_right) / 2
                        cv2.putText(frame, f'Average EAR: {EAR:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        if EAR < 0.6:
                            if self.eyes_closed_start is None:
                                self.eyes_closed_start = datetime.now()
                            else:
                                cv2.putText(frame, "Time: " +str( datetime.now() - self.eyes_closed_start )+ " S", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                if datetime.now() - self.eyes_closed_start >= timedelta(seconds=1) and self.timer[0] == True:
                                    self.counter.increment()
                                    print(self.counter.get_value())
                                    self.timer[0] = False
                                if datetime.now() - self.eyes_closed_start >= timedelta(seconds=2) and self.timer[1] == True:
                                    self.counter.incrementByValue(2)
                                    print(self.counter.get_value())
                                    self.timer[1] = False
                                if datetime.now() - self.eyes_closed_start >= timedelta(seconds=3) and self.timer[2] == True:
                                    self.counter.incrementByValue(3)
                                    print(self.counter.get_value())
                                    self.timer[2] = False
                                if datetime.now() - self.eyes_closed_start >= timedelta(seconds=4) and self.timer[3] == True:
                                    self.counter.incrementByValue(4)
                                    print(self.counter.get_value())
                                    self.timer[3] = False
                                if datetime.now() - self.eyes_closed_start >= timedelta(seconds=5) and self.timer[4] == True:
                                    self.counter.incrementByValue(5)
                                    print(self.counter.get_value())
                                    self.timer[4] = False
                        else:
                            self.eyes_closed_start = None  # Reset the timer
                            cv2.putText(frame, "Normal", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            self.timer = [True, True, True, True, True]

                        self.counter.check_value()

                cv2.imshow(window_name, frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
            else:
            # Display a static message or blank frame when the conditions are not met
                blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(blank_frame, "System Paused", (180, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow(window_name, blank_frame)

