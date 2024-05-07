import cv2
import mediapipe as mp
import numpy as np
import time
import math
import pygame
from datetime import datetime, timedelta
import globals

pygame.init()


class HeadPoseDetector:
    def __init__(self, counter, camera_manager):
        self.counter = counter
        self.camera_manager = camera_manager
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.last_yawn_time = 0  # To implement a cooldown period after each yawn
        self.down = None
        self.tild = None
        self.timer_tild = [True, True, True, True, True]
        self.timer_down = [True, True, True, True, True]
        self.tilt_iterations = 1
        self.down_iterations = 1

    def run(self):
        window_name = "Head"  # Unique name for this window
        cv2.namedWindow(window_name)
        while True:
            if globals.headON and globals.systemON:
                frame = self.camera_manager.get_frame()
                if frame is None:
                    continue

                image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Get the result
                results = self.face_mesh.process(image)

                # To improve performance
                image.flags.writeable = True

                # Convert the color space from RGB to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                img_h, img_w, img_c = image.shape
                face_3d = []
                face_2d = []

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        for idx, lm in enumerate(face_landmarks.landmark):
                            if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                                if idx == 1:
                                    nose_2d = (lm.x * img_w, lm.y * img_h)
                                    nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                                x, y = int(lm.x * img_w), int(lm.y * img_h)

                                # Get the 2D Coordinates
                                face_2d.append([x, y])

                                # Get the 3D Coordinates
                                face_3d.append([x, y, lm.z])

                        face_2d = np.array(face_2d, dtype=np.float64)

                        # Convert it to the NumPy array
                        face_3d = np.array(face_3d, dtype=np.float64)
                        deltaY = face_landmarks.landmark[152].y - face_landmarks.landmark[10].y
                        deltaX = face_landmarks.landmark[152].x - face_landmarks.landmark[10].x
                        angle_y_axis = math.degrees(math.atan2(deltaY, deltaX))


                        focal_length = 1 * img_w

                        cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                                [0, focal_length, img_w / 2],
                                                [0, 0, 1]])

                        dist_matrix = np.zeros((4, 1), dtype=np.float64)

                        # Solve PnP
                        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, np.array([[img_w / 2, 0, img_w / 2], [0, img_h / 2, img_h / 2], [0, 0, 1]], dtype='float32'), dist_matrix)
                        # Get rotational matrix
                        rmat, jac = cv2.Rodrigues(rot_vec)

                        # Get angles
                        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                        # Get the y rotation degree
                        x = angles[0] * 360
                        y = angles[1] * 360
                        z = angles[2] * 360
                        if x < -10:
                            if self.down is None:
                                self.down = datetime.now()
                            else:
                                cv2.putText(image, "Down_Time: " +str( datetime.now() - self.down )+ " S", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                if datetime.now() - self.down >= timedelta(seconds=1) and self.timer_down[0] == True:
                                    self.counter.increment()
                                    print("down " + str(self.counter.get_value()))
                                    self.timer_down[0] = False
                                if datetime.now() - self.down >= timedelta(seconds=2) and self.timer_down[1] == True:
                                    self.counter.incrementByValue(2)
                                    print("down " + str(self.counter.get_value()))
                                    self.timer_down[1] = False
                                if datetime.now() - self.down >= timedelta(seconds=3) and self.timer_down[2] == True:
                                    self.counter.incrementByValue(3)
                                    print("down "+ str(self.counter.get_value()))
                                    self.timer_down[2] = False
                                if datetime.now() - self.down >= timedelta(seconds=4) and self.timer_down[3] == True:
                                    self.counter.incrementByValue(4)
                                    print("down "+ str(self.counter.get_value()))
                                    self.timer_down[3] = False
                                if datetime.now() - self.down >= timedelta(seconds=5) and self.timer_down[4] == True:
                                    self.counter.incrementByValue(5)
                                    print("down "+ str(self.counter.get_value()))
                                    self.timer_down[4] = False
                        else:
                            self.down = None
                            text = "Normal"
                            cv2.putText(frame, text, (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                            self.timer_down = [True, True, True, True, True]

                        if (angle_y_axis < 70 or angle_y_axis > 110):
                            if self.tild is None:
                                self.tild = datetime.now()
                            else:
                                cv2.putText(image, "TildTime: " +str( datetime.now() - self.tild )+ " S", (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                if datetime.now() - self.tild >= timedelta(seconds=1) and self.timer_tild[0] == True:
                                    self.counter.increment()
                                    print("tild "+ str(self.counter.get_value()))
                                    self.timer_tild[0] = False
                                if datetime.now() - self.tild >= timedelta(seconds=2) and self.timer_tild[1] == True:
                                    self.counter.incrementByValue(2)
                                    print("tild "+ str(self.counter.get_value()))
                                    self.timer_tild[1] = False
                                if datetime.now() - self.tild >= timedelta(seconds=3) and self.timer_tild[2] == True:
                                    self.counter.incrementByValue(3)
                                    print("tild "+ str(self.counter.get_value()))
                                    self.timer_tild[2] = False
                                if datetime.now() - self.tild >= timedelta(seconds=4) and self.timer_tild[3] == True:
                                    self.counter.incrementByValue(4)
                                    print("tild "+ str(self.counter.get_value()))
                                    self.timer_tild[3] = False
                                if datetime.now() - self.tild >= timedelta(seconds=5) and self.timer_tild[4] == True:
                                    self.counter.incrementByValue(5)
                                    print("tild "+ str(self.counter.get_value()))
                                    self.timer_tild[4] = False
                        else:
                            self.tild  = None
                            text = "Normal"
                            cv2.putText(frame, text, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                            self.timer_tild = [True, True, True, True, True]



                        # Add the text on the image
                        cv2.putText(image, f'Angle (Y-axis): {angle_y_axis:.2f} degrees',
                                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        self.mp_drawing.draw_landmarks(image, face_landmarks, mp.solutions.face_mesh.FACEMESH_CONTOURS, self.drawing_spec, self.drawing_spec)



                    self.mp_drawing.draw_landmarks(
                                image=image,
                                landmark_list=face_landmarks,
                                landmark_drawing_spec=self.drawing_spec,
                                connection_drawing_spec=self.drawing_spec)
                    
                    self.counter.check_value()

                cv2.imshow(window_name, image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
            else:
            # Display a static message or blank frame when the conditions are not met
                blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(blank_frame, "System Paused", (180, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow(window_name, blank_frame)