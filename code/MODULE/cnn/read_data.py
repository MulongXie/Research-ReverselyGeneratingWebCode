import cv2
import numpy as np
from os.path import join as pjoin
import glob


class Data:

    def __init__(self):
        self.imgs = []
        self.labels = []
        self.imgs_shape = None
        self.labels_shape = None

        self.labels_map = {'button': 0, 'input': 1, 'select': 3, 'search': 4, 'list': 5}
        self.INPUT_ROOT = "E:/Mulong/Datasets/dataset_webpage/elements"

    def read_data(self):
        element_paths = glob.glob(pjoin(self.INPUT_ROOT, '*'))

        for ele_path in element_paths:
            img_paths = glob.glob(pjoin(ele_path, '*.png'))
            label = ele_path.split('\\')[-1]

            self.imgs += [cv2.imread(path) for path in img_paths]
            self.labels += list(np.full(len(img_paths), self.labels_map[label], dtype=int))
