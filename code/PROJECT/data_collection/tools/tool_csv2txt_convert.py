'''
convert the labels into YOLO format
'''
import os
import numpy as np
import pandas as pd


def label_convert(label_root, img_root):

    def box_convert(label):
        x_min = label['bx']
        y_min = label['by']
        x_max = x_min + label['bw']
        y_max = y_min + label['bh']
        if label['element'] == 'button':
            element = '0'
        elif label['element'] == 'input':
            element = '1'
        elif label['element'] == 'select':
            element = '2'
        elif label['element'] == 'search':
            element = '3'
        elif label['element'] == 'list':
            element = '4'
        return " " + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + "," + element

    stamp = 302

    label_news = ""
    indices = os.listdir(label_root)
    indices = [i[:-4] for i in indices]
    indices.sort(key=lambda x: int(x))
    for index in indices:
        label_path = label_root + '/' + index + '.csv'
        img_path = img_root + '/' + str(int(index) + stamp)

        label = pd.read_csv(label_path)
        label_new = {}
        for i in range(len(label)):
            l = label.iloc[i]
            seg_no = str(int(l['segment_no']))
            if seg_no not in label_new:
                label_new[seg_no] = img_path + '/' + seg_no + ".png"
            label_new[seg_no] += box_convert(l)

        if len(label_new) > 0:
            label_news += "\n".join(label_new.values())
            label_news += '\n'

    open('label.txt', 'w').write(label_news)
    open('label_colab.txt', 'w').write(label_news.replace(img_root, './data'))
    return label_news


img_root = 'E:/Mulong/Datasets/dataset_webpage/page10000/ip_img_segment'
label_root = 'E:/Mulong/Datasets/dataset_webpage/page10000/relabel'
l = label_convert(label_root, img_root)
