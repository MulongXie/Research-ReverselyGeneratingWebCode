import ip_detection as det
import ip_preprocessing as pre

import cv2
import numpy as np
import time


org, gray = pre.read_img('2.png', [600, 1500])
binary = pre.preprocess(gray)
boundary_all, boundary_rec = det.rectangle_detection(binary)
corners = det.get_corner(boundary_rec)
det.draw_bounding_box(corners, org)

cv2.imshow('org', org)
cv2.imshow('binary', binary)
cv2.waitKey(0)