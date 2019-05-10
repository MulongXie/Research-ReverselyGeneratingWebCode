import cv2
import numpy as np
import os
import pandas as pd


def split_img(img_root_path = "D:\datasets\dataset_webpage\data\split\img"):
    img_name = 0
    img_path = os.path.join(img_root_path, str(img_name))
    img_input_path = os.path.join(img_path, 'org.png')
    img_output_path = os.path.join(img_path, 'section')

    height_avg = 600

    print(img_input_path)

    img = cv2.imread(img_input_path)
    height_bottom = np.shape(img)[0]

    print(np.shape(img))

    h = 0
    section_no = 0
    while h < height_bottom:
        section_range = {}

        section_range['top'] = h
        section_range['bottom'] = h + height_avg if h + height_avg <= height_bottom else height_bottom
        section_img = img[section_range['top']:section_range['bottom'], :, :]
        cv2.imwrite(os.path.join(img_output_path, str(section_no) + '.png'), section_img)

        h += height_avg
        section_no += 1

        cv2.imshow('img', section_img)
        cv2.waitKey(0)


def split_label(label_root_path="D:\datasets\dataset_webpage\data\split\label"):
    label_name = 0
    label_path = os.path.join(label_root_path, str(label_name))
    org_label_path = os.path.join(label_path, 'org.csv')
    split_label_path = os.path.join(label_path, 'split.csv')

    label = pd.read_csv(org_label_path, index_col=0)
    avg_height = 600

    colums = label.columns.values
    colums = np.append(colums, ['split_no'])

    split_label = pd.DataFrame(columns=colums)
    for i in range(len(label)):
        item = label.iloc[i].copy()

        split_no = int(item.by / avg_height)
        item['by'] = item.by % avg_height
        item['split_no'] = split_no

        split_label.loc[i] = item

    print(split_label)
    split_label.to_csv(split_label_path)


split_img()
split_label()