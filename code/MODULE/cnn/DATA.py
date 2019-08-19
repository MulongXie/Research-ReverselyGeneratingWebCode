import cv2
import numpy as np
from os.path import join as pjoin
import glob


class Data:

    def __init__(self):
        self.data_num = 0
        self.images = []
        self.labels = []
        self.images_number = None
        self.labels_number = None

        self.X_train, self.Y_train = None, None
        self.X_test, self.Y_test = None, None

        self.image_shape = (64, 64, 3)
        self.label_map = {'button': 0, 'input': 1, 'select': 3, 'search': 4, 'list': 5}
        self.INPUT_ROOT = "E:/Mulong/Datasets/dataset_webpage/elements"

    def load_data(self, resize=True, shape=None):
        # if customize shape
        if shape is not None:
            self.image_shape = shape
        else:
            shape = self.image_shape
        # load data
        element_paths = glob.glob(pjoin(self.INPUT_ROOT, '*'))
        for ele_path in element_paths:
            label = self.label_map[ele_path.split('\\')[-1]]
            image_paths = glob.glob(pjoin(ele_path, '*.png'))
            for image_path in image_paths:
                image = cv2.imread(image_path)
                if resize:
                    image = cv2.resize(image, shape[:2])
                self.images.append(image)
                self.labels.append(label)

        assert len(self.images) == len(self.labels)
        self.data_num = len(self.images)

    def generate_training_data(self, train_data_ratio=0.8):
        # reshuffle
        np.random.seed(0)
        self.images = np.random.permutation(self.images)
        np.random.seed(0)
        self.labels = np.random.permutation(self.labels)
        # separate dataset
        cut = int(train_data_ratio * self.data_num)
        self.X_train = self.images[:cut]
        self.X_test = self.images[cut:]
        self.Y_train = self.labels[:cut]
        self.Y_test = self.labels[cut:]