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

is_save = True
is_show = False

for i in os.listdir(input_root):

    start = time.clock()

    # pre-processing: gray, gradient, binary
    org, gray = pre.read_img(os.path.join(input_root, i), (0, 3000))  # cut out partial img
    binary = pre.preprocess(gray, 1)

    # processing: connected areas, boundary, rectangle check, rectangle compression, corners, wireframe check
    boundary_all, boundary_rec = det.boundary_detection(binary, C.THRESHOLD_MIN_OBJ_AREA, C.THRESHOLD_MIN_REC_PARAMETER,
                                                        C.THRESHOLD_MIN_REC_EVENNESS, C.THRESHOLD_MAX_EDGE_RATIO,
                                                        C.THRESHOLD_MIN_LINE_THICKNESS)
    corners = det.get_corner(boundary_rec)
    wire_corners, rec_corners = det.is_wireframe(binary, corners, C.THRESHOLD_MAX_BORDER_THICKNESS)
    refined_rec_corners = det.rec_refine(binary, rec_corners, C.THRESHOLD_MAX_BORDER_THICKNESS)

    # draw results
    bounding_drawn = draw.draw_bounding_box(wire_corners, org, (0, 255, 0))
    bounding_drawn = draw.draw_bounding_box(refined_rec_corners, bounding_drawn, (0, 0, 255))
    boundary_drawn = draw.draw_boundary(boundary_all, org.shape)
    # save results
    if is_save:
        cv2.imwrite(os.path.join(output_root, ('labeled/' + i[:-4] + '.png')), bounding_drawn)
        cv2.imwrite(os.path.join(output_root, ('boundary/' + i[:-4] + '.png')), boundary_drawn)
        cv2.imwrite(os.path.join(output_root, ('gradient/' + i[:-4] + '.png')), binary)
    # show results
    if is_show:
        cv2.imshow('org', bounding_drawn)
        cv2.imshow('boundary', boundary_drawn)
        cv2.imshow('gradient', binary)
        cv2.waitKey(0)

    print(time.clock() - start)  # running time
