import ip_detection as det
import ip_preprocessing as pre

import cv2
import numpy as np
import time


org, gray = pre.read_img('2.png', [0, 600])
binary = pre.preprocess(gray)
boundary_all, boundary_rec = det.rectangle_detection(binary)

cv2.imshow('org', org)
cv2.imshow('gray', gray)
cv2.imshow('binary', binary)
cv2.imshow('boundary_all', boundary_all)
cv2.imshow('rec', boundary_rec)
cv2.waitKey(0)