import cv2
import re
import pandas as pd
import numpy as np


def get_most_value(array):
    array = np.reshape(array, (np.shape(array)[0] * np.shape(array)[1]))
    most = np.bincount(array).argmax()
    return most


def color_main(img, block):
    component = img[block['x_min']:block['x_max'], block['y_min']:block['y_max']]
    cv2.imshow('a', component)
    cv2.waitKey(0)
    b = component[:, :, 0]
    g = component[:, :, 1]
    r = component[:, :, 2]
    b_most = get_most_value(r)
    g_most = get_most_value(g)
    r_most = get_most_value(b)

    print(b_most, g_most, r_most)
    pass


def color_surrounding(img, corner, range):
    x_min = corner['x_min'] - range if corner['x_min'] - range >= 0 else 0
    x_max = corner['x_max'] + range if corner['x_max'] + range < img.shape[0] else img.shape[0] - 1
    y_min = corner['y_min'] - range if corner['y_min'] - range >= 0 else 0
    y_max = corner['y_max'] + range if corner['y_max'] + range < img.shape[1] else img.shape[1] - 1

    surrounding = img[x_min:x_max, y_min:y_max]
    cv2.imshow('a', surrounding)
    cv2.waitKey(0)
    pass
    

element = pd.read_csv('corners.csv')
blocks = element[element['component'] == 'div']
img = cv2.imread('10.png')

for i in range(len(blocks)):
    block = blocks.iloc[i]
    color_surrounding(img, block, 10)
