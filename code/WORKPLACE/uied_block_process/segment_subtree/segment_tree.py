import cv2
import json
import numpy as np
import os

import segment_subtree.Detected_Block as Block
import segment_subtree.Tree as Tree
import lib_ip.ip_draw as draw
import lib_ip.ip_preprocessing as pre
from lib_ip.Bbox import Bbox


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


def resize_block(blocks, det_height, tgt_height, bias):
    for block in blocks:
        block.resize_bbox(det_height, tgt_height, bias)


def check_subtree(block, tree, test=False):
    '''
    relation: -1 : a in b
               0  : a, b are not intersected
               1  : b in a
               2  : a, b are identical or intersected
    '''
    relation = block.relation(tree['bounds'])
    if test:
        print(relation, block.put_bbox(), tree['bounds'])
        board_test_blk = draw.draw_bounding_box(img, [block], line=5)
        board_test_tree = cv2.resize(img, (1440, 2560))
        Tree.draw_tree(tree, board_test_tree, 0, 2)
        cv2.imshow('tree-test', cv2.resize(board_test_tree, (300, 500)))
        cv2.imshow('blk-test', cv2.resize(board_test_blk, (300, 500)))
        cv2.waitKey()

    # block contains tree or block and tree are same
    if relation == 1 or relation == 3:
        return tree
    # non-intersected
    elif relation == 0:
        return None
    # else search children
    else:
        if 'children' not in tree:
            return None
        subtrees = []
        for child in tree['children']:
            subtree = check_subtree(block, child)
            if subtree is not None:
                if type(subtree) is list:
                    subtrees += subtree
                else:
                    subtrees.append(subtree)
        if len(subtrees) > 0:
            return subtrees
        else:
            return None


def segment_subtree(blocks, tree):
    segmented_subtree = {'segments':[]}
    for block in blocks:
        subtree = check_subtree(block, tree)
        if subtree is not None:
            segment = {'block': block.put_bbox(), 'subtree':subtree}
            segmented_subtree['segments'].append(segment)
    return segmented_subtree


if '__main__':
    save = True
    show = True
    start = 27  # start point
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

        img, _ = pre.read_img(img_path, resize_height=2560)
        block_img = cv2.imread(block_root + str(index) + '_blk.png')

        blocks = Block.load_blocks(block_path)
        resize_block(blocks, det_height=800, tgt_height=2560, bias=0)
        board_block = draw.draw_bounding_box(img, blocks, line=5)

        tree = Tree.load_tree(tree_path)
        board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
        Tree.draw_tree(tree, board_tree, 0)

        cv2.imshow('blk_img', cv2.resize(block_img, (300, 500)))
        cv2.imshow('block', cv2.resize(board_block, (300, 500)))
        cv2.imshow('tree', cv2.resize(board_tree, (300, 500)))
        cv2.waitKey()
        cv2.destroyAllWindows()

        seg_subtrees = segment_subtree(blocks, tree)
        print(seg_subtrees)

        jfile = open('subtrees.json', 'w')
        json.dump(seg_subtrees, jfile, indent=4)
        print('write to subtrees.json')
        break
