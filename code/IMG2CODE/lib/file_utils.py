import os
import pandas as pd
import time


def save_corners(file_path, corners, compo_name, clear=True):
    try:
        df = pd.read_csv(file_path, index_col=0)
    except:
        print('No existing csv file')
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


def timer(start):
    now = time.clock()
    print('Time Taken:%.3f s' % (now - start))
    return now
