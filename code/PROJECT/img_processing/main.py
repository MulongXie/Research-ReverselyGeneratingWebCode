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

start_index = 10
end_index = 1000

for input_path in input_paths:
    index = input_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    start = time.clock()

    # set paths
    print(input_path)
    out_img_draw = pyjoin(C.ROOT_IMG_DRAWN, index + '.png')
    out_img_clean = pyjoin(C.ROOT_IMG_CLEAN, index + '.png')
    out_img_gradient = pyjoin(C.ROOT_IMG_GRADIENT, index + '.png')
    out_img_segment = pyjoin(C.ROOT_IMG_SEGMENT, index)
    out_label = pyjoin(C.ROOT_LABEL, index)

    # pre-processing: gray, gradient, binary
    org, gray = pre.read_img(input_path, (0, 3000))  # cut out partial img
    binary = pre.preprocess(gray, 1)

    # processing: get connected areas -> get boundary -> rectangle check -> get corner of boundaries -> img or frame check -> refine img component
    boundary_rec, boundary_non_rec = det.boundary_detection(binary, C.THRESHOLD_MIN_OBJ_AREA,
                                                            C.THRESHOLD_MIN_REC_PARAMETER, C.THRESHOLD_MIN_REC_EVENNESS,
                                                            C.THRESHOLD_MIN_LINE_THICKNESS)
    corners_rec = det.get_corner(boundary_rec)
    corners_block, corners_img = det.block_or_img(binary, corners_rec, C.THRESHOLD_MAX_BORDER_THICKNESS)
    corners_img = det.img_refine2(corners_img, C.THRESHOLD_MAX_EDGE_RATIO)

    # remove img elements and segment into smaller size
    img_clean = draw.draw_bounding_box(corners_img, org, (255, 255, 255), -1)
    seg.segment_img(img_clean, 600, out_img_segment)

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
