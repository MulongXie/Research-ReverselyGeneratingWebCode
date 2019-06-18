import cv2
import numpy as np


def is_truncation(img, direction, x, y, para):
    (u, d, l, r) = para
    trun = 0
    # calculate the truncation
    if direction == 'up':
        trun = img[x - u, y - l: y + r + 1] - img[x - u - 1, y - l: y + r + 1]
    elif direction == 'down':
        trun = img[x + d, y - l: y + r + 1] - img[x + d + 1, y - l: y + r + 1]
    elif direction == 'left':
        trun = img[x - u: x + d + 1, y - l] - img[x - u: x + d + 1, y - l - 1]
    elif direction == 'right':
        trun = img[x - u: x + d + 1, y + r] - img[x - u: x + d + 1, y + r + 1]

    trun = int (np.sum(trun) / 255)
    print(direction)
    print("truncation:", trun)
    print(para, '\n')
    return trun


def is_rec(img, mask, x, y):
    # diffuse towards four directions
    up, down, left, right = (0, 0, 0, 0)
    is_trun_up, is_trun_down, is_trun_left, is_trun_right = (False, False, False, False)
    t_up, t_dowm, t_left, t_right = (1, 1, 1, 1)

    width = left + right + 1
    height = up + down + 1
    while not (is_trun_up and is_trun_down and is_trun_left and is_trun_right):
        width = left + right + 1
        height = up + down + 1
        if not is_trun_up:
            t_up = is_truncation(img, 'up', x, y, (up, down, left, right))
        if not is_trun_down:
            t_dowm = is_truncation(img, 'down', x, y, (up, down, left, right))
        if not is_trun_left:
            t_left = is_truncation(img, 'left', x, y, (up, down, left, right))
        if not is_trun_right:
            t_right = is_truncation(img, 'right', x, y, (up, down, left, right))

        if not is_trun_up and (t_up / width) >= 0.6:
            is_trun_up = True
        else:
            up = up + 1 if x - up >= 0 else up
        if not is_trun_down and (t_dowm / width) >= 0.6:
            is_trun_down = True
        else:
            down = down + 1 if x + down < img.shape[0] else down
        if not is_trun_left and (t_left / height) >= 0.6:
            is_trun_left = True
        else:
            left = left + 1 if y - left >= 0 else left
        if not is_trun_right and (t_right / height) >= 0.6:
            is_trun_right = True
        else:
            right = right + 1 if y + right < img.shape[1] else right


    mask[x - up: x + down, y - left: y + right] = 1
    return width, height


def scan(img):
    mask = np.zeros(img.shape, dtype=np.uint8)
    row = img.shape[0]
    column = img.shape[1]

    for i in range(row):
        for j in range(column):
            if img[i, j] == 255 and mask[i, j] == 0:
                is_rec(img, mask, i, j)

    cv2.imshow('mask', mask)


img = np.zeros((600, 600, 3), dtype=np.uint8)
img[30:50, 30:50, :] = 255
img[90:138, 50:76, :] = 255
img[100:103, 66:70] = 0

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

scan(bin)

cv2.imshow('bin', bin)
cv2.waitKey(0)