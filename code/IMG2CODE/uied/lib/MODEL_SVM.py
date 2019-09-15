from sklearn import svm
from sklearn.externals import joblib
import cv2
import numpy as np
from skimage.feature import hog

from CONFIG_SVM import Config
cfg = Config()


class SVM:

    def __init__(self):
        self.data = None
        self.model = None

        self.image_shape = cfg.image_shape
        self.class_number = cfg.class_number
        self.class_map = cfg.class_map
        self.MODEL_PATH = cfg.MODEL_PATH

    def train(self, data):
        self.data = data
        self.model = svm.SVC(verbose=True, probability=True)
        self.model.fit(data.X_train, data.Y_train)
        joblib.dump(self.model, self.MODEL_PATH)
        print("Trained model is saved to", self.MODEL_PATH)

    def evaluate(self, data, load=True):
        self.data.score(data.X_test, data.Y_test)

    def predict(self, imgs, load=False, show=False):
        """
        :type img_path: list of img path
        """
        if load:
            self.load()
        predictions = []
        for img in imgs:
            if len(img.shape) > 2:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, self.image_shape[:2])
            X = hog(img, block_norm='L2')
            X = np.reshape(X, (1, -1))
            Y = self.class_map[int(self.model.predict(X))]
            predictions.append(Y)
            if show:
                print(Y)
                cv2.imshow('img', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        return predictions

    def load(self):
        self.model = joblib.load(self.MODEL_PATH)
        print('Model Loaded From', self.MODEL_PATH)
