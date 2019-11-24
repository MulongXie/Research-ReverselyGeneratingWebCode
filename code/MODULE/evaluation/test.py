import glob
import pandas as pd
from os.path import join as pjoin
import cv2

root = "E:\Mulong\Datasets\dataset_webpage\manually_labelled"
img_paths = pjoin(root, 'data')
label_paths = pjoin(root, 'label')

f = open('label.txt', 'r')

colors = [(255, 0, 255), (255, 160, 0), (0, 150, 255), (255, 150, 255), (255, 255, 0)]
ele_name = ['button', 'input', 'select', 'search', 'list']


def draw_label(line):
    line = line.split()
    print(line[0])
    img = cv2.imread(line[0])
    label = line[1:]

    for i in range(len(label)):
        # col_min, row_min, col_max, row_max, element_class
        l = [int(e) for e in label[i].split(',')]
        element = ele_name[l[-1]]
        color = colors[l[-1]]
        cv2.rectangle(img, (l[0], l[1]), (l[2], l[3]), color, 1)
        cv2.putText(img, element, (l[0], l[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    cv2.imshow('img', img)
    cv2.waitKey()


for line in f.readlines():
    draw_label(line)
