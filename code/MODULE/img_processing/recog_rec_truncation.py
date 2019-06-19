import cv2
import numpy as np


def is_truncation(img, direction, x, y, para, thresh=0.8):
    (u, d, l, r) = para
    width = l + r + 1
    height = u + d + 1

    # calculate the truncation
    if direction == 'up':
        # boundary
        if x - u - 1 < 0: return True
        trun = img[x - u, y - l: y + r + 1] - img[x - u - 1, y - l: y + r + 1]
        trun = int(np.sum(trun) / 255)
        if trun / width >= thresh: return True
    elif direction == 'down':
        # boundary
        if x + d + 1 == img.shape[0]: return True
        trun = img[x + d, y - l: y + r + 1] - img[x + d + 1, y - l: y + r + 1]
        trun = int(np.sum(trun) / 255)
        if trun / width >= thresh: return True
    elif direction == 'left':
        # boundary
        if y - l - 1 < 0: return True
        trun = img[x - u: x + d + 1, y - l] - img[x - u: x + d + 1, y - l - 1]
        trun = int(np.sum(trun) / 255)
        if trun / height >= thresh: return True
    elif direction == 'right':
        # boundary
        if y + r + 1 == img.shape[1]: return True
        trun = img[x - u: x + d + 1, y + r] - img[x - u: x + d + 1, y + r + 1]
        trun = int(np.sum(trun) / 255)
        if trun / height >= thresh: return True

    return False


def is_rec(img, mask, x, y):
    # diffuse towards four directions
    up, down, left, right = (0, 0, 0, 0)
    is_trun_up, is_trun_down, is_trun_left, is_trun_right = (False, False, False, False)

    while not (is_trun_up and is_trun_down and is_trun_left and is_trun_right):
        if not is_trun_up:
            if is_truncation(img, 'up', x, y, (up, down, left, right)):
                is_trun_up = True

        if not is_trun_down:
            if is_truncation(img, 'down', x, y, (up, down, left, right)):
                is_trun_down = True

        if not is_trun_left:
            if is_truncation(img, 'left', x, y, (up, down, left, right)):
                is_trun_left = True

        if not is_trun_right:
            if is_truncation(img, 'right', x, y, (up, down, left, right)):
                is_trun_right = True

        if not is_trun_up: up = up + 1 if x - up >= 0 else up
        if not is_trun_down: down = down + 1 if x + down < img.shape[0] else down
        if not is_trun_left: left = left + 1 if y - left >= 0 else left
        if not is_trun_right: right = right + 1 if y + right < img.shape[1] else right

    print(up, down, left, right)

    width = left + right + 1
    height = up + down + 1
    mask[x - up: x + down + 1, y - left: y + right + 1] = 255
    img[x - up: x + down + 1, y - left: y + right + 1] = 0

    return x - up, y - left, width, height


def scan(img):
    mask = np.full(img.shape, 0, dtype=np.uint8)
    row = img.shape[0]
    column = img.shape[1]

    rectangles = []
    for i in range(row):
        for j in range(column):
            rectangle = {}
            if img[i, j] == 255 and mask[i, j] == 0:
                print('\n', i, j)
                rectangle['x'], rectangle['y'], rectangle['width'], rectangle['height'] = is_rec(img, mask, i, j)
                rectangles.append(rectangle)

                cv2.imshow('mask', mask)
                cv2.imshow('copy', img)
                cv2.waitKey(0)

    print(rectangles)
    return rectangles


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
scan(bin)