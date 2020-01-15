import json
import cv2
import numpy as np
from random import randint as rint


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1]/ratio), int(img.shape[0]/ratio)))


objects = json.load(open('objects.json'))
board = np.zeros((2560, 1440, 3), dtype=np.uint8)
img = cv2.imread('0.jpg')
img = cv2.resize(img, (1440, 2560))

for obj in objects:
    print(obj)
    color = (rint(0,255), rint(0,255), rint(0,255))

    cv2.rectangle(board, (obj['rel-bounds'][0], obj['rel-bounds'][1]), (obj['rel-bounds'][2], obj['rel-bounds'][3]), color, -1)
    board_show = shrink(board, 3)
    cv2.imshow('board_show', board_show)
    cv2.waitKey()