import os
import pandas as pd
import json
from os.path import join as pjoin
import time
import cv2


def save_corners(file_path, corners, compo_name, clear=True):
    try:
        df = pd.read_csv(file_path, index_col=0)
    except:
        df = pd.DataFrame(columns=['component', 'x_max', 'x_min', 'y_max', 'y_min', 'height', 'width'])

    if clear:
        df = df.drop(df.index)
    for corner in corners:
        (up_left, bottom_right) = corner
        c = {'component': compo_name}
        (c['y_min'], c['x_min']) = up_left
        (c['y_max'], c['x_max']) = bottom_right
        c['width'] = c['y_max'] - c['y_min']
        c['height'] = c['x_max'] - c['x_min']
        df = df.append(c, True)
    df.to_csv(file_path)


def save_corners_json(file_path, corners, compo_classes):
    try:
        f_in = open(file_path, 'r')
        components = json.load(f_in)
    except:
        components = {'compos': []}
    f_out = open(file_path, 'w')

    for i in range(len(corners)):
        (up_left, bottom_right) = corners[i]
        c = {'id': i, 'class': compo_classes[i]}
        (c['column_min'], c['row_min']) = up_left
        (c['column_max'], c['row_max']) = bottom_right
        c['width'] = c['column_max'] - c['column_min']
        c['height'] = c['row_max'] - c['row_min']
        components['compos'].append(c)

    json.dump(components, f_out, indent=4)


def save_clipping(org, output_root, corners, compo_classes):
    if not os.path.exists(output_root):
        os.mkdir(output_root)
    for i in range(len(corners)):
        compo = compo_classes[i]
        path = pjoin(output_root, compo)
        (up_left, bottom_right) = corners[i]
        (col_min, row_min) = up_left
        (col_max, row_max) = bottom_right
        if not os.path.exists(path):
            os.mkdir(path)
        clip = org[row_min:row_max, col_min:col_max]
        cv2.imwrite(pjoin(path, str(i) + '.png'), clip)


def timer(start):
    now = time.clock()
    print('Time Taken:%.3f s' % (now - start))
    return now
