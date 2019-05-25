import cv2
import numpy as np


def count_column(img, mask, a, b, height):
    count = 0
    for i in range(a+1, a+height):
        if img[i, b] == 255 and mask[i, b] == 0:
            count += 1
            mask[i, b] = 255

    return count


def count_row(img, mask, a, b, width):
    count = 0
    for j in range(b+1, b+width):
        if img[a, j] == 255 and mask[a, j] == 0:
            count += 1
            mask[a, j] = 255
    return count


def check_rec(img, mask, x, y):
    check_row = True
    check_column = True
    width = 1
    height = 1
    i = 1
    j = 1
    while check_row or check_column:
        cc = count_column(img, mask, x, y + j, height)
        cr = count_row(img, mask, x + i, y, width)
        if cc / height < 0.3:
            check_column = False
        else:
            height += 1
        if cr / width < 0.3:
            check_row = False
        else:
            width += 1
    print('width:%d height:%d ' %(width, height))


def locate_point(img):
    mask = np.zeros(img.shape, dtype=np.uint8)
    row = img.shape[0]
    column = img.shape[1]
    for i in range(row):
        for j in range(column):
            if img[i, j] == 255 and mask[i, j] == 0:
                check_rec(img, mask, i, j)


img = np.zeros((600, 600), dtype=np.uint8)
img[30:70, 200:320] = 255

locate_point(img)

cv2.imshow('img', img)
cv2.waitKey(0)