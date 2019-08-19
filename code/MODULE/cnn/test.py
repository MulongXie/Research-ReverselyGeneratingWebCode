from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

from DATA import Data


class CNN:

    def __init__(self, data):
        self.data = data
        self.model = Sequential()
        self.OUTPUT_ROOT = 'E:/Mulong/Model/ui_compos'

    def model(self, data):
        # block 1
        self.model.add(Conv2D(64, (3, 3), activation='relu', input_shape=data.image_shape, padding='same'))
        self.model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        self.model.add(MaxPool2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        # block 2
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        # block 3
        self.model.add(Dense(data.class_number, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
        self.model.fit(data.X_train, data.Y_train, batch_size=64, epochs=10, verbose=1, validation_data=(data.X_test, data.Y_test))

    def train(self):
        self.model(self.data)
        self.model.save(self.OUTPUT_ROOT)