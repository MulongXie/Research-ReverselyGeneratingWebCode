import cv2
import numpy as np
from os.path import join as pjoin
import glob
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
                image = cv2.imread(image_path)
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
        print('%d Data Loaded with Shape:(%d, %d)' % (self.data_num, shape[0], shape[1]))

    def generate_training_data(self, train_data_ratio=0.8):
        # transfer int into c dimensions one-hot array
        def expand(label, class_number):
            # return y : (num_class, num_samples)
            y = np.eye(class_number)[label]
            y = np.squeeze(y)
            return y

        # reshuffle
        np.random.seed(0)
        self.images = np.array(np.random.permutation(self.images))
        np.random.seed(0)
        self.labels = np.random.permutation(self.labels)
        Y = expand(self.labels, self.class_number)

        # separate dataset
        cut = int(train_data_ratio * self.data_num)
        self.X_train = (self.images[:cut] / 255).astype('float32')
        self.X_test = (self.images[cut:] / 255).astype('float32')
        self.Y_train = Y[:cut]
        self.Y_test = Y[cut:]

        print('X_train:%d, Y_train:%d' % (len(self.X_train), len(self.Y_train)))
        print('X_test:%d, Y_test:%d' % (len(self.X_test), len(self.Y_test)))
