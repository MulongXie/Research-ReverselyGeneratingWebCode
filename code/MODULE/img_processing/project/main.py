import ip_detection as det
import ip_preprocessing as pre

import cv2
import time

start = time.clock()

org, gray = pre.read_img('1.png', (1500, 2200))  # cut out partial img
binary = pre.preprocess(gray)
boundary_all, boundary_rec = det.rectangle_detection(binary)
corners = det.get_corner(boundary_rec)
det.draw_bounding_box(corners, org)

print(time.clock() - start)  # running time

cv2.imshow('org', org)
cv2.imshow('binary', binary)
cv2.waitKey(0)