import cv2
import numpy as np


def is_boundary(img, direction, x, y, para, thresh=0.8):
    (u, d, l, r) = para

    # calculate the truncation
    if direction == 'up':
        # boundary
        if x - u - 1 < 0 or np.sum(img[x - u, y - l: y + r + 1]) == 0: return True
    elif direction == 'down':
        # boundary
        if x + d + 1 == img.shape[0] or np.sum(img[x + d, y - l: y + r + 1]) == 0: return True
    elif direction == 'left':
        # boundary
        if y - l - 1 < 0 or np.sum(img[x - u: x + d + 1, y - l]) == 0: return True
    elif direction == 'right':
        # boundary
        if y + r + 1 == img.shape[1] or np.sum(img[x - u: x + d + 1, y + r]) == 0: return True

    return False


def is_rec(img, mask, x, y, min_area=1000):
    # diffuse towards four directions
    up, down, left, right = (0, 0, 0, 0)
    is_boundary_up, is_boundary_down, is_boundary_left, is_boundary_right = (False, False, False, False)

    while not (is_boundary_up and is_boundary_down and is_boundary_left and is_boundary_right):
        if not is_boundary_up:
            if is_boundary(img, 'up', x, y, (up, down, left, right)):
                is_boundary_up = True

        if not is_boundary_down:
            if is_boundary(img, 'down', x, y, (up, down, left, right)):
                is_boundary_down = True

        if not is_boundary_left:
            if is_boundary(img, 'left', x, y, (up, down, left, right)):
                is_boundary_left = True

        if not is_boundary_right:
            if is_boundary(img, 'right', x, y, (up, down, left, right)):
                is_boundary_right = True

        if not is_boundary_up and x - up >= 0: up = up + 1
        if not is_boundary_down and x + down < img.shape[0]: down = down + 1
        if not is_boundary_left and y - left >= 0: left = left + 1
        if not is_boundary_right and y + right < img.shape[1]: right = right + 1

    print(up, down, left, right)

    width = left + right + 1
    height = up + down + 1
    img[x - up: x + down + 1, y - left - 1: y + right + 1] = 0

    if width * height <= min_area:
        print('too small')
        return -1, -1, -1, -1

    mask[x - up: x + down + 1, y - left: y + right + 1] = 255

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
                if (rectangle['x'], rectangle['y'], rectangle['width'], rectangle['height']) == (-1, -1, -1, -1):
                    print('aaaaa')
                    continue
                print('bbbbb')
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