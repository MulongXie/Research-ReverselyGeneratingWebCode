import json
from random import randint as rint
import cv2

from lib_ip.Bbox import Bbox


def load_tree(file_path):
    root = json.load(open(file_path, encoding="utf8"))
    return root


def draw_tree(node, board, node_count):
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, -1)
    cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    # print(node['bounds'], node['bounds'][2] - node['bounds'][0], node['bounds'][3] - node['bounds'][1])

    if 'children' not in node:
        return node_count
    for child in node['children']:
        node_count = draw_tree(child, board, node_count)
    return node_count


