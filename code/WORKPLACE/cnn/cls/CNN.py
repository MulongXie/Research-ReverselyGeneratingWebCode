import keras
from keras.applications.resnet50 import ResNet50
from keras.models import Model,load_model
from keras.layers import Dense, Activation, Flatten, Dropout
from sklearn.metrics import confusion_matrix
import numpy as np
import cv2


class CNN:
    def __init__(self, model_path, is_load=True):
        '''
        :param classifier_type: 'Text' or 'Noise' or 'Elements'
        '''
        self.model = None
        self.image_shape = (64,64,3)
        self.class_number = 15
        self.class_map = {'0':'Button', '1':'CheckBox', '2':'Chronometer', '3':'EditText', '4':'ImageButton', '5':'ImageView',
               '6':'ProgressBar', '7':'RadioButton', '8':'RatingBar', '9':'SeekBar', '10':'Spinner', '11':'Switch',
               '12':'ToggleButton', '13':'VideoView', '14':'TextView'}
        self.model_path = model_path
        if is_load:
            self.load()

    def load(self):
        self.class_number = len(self.class_map)
        self.model = load_model(self.model_path)
        print('Model Loaded From', self.model_path)

    def preprocess_img(self, image):
        image = cv2.resize(image, self.image_shape[:2])
        x = (image / 255).astype('float32')
        x = np.array([x])
        return x

    def predict(self, imgs, load=False, show=False):
        """
        :type img_path: list of img path
        """
        classes = []
        if load:
            self.load()
        if self.model is None:
            print("*** No model loaded ***")
            return
        for i in range(len(imgs)):
            X = self.preprocess_img(imgs[i])
            Y = self.class_map[str(np.argmax(self.model.predict(X)))]
            classes.append(Y)
            if show:
                print(Y)
                cv2.imshow('element', imgs[i])
                cv2.waitKey()
        return classes

