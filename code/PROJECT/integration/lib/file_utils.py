import os
import pandas as pd
import json
import time


def build_output_folders(C):
    if not os.path.exists(C.ROOT_LABEL):
        os.mkdir(C.ROOT_LABEL)
    if not os.path.exists(C.ROOT_IMG_DRAWN):
        os.mkdir(C.ROOT_IMG_DRAWN)
    if not os.path.exists(C.ROOT_IMG_GRADIENT):
        os.mkdir(C.ROOT_IMG_GRADIENT)
    if not os.path.exists(C.ROOT_IMG_GRADIENT_NO_LINE):
        os.mkdir(C.ROOT_IMG_GRADIENT_NO_LINE)
    if not os.path.exists(C.ROOT_IMG_CLEAN):
        os.mkdir(C.ROOT_IMG_CLEAN)
    if not os.path.exists(C.ROOT_IMG_SEGMENT):
        os.mkdir(C.ROOT_IMG_SEGMENT)


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


def save_corners_json(file_path, corners, compo_name):
    if os.path.exists(file_path):
        f_in = open(file_path, 'r')
        components = json.load(f_in)
    else:
        components = {'compos': []}
    f_out = open(file_path, 'w')

    for corner in corners:
        (up_left, bottom_right) = corner
        c = {'component': compo_name}
        (c['column_min'], c['row_min']) = up_left
        (c['column_max'], c['row_max']) = bottom_right
        c['width'] = c['column_max'] - c['column_min']
        c['height'] = c['row_max'] - c['row_min']
        components['compos'].append(c)

    print(components)
    json.dump(components, f_out)


def timer(start):
    now = time.clock()
    print('Time Taken:%.3f s' % (now - start))
    return now
