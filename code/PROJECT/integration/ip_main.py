import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import file_utils as file
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
org, gray = pre.read_img('input/2.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)

# processing: get connected areas -> get boundary -> rectangle check -> get corner of boundaries -> img or frame check -> refine img component
boundary_rec, boundary_non_rec = det.boundary_detection(binary, C.THRESHOLD_MIN_OBJ_AREA, C.THRESHOLD_MIN_REC_PARAMETER, C.THRESHOLD_MIN_REC_EVENNESS, C.THRESHOLD_MIN_LINE_THICKNESS)
corners_rec = det.get_corner(boundary_rec)
corners_block, corners_img = det.block_or_img(binary, corners_rec, C.THRESHOLD_MAX_BORDER_THICKNESS)
corners_img = det.img_refine2(corners_img, C.THRESHOLD_MAX_EDGE_RATIO)

# draw results
bounding_drawn = draw.draw_bounding_box(corners_block, org, (0, 255, 0))
bounding_drawn = draw.draw_bounding_box(corners_img, bounding_drawn, (0, 0, 255))
wireframe = draw.draw_bounding_box(corners_img, org, (119, 136, 153), -1)
boundary_drawn = draw.draw_boundary(boundary_rec, org.shape)
# save results
if is_save:
    cv2.imwrite('output/org.png', org)
    cv2.imwrite('output/labeled.png', bounding_drawn)
    cv2.imwrite('output/boundary.png', boundary_drawn)
    cv2.imwrite('output/gradient.png', binary)
    cv2.imwrite('output/wireframe.png', wireframe)
    file.save_corners('output/corners.csv', corners_block, 'div')
    file.save_corners('output/corners.csv', corners_img, 'img', False)

# show results
if is_show:
    cv2.imshow('org', bounding_drawn)
    cv2.imshow('boundary', boundary_drawn)
    cv2.imshow('gradient', binary)
    cv2.imshow('wireframe', wireframe)
    cv2.waitKey(0)

print(time.clock() - start)  # running time
