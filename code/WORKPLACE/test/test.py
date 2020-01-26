import cv2
import numpy as np


def shrink(img, ratio=3.5):
    img_shrink = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))
    return img_shrink


def flood_fill(img, x, y, last_color, thresh=10):
    if x >= img.shape[0] or x < 0 or y >= img.shape[1] or y < 0 or\
            mask[x][y]==1 or abs(img[x][y] - last_color) > thresh:
        return

    mask[x][y] = 1
    last_color = img[x][y]
    flood_fill(img, x + 1, y, last_color, thresh)
    flood_fill(img, x - 1, y, last_color, thresh)
    flood_fill(img, x, y + 1, last_color, thresh)
    flood_fill(img, x, y - 1, last_color, thresh)
    flood_fill(img, x + 1, y + 1, last_color, thresh)
    flood_fill(img, x + 1, y - 1, last_color, thresh)
    flood_fill(img, x - 1, y + 1, last_color, thresh)
    flood_fill(img, x - 1, y - 1, last_color, thresh)


org = cv2.imread('4.jpg')
org = shrink(org)
grey = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
mask = np.zeros((org.shape[0], org.shape[1]), dtype=np.uint8)

print(np.shape(mask), np.shape(org))

flood_fill(grey, 0, 0, grey[0][0])

cv2.imshow('org', org)
cv2.imshow('grey', org)
cv2.waitKey()