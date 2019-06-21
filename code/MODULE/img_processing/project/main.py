import ip_detection as det
import ip_preprocessing as pre

import cv2
import time

start = time.clock()

org, gray = pre.read_img('1.png', (0, 600))  # cut out partial img
binary = pre.preprocess(gray)
boundary_all, boundary_rec = det.rectangle_detection(binary)
corners = det.get_corner(boundary_rec)

bounding_broad = det.draw_bounding_box(corners, org)
boundary_broad = det.draw_boundary(boundary_all, org.shape)

print(time.clock() - start)  # running time

cv2.imshow('org', bounding_broad)
cv2.imshow('boundary', boundary_broad)
cv2.imshow('gradient', binary)
cv2.waitKey(0)