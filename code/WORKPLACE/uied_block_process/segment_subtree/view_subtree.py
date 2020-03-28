import json
import cv2
import numpy as np
from random import randint as rint


def draw_tree(tree, board, line=-1):
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (tree['bounds'][0], tree['bounds'][1]), (tree['bounds'][2], tree['bounds'][3]), color, line)
    # cv2.putText(board, tree['class'], (int((tree['bounds'][0] + tree['bounds'][2]) / 2) - 50, int((tree['bounds'][1] + tree['bounds'][3]) / 2)),
    #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    if 'children' not in tree:
        return
    for child in tree['children']:
        draw_tree(child, board)


if __name__ == '__main__':
    show = True
    start = 27  # start point
    end = 100000
    img_root = 'E:\\Mulong\\Datasets\\rico\\combined\\'
    segment_root = 'E:\\Temp\\rico-subtree'
    segments = json.load(open('subtrees.json'))['segments']
    # for index in range(start, end):
    for segment in segments:
        block = segment['block']
        subtrees = segment['subtree']

        if show:
            board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
            for subtree in subtrees:
                draw_tree(subtree, board_tree)
            cv2.imshow('tree', cv2.resize(board_tree, (300, 500)))
            cv2.waitKey()