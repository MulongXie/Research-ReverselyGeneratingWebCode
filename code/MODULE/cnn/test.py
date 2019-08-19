from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
import cv2
import numpy as np
from CONFIG import Config

cfg = Config()


class CNN:

    def __init__(self):
        self.data = None
        self.model = None

        self.image_shape = cfg.image_shape
        self.class_number = cfg.class_number
        self.class_map = cfg.class_map
        self.MODEL_PATH = cfg.MODEL_PATH

    def network(self):
        # block 1
        self.model.add(Conv2D(64, (3, 3), activation='relu', input_shape=self.image_shape, padding='same'))
        self.model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        self.model.add(MaxPool2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        # block 2
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        # block 3
        self.model.add(Dense(self.class_number, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
        self.model.fit(self.data.X_train, self.data.Y_train, batch_size=64, epochs=10, verbose=1, validation_data=(self.data.X_test, self.data.Y_test))

    def train(self, data):
        self.data = data
        self.model = Sequential()
        self.network()
        self.model.save(self.MODEL_PATH)
        print("Trained model is saved to", self.MODEL_PATH)

    def predict(self, img_path):
        """
        :type img: list of img path
        """
        self.model = load_model(self.MODEL_PATH)
        for path in img_path:
            img = cv2.imread(path)
            X = cv2.resize(img, self.image_shape[:2])
            X = np.array([X])  # from (64, 64, 3) to (1, 64, 64, 3)
            Y = self.model.predict(X)
            print(Y)