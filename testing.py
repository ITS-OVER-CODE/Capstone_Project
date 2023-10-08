import cv2
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Construct the audio file path
audio_file = os.path.join(os.path.dirname(__file__), 'warning.mp3')

# Load the pre-trained eye state classification model (replace 'my_model.h5' with the path to your model)
model = keras.models.load_model('drowsy_driver_model.h5')

# Set the desired image size to 224x224
img_size = 224

# Load the eye cascade classifier
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open a video capture stream (change the parameter to 0 if you want to use the default camera)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FPS, 5)
counter = 0
eyes_roi = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

    for x, y, w, h in eyes:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes_roi = roi_color

    if eyes_roi is not None:
        final_image = cv2.resize(eyes_roi, (img_size, img_size))
        final_image = np.expand_dims(final_image, axis=0)
        final_image = final_image / 255.0

        # Predict eye state using your trained model
        predictions = model.predict(final_image)

        if predictions[0][0] >= 0.3:
            status = "Open Eyes"
            x1, y1, w1, h1 = 0, 0, 175, 75
            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
            cv2.putText(frame, 'Active', (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0), 2)
        else:
            counter = counter + 1
            status = "Closed Eyes"
            x1, y1, w1, h1 = 0, 0, 175, 75
            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)

            if counter > 10:
                x1, y1, w1, h1 = 0, 0, 175, 75
                cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
                cv2.putText(frame, "Sleep Alert !!!", (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255), 2)
                # Play the alert sound
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                # You can adjust the duration of the alert sound as needed
                pygame.time.wait(5000)  # Play for 5 seconds
                counter = 0

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()  # Quit the mixer when done