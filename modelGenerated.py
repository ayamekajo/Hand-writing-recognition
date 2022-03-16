import os
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import numpy as np
import tensorflow.python.keras as keras
from tensorflow.python.keras import layers
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D





# Build the model
model = Sequential()

# Convolution layers
model.add(
    Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding='same',
        input_shape=(28, 28, 1),
        activation='relu'))

# Pooling layers
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

#Convolution layers
model.add(
    Conv2D(filters=256, kernel_size=(3, 3), padding='same', activation='relu'))

# Pooling layers
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

#Convolution layers
model.add(
    Conv2D(filters=256, kernel_size=(3, 3), padding='same', activation='relu'))

# Pooling layers
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))


# flatten layers
model.add(Flatten())


# fully-connected layers
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(52, activation='softmax'))



#Output the parameters of each layers in model
model.summary()


#save model
model.save('saved_model/my_model_28')