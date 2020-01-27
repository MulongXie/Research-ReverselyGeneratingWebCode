import cv2
import numpy as np
from random import randint as rint
import time

import ip_preprocessing as pre
import ip_detection_utils as util
import ip_detection as det
import ip_draw as draw


def draw_region(region, broad):
    color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        broad[point[0], point[1]] = color


def shrink(img, ratio=3.5):
    img_shrink = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))
    return img_shrink


def flood_fill_bfs(img, x_start, y_start, mark):
    def neighbor(x, y):
        for i in range(x - 1, x + 2):
            if i < 0 or i >= img.shape[0]: continue
            for j in range(y - 1, y + 2):
                if j < 0 or j >= img.shape[1]: continue
                if mark[i, j] == 0 and abs(img[i, j] - img[x, y]) < 8:
                    stack.append([i, j])
                    mark[i, j] = 255

    stack = [[x_start, y_start]]  # points waiting for inspection
    region = [[x_start, y_start]]   # points of this connected region
    mark[x_start, y_start] = 255  # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        region.append(point)
        neighbor(point[0], point[1])
    return region


def block_division(org, grey):
    blocks = []
    mask = np.zeros((org.shape[0], org.shape[1]), dtype=np.uint8)
    broad = np.zeros((org.shape[0], org.shape[1], 3), dtype=np.uint8)

    row, column = org.shape[0], org.shape[1]
    for x in range(row):
        for y in range(column):
            if mask[x, y] == 0:
                region = flood_fill_bfs(grey, x, y, mask)
                if len(region) < 500:
                    continue

                boundary = util.boundary_get_boundary(region)
                if util.boundary_is_line(boundary, 5):
                    continue
                if not util.boundary_is_rectangle(boundary, 0.66, 0.1):
                    continue
                else:
                    draw.draw_boundary([boundary], org.shape, show=True)

                blocks.append(boundary)
                draw_region(region, broad)
                cv2.imshow('broad', broad)
                cv2.waitKey()

    blocks_corner = det.get_corner(blocks)
    cv2.imshow('broad', broad)
    cv2.waitKey()

    return blocks_corner


start = time.clock()

org = cv2.imread('2.jpg')
org = shrink(org)
grey = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
binary = pre.preprocess(grey)

block_division(org, grey)

print(time.clock() - start)
