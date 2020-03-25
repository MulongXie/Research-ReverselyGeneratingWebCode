from os.path import join as pjoin
import os
from glob import glob
import random
import pandas as pd
import cv2
import numpy as np
import json
from tqdm import tqdm
from random import randint as rint

element_map = {'0':'Button', '1':'CheckBox', '2':'Chronometer', '3':'EditText', '4':'ImageButton', '5':'ImageView',
               '6':'ProgressBar', '7':'RadioButton', '8':'RatingBar', '9':'SeekBar', '10':'Spinner', '11':'Switch',
               '12':'ToggleButton', '13':'VideoView', '14':'TextView'}


def draw_bounding_box(org, corners, color=(0, 255, 0), line=2, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('board', board)
        cv2.waitKey(0)
    return board


def load(input_root, output_root, max_num, show=False):
    def random_bbox(img_shape):
        # random.seed(seed)
        img_height, img_width = img_shape[:2]
        height = rint(5, 30)
        width = rint(5, 30)
        if img_height <= height or img_width <= width:
            return None
        row_min = rint(0, img_height - height - 1)
        col_min = rint(0, img_width - width - 1)
        return col_min, row_min, col_min + width, row_min + height

    count = 0
    image_paths = glob(pjoin(input_root, '*.png'))
    for image_path in image_paths:
        print(image_path, count)
        org = cv2.imread(image_path)
        num = int(org.shape[0] / 15)
        bboxes = []
        for i in range(num):
            bbox = random_bbox(org.shape)
            if bbox is None:
                continue
            clip = org[bbox[0]:bbox[2], bbox[1]:bbox[3]]
            if clip.shape[0] > 10 and clip.shape[1] > 10:
                count += 1
                cv2.imwrite(pjoin(output_root, str(count) + '.png'), clip)
                bboxes.append(bbox)

        if show:
            draw_bounding_box(org, bboxes, show=True)

        if count > max_num:
            return


ROOT_OUTPUT = "E:/Mulong/Datasets/rico/element-noise"
ROOT_INPUT = 'E:/Mulong/Datasets/rico/elements-14/ImageView'
ROOT_IMG = 'E:/Mulong/Datasets/rico/combined'
load(ROOT_INPUT, ROOT_OUTPUT, 20000 - 2104, show=False)
