from os.path import join as pjoin
import glob
import pandas as pd
import cv2
import numpy as np

import CONFIG

C = CONFIG.Config()
element_map = {'0':'button', '1':'input', '2':'select', '3':'search', '4':'list'}
element_number = {'button':0, 'input':0, 'select':0, 'search':0, 'list':0}


def view(img, label):

    # 'x_min, y_min, x_max, y_max, element'
    for l in label:
        l = l.split(',')
        print(l)
        x_min = int(l[0])
        y_min = int(l[1])
        x_max = int(l[2])
        y_max = int(l[3])
        element = element_map[l[4]]
        element_number[element] += 1
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)
        cv2.imshow('img', img)
        cv2.waitKey(0)


def read_files():
    labels = open(C.ROOT_RELABEL, 'r')
    for l in labels.readlines():
        l = l.replace('./', C.ROOT_IMG_SEGMENT).split()
        img_path = l[0]
        label = l[1:]
        img = cv2.imread(img_path)
        print(img_path)
        view(img, label)


read_files()