import cv2
import numpy as np

import ip_preprocessing as pre


def magnify(img, re_height):
    w_h_ratio = img.shape[1] / img.shape[0]
    re_width = re_height * w_h_ratio
    img = cv2.resize(img, (int(re_width), int(re_height)))


img, gray = pre.read_img('input/dribbble/x.png', resize_h=600)
print(img.shape)
cv2.imshow('img', img)
cv2.waitKey()

