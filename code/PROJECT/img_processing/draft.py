import cv2
import numpy as np

from CONFIG import Config
import ip_detection as det
import ip_detection_utils as utils
import ip_draw as draw

C = Config()


def compo_in_img(org, bin, corners):
    def reverse(img):
        rec, b = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY_INV)
        return b

    corners_compo = []
    pad = 2
    for corner in corners:
        (top_left, bottom_right) = corner
        (col_min, row_min) = top_left
        (col_max, row_max) = bottom_right
        col_min = max(col_min - pad, 0)
        col_max = min(col_max + pad, org.shape[1])
        row_min = max(row_min - pad, 0)
        row_max = min(row_max + pad, org.shape[0])

        clip_bin = bin[row_min:row_max, col_min:col_max]
        clip_bin = reverse(clip_bin)
        boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(clip_bin,
                                                    C.THRESHOLD_OBJ_MIN_AREA, C.THRESHOLD_OBJ_MIN_PERIMETER,  # size of area
                                                    C.THRESHOLD_LINE_THICKNESS,  # line check
                                                    C.THRESHOLD_REC_MIN_EVENNESS_STRONG, C.THRESHOLD_IMG_MAX_DENT_RATIO)  # rectangle check
        corners_rec = det.get_corner(boundary_rec)
        corners_rec = utils.corner_cvt_relative_position(corners_rec, col_min, row_min)
        corners_compo += corners_rec

    draw.draw_bounding_box(org, corners_compo, show=True)

    return corners_compo
