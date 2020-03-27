import cv2
import json
import numpy as np
import os

import segment_subtree.Detected_Block as Block
import lib_ip.ip_draw as draw
import lib_ip.ip_preprocessing as pre


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


if '__main__':
    save = True
    show = True
    start = 0  # start point
    end = 100000
    img_root = 'E:\\Mulong\\Datasets\\rico\\combined\\'
    json_root = 'E:\\Temp\\rico-block\\'
    for index in range(start, end):
        img_path = img_root + str(index) + '.jpg'
        json_path = json_root + str(index) + '.json'

        if not os.path.exists(json_path):
            continue

        img, _ = pre.read_img(img_path, resize_height=800)
        blocks = Block.load_blocks(json_path)

        draw.draw_bounding_box(img, blocks, show=show)
