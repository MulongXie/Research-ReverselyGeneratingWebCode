import cv2
import numpy as np
from random import randint as rint
import time

import lib_ip.ip_draw as draw
import lib_ip.ip_segment as seg
from lib_ip.Block import Block
from config.CONFIG_UIED import Config
C = Config()


def block_hierarchy(blocks):
    for i in range(len(blocks) - 1):
        for j in range(i + 1, len(blocks)):
            relation = blocks[i].compo_relation(blocks[j])
            # j contains i
            if relation == -1:
                # add j's children
                blocks[j].children.append(i)
                # set i's parent
                blocks[i].layer += 1
                if blocks[i].parent is None:
                    blocks[i].parent = j
                else:
                    # set the closest container as parent
                    if j in blocks[blocks[i].parent].children:
                        blocks[i].parent = j

            # i contains j
            elif relation == 1:
                # add i'children
                blocks[i].children.append(j)
                # set j's parent
                blocks[j].layer += 1
                if blocks[j].parent is None:
                    blocks[j].parent = i
                else:
                    # set the closest container as parent
                    if i in blocks[blocks[j].parent].children:
                        blocks[j].parent = i

    layers = {}
    for i in range(len(blocks)):
        if blocks[i].layer not in layers:
            layers[str(blocks[i].layer)] = [i]
        else:
            layers[str(blocks[i].layer)].append(i)
    return layers


def block_filter(blocks, img_shape):
    blocks_new = []
    for block in blocks:
        # filter
        if block.block_is_top_or_bottom_bar(img_shape, C.THRESHOLD_TOP_BOTTOM_BAR) or \
                block.block_is_uicompo(img_shape, C.THRESHOLD_COMPO_MAX_SCALE) or \
                block.height < 40 and block.width < 40:
            continue
        blocks_new.append(block)
    return blocks_new


def block_add_bkg(blocks, org, img_shape, show=False):
    board = np.full(img_shape[:2], 255, dtype=np.uint8)
    for block in blocks:
        block.block_fill_color(board, 0, flag='bbox')

    blocks_bkg = block_division(board, is_background=True)

    if show:
        ratio = 2
        board_bkg = draw.draw_bounding_box(org, blocks_bkg, name='block_bkg')
        cv2.imshow('bkg_board', cv2.resize(board_bkg, (int(board_bkg.shape[1]/ratio), int(board_bkg.shape[0]/ratio))))
        cv2.imshow('filled_board', cv2.resize(board, (int(board.shape[1]/ratio), int(board.shape[0]/ratio))))
        cv2.waitKey()

    return blocks_bkg + blocks


def block_division(grey, step_h=10, step_v=10, is_background=False,
                   grad_thresh=C.THRESHOLD_BLOCK_GRADIENT,
                   line_thickness=C.THRESHOLD_LINE_THICKNESS,
                   min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS,
                   max_dent_ratio=C.THRESHOLD_REC_MAX_DENT_RATIO):
    '''
    :param grey: grey-scale of original image
    :return: corners: list of [(top_left, bottom_right)]
                        -> top_left: (column_min, row_min)
                        -> bottom_right: (column_max, row_max)
    '''
    blocks = []
    mask = np.zeros((grey.shape[0]+2, grey.shape[1]+2), dtype=np.uint8)

    row, column = grey.shape[0], grey.shape[1]
    for x in range(0, row, step_h):
        for y in range(0, column, step_v):
            if is_background and grey[x, y] == 0:
                continue
            if mask[x, y] == 0:
                # region = flood_fill_bfs(grey, x, y, mask)

                # flood fill algorithm to get background (layout block)
                mask_copy = mask.copy()
                cv2.floodFill(grey, mask, (y,x), None, grad_thresh, grad_thresh, cv2.FLOODFILL_MASK_ONLY)
                mask_copy = mask - mask_copy
                region = np.nonzero(mask_copy[1:-1, 1:-1])
                region = list(zip(region[0], region[1]))

                # ignore small regions
                if len(region) < 500:
                    continue
                block = Block(region, grey.shape)

                # get the boundary of this region
                # ignore lines
                if block.compo_is_line(line_thickness):
                    continue
                # ignore non-rectangle as blocks must be rectangular
                if not is_background and not block.compo_is_rectangle(min_rec_evenness, max_dent_ratio):
                    continue

                blocks.append(block)
    return blocks
