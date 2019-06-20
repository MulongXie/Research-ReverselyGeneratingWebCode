import cv2
import numpy as np


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


def scan(img):
    mark = np.full(img.shape, 0, dtype=np.uint8)
    row, column = img.shape[0], img.shape[1]

    areas = []
    for i in range(row):
        for j in range(column):
            if img[i, j] == 255 and mark[i, j] == 0:
                area = bfs_connected_area(img, i, j, mark)
                areas.append(area)
                cv2.imshow('mark', mark)
                cv2.waitKey(0)
                print(area)


# img = np.zeros((600, 600, 3), dtype=np.uint8)
# img[30:50, 30:50, :] = 255
# img[90:138, 50:76, :] = 255
# img[100:103, 66:70] = 0
# img[220: 230, :, :] = 255

img = cv2.imread('c_close.png')
img = img[600: 1200, :]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
bin_copy = bin.copy()

cv2.imshow('img', bin_copy)

scan(bin_copy)
