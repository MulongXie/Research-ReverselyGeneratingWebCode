import cv2
import numpy as np
from random import randint as rint


def draw_region(region, broad):
    color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        broad[point[0], point[1]] = color


def shrink(img, ratio=3.5):
    img_shrink = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))
    return img_shrink


def valid_block(region):
    if len(region) < 500:
        return False
    return True


def flood_fill_bfs(img, x_start, y_start, mark):
    def neighbor(x, y):
        for i in range(x - 1, x + 2):
            if i < 0 or i >= img.shape[0]: continue
            for j in range(y - 1, y + 2):
                if j < 0 or j >= img.shape[1]: continue
                if mark[i, j] == 0 and abs(img[i, j] - img[x, y]) < 5:
                    stack.append([i, j])
                    mark[i, j] = 255

    stack = [[x_start, y_start]]  # points waiting for inspection
    region = [[x_start, y_start]]   # points of this connected region
    mark[x_start, y_start] = 255  # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        region.append(point)
        neighbor(point[0], point[1])

    if valid_block(region):
        return region
    else:
        return False


org = cv2.imread('4.jpg')
org = shrink(org)
grey = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
mask = np.zeros((org.shape[0], org.shape[1]), dtype=np.uint8)
broad = np.zeros((org.shape[0], org.shape[1], 3), dtype=np.uint8)

row, column = org.shape[0], org.shape[1]

for x in range(row):
    for y in range(column):
        if mask[x, y] == 0:
            region = flood_fill_bfs(grey, x, y, mask)
            if region is not False:
                draw_region(region, broad)


cv2.imshow('org', org)
cv2.imshow('grey', org)
cv2.imshow('broad', broad)
cv2.waitKey()