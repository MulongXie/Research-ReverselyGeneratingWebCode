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

# *** Step 1 *** pre-processing: gray, gradient, binary
org, gray = pre.read_img('input/9.png', (0, 1000))  # cut out partial img
binary = pre.preprocess(gray, 1)


# *** Step 2 *** processing: get connected areas -> get boundary -> rectangle check
boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(binary, C.THRESHOLD_MIN_OBJ_AREA,
                                                        C.THRESHOLD_MIN_OBJ_PERIMETER, C.THRESHOLD_MIN_REC_EVENNESS,
                                                        C.THRESHOLD_MIN_LINE_THICKNESS, C.THRESHOLD_MIN_LINE_LENGTH,
                                                        C.THRESHOLD_MAX_IMG_DENT_RATIO)
# get corner of boundaries -> img or block check
corners_rec = det.get_corner(boundary_rec)
corners_nonrec = det.get_corner(boundary_nonrec)
# identify rectangular block and rectangular img from rectangular shapes
corners_block, corners_img = det.block_or_img(binary, corners_rec, C.THRESHOLD_MAX_BLOCK_BORDER_THICKNESS,
                                              C.THRESHOLD_MAX_BLOCK_CROSS_POINT, C.THRESHOLD_TEXT_EDGE_RATIO,
                                              C.THRESHOLD_TEXT_HEIGHT)
corners_block = det.rm_text(org, corners_block, C.OCR_PADDING, C.OCR_MIN_WORD_AREA, C.THRESHOLD_MUST_IMG_HEIGHT,
                            C.THRESHOLD_MUST_IMG_WIDTH)
# identify irregular-shape img from irregular shapes
corners_img += det.irregular_img(corners_nonrec, C.THRESHOLD_MUST_IMG_HEIGHT, C.THRESHOLD_MUST_IMG_WIDTH,
                                 C.THRESHOLD_TEXT_EDGE_RATIO, C.THRESHOLD_TEXT_HEIGHT)
corners_img = det.rm_text(org, corners_img, C.OCR_PADDING, C.OCR_MIN_WORD_AREA, C.THRESHOLD_MUST_IMG_HEIGHT,
                          C.THRESHOLD_MUST_IMG_WIDTH)
corners_img = det.rm_inner_rec(corners_img)


# *** Step 3 *** post-processing: remove img elements from original image and segment into smaller size
img_clean = draw.draw_bounding_box(corners_img, org, (255, 255, 255), -1)
seg.segment_img(img_clean, 600, 'output/segment')
# draw results
draw_bounding = draw.draw_bounding_box(corners_block, org, (0, 255, 0))
draw_bounding = draw.draw_bounding_box(corners_img, draw_bounding, (0, 0, 255))
draw_boundary = draw.draw_boundary(boundary_all, org.shape)
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
