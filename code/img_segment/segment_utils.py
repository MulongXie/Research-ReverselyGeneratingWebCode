import cv2
import numpy as np
import os
import pandas as pd

import segment_drawLabel as sd


def segment_img(segment_size, img_name=0, img_root_path="D:\datasets\dataset_webpage\data\segment\img", show=True):
    img_path = os.path.join(img_root_path, str(img_name))
    img_input_path = os.path.join(img_path, 'org.png')
    img_output_path = os.path.join(img_path, 'segment')

    print(img_path)

    img = cv2.imread(img_input_path)
    height_bottom = np.shape(img)[0]

    print(np.shape(img))

    h = 0
    segment_no = 0
    while h < height_bottom:
        segment_range = {}

        segment_range['top'] = h
        segment_range['bottom'] = h + segment_size if h + segment_size <= height_bottom else height_bottom
        segment_img = img[segment_range['top']:segment_range['bottom'], :, :]
        cv2.imwrite(os.path.join(img_output_path, str(segment_no) + '.png'), segment_img)

        h += segment_size
        segment_no += 1

        if show:
            cv2.imshow('img', segment_img)
            cv2.waitKey(0)


def segment_label(segment_size, label_name=0, label_root_path="D:\datasets\dataset_webpage\data\segment\label"):
    label_path = os.path.join(label_root_path, str(label_name))
    org_label_path = os.path.join(label_path, 'org.csv')
    segment_label_path = os.path.join(label_path, 'segment.csv')

    # read the original label
    org_label = pd.read_csv(org_label_path, index_col=0)

    # initialize the segment labels by adding segment_no column and changing the relative label coordinate
    colums = org_label.columns.values
    colums = np.append(colums, ['segment_no'])
    segment_label = pd.DataFrame(columns=colums)

    for i in range(len(org_label)):
        item = org_label.iloc[i].copy()
        segment_no = int(item.by / segment_size)
        item['by'] = item.by % segment_size
        item['segment_no'] = segment_no

        segment_label.loc[i] = item

    segment_label.to_csv(segment_label_path)


def segment_draw_label_by_no(img_root_path, label_root_path, name=0, show=True):

    img_path = os.path.join(img_root_path, str(name))
    input_path = os.path.join(img_path, 'segment')
    output_path = os.path.join(img_path, 'labeled')
    label_path = os.path.join(label_root_path, str(name) + '\\segment.csv')

    label = pd.read_csv(label_path)

    for s in range(label.iloc[-1].segment_no + 1):
        seg_input_path = os.path.join(input_path, str(s) + '.png')
        seg_output_path = os.path.join(output_path, str(s) + '.png')
        seg_img = cv2.imread(seg_input_path)
        seg_label = label[label['segment_no'] == s]

        sd.label(seg_label, seg_img, seg_output_path, show)