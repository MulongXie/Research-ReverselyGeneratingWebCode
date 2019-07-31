import cv2
import pandas as pd
import numpy as np
import glob
from os.path import join as pjoin


def box_convert(label):
    element = label['element']
    if element == 'button':
        ele_no = 0
    elif element == 'input':
        ele_no = 1
    elif element == 'select':
        ele_no = 2
    x_min = label['bx']
    y_min = label['by']
    x_max = x_min + label['bw']
    y_max = y_min + label['bh']
    return " " + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + "," + ele_no


def label_convert(img_root='E:\\Mulong\\Datasets\\dataset_webpage\\img_segment', label_root='E:\\Mulong\\Datasets\\dataset_webpage\\relabel'):
    label_paths = glob.glob(pjoin(label_root, '*.csv'))
    label_paths.sort(key=lambda x: int(x.split('\\')[-1][:-4]))

    for label_path in label_paths:
        print(label_path)
        label = pd.read_csv(label_path)
        label_new = {}
        for i in range(len(label)):
            l = label.iloc[i]
            seg_no = l['segment_no']
            if seg_no not in label_new:
                label_new[seg_no] = pjoin()


label_convert()