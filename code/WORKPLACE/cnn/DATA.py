import cv2
import numpy as np
from os.path import join as pjoin
import glob
from tqdm import tqdm
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
        self.class_number = cfg.class_number
        self.class_map = cfg.class_map
        self.DATA_PATH = cfg.DATA_PATH

    def load_data(self, resize=True, shape=None, max_number=1000000):
        # if customize shape
        if shape is not None:
            self.image_shape = shape
        else:
            shape = self.image_shape
        # load data
        for p in glob.glob(pjoin(self.DATA_PATH, '*')):
            print("*** Loading components of %s: %d ***" %(p.split('\\')[-1], int(len(glob.glob(pjoin(p, '*.png'))))))
            if p.split('\\')[-1] == 'text':
                label = 0
                max_number = 100000
            else:
                label = 1

            for i, image_path in enumerate(tqdm(glob.glob(pjoin(p, '*.png'))[:max_number])):
                try:
                    image = cv2.imread(image_path)
                    if resize:
                        image = cv2.resize(image, shape[:2])
                    self.images.append(image)
                    self.labels.append(label)
                except:
                    continue
        assert len(self.images) == len(self.labels)
        self.data_num = len(self.images)
        print('%d Data Loaded' % self.data_num)

    def load_data_textview(self, resize=True, shape=None, max_number=10000):
        # if customize shape
        if shape is not None:
            self.image_shape = shape
        else:
            shape = self.image_shape
        # load text
        PATH_TEXT = 'E:\\Mulong\\Datasets\\rico\\elements-14\\TextView'
        print("*** Loading texts of %s: %d ***" %(PATH_TEXT.split('\\')[-1], int(len(glob.glob(pjoin(PATH_TEXT, '*.png'))))))
        label = 0
        for i, image_path in enumerate(tqdm(glob.glob(pjoin(PATH_TEXT, '*.png'))[:20000])):
            try:
                image = cv2.imread(image_path)
                if resize:
                    image = cv2.resize(image, shape[:2])
                self.images.append(image)
                self.labels.append(label)
            except:
                continue
        # load non-text
        PATH_COMPO = "E:\Mulong\Datasets\dataset_webpage\Components3"
        for p in glob.glob(pjoin(PATH_COMPO, '*')):
            if p.split('\\')[-1] == 'text':
                continue
            print("*** Loading components of %s: %d ***" % (p.split('\\')[-1], int(len(glob.glob(pjoin(p, '*.png'))))))
            label = 1
            for i, image_path in enumerate(tqdm(glob.glob(pjoin(p, '*.png'))[:max_number])):
                try:
                    image = cv2.imread(image_path)
                    if resize:
                        image = cv2.resize(image, shape[:2])
                    self.images.append(image)
                    self.labels.append(label)
                except:
                    continue
        assert len(self.images) == len(self.labels)
        self.data_num = len(self.images)
        print('%d Data Loaded' % self.data_num)

    def load_data_noise(self, resize=True, shape=None, max_number=10000):
        # if customize shape
        if shape is not None:
            self.image_shape = shape
        else:
            shape = self.image_shape
        # load noise
        PATH_NOISE = 'E:\\Mulong\\Datasets\\rico\\element-noise'
        print("*** Loading %s: %d ***" %(PATH_NOISE.split('\\')[-1], int(len(glob.glob(pjoin(PATH_NOISE, '*.png'))))))
        label = 0
        for i, image_path in enumerate(tqdm(glob.glob(pjoin(PATH_NOISE, '*.png'))[:20000])):
            try:
                image = cv2.imread(image_path)
                if resize:
                    image = cv2.resize(image, shape[:2])
                self.images.append(image)
                self.labels.append(label)
            except:
                continue
        # load non-noise
        PATH_COMPO = "E:\Mulong\Datasets\dataset_webpage\Components3"
        for p in glob.glob(pjoin(PATH_COMPO, '*')):
            print("*** Loading components of %s: %d ***" % (p.split('\\')[-1], int(len(glob.glob(pjoin(p, '*.png'))))))
            label = 1
            for i, image_path in enumerate(tqdm(glob.glob(pjoin(p, '*.png'))[:max_number])):
                try:
                    image = cv2.imread(image_path)
                    if resize:
                        image = cv2.resize(image, shape[:2])
                    self.images.append(image)
                    self.labels.append(label)
                except:
                    continue
        assert len(self.images) == len(self.labels)
        self.data_num = len(self.images)
        print('%d Data Loaded' % self.data_num)

    def load_data_image(self, resize=True, shape=None, max_number=10000):
        # if customize shape
        if shape is not None:
            self.image_shape = shape
        else:
            shape = self.image_shape
        # load image
        PATH_IMAGE = 'E:\\Mulong\\Datasets\\dataset_webpage\\Components3\\img'
        print("*** Loading %s: %d ***" %(PATH_IMAGE.split('\\')[-1], int(len(glob.glob(pjoin(PATH_IMAGE, '*.png'))))))
        label = 0
        for i, image_path in enumerate(tqdm(glob.glob(pjoin(PATH_IMAGE, '*.png'))[:20000])):
            try:
                image = cv2.imread(image_path)
                if resize:
                    image = cv2.resize(image, shape[:2])
                self.images.append(image)
                self.labels.append(label)
            except:
                continue
        # load non-image
        PATH_COMPO = "E:\Mulong\Datasets\dataset_webpage\Components3"
        label = 1
        for p in glob.glob(pjoin(PATH_COMPO, '*')):
            if p.split('\\')[-1] == 'img':
                continue
            print("*** Loading components of %s: %d ***" % (p.split('\\')[-1], int(len(glob.glob(pjoin(p, '*.png'))))))
            for i, image_path in enumerate(tqdm(glob.glob(pjoin(p, '*.png'))[:max_number])):
                try:
                    image = cv2.imread(image_path)
                    if resize:
                        image = cv2.resize(image, shape[:2])
                    self.images.append(image)
                    self.labels.append(label)
                except:
                    continue
        assert len(self.images) == len(self.labels)
        self.data_num = len(self.images)
        print('%d Data Loaded' % self.data_num)

    def generate_training_data(self, train_data_ratio=0.8):
        # transfer int into c dimensions one-hot array
        def expand(label, class_number):
            # return y : (num_class, num_samples)
            y = np.eye(class_number)[label]
            y = np.squeeze(y)
            return y
        # reshuffle
        np.random.seed(0)
        self.images = np.random.permutation(self.images)
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
