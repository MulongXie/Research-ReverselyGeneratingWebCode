import cv2
import numpy as np


def scan_row(img, mask, x, y, max_gap):
    width = 0
    gap = 0
    i = 0
    while gap <= max_gap and x < img.shape[0] and y + i < img.shape[1]:
        if img[x, y + i] == 255 and mask[x, y + i] == 0:
            mask[x, y + i] = 255
            width = i
            gap = 0
        else:
            gap += 1
        i += 1
    return width


def scan_column(img, mask, x, y, max_gap):
    height = 0
    gap = 0
    i = 0
    while gap <= max_gap and x + i < img.shape[0] and y < img.shape[1]:
        if img[x + i, y] == 255 and mask[x + i, y] == 0:
            mask[x + i, y] = 255
            height = i
            gap = 0
        else:
            gap += 1
        i += 1
    return height


def is_rec(img, mask, x, y, max_gap, is_filled):
    width = -1
    height = -1

    width1 = scan_row(img, mask, x, y, max_gap)
    height1 = scan_column(img, mask, x, y, max_gap)
    width2 = scan_row(img, mask, x + height1, y, max_gap)
    height2 = scan_column(img, mask, x, y + width1, max_gap)

    # if the two groups of edge are same length respectively then define as rectangle
    if abs(width1 - width2) <= 5 and abs(height1 - height2) <= 5:
        width = width1 if width1 > width2 else width2
        height = height1 if height1 > height2 else height2

        # scan the inner point
        if img[x + 1, y + 1] == 255 and mask[x + 1, y + 1] == 0:
            width_child, height_child, is_filled = is_rec(img, mask, x + 1, y + 1, max_gap, is_filled)
            if width_child == 1 or height_child == 1:
                is_filled = True

    return width, height, is_filled


def scan(img):
    mask = np.zeros(img.shape, dtype=np.uint8)
    row = img.shape[0]
    column = img.shape[1]

    rectangles = []
    for i in range(row):
        for j in range(column):
            rectangle = {}
            if img[i, j] == 255 and mask[i, j] == 0:
                rectangle['x'] = i
                rectangle['y'] = j
                rectangle['width'], rectangle['height'], rectangle['is_filled'] = is_rec(img, mask, i, j, 3, False)
                if rectangle['width'] > 3 and rectangle['height'] > 3:
                    rectangles.append(rectangle)

    cv2.imshow('mask', mask)
    return rectangles


def draw(img, recs):
    for rec in recs:
        cv2.rectangle(img, (rec['y'], rec['x']), (rec['y'] + rec['width'], rec['x'] + rec['height']), (255,0,0), 2)


# img = np.zeros((600, 600, 3), dtype=np.uint8)
# img[30:50, 30:50, :] = 255
# img[90:138, 50:76, :] = 255
# img[100:103, 66:70] = 0
# img = cv2.rectangle(img, (20, 20), (200, 200), (255, 0, 0), 5)

img = cv2.imread('bb.png')
# img = img[:600, :, :]
img = cv2.blur(img, (5, 5))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
cv2.imshow('bin', bin)

recs = scan(bin)
print(recs)
draw(img, recs)

cv2.imshow('img', img)
cv2.imwrite('ba.png', img)
cv2.waitKey(0)