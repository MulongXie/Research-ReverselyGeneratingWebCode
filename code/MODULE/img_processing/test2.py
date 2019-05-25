import cv2
import numpy as np
import time


def search_right(img, mask, x, y, max_gap):
    gap = 0
    width = 0
    while gap <= max_gap and y < img.shape[1]:
        if img[x, y] == 255:
            width += 1
            mask[x, y] = 255
        else:
            gap += 1
        y += 1
    return width


def search_down(img, mask, x, y, max_gap):
    gap = 0
    height = 0
    while gap <= max_gap and x < img.shape[0]:
        if img[x, y] == 255:
            height += 1
            mask[x, y] = 255
        else:
            gap += 1
        x += 1
    return height


def is_wire(img, x, y, width, height, max_gap):
    gap_area_horizontal = img[x+1:x+max_gap, y:y+width]
    if np.sum(gap_area_horizontal)/(gap_area_horizontal.shape[0] * gap_area_horizontal.shape[1]) < 50:
        return True
    gap_area_vertical = img[x:x+height, y+1:y+max_gap]
    if np.sum(gap_area_vertical)/(gap_area_vertical.shape[0] * gap_area_vertical.shape[1]) < 50:
        return True
    print(np.sum(gap_area_horizontal)/(gap_area_horizontal.shape[0] * gap_area_horizontal.shape[1]))
    return False


def walk_pic(img, min_width, min_height, max_gap):
    row = img.shape[0]
    column = img.shape[1]

    mask = np.zeros(img.shape, dtype=np.uint8)

    for x in range(row):
        for y in range(column):
            if img[x, y] == 255 and mask[x, y] == 0:
                width = search_right(img, mask, x, y, max_gap)
                height = search_down(img, mask, x, y, max_gap)
                # if not is_wire(img, x, y, width, height, 20):
                mask[x+1:x+height, y+1:y+width] = 100
                print('width:%d height%d' %(width, height))

    cv2.imshow('mask', mask)
    cv2.imshow('img', img)
    cv2.waitKey(0)


start = time.clock()

img = cv2.imread('bb.png')
img = img[:600, :]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

walk_pic(bin, 1, 1, 10)

end = time.clock()
print(end - start)