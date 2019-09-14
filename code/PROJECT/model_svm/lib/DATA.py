import cv2
import numpy as np
from os.path import join as pjoin
import glob
from skimage.feature import hog

from CONFIG import Config

cfg = Config()


class Data:

    def __init__(self):
        self.data_num = 0
        self.images = []
        self.labels = []
        self.X_train, self.Y_train = None, None
        self.X_test, self.Y_test = None, None

        self.image_shape = cfg.image_shape
        self.class_map = cfg.class_map
        self.class_number = len(cfg.class_map)
        self.element_number = {}
        self.DATA_PATH = cfg.DATA_PATH

    def load_data(self, resize=True, shape=None):
        # count elements in each classes
        for c in self.class_map:
            self.element_number[c] = 0

        # if customize shape
        if shape is not None:
            self.image_shape = shape
        else:
            shape = self.image_shape

        # load data
        for p in glob.glob(pjoin(self.DATA_PATH, '*')):
            class_name = p.split('\\')[-1]
            label = self.class_map.index(class_name)  # map to index of classes
            for image_path in glob.glob(pjoin(p, '*.png'))[:30000]:
                image = cv2.imread(image_path, 0)
                if resize:
                    try:
                        image = cv2.resize(image, shape[:2])
                    except:
                        print(image_path)
                        continue
                self.images.append(image)
                self.labels.append(label)
                self.element_number[class_name] += 1

            assert len(self.images) == len(self.labels)
            print(self.element_number)

        self.data_num = len(self.images)
        print('%d Data Loaded' % self.data_num)

    def generate_training_data_HOG(self, train_data_ratio=0.8):

        def calc_hog(imgs):
            imgs_hog = []
            for img in imgs:
                imgs_hog.append(hog(img, block_norm='L2'))
            return imgs_hog

        # reshuffle
        np.random.seed(0)
        self.images = np.random.permutation(self.images)
        np.random.seed(0)
        self.labels = np.random.permutation(self.labels)

        # separate dataset
        cut = int(train_data_ratio * self.data_num)
        self.X_train = calc_hog(self.images[:cut])
        self.X_test = calc_hog(self.images[cut:])
        self.Y_train = self.labels[:cut]
        self.Y_test = self.labels[cut:]

        print('X_train:%d, Y_train:%d' % (len(self.X_train), len(self.Y_train)))
        print('X_test:%d, Y_test:%d' % (len(self.X_test), len(self.Y_test)))
