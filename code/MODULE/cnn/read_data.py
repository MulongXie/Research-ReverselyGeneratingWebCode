import cv2
import numpy as np
from os.path import join as pjoin
import glob


def read_data(img_root):
    element_paths = glob.glob(pjoin(ROOT_INPUT, '*'))

    for ele_path in element_paths:
        img_paths = glob.glob(pjoin(ele_path, '*.png'))

        label = ele_path.split('\\')[-1]

        print(label, len(img_paths))


ROOT_INPUT = "E:/Mulong/Datasets/dataset_webpage/elements"
read_data(ROOT_INPUT)