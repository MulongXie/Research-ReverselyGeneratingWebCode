import cv2
import numpy as np
from random import randint as rint
import time

import lib_uied.ip_preprocessing as pre
import lib_uied.ip_detection_utils as util
import lib_uied.ip_detection as det
import lib_uied.ip_draw as draw
import lib_uied.ip_segment as seg


def draw_region(region, broad):
    color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        broad[point[0], point[1]] = color


def shrink(img, ratio=3.5):
    img_shrink = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))
    return img_shrink


def block_division(grey, show=False):
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
                    if mark[i, j] == 0 and abs(img[i, j] - img[x, y]) < 8:
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

    blocks = []
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
                # get the boundary of this region
                boundary = util.boundary_get_boundary(region)
                # ignore lines
                if util.boundary_is_line(boundary, 5):
                    continue
                # ignore non-rectangle as blocks must be rectangular
                if not util.boundary_is_rectangle(boundary, 0.66, 0.25):
                    continue
                blocks.append(boundary)
                draw_region(region, broad)
    if show:
        cv2.imshow('broad', broad)
        cv2.waitKey()

    blocks_corner = det.get_corner(blocks)
    return blocks_corner


def block_clip(org, blocks_corner):
    blocks_clip = seg.clipping(org, blocks_corner, True)
    return blocks_clip


def main():
    org = cv2.imread('data/4.jpg')
    org = shrink(org)
    grey = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)

    blocks_corner = block_division(grey, show=True)
    blocks_clip = block_clip(org, blocks_corner)


if __name__ == '__main__':
    start = time.clock()
    main()
    print(time.clock() - start)