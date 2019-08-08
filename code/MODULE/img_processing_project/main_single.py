import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
from CONFIG import Config

import cv2
import time


C = Config()
input_root = C.ROOT_IMG_ORG

is_save = True
start = time.clock()

# pre-processing: gray, gradient, binary
org, gray = pre.read_img('input/0.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)

# processing: get connected areas -> get boundary -> rectangle check -> get corner of boundaries ->
# img or frame check -> refine img component
boundary_rec, boundary_all = det.boundary_detection(binary, C.THRESHOLD_MIN_OBJ_AREA,
                                                        C.THRESHOLD_MIN_REC_PARAMETER, C.THRESHOLD_MIN_REC_EVENNESS,
                                                        C.THRESHOLD_MIN_LINE_THICKNESS)
corners_rec = det.get_corner(boundary_rec)
corners_block, corners_img = det.block_or_img(binary, corners_rec, C.THRESHOLD_MAX_BLOCK_BORDER_THICKNESS, C.THRESHOLD_MAX_BLOCK_CROSS_POINT)
corners_img = det.img_refine2(corners_img, C.THRESHOLD_MAX_IMG_EDGE_RATIO, C.THRESHOLD_MIN_IMG_EDGE_LENGTH)

# remove img elements and segment into smaller size
img_clean = draw.draw_bounding_box(corners_img, org, (255, 255, 255), -1)
seg.segment_img(img_clean, 600, 'output/segment')

# draw results
draw_bounding = draw.draw_bounding_box(corners_block, org, (0, 255, 0))
draw_bounding = draw.draw_bounding_box(corners_img, draw_bounding, (0, 0, 255))
draw_boundary = draw.draw_boundary(boundary_rec, org.shape)
# draw_boundary = draw.draw_boundary(boundary_rec, org.shape)

# save results
if is_save:
    cv2.imwrite('output/org.png', org)
    cv2.imwrite('output/labeled.png', draw_bounding)
    cv2.imwrite('output/boundary.png', draw_boundary)
    cv2.imwrite('output/gradient.png', binary)
    cv2.imwrite('output/clean.png', img_clean)
    file.save_corners('output/corners.csv', corners_block, 'div')
    file.save_corners('output/corners.csv', corners_img, 'img', False)

end = file.timer(start)
