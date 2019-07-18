import cv2
import numpy as np


def get_most_value(array):
    array = np.reshape(array, (np.shape(array)[0] * np.shape(array)[1]))
    most = np.bincount(array).argmax()
    return most


def html_color(component):
    b = component[:, :, 0]
    g = component[:, :, 1]
    r = component[:, :, 2]
    b_most = get_most_value(r)
    g_most = get_most_value(g)
    r_most = get_most_value(b)

    print(b_most, g_most, r_most)


img = cv2.imread('input/c.png')
html_color(img)
