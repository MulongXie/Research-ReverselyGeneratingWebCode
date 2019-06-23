import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw

import cv2
import time

start = time.clock()

org, gray = pre.read_img('3.png', (1900, 2000))  # cut out partial img

cv2.imshow('img', gray)
cv2.waitKey(0)