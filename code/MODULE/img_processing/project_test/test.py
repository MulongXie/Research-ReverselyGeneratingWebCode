import ip_detection as det
import ip_preprocessing as pre

import cv2
import numpy as np


gray = np.zeros((600, 600), dtype=np.uint8)
cv2.line(gray, (200, 200), (200, 300), (255))

binary = pre.preprocess(gray, 1)
boundary_all, boundary_rec = det.rectangle_detection(binary)
corners = det.get_corner(boundary_rec)

print(det.is_line(boundary_all[0]))


cv2.imshow('line', gray)
cv2.imshow('gradient', binary)
cv2.waitKey(0)
