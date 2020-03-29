import json
from random import randint as rint
import cv2
import numpy as np

import lib_ip.ip_draw as draw
from lib_ip.Bbox import Bbox


def load_tree(file_path):
    root = json.load(open(file_path, 'r', encoding="utf8"))
    return root


def draw_tree(node, board, line=-1):
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, line)
    cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    # print(node['bounds'], node['bounds'][2] - node['bounds'][0], node['bounds'][3] - node['bounds'][1])

    if 'children' not in node:
        return
    for child in node['children']:
        draw_tree(child, board)


def draw_single_node(root):
    nodes = [root]
    while len(nodes) > 0:
        node = nodes.pop()
        board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
        draw_tree(node, board_tree, 0)
        cv2.imshow('tree', cv2.resize(board_tree, (300, 500)))
        cv2.waitKey()
        if 'children' in node:
            nodes += node['children']


def view_segments(segments, org):
    for segment in segments['segments']:
        block = segment['block']
        subtrees = segment['subtree']

        board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
        for subtree in subtrees:
            draw_tree(subtree, board_tree)

        board_block = draw.draw_bounding_box(org, [Bbox(block[0], block[1], block[2], block[3])], line=5)
        cv2.imshow('seg_block', cv2.resize(board_block, (300, 500)))
        cv2.imshow('seg_tree', cv2.resize(board_tree, (300, 500)))
        cv2.waitKey()


class Tree:
    def __init__(self):
        self.class_name = None
        self.bounds = None
        self.children = None
        self.parent = None
