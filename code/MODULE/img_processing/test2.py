import cv2
import numpy as np
import time


def neighbor(img, x, y, mark, stack):
    for i in range(x - 1, x + 2):
        if i < 0 or i >= img.shape[0]: continue
        for j in range(y - 1, y + 2):
            if j < 0 or j >= img.shape[1]: continue
            if img[i, j] == 255 and mark[i, j] == 0:
                stack.append([i, j])
                mark[i, j] = 255


def bfs_connected_area(img, x, y, mark):
    stack = [[x, y]]    # points waiting for inspection
    area = [[x, y]]   # points of this area
    mark[x, y] = 255    # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        area.append(point)
        neighbor(img, point[0], point[1], mark, stack)
    return area


def draw_boundary(boundary, broad):
    # up and bottom: (column_index, min/max row border)
    for point in boundary[0] + boundary[1]:
        broad[point[1], point[0]] = 255
    # left, right: (row_index, min/max column border)
    for point in boundary[2] + boundary[3]:
        broad[point[0], point[1]] = 255


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


# detect if it is rectangle by evenness of each border
def is_rectangle(boundary, thresh=0.9):

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

    return True


def scan(img):
    mark = np.full(img.shape, 0, dtype=np.uint8)
    wire = mark.copy()
    row, column = img.shape[0], img.shape[1]

    for i in range(row):
        for j in range(column):
            if img[i, j] == 255 and mark[i, j] == 0:
                area = bfs_connected_area(img, i, j, mark)
                boundary = get_boundary(area)
                if is_rectangle(boundary):
                    draw_boundary(boundary, wire)

                # cv2.imshow('org', img)
                # cv2.imshow('mark', mark)
    cv2.imshow('boundary', wire)
    cv2.waitKey(0)


img = cv2.imread('c_close.png')
img = img[: 600, :]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
bin_copy = bin.copy()

s = time.clock()
scan(bin_copy)
print(time.clock() - s)