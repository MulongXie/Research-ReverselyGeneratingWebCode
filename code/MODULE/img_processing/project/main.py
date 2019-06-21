import ip_detection as det
import ip_preprocessing as pre

import cv2
import numpy as np
import time

img = cv2.imread('c_close.png')
img = img[600: 1200, :]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

s = time.clock()
det.rectangle_detection(bin)
e = time.clock()
print(e - s)