import cv2
import numpy as np
from collections import Counter

import ip_draw as draw


def neighbor(img, x, y, mark, stack):
    for i in range(x - 1, x + 2):
        if i < 0 or i >= img.shape[0]: continue
        for j in range(y - 1, y + 2):
            if j < 0 or j >= img.shape[1]: continue
            if img[i, j] == 255 and mark[i, j] == 0:
                stack.append([i, j])
                mark[i, j] = 255


def is_line(boundary, thresh=3):
    # up and bottom
    difference = [abs(boundary[0][i][1] - boundary[1][i][1]) for i in range(len(boundary[1]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < thresh:
        return True
    # left and right
    difference = [abs(boundary[2][i][1] - boundary[3][i][1]) for i in range(len(boundary[2]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < thresh:
        return True

    return False


# detect if it is rectangle by evenness of each border
def is_rectangle(boundary, thresh):

    # up, bottom: (column_index, min/max row border)
    # left, right: (row_index, min/max column border)
    for border in boundary:
        # calculate the evenness of each border
        evenness = 0
        for i in range(len(border) - 1):
            if border[i][1] - border[i + 1][1] == 0:
                evenness += 1
        if evenness / len(border) < thresh:
            return False
        if is_line(boundary):
            return False

    return True




def bfs_connected_area(img, x, y, mark):
    stack = [[x, y]]    # points waiting for inspection
    area = [[x, y]]   # points of this area
    mark[x, y] = 255    # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        area.append(point)
        neighbor(img, point[0], point[1], mark, stack)
    return area


def get_boundary(area):
    border_up, border_bottom, border_left, border_right = ({}, {}, {}, {})
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
    for i in range(len(boundary)):
        boundary[i] = sorted(boundary[i].items(), key=lambda x: x[0])

    return boundary


def get_corner(boundaries):
    corners = []
    for bounary in boundaries:
        up_left = (bounary[0][0][0], bounary[2][0][0])
        bottom_right = (bounary[1][-1][0], bounary[3][-1][0])
        corners.append((up_left, bottom_right))
    return corners


# take the binary image as input
def rectangle_detection(bin, min_evenness=0.9, min_area=400):
    mark = np.full(bin.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    row, column = bin.shape[0], bin.shape[1]

    broad = np.zeros(bin.shape, dtype=np.uint8)  # binary broad

    for i in range(row):
        for j in range(column):
            if bin[i, j] == 255 and mark[i, j] == 0:
                area = bfs_connected_area(bin, i, j, mark)
                print(len(area))
                if len(area) > min_area:
                    boundary = get_boundary(area)
                    boundary_all.append(boundary)
                    if is_rectangle(boundary, min_evenness):
                        boundary_rec.append(boundary)

                    draw.draw_boundary(boundary, broad)
                    cv2.imshow('bon', broad)
                    cv2.waitKey(0)

    return boundary_all, boundary_rec


