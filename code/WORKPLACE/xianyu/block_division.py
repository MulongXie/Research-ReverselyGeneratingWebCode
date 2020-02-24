import cv2
import numpy as np
from random import randint as rint
import time


def draw_region(region, broad, show=False):
    color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        broad[point[0], point[1]] = color

    if show:
        cv2.imshow('region', broad)
        cv2.waitKey()
    return broad


def block_division(grey, show=False, write_path=None,
                   grad_thresh=8):
    '''
    :param grey: grey-scale of original image
    :return: corners: list of [(top_left, bottom_right)]
                        -> top_left: (column_min, row_min)
                        -> bottom_right: (column_max, row_max)
    '''

    def flood_fill_bfs(img, x_start, y_start, mark):
        '''
        Identify the connected region based on the background color
        :param img: grey-scale image
        :param x_start: row coordinate of start position
        :param y_start: column coordinate of start position
        :param mark: record passed points
        :return: region: list of connected points
        '''

        def neighbor(x, y):
            for i in range(x - 1, x + 2):
                if i < 0 or i >= img.shape[0]: continue
                for j in range(y - 1, y + 2):
                    if j < 0 or j >= img.shape[1]: continue
                    if mark[i, j] == 0 and abs(img[i, j] - img[x, y]) < grad_thresh:
                        stack.append([i, j])
                        mark[i, j] = 255

        stack = [[x_start, y_start]]  # points waiting for inspection
        region = [[x_start, y_start]]  # points of this connected region
        mark[x_start, y_start] = 255  # drawing broad
        while len(stack) > 0:
            point = stack.pop()
            region.append(point)
            neighbor(point[0], point[1])
        return region

    blocks_corner = []
    mask = np.zeros((grey.shape[0], grey.shape[1]), dtype=np.uint8)
    broad = np.zeros((grey.shape[0], grey.shape[1], 3), dtype=np.uint8)

    row, column = grey.shape[0], grey.shape[1]
    for x in range(row):
        for y in range(column):
            if mask[x, y] == 0:
                region = flood_fill_bfs(grey, x, y, mask)
                # ignore small regions
                if len(region) < 500:
                    continue
                draw_region(region, broad)
    if show:
        cv2.imshow('block', broad)
        cv2.waitKey()
    if write_path is not None:
        cv2.imwrite(write_path, broad)
    return blocks_corner
