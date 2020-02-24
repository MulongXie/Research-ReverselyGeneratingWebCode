import cv2
import numpy as np
from random import randint as rint
import time


def draw_region(region, board, show=False):
    color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        board[point[0], point[1]] = color

    if show:
        cv2.imshow('region', board)
        cv2.waitKey()
    return board


def boundary_get_boundary(area):
    border_up, border_bottom, border_left, border_right = {}, {}, {}, {}
    for point in area:
        # point: (row_index, column_index)
        # up, bottom: (column_index, min/max row border) detect range of each column
        if point[1] not in border_up or border_up[point[1]] > point[0]:
            border_up[point[1]] = point[0]
        if point[1] not in border_bottom or border_bottom[point[1]] < point[0]:
            border_bottom[point[1]] = point[0]
        # left, right: (row_index, min/max column border) detect range of each row
        if point[0] not in border_left or border_left[point[0]] > point[1]:
            border_left[point[0]] = point[1]
        if point[0] not in border_right or border_right[point[0]] < point[1]:
            border_right[point[0]] = point[1]

    boundary = [border_up, border_bottom, border_left, border_right]
    # descending sort
    for i in range(len(boundary)):
        boundary[i] = [[k, boundary[i][k]] for k in boundary[i].keys()]
        boundary[i] = sorted(boundary[i], key=lambda x: x[0])
    return boundary


ratio = 1

start = time.clock()
img = cv2.imread('a.jpg')
img = cv2.resize(img, (int(img.shape[1]/ratio), int(img.shape[0]/ratio)))
img = cv2.GaussianBlur(img, (3,3), 0)
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(grey, 20, 80)
dilate = cv2.morphologyEx(canny, cv2.MORPH_DILATE, (3,3))

grad_thresh = 0
mk = np.zeros((grey.shape[0]+2, grey.shape[1]+2), dtype=np.uint8)
board = np.zeros((grey.shape[0], grey.shape[1], 3), dtype=np.uint8)
for x in range(0, img.shape[0], 10):
    for y in range(0, img.shape[1], 10):
        # print(x, y)
        if mk[x, y] == 0:
            mk_copy = mk.copy()
            cv2.floodFill(dilate, mk, (y, x), 255, grad_thresh, grad_thresh, cv2.FLOODFILL_MASK_ONLY)
            mk_copy = mk - mk_copy
            region = np.nonzero(mk_copy[1:-1, 1:-1])
            region = list(zip(region[0], region[1]))
            if len(region) < 500:
                continue
            draw_region(region, board)

print(time.clock() - start)
cv2.imshow('bin', dilate)
cv2.imshow('msk', board)
cv2.waitKey()
