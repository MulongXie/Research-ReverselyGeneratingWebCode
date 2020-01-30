import lib_uied.ip_preprocessing as pre
import lib_uied.ip_draw as draw
import lib_uied.ip_detection as det
import lib_uied.ip_segment as seg
import lib_uied.file_utils as file
import lib_uied.ocr_classify_text as ocr
import lib_uied.ip_detection_utils as util
from config.CONFIG_UIED import Config

import cv2

# initialization
C = Config()
is_ocr = False
is_shrink_img = False


def processing_block(org, blocks_corner, classifier):
    '''
    :param org: original image
    :param blocks_corner: list of corners of blocks
                        [(top_left, bottom_right)]
                        -> top_left: (column_min, row_min)
                        -> bottom_right: (column_max, row_max)
    :param classifier: cnn model
    :return: boundaries of detected components in blocks;
                        [up, bottom, left, right]
                        -> up, bottom: list of [(column_index, min/max row border)]
                        -> left, right: list of [(row_index, min/max column border)]
             corners of detected components in blocks;
             corresponding classes of components;
    '''
    blocks_clip = seg.clipping(org, blocks_corner, shrink=3)

    all_compos_boundary = []
    all_compos_corner = []
    all_compos_class = []
    for i in range(len(blocks_corner)):
        # *** Step 1 *** pre-processing: get block information -> binarization
        block_corner = blocks_corner[i]
        block_clip = blocks_clip[i]
        binary = pre.preprocess(block_clip)

        # *** Step 2 *** object extraction: extract components boundary -> get bounding box corner
        compos_boundary = det.boundary_detection(binary, rec_detect=False)
        compos_corner = det.get_corner(compos_boundary)

        # *** Step 3 *** classification: clip components -> classify components
        compos_clip = seg.clipping(block_clip, compos_corner)
        compos_class = classifier.predict(compos_clip)

        # *** Step 4 *** refining: merge overlapping components -> convert the corners to holistic value in entire image
        compos_corner, compos_class = det.merge_corner(compos_corner, compos_class)
        compos_corner = util.corner_cvt_relative_position(compos_corner, block_corner[0][0], block_corner[0][1])

        if len(compos_boundary) > 0:
            all_compos_boundary += compos_boundary
            all_compos_corner += compos_corner
            all_compos_class += compos_class
    return all_compos_boundary, all_compos_corner, all_compos_class


def processing(org, binary, clf):
    # *** Step 1 *** object detection: get connected areas -> get boundary -> get corners
    boundary_rec, boundary_non_rec = det.boundary_detection(binary)
    corners_rec = det.get_corner(boundary_rec)
    corners_non_rec = det.get_corner(boundary_non_rec)

    # *** Step 2 *** data processing: identify blocks and compos from rectangles -> identify irregular compos
    corners_block, corners_img, corners_compo = det.block_or_compo(org, binary, corners_rec)
    det.compo_irregular(org, corners_non_rec, corners_img, corners_compo)

