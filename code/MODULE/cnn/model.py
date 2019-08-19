import cv2
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

from DATA import Data

data = Data()
data.load_data(resize=True)
data.generate_training_data()

model = Sequential()
# block 1
model.add(Conv2D(64, (3,3), activation='relu', input_shape=data.image_shape, padding='same'))
model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))
# block 2
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
# block 3
model.add(Dense(data.class_number, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
model.fit(data.X_train, data.Y_train, batch_size=64, epochs=10, verbose=1, validation_data=(data.X_test, data.Y_test))