import cv2
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout


def network(model, data):
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


def train(data, model_path='E:/Mulong/Model/ui_compos/cnn1.h5'):
    model = Sequential()
    network(model, data)
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    model.fit(data.X_train, data.Y_train, batch_size=64, epochs=10, verbose=1, validation_data=(data.X_test, data.Y_test))
    model.save(model_path)


def predict(img_path, model_path='E:/Mulong/Model/ui_compos/cnn1.h5'):
    for path in img_path:
        img = cv2.imread(path)
        X = cv2.resize(img, (64, 64))
        X = np.reshape(X, (1, 64, 64, 3))
        model = load_model(model_path)
        pre = model.predict(X)
        print(pre)