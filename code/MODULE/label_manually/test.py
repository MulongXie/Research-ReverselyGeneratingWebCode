import cv2
import pandas as pd
import numpy as np
import glob
from os.path import join as pjoin


def box_convert(label):
    element = label['element']
    if element == 'button':
        ele_no = '0'
    elif element == 'input':
        ele_no = '1'
    elif element == 'select':
        ele_no = '2'
    x_min = label['bx']
    y_min = label['by']
    x_max = x_min + label['bw']
    y_max = y_min + label['bh']
    return " " + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + "," + ele_no


def label_convert(output_path, img_root='E:\\Mulong\\Datasets\\dataset_webpage\\img_segment', label_root='E:\\Mulong\\Datasets\\dataset_webpage\\relabel'):
    label_paths = glob.glob(pjoin(label_root, '*.csv'))
    label_paths.sort(key=lambda x: int(x.split('\\')[-1][:-4]))
    label_converted = ''
    for label_path in label_paths:
        index = label_path.split('\\')[-1][:-4]
        label = pd.read_csv(label_path)
        label_new = {}
        for i in range(len(label)):
            l = label.iloc[i]
            seg_no = int(l['segment_no'])
            if seg_no not in label_new:
                label_new[seg_no] = pjoin(img_root, index, str(seg_no) + '.png')
            label_new[seg_no] += box_convert(l)

        label_converted += "\n".join(label_new.values()) + "\n"
    print(label_converted)
    f = open(output_path, 'w')
    f.write(label_converted)


def label_colab(output_path, org_label='E:\\Mulong\\Datasets\\dataset_webpage\\label.txt'):
    label = open(org_label, 'r')
    colab_l = ''
    for l in label.readlines():
        colab_l += './data/' + '/'.join(l.split('\\')[-2:])
    # colab_l.replace('\\', '/')
    print(colab_l)
    label_new = open(output_path, 'w')
    label_new.write(colab_l)


# label_convert('E:\\Mulong\\Datasets\\dataset_webpage\\label.txt')
label_colab('E:\\Mulong\\Datasets\\dataset_webpage\\label_colab.txt')