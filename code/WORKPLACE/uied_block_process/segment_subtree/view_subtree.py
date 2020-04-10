import json
import cv2
import numpy as np
from random import randint as rint
from os.path import join as pjoin
import os


def draw_tree(tree, board, line=-1):
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (tree['bounds'][0], tree['bounds'][1]), (tree['bounds'][2], tree['bounds'][3]), color, line)
    if 'children' not in tree:
        return
    for child in tree['children']:
        draw_tree(child, board)


def view_segments(segments, org):
    for segment in segments['segments']:
        block = segment['block']
        subtrees = segment['subtree']

        board_block = org.copy()
        board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
        for subtree in subtrees:
            draw_tree(subtree, board_tree)

        cv2.rectangle(board_block, (block[0], block[1]), (block[2], block[3]), (0,255,0), 5)
        cv2.imshow('seg_block', cv2.resize(board_block, (300, 500)))
        # cv2.imshow('seg_block', org)
        cv2.imshow('seg_tree', cv2.resize(board_tree, (300, 500)))
        cv2.waitKey()


if __name__ == '__main__':
    show = True
    start = 27  # start point
    end = 100000
    img_root = 'E:\\Mulong\\Datasets\\rico\\combined\\'
    segment_root = 'E:\\Temp\\rico-subtree\\'

    for index in range(start, end):
        img_path = pjoin(img_root, str(index) + '.jpg')
        segment_path = pjoin(segment_root, str(index) + '.json')
        if not os.path.exists(segment_path):
            continue

        print('View:', segment_path)
        segments_tree = json.load(open(segment_path))
        img = cv2.resize(cv2.imread(img_path), (1440, 2560))
        view_segments(segments_tree, img)
