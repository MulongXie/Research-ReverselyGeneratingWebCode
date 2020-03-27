import cv2
import json
import numpy as np
import os

import segment_subtree.Detected_Block as Block
import segment_subtree.Tree as Tree
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
    block_root = 'E:\\Temp\\rico-block\\'
    tree_root = 'E:\\Temp\\rico-tree\\'
    for index in range(start, end):
        img_path = img_root + str(index) + '.jpg'
        block_path = block_root + str(index) + '.json'
        tree_path = tree_root + str(index) + '.json'

        if not os.path.exists(block_path) or not os.path.exists(tree_path):
            continue

        img, _ = pre.read_img(img_path, resize_height=800)
        blocks = Block.load_blocks(block_path)
        board_block = draw.draw_bounding_box(img, blocks)

        tree = Tree.load_tree(tree_path)
        board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
        Tree.draw_tree(tree, board_tree, 0)

        block_img = cv2.imread(block_root + str(index) + '_blk.png')
        cv2.imshow('blk_img', cv2.resize(block_img, (300, 500)))
        cv2.imshow('block', cv2.resize(board_block, (300, 500)))
        cv2.imshow('tree', cv2.resize(board_tree, (300, 500)))
        cv2.waitKey()