import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
from CONFIG import Config

import cv2
import time
import os

C = Config()
input_root = C.IMG_ROOT
output_root = C.OUTPUT_ROOT


for i in os.listdir(input_root):

    start = time.clock()
    org, gray = pre.read_img(os.path.join(input_root, i), (0, 3000))  # cut out partial img
    binary = pre.preprocess(gray, 1)
    boundary_all, boundary_rec = det.boundary_detection(binary)
    corners = det.get_corner(boundary_rec)
    wire_corners, rec_corners = det.is_wireframe(binary, corners)
    # draw result
    bounding_drawn = draw.draw_bounding_box(wire_corners, org, (0, 255, 0))
    bounding_drawn = draw.draw_bounding_box(rec_corners, bounding_drawn, (0, 0, 255))
    boundary_drawn = draw.draw_boundary(boundary_all, org.shape)

    print(time.clock() - start)  # running time

    cv2.imwrite(os.path.join(output_root, ('labeled/' + i[:-4] + '.png')), bounding_drawn)
    cv2.imwrite(os.path.join(output_root, ('boundary/' + i[:-4] + '.png')), boundary_drawn)
    cv2.imwrite(os.path.join(output_root, ('gradient/' + i[:-4] + '.png')), binary)

    # cv2.imshow('org', bounding_drawn)
    # cv2.imshow('boundary', boundary_drawn)
    # cv2.imshow('gradient', binary)
    # cv2.waitKey(0)
