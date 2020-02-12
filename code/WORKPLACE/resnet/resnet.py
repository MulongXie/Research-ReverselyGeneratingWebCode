import keras
from keras.applications.resnet50 import ResNet50
from keras.models import Model,load_model
from keras.layers import Dense, Activation, Flatten, Dropout
import numpy as np

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

        self.model = Model(inputs=base_model, outputs=self.model)
        if is_compile:
            self.model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
            self.model.fit(self.data.X_train, self.data.Y_train, batch_size=64, epochs=epoch_num, verbose=1, validation_data=(self.data.X_test, self.data.Y_test))

    def train(self, data, epoch_num=30):
        self.data = data
        self.build_model(epoch_num)
        self.model.save(self.MODEL_PATH)
        print("Trained model is saved to", self.MODEL_PATH)