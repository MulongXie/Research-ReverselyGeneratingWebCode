'''
convert the labels into YOLO format
'''
import os
import numpy as np
import pandas as pd


def box_convert(label):
    x_min = label['bx']
    y_min = label['by']
    x_max = x_min + label['bw']
    y_max = y_min + label['bh']
    return " " + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + ",0"


def label_convert(label_root, img_root, output_path):
    label_news = ""
    indices = os.listdir(os.path.join(label_root))
    indices = [i[:-4] for i in indices]
    for index in indices:
        label_path = os.path.join(label_root, index + '.csv')
        img_path = os.path.join(img_root, index + '\segment')

        label = pd.read_csv(label_path)
        if len(label) == 0:
            print("%s is empty" % label_path)
            continue
        label_new = {}
        for i in range(len(label)):
            l = label.iloc[i]
            seg_no = str(l['segment_no'])
            if seg_no not in label_new:
                label_new[seg_no] = os.path.join(img_path, seg_no + ".png")
            label_new[seg_no] += box_convert(l)

        if len(label_new) > 0:
            label_news += "\n".join(label_new.values())
            label_news += '\n'

        f = open(output_path, 'w')
        f.write(label_news)
    return label_news


data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_segment')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')

root = "D:\\datasets\\dataset_webpage\\data"
l = label_convert(label_root, img_root, 'label.txt')

print(l)