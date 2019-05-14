import os
import numpy as np
import pandas as pd


def box_convert(label):
    x_min = label['bx']
    y_min = label['by']
    x_max = x_min + label['bw']
    y_max = y_min + label['bh']
    return " " + str(x_min) + " " + str(y_min) + " " + str(x_max) + " " + str(y_max) + " 1"


def label_convert(root):
    label_new = ""
    names = os.listdir(os.path.join(root, 'segment\\img'))
    for name in names:
        label_path = os.path.join(root, 'segment\\label\\' + str(name))
        img_path = os.path.join(root, 'segment\\img\\' + str(name))

        label_segments = pd.read_csv(os.path.join(label_path, 'segment.csv'))

        label_convert = {}
        for i in range(len(label_segments)):
            l = label_segments.iloc[i]
            seg_no = str(l['segment_no'])
            if seg_no not in label_convert:
                label_convert[seg_no] = img_path + "\\segment\\" + seg_no + ".jpg "
            label_convert[seg_no] += box_convert(l)

        label_new += "\n".join(label_convert.values())
    return label_new


root = "D:\\datasets\\dataset_webpage\\data"
l = label_convert(root)
print(l)