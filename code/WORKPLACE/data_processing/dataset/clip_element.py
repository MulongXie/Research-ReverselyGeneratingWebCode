from os.path import join as pjoin
import os
import glob
import pandas as pd
import cv2
import numpy as np

element_map = {'0':'Image', '1':'Icon', '2':'Button', '3':'Input'}
element_number = {'Image':176976, 'Icon':148376, 'Button':72371, 'Input':14664}
ROOT_OUTPUT = "E:/Mulong/Datasets/rico/elements"
ROOT_IMG = 'E:/Mulong/Datasets/rico/combined'
ROOT_LABEL = 'label_val.txt'


def setup_folder():
    for name in element_number:
        path = pjoin(ROOT_OUTPUT, name)
        if not os.path.exists(path):
            os.mkdir(path)


def fetch_and_clip(img, label, output_root, shrink_ratio=3, pad=False, show_label=False, show_clip=False, write_clip=True):

    def padding(clip):
        height = np.shape(clip)[0]
        width = np.shape(clip)[1]

        pad_height = int(height / 10)
        pad_wid = int(width / 10)
        pad_img = np.full(((height + pad_height), (width + pad_wid), 3), 255, dtype=np.uint8)
        pad_img[int(pad_height / 2):(int(pad_height / 2) + height), int(pad_wid / 2):(int(pad_wid / 2) + width)] = clip
        return pad_img

    def shrink(img, ratio=3.5):
        img_shrink = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))
        return img_shrink

    def clipping():
        clip = img[y_min:y_max, x_min:x_max]
        clip = cv2.resize(clip, (int(clip.shape[1] / shrink_ratio), int(clip.shape[0] / shrink_ratio)))
        if pad:
            clip = padding(clip)
        clip = shrink(clip)
        if write_clip:
            cv2.imwrite(pjoin(output_root, element, str(element_number[element]) + '.png'), clip)
        if show_clip:
            cv2.imshow('clip', clip)
            cv2.waitKey(0)

    # 'x_min, y_min, x_max, y_max, element'
    for l in label:
        l = l.split(',')
        x_min = min(int(l[0]), int(l[2]))
        y_min = min(int(l[1]), int(l[3]))
        x_max = max(int(l[0]), int(l[2]))
        y_max = max(int(l[1]), int(l[3]))
        if y_max - y_min < 20 or x_max - x_min < 20:
            continue
        element = element_map[l[4]]
        element_number[element] += 1

        clipping()

        if show_label:
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)
            cv2.imshow('img', shrink(img))
            cv2.waitKey(0)


def read_files():
    start_point = '38074'
    locate = False
    bad_img = 1
    labels = open(ROOT_LABEL, 'r')
    for i, l in enumerate(labels.readlines()):
        l = l.replace('./', ROOT_IMG).split()
        img_path = l[0]
        label = l[1:]
        index = img_path.split('\\')[-1][:-4]

        if locate:
            if index != start_point:
                continue
            else:
                print('Start from ', start_point)
                locate = False

        img = cv2.imread(img_path)
        img = cv2.resize(img, (1440, 2560))
        print(i, img_path)

        try:
            fetch_and_clip(img, label, ROOT_OUTPUT, show_label=False)
        except:
            print('*** Bad img:', bad_img, img_path, '***')


setup_folder()
read_files()
print(element_number)
