import cv2
import numpy as np


def is_truncation(img, direction, x, y, para):
    (u, d, l, r) = para
    width = l + r + 1
    height = u + d + 1

    if x + d + 1 == img.shape[0] or x - u - 1 < 0 or y + r + 1 == img.shape[1] or y - l - 1 < 0: return True

    # calculate the truncation
    if direction == 'up':
        trun = img[x - u, y - l: y + r + 1] - img[x - u - 1, y - l: y + r + 1]
        trun = int(np.sum(trun) / 255)
        if trun / width >= 0.6: return True
    elif direction == 'down':
        trun = img[x + d, y - l: y + r + 1] - img[x + d + 1, y - l: y + r + 1]
        trun = int(np.sum(trun) / 255)
        if trun / width >= 0.6: return True
    elif direction == 'left':
        trun = img[x - u: x + d + 1, y - l] - img[x - u: x + d + 1, y - l - 1]
        trun = int(np.sum(trun) / 255)
        if trun / height >= 0.6: return True
    elif direction == 'right':
        trun = img[x - u: x + d + 1, y + r] - img[x - u: x + d + 1, y + r + 1]
        trun = int(np.sum(trun) / 255)
        if trun / height >= 0.6: return True

    return False


def is_rec(img, mask, x, y):
    # diffuse towards four directions
    up, down, left, right = (0, 0, 0, 0)
    is_trun_up, is_trun_down, is_trun_left, is_trun_right = (x == 0, x == img.shape[0] - 1, y == 0, y == img.shape[1] - 1)

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

        if not is_trun_up and x - up > 0: up = up + 1
        if not is_trun_down and x + down < img.shape[0] - 1: down = down + 1
        if not is_trun_left and y - left > 0: left = left + 1
        if not is_trun_right and y + right < img.shape[1] - 1: right = right + 1

    print(x - up, x + down, y - left, y + right)
    # up = up + 1 if x - up > 0 else up
    # down = down + 1 if x + down < img.shape[0] - 1 else down
    # left = left + 1 if y - left > 0 else left
    # right = right + 1 if y + right < img.shape[1] - 1 else right
    width = left + right + 1
    height = up + down + 1

    mask[x - up: x + down, y - left: y + right] = 255

    return x - up, y - left, width, height


def scan(img):
    mask = np.zeros(img.shape, dtype=np.uint8)
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
                cv2.waitKey(0)

    print(rectangles)
    return rectangles


img = np.zeros((600, 600, 3), dtype=np.uint8)
img[30:50, 30:50, :] = 255
img[90:138, 50:76, :] = 255
img[100:103, 66:70] = 0

img[:50 , 50:200, :] = 255


# img = cv2.imread('c_close.png')
# img = img[600: 1200, :]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

scan(bin)