import numpy as np
import cv2
from random import randint as rint
from os.path import join as pjoin


def generate_parameters():
    offset = min_block_edge + 5
    corner_top = rint(offset, img_height - offset)
    corner_left = rint(offset, img_width - offset)
    height = rint(min_block_edge, img_height - corner_top)
    width = rint(min_block_edge, img_width - corner_left)
    corner_bottom = corner_top + height
    corner_right = corner_left + width
    return corner_top, corner_left, corner_bottom, corner_right


def generate_blocks(blocks_number):
    def is_overlap(b):
        for a in blocks:
            # calculate the intersected area between b and all other blocks
            col_min_s = max(a[0], b[0])
            row_min_s = max(a[1], b[1])
            col_max_s = min(a[2], b[2])
            row_max_s = min(a[3], b[3])
            w = np.maximum(0, col_max_s - col_min_s + 10)
            h = np.maximum(0, row_max_s - row_min_s + 10)
            if w * h != 0:
                return True
        return False

    blocks = []
    for i in range(blocks_number):
        block = generate_parameters()
        while is_overlap(block):
            block = generate_parameters()
        blocks.append(block)
    return blocks


def draw_blocks(blocks, is_show=False, is_write=False, output='E:\\Mulong\Datasets\\fake_shapes'):
    f = open('label.txt', 'a')
    f.write(output + ' ')

    board = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    for block in blocks:
        cv2.rectangle(board, (block[1], block[0]), (block[3], block[2]), (255,255,255), -1)
        f.write(str(block[1]) + ',' + str(block[0]) + ',' + str(block[2]) + str(block[3]) + ',0 ')

        if is_show:
            cv2.imshow('img', board)
            cv2.waitKey()
    if is_write:
        cv2.imwrite(pjoin(output, str(index) + '.png'), board)
    f.write('\n')


img_height = 600
img_width = 800
min_block_edge = 15
img_number = 40

for index in range(img_number):
    bs = generate_blocks(rint(2, 6))
    draw_blocks(bs, is_write=True)
