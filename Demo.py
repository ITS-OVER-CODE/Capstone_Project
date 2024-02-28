import cv2
import mediapipe as mp
import math
import os


def draw_landmarks(frame, landmarks):
    for landmark in landmarks:
        x, y, z = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]), landmark.z
        cv2.circle(frame, (x, y), 1, (0, 255, 0), 1)  # Draw a point for each landmark

audio_file = os.path.join(os.path.dirname(__file__), 'warning.mp3')

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with FaceMesh
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw landmarks
            draw_landmarks(frame, face_landmarks.landmark)

            # Calculate the angle with respect to the y-axis (vertical)
            deltaY = face_landmarks.landmark[152].y - face_landmarks.landmark[10].y
            deltaX = face_landmarks.landmark[152].x - face_landmarks.landmark[10].x
            angle_y_axis = math.degrees(math.atan2(deltaY, deltaX))

            # Calculate the angle with respect to the x-axis (horizontal)
            deltaY_x = face_landmarks.landmark[454].y - face_landmarks.landmark[234].y
            deltaX_x = face_landmarks.landmark[454].x - face_landmarks.landmark[234].x
            angle_x_axis = math.degrees(math.atan2(deltaY_x, deltaX_x))


            # Display angles on the frame
            if angle_y_axis < 110 or  angle_y_axis > 70:
                cv2.putText(frame, f'Angle (Y-axis): {angle_y_axis:.2f} degrees',
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'Angle (X-axis): {angle_x_axis:.2f} degrees',
                            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if angle_y_axis > 110 or  angle_y_axis < 70:
                cv2.putText(frame, f'Angle (Y-axis): {angle_y_axis:.2f} degrees',
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, f'Angle (X-axis): {angle_x_axis:.2f} degrees',
                            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            

    # Display the frame with landmarks
    cv2.imshow('Face Mesh Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
