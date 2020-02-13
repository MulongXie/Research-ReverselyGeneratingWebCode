import keras
from keras.applications.resnet50 import ResNet50
from keras.models import Model,load_model
from keras.layers import Dense, Activation, Flatten, Dropout
import numpy as np
import cv2

from Config import Config
cfg = Config()


class ResClassifier():
    def __init__(self):
        self.data = None
        self.model = None

        self.image_shape = cfg.image_shape
        self.class_number = cfg.class_number
        self.class_map = cfg.class_map
        self.MODEL_PATH = cfg.MODEL_PATH

    def build_model(self, epoch_num, is_compile=True):
        base_model = ResNet50(include_top=False, weights='imagenet', input_shape=self.image_shape)
        for layer in base_model.layers:
            layer.trainable = False
        self.model = Flatten()(base_model.output)
        self.model = Dense(128, activation='relu')(self.model)
        self.model = Dropout(0.5)(self.model)
        self.model = Dense(15, activation='softmax')(self.model)

        self.model = Model(inputs=base_model.input, outputs=self.model)
        if is_compile:
            self.model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
            self.model.fit(self.data.X_train, self.data.Y_train, batch_size=64, epochs=epoch_num, verbose=1,
                           validation_data=(self.data.X_test, self.data.Y_test))

    def train(self, data, epoch_num=30):
        self.data = data
        self.build_model(epoch_num)
        self.model.save(self.MODEL_PATH)
        print("Trained model is saved to", self.MODEL_PATH)

    def predict(self, img_path, load=True, show=False):
        """
        :type img_path: list of img path
        """
        if load:
            self.load()
        for path in img_path:
            img = cv2.imread(path)
            X = cv2.resize(img, self.image_shape[:2])
            X = np.array([X])  # from (64, 64, 3) to (1, 64, 64, 3)
            Y = self.class_map[np.argmax(self.model.predict(X))]
            print(Y)
            if show:
                cv2.imshow('img', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def load(self):
        self.model = load_model(self.MODEL_PATH)
        print('Model Loaded From', self.MODEL_PATH)