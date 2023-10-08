import tensorflow as tf
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Constants
Datadirectory = "/mnt/c/Users/bader/Desktop/C_project/Datasets"
Classes = ["Closed", "Opened"]
img_size = 224
batch_size = 32

# Load and preprocess images on-the-fly using a data generator
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255.0,
    validation_split=0.2
)

train_data_generator = datagen.flow_from_directory(
    Datadirectory,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True,
    subset='training'  # Specify 'training' for the training set
)

valid_data_generator = datagen.flow_from_directory(
    Datadirectory,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True,
    subset='validation'  # Specify 'validation' for the validation set
)

# Create the model
model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(5, 5), activation='relu', input_shape=(img_size, img_size, 3)))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=16, kernel_size=(7, 7), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=8, kernel_size=(5, 5), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(Dense(64, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(Dense(len(Classes), activation="softmax"))

model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.0001), metrics=['accuracy'])

model.summary()

# Train the model
epochs = 20
history = model.fit(train_data_generator, epochs=epochs, validation_data=valid_data_generator)

# Save the trained model
model.save("drowsy_driver_model.h5")

# Plot the training history
plt.figure(figsize=(12, 5))
plt.plot(history.history['accuracy'], color='r', label='Train Accuracy')
plt.plot(history.history['val_accuracy'], color='b', label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend()
plt.show()

# Load the test data using the same data generator
test_data_generator = datagen.flow_from_directory(
    Datadirectory,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False,  # Set shuffle to False for the test set
    subset='validation'  # Specify 'validation' for the test set
)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(test_data_generator)

# Print the test accuracy
print(f"Test accuracy: {test_accuracy}")
