import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
from CONFIG import Config

import cv2
import time
import glob
from os.path import join as pyjoin


C = Config()
input_root = C.ROOT_IMG_ORG

is_save = True

input_paths = glob.glob(pyjoin(input_root, '*.png'))
input_paths = sorted(input_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

start_index = 16
end_index = 16

for input_path in input_paths:
    index = input_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    start = time.clock()

    # set paths
    print(input_path)
    print(time.ctime())
    out_img_draw = pyjoin(C.ROOT_IMG_DRAWN, index + '.png')
    out_img_clean = pyjoin(C.ROOT_IMG_CLEAN, index + '.png')
    out_img_gradient = pyjoin(C.ROOT_IMG_GRADIENT, index + '.png')
    out_img_segment = pyjoin(C.ROOT_IMG_SEGMENT, index)
    out_label = pyjoin(C.ROOT_LABEL, index)


    # *** Step 1 *** pre-processing: gray, gradient, binary
    org, gray = pre.read_img(input_path, (0, 3000))  # cut out partial img
    if org is None or gray is None: continue
    binary = pre.preprocess(gray, 1)

    # *** Step 2 *** processing: get connected areas -> get boundary -> rectangle check
    boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(binary,
                                                                         C.THRESHOLD_MIN_OBJ_AREA, C.THRESHOLD_MIN_OBJ_PERIMETER,       # size of area
                                                                         C.THRESHOLD_MIN_LINE_THICKNESS, C.THRESHOLD_MIN_LINE_LENGTH,   # line check
                                                                         C.THRESHOLD_MIN_REC_EVENNESS, C.THRESHOLD_MAX_IMG_DENT_RATIO)  # rectangle check
    # get corner of boundaries -> img or block check
    corners_rec = det.get_corner(boundary_rec)
    corners_nonrec = det.get_corner(boundary_nonrec)
    # identify rectangular block and rectangular img from rectangular shapes
    corners_block, corners_img = det.block_or_img(org, binary, corners_rec,
                                                  C.THRESHOLD_MAX_BLOCK_BORDER_THICKNESS, C.THRESHOLD_MAX_BLOCK_CROSS_POINT,  # block check
                                                  C.THRESHOLD_TEXT_EDGE_RATIO, C.THRESHOLD_TEXT_HEIGHT)                       # ignore text area
    # identify irregular-shape img from irregular shapes
    corners_img += det.irregular_img(org, corners_nonrec,
                                     C.THRESHOLD_MUST_IMG_HEIGHT, C.THRESHOLD_MUST_IMG_WIDTH,  # img assertion
                                     C.THRESHOLD_TEXT_EDGE_RATIO, C.THRESHOLD_TEXT_HEIGHT)     # ignore text area
    # merge overlapped corners, and remove nested corners
    corners_img = det.merge_corners(corners_img)
    # remove text area
    corners_block = det.rm_text(org, corners_block,
                                C.THRESHOLD_MUST_IMG_HEIGHT, C.THRESHOLD_MUST_IMG_WIDTH,  # img assertion
                                C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                       # ignore text area
    corners_img = det.rm_text(org, corners_img,
                              C.THRESHOLD_MUST_IMG_HEIGHT, C.THRESHOLD_MUST_IMG_WIDTH,  # img assertion
                              C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                       # ignore text area

    # *** Step 3 *** post-processing: remove img elements from original image and segment into smaller size
    img_clean = draw.draw_bounding_box(corners_img, org, (255, 255, 255), -1)
    seg.segment_img(img_clean, 600, out_img_segment, 0)
    # draw results
    draw_bounding = draw.draw_bounding_box(corners_block, org, (0, 255, 0))
    draw_bounding = draw.draw_bounding_box(corners_img, draw_bounding, (0, 0, 255))
    # draw_boundary = draw.draw_boundary(boundary_rec, org.shape)
    # save results
    if is_save:
        cv2.imwrite(out_img_draw, draw_bounding)
        cv2.imwrite(out_img_gradient, binary)
        cv2.imwrite(out_img_clean, img_clean)
        file.save_corners(out_label, corners_block, 'div')
        file.save_corners(out_label, corners_img, 'img', False)

    end = file.timer(start)
    print('Save ' + index + '\n')
