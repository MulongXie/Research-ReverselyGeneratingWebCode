import json
from random import randint as rint
import cv2
import numpy as np

from lib_ip.Bbox import Bbox


def load_tree(file_path):
    root = json.load(open(file_path, encoding="utf8"))
    return root


def draw_tree(node, board, node_count, line=-1):
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, line)
    cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    # print(node['bounds'], node['bounds'][2] - node['bounds'][0], node['bounds'][3] - node['bounds'][1])

    if 'children' not in node:
        return node_count
    for child in node['children']:
        node_count = draw_tree(child, board, node_count)
    return node_count


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


class Tree:
    def __init__(self):
        self.class_name = None
        self.bounds = None
        self.children = None
        self.parent = None
