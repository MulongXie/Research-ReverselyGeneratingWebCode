import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
from CONFIG import Config

import cv2
import time

C = Config()
input_root = C.IMG_ROOT
output_root = C.OUTPUT_ROOT

is_save = True
is_show = False

start = time.clock()

# pre-processing: gray, gradient, binary
org, gray = pre.read_img('input/8.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)

boundary_non_rec, boundary_rec = det.boundary_detection(binary, C.THRESHOLD_MIN_OBJ_AREA, C.THRESHOLD_MIN_REC_PARAMETER, C.THRESHOLD_MIN_REC_EVENNESS, C.THRESHOLD_MIN_LINE_THICKNESS)
corners = det.get_corner(boundary_non_rec)
corners = det.is_text(corners, 25, 2)

bounding_drawn = draw.draw_bounding_box(corners, org, (255, 255, 0))

cv2.imshow('b', bounding_drawn)
cv2.waitKey(0)
