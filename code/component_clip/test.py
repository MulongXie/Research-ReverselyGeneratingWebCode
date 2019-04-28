import numpy as np
import cv2


def padding(img):
    height = np.shape(img)[0]
    width = np.shape(img)[1]

    pad_height = int(height / 10)
    pad_wid = int(width / 10)
    pad_img = np.full(((height + pad_height), (width + pad_wid), 3), 255, dtype=np.uint8)
    pad_img[int(pad_height / 2):(int(pad_height / 2) + height), int(pad_wid / 2):(int(pad_wid / 2) + width)] = img

    return pad_img


img = cv2.imread('15.png')
pad = padding(img)

cv2.imshow('org', img)
cv2.imshow('pad', pad)
cv2.waitKey(0)