import cv2
import json
import numpy as np
from random import randint as rint
import os
from os.path import join as pjoin


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


def draw_node(node, board, layer_count, shrink_ratio=4):

    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, -1)
    cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    print(node['bounds'], node['bounds'][2] - node['bounds'][0], node['bounds'][3] - node['bounds'][1])
    cv2.imshow('board', shrink(board, shrink_ratio))
    cv2.waitKey()
    layer_count += 1

    if 'children' not in node:
        return layer_count
    for child in node['children']:
        layer_count = draw_node(child, board, layer_count)
    return layer_count


if '__main__':
    save = True
    show = False
    start = 7681  # start point
    end = 100000
    img_root = 'E:\\Mulong\\Datasets\\rico\\combined\\'
    json_root = 'E:\\Temp\\rico-tree\\'
    for index in range(start, end):
        img_path = img_root + str(index) + '.jpg'
        json_path = json_root + str(index) + '.json'

        if not os.path.exists(json_path):
            continue
        img = cv2.imread(img_path)
        tree = json.load(open(json_path, encoding="utf8"))

        org = cv2.resize(img, (1440, 2560))
        board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
        draw_node(tree, board, 0)

